import json

from pony.orm import db_session, select, desc, max

from db.models import CropRotationRule, Planting, FieldSoilProfile, Crop, Field


class CropRotationService:
    @db_session
    def get_rotation_recommendations(self, field_id: int, target_year: int, limit: int = 5):
        field = Field[field_id]

        planting_history = select(
            p for p in Planting
            if p.field == field
        ).order_by(desc(Planting.planting_date))[:10]

        soil_profile = select(
            fsp for fsp in FieldSoilProfile
            if fsp.field == field
        ).order_by(desc(FieldSoilProfile.sample_date)).first()

        all_crops = select(c for c in Crop)[:]

        recommendations = []

        for crop in all_crops:
            score, reasons = self._calculate_crop_score(
                crop, planting_history, soil_profile, target_year
            )

            if score >= 90:
                compatibility = "excellent"
            elif score >= 70:
                compatibility = "good"
            elif score >= 50:
                compatibility = "fair"
            else:
                compatibility = "poor"

            recommendations.append({
                'crop_id': crop.id,
                'crop_name': crop.name,
                'family_name': crop.family.name if crop.family else "Не указано",
                'score': score,
                'compatibility': compatibility,
                'reasons': reasons,
                'rotation_interval': crop.recommended_rotation_interval
            })

        recommendations.sort(key=lambda x: x['score'], reverse=True)

        for rec in recommendations[:limit]:
            from db.models import RotationRecommendation
            RotationRecommendation(
                field=field,
                crop=Crop[rec['crop_id']],
                target_year=target_year,
                agro_score=rec['score'],
                compatibility=rec['compatibility'],
                reasons=json.dumps(rec['reasons']),
                soil_adaptation=any('почв' in reason for reason in rec['reasons']),
                rotation_compliance=rec['score'] >= 70
            )

        return recommendations[:limit]

    def _calculate_crop_score(self, candidate_crop, planting_history, soil_profile, target_year):
        score = 100
        reasons = []

        last_planting_year = None
        for planting in planting_history:
            if planting.crop.id == candidate_crop.id:
                last_planting_year = planting.planting_date.year
                break

        if last_planting_year:
            years_since_last = target_year - last_planting_year
            min_interval = candidate_crop.recommended_rotation_interval

            if years_since_last < min_interval:
                penalty = (min_interval - years_since_last) * 15
                score -= penalty
                reasons.append(
                    f"Нарушен интервал севооборота: {years_since_last} лет вместо {min_interval}"
                )
            else:
                reasons.append(f"Интервал севооборота соблюден: {years_since_last} лет")

        if planting_history:
            last_crop = planting_history[0].crop

            rotation_rule = CropRotationRule.get(
                previous_crop=last_crop,
                next_crop=candidate_crop
            )

            if rotation_rule:
                if rotation_rule.compatibility == 'good':
                    score += 20
                    reasons.append(f"Хороший предшественник: {last_crop.name}")
                elif rotation_rule.compatibility == 'bad':
                    score -= 30
                    reasons.append(f"Плохой предшественник: {last_crop.name}")

            if last_crop.family == candidate_crop.family:
                score -= 25
                reasons.append(f"Одинаковое семейство с предшественником: {candidate_crop.family.name}")

        if soil_profile:
            if (hasattr(candidate_crop, 'preferred_ph') and
                    hasattr(soil_profile, 'pH') and soil_profile.pH is not None):

                if (candidate_crop.preferred_ph == 'acidic' and soil_profile.pH >= 6.5):
                    score -= 20
                    reasons.append("Культура предпочитает кислые почвы")
                elif (candidate_crop.preferred_ph == 'alkaline' and soil_profile.pH <= 6.5):
                    score -= 20
                    reasons.append("Культура предпочитает щелочные почвы")

            if (hasattr(candidate_crop, 'nutrient_demand') and
                    hasattr(soil_profile, 'organic_matter') and soil_profile.organic_matter is not None):

                if (candidate_crop.nutrient_demand == 'high' and soil_profile.organic_matter < 2.5):
                    score -= 15
                    reasons.append("Высокая потребность в питательных веществах при бедной почве")
        else:
            reasons.append("Данные анализа почвы отсутствуют")

        recent_crop_types = [p.crop.crop_type for p in planting_history[:3] if p.crop.crop_type]
        if (hasattr(candidate_crop, 'crop_type') and
                candidate_crop.crop_type and
                candidate_crop.crop_type in recent_crop_types):
            score -= 10
            reasons.append("Частое повторение типа культуры в истории поля")

        return max(score, 0), reasons
