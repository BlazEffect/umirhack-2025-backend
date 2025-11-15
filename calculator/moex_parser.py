import requests
from datetime import datetime


class MoexParser:
    BASE_LIST_URL = "https://iss.moex.com/iss/engines/futures/markets/forts/securities.json"
    BASE_PRICE_URL = "https://iss.moex.com/iss/engines/futures/markets/forts/securities/{}/securities.json"

    # Префиксы фьючерсов культур на MOEX
    CULTURE_PREFIXES = {
        "пшеница": "WHEAT",
        "кукуруза": "CORN",
        "соя": "SOYB",
    }

    # -----------------------------
    # Получение всех фьючерсов FORTS
    # -----------------------------
    @classmethod
    def get_all_futures(cls):
        resp = requests.get(cls.BASE_LIST_URL, timeout=7)
        resp.raise_for_status()

        data = resp.json()
        rows = data["securities"]["data"]
        columns = data["securities"]["columns"]


        secid_idx = columns.index("SECID")
        short_name_ids = columns.index("SHORTNAME")
        last_trade_idx = columns.index("LASTTRADEDATE")

        futures = []
        for row in rows:
            secid = row[secid_idx]
            short_name = row[short_name_ids]
            last_trade_date = row[last_trade_idx]



            if last_trade_date:
                try:
                    last_trade_date = datetime.fromisoformat(last_trade_date)
                except ValueError:
                    last_trade_date = None

            futures.append({
                "secid": secid,
                "short_name": short_name,
                "last_trade_date": last_trade_date
            })

        return futures

    # -----------------------------
    # Фильтр фьючерсов по префиксу
    # -----------------------------
    @classmethod
    def get_futures_by_prefix(cls, prefix: str):
        all_futures = cls.get_all_futures()

        filtered = [
            f for f in all_futures if f["short_name"].startswith(prefix)
        ]

        # сортировка по дате экспирации
        filtered.sort(key=lambda x: x["last_trade_date"] or datetime.max)

        return filtered

    # -----------------------------
    # Получение цены фьючерса
    # -----------------------------
    @classmethod
    def get_price(cls, ticker: str) -> float | None:
        """
        Получить цену фьючерса через marketdata.json
        Берет LAST, если нет — SETTLEPRICE
        """
        url = f"https://iss.moex.com/iss/engines/futures/markets/forts/securities/{ticker}/marketdata.json"
        try:
            resp = requests.get(url, timeout=7)
            resp.raise_for_status()
        except:
            return None

        data = resp.json()
        marketdata = data.get("marketdata", {})
        rows = marketdata.get("data", [])
        columns = marketdata.get("columns", [])

        if not rows or not columns:
            return None

        price = None

        # LAST — цена последней сделки
        if "LAST" in columns:
            idx = columns.index("LAST")
            price = rows[0][idx]

        # Если LAST пустая, берем SETTLEPRICE
        if (price is None or price == "") and "SETTLEPRICE" in columns:
            idx = columns.index("SETTLEPRICE")
            price = rows[0][idx]

        if price is None or price == "":
            return None

        return float(price)

    # -----------------------------
    # Основной метод: цена культуры
    # -----------------------------
    @classmethod
    def get_culture_price(cls, culture: str) -> float:
        if culture not in cls.CULTURE_PREFIXES:
            raise ValueError("Неизвестная культура")

        prefix = cls.CULTURE_PREFIXES[culture]

        futures = cls.get_futures_by_prefix(prefix)
        if not futures:
            raise ValueError("Не найдены фьючерсы культуры")

        # Перебор ближайших по экспирации
        for f in futures:
            price = cls.get_price(f["secid"])
            if price:
                return price

        raise ValueError("Не удалось получить цену ни по одному тикеру")

    # -----------------------------
    # Цена семян (можно выделить в отдельную модель)
    # -----------------------------
    @classmethod
    def get_seed_price_from_market(cls, culture: str) -> float:
        return cls.get_culture_price(culture)
