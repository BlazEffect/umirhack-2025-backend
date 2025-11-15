from calculator.moex_parser import MoexParser


class EconomicCalculator:

    YIELD = {
        "пшеница": 35,
        "кукуруза": 60,
        "соя": 25,
    }

    SEEDING_RATE = {
        "пшеница": 120,
        "кукуруза": 25,
        "соя": 80,
    }

    def calculate(self, culture: str, area: float, avg_yield_cq: float) -> dict:
        culture = culture.lower()

        if culture not in self.YIELD:
            raise ValueError("Неизвестная культура")

        # 1. Цена культуры (динамически)
        culture_price = MoexParser.get_culture_price(culture)

        # 2. Цена семян
        seed_price_per_kg = MoexParser.get_seed_price_from_market(culture)

        seeds_cost = seed_price_per_kg * self.SEEDING_RATE[culture] * area

        # 4. Урожайность → доход
        total_yield_kg = (avg_yield_cq * area) * 100  # центнеры → кг
        revenue = culture_price * total_yield_kg

        return {
            "seeds_cost": round(seeds_cost, 2),
            "revenue": round(revenue, 2),
            "profit": round(revenue - seeds_cost, 2),
        }
