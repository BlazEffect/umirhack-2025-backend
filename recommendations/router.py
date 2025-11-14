from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from pony.orm import db_session, select, desc

from db.models import (
    Field, Crop, RotationRecommendation, Planting,
    FieldSoilProfile, CropRotationRule, User, Season
)
from recommendations.crop_rotation_service import CropRotationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

rotation_service = CropRotationService()


@router.get("/field/{field_id}")
async def get_recommendations_for_field(
        field_id: int,
        target_year: Optional[int] = None,
        limit: int = 5
):
    try:
        with db_session:
            field = Field.get(id=field_id)
            if not field:
                raise HTTPException(status_code=404, detail="Поле не найдено")

            if target_year is None:
                target_year = datetime.now().year + 1

            recommendations = rotation_service.get_rotation_recommendations(
                field_id, target_year, limit
            )

            return {
                "field_id": field_id,
                "field_name": field.name,
                "target_year": target_year,
                "recommendations": recommendations
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/field/{field_id}/apply/{recommendation_id}")
async def apply_recommendation(
        field_id: int,
        recommendation_id: int
):
    try:
        with db_session:
            recommendation = RotationRecommendation.get(id=recommendation_id)
            field = Field.get(id=field_id)

            if not recommendation or not field:
                raise HTTPException(status_code=404, detail="Рекомендация или поле не найдены")

            if recommendation.field.id != field_id:
                raise HTTPException(status_code=400, detail="Рекомендация не принадлежит указанному полю")

            planting = Planting(
                field=field,
                crop=recommendation.crop,
                season=select(s for s in Season if s.season_year == recommendation.target_year).first(),
                planting_date=datetime(recommendation.target_year, 3, 1),
                notes=f"Посадка создана на основе рекомендации #{recommendation_id}",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            recommendation.is_applied = True

            return {
                "message": "Рекомендация успешно применена",
                "planting_id": planting.id,
                "recommendation_id": recommendation_id
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/field/{field_id}/history")
async def get_field_rotation_history(
        field_id: int,
        years_back: int = 5
):
    try:
        with db_session:
            field = Field.get(id=field_id)
            if not field:
                raise HTTPException(status_code=404, detail="Поле не найдено")

            current_year = datetime.now().year

            plantings = select(
                p for p in Planting
                if p.field == field and
                p.season.date_start.year >= (current_year - years_back)
            ).order_by(lambda p: desc(p.season.date_start.year))

            history = []
            for planting in plantings:
                history.append({
                    "year": planting.season.date_start.year,
                    "crop_name": planting.crop.name,
                    "crop_family": planting.crop.family.name,
                    "yield_amount": planting.yield_amount,
                    "yield_quality": planting.yield_quality,
                    "planting_date": planting.planting_date,
                    "harvest_date": planting.harvest_date
                })

            return {
                "field_id": field_id,
                "field_name": field.name,
                "history_years": years_back,
                "rotation_history": history
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crops/compatibility/{crop_id}")
async def get_crop_compatibility(crop_id: int):
    try:
        with db_session:
            crop = Crop.get(id=crop_id)
            if not crop:
                raise HTTPException(status_code=404, detail="Культура не найдена")

            good_followers = select(
                r for r in CropRotationRule
                if r.previous_crop == crop and r.compatibility == 'good'
            )

            bad_followers = select(
                r for r in CropRotationRule
                if r.previous_crop == crop and r.compatibility == 'bad'
            )

            good_predecessors = select(
                r for r in CropRotationRule
                if r.next_crop == crop and r.compatibility == 'good'
            )

            return {
                "crop_id": crop.id,
                "crop_name": crop.name,
                "good_followers": [
                    {
                        "crop_id": rule.next_crop.id,
                        "crop_name": rule.next_crop.name,
                        "reason": rule.rule_description
                    }
                    for rule in good_followers
                ],
                "bad_followers": [
                    {
                        "crop_id": rule.next_crop.id,
                        "crop_name": rule.next_crop.name,
                        "reason": rule.rule_description
                    }
                    for rule in bad_followers
                ],
                "good_predecessors": [
                    {
                        "crop_id": rule.previous_crop.id,
                        "crop_name": rule.previous_crop.name,
                        "reason": rule.rule_description
                    }
                    for rule in good_predecessors
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/soil-analysis/field/{field_id}")
async def get_soil_analysis(field_id: int):
    try:
        with db_session:
            field = Field.get(id=field_id)
            if not field:
                raise HTTPException(status_code=404, detail="Поле не найдено")

            soil_profile = FieldSoilProfile.get(
                field=field,
                sample_date=select(
                    max(fsp.sample_date) for fsp in FieldSoilProfile
                    if fsp.field == field
                )
            )

            if not soil_profile:
                return {
                    "field_id": field_id,
                    "message": "Данные анализа почвы отсутствуют",
                    "soil_data": None
                }

            soil_analysis = {
                "ph_status": "нейтральная",
                "organic_status": "средняя",
                "recommendations": []
            }

            if soil_profile.pH:
                if soil_profile.pH < 5.5:
                    soil_analysis["ph_status"] = "кислая"
                    soil_analysis["recommendations"].append("Рекомендуется известкование")
                elif soil_profile.pH > 7.5:
                    soil_analysis["ph_status"] = "щелочная"
                    soil_analysis["recommendations"].append("Рекомендуется гипсование")

            if soil_profile.organic_matter:
                if soil_profile.organic_matter < 2.0:
                    soil_analysis["organic_status"] = "низкая"
                    soil_analysis["recommendations"].append("Рекомендуется внесение органических удобрений")
                elif soil_profile.organic_matter > 4.0:
                    soil_analysis["organic_status"] = "высокая"

            return {
                "field_id": field_id,
                "field_name": field.name,
                "soil_data": {
                    "pH": soil_profile.pH,
                    "organic_matter": soil_profile.organic_matter,
                    "nitrogen": soil_profile.nitrogen,
                    "phosphorus": soil_profile.phosphorus,
                    "potassium": soil_profile.potassium,
                    "sample_date": soil_profile.sample_date
                },
                "soil_analysis": soil_analysis
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/applied-recommendations")
async def get_user_applied_recommendations(user_id: int):
    try:
        with db_session:
            user = User.get(id=user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найдено")

            applied_recommendations = select(
                r for r in RotationRecommendation
                if r.field.owner == user and r.is_applied == True
            )

            result = []
            for rec in applied_recommendations:
                result.append({
                    "recommendation_id": rec.id,
                    "field_name": rec.field.name,
                    "crop_name": rec.crop.name,
                    "target_year": rec.target_year,
                    "agro_score": rec.agro_score,
                    "applied_date": rec.generated_at,
                    "reasons": rec.reasons
                })

            return {
                "user_id": user_id,
                "applied_recommendations": result
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/field/{field_id}/generate")
async def generate_recommendations(
        field_id: int,
        target_year: Optional[int] = None
):
    try:
        with db_session:
            field = Field.get(id=field_id)
            if not field:
                raise HTTPException(status_code=404, detail="Поле не найдено")

            if target_year is None:
                target_year = datetime.now().year + 1

            old_recommendations = select(
                r for r in RotationRecommendation
                if r.field == field and r.target_year == target_year
            )
            old_recommendations.delete(bulk=True)

            recommendations = rotation_service.get_rotation_recommendations(
                field_id, target_year, limit=5
            )

            return {
                "field_id": field_id,
                "field_name": field.name,
                "target_year": target_year,
                "generated_count": len(recommendations),
                "message": "Новые рекомендации успешно сгенерированы"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crops/suitable-for-soil")
async def get_crops_suitable_for_soil(
        ph_min: Optional[float] = None,
        ph_max: Optional[float] = None,
        organic_matter_min: Optional[float] = None
):
    try:
        with db_session:
            query = select(c for c in Crop)

            if ph_min is not None and ph_max is not None:
                suitable_crops = []
                for crop in query:
                    if crop.preferred_ph == 'acidic' and ph_min <= 6.5:
                        suitable_crops.append(crop)
                    elif crop.preferred_ph == 'alkaline' and ph_max >= 7.0:
                        suitable_crops.append(crop)
                    elif crop.preferred_ph == 'neutral' and 6.0 <= ph_min <= 7.5:
                        suitable_crops.append(crop)
                    elif crop.preferred_ph is None:
                        suitable_crops.append(crop)
                query = suitable_crops

            crops_data = []
            for crop in query[:20]:
                crops_data.append({
                    "crop_id": crop.id,
                    "crop_name": crop.name,
                    "family": crop.family.name,
                    "nutrient_demand": crop.nutrient_demand,
                    "water_demand": crop.water_demand,
                    "preferred_ph": crop.preferred_ph,
                    "rotation_interval": crop.recommended_rotation_interval
                })

            return {
                "filters": {
                    "ph_range": [ph_min, ph_max],
                    "organic_matter_min": organic_matter_min
                },
                "suitable_crops": crops_data
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
