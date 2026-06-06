import pandas as pd
from sqlalchemy import text
from ..extensions import db

class AnalyticsService:
    @staticmethod
    def _load_dataframe() -> pd.DataFrame:
        """Charge les biens dans un DataFrame pandas via une requête SQL brute."""
        sql = text("SELECT id, title, city, price, surface, rooms, property_type, status FROM properties")
        rows = db.session.execute(sql).mappings().all()
        df = pd.DataFrame(rows)
        if not df.empty:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
            df["surface"] = pd.to_numeric(df["surface"], errors="coerce")
            df = df.dropna(subset=["price", "surface"])
            df = df[df["surface"] > 0]
            df["price_per_m2"] = (df["price"] / df["surface"]).round(2)
        return df

    @classmethod
    def global_summary(cls) -> dict:
        df = cls._load_dataframe()
        if df.empty:
            return {"total_biens": 0, "prix_moyen": 0, "prix_m2_moyen": 0, "surface_moyenne": 0}
        return {
            "total_biens": int(len(df)),
            "prix_moyen": round(float(df["price"].mean()), 2),
            "prix_m2_moyen": round(float(df["price_per_m2"].mean()), 2),
            "surface_moyenne": round(float(df["surface"].mean()), 2),
        }

    @classmethod
    def stats_by_city(cls) -> list[dict]:
        df = cls._load_dataframe()
        if df.empty: return []
        grouped = df.groupby("city").agg(nb_biens=("id", "count"), prix_moyen=("price", "mean"), prix_m2_moyen=("price_per_m2", "mean")).reset_index().sort_values("nb_biens", ascending=False)
        grouped["prix_moyen"] = grouped["prix_moyen"].round(0)
        grouped["prix_m2_moyen"] = grouped["prix_m2_moyen"].round(2)
        return grouped.to_dict(orient="records")

    @classmethod
    def popular_types(cls) -> list[dict]:
        df = cls._load_dataframe()
        if df.empty: return []
        counts = df["property_type"].value_counts().reset_index()
        counts.columns = ["property_type", "nb_biens"]
        return counts.to_dict(orient="records")

    @classmethod
    def best_cities_to_buy(cls, top_n: int = 3) -> list[dict]:
        """Retourne le Top 3 des villes les moins chères au m², sans restriction de volume."""
        df = cls._load_dataframe()
        if df.empty: return []
        grouped = df.groupby("city").agg(nb_biens=("id", "count"), prix_m2_moyen=("price_per_m2", "mean")).reset_index()
        grouped["prix_m2_moyen"] = grouped["prix_m2_moyen"].round(2)
        grouped = grouped.sort_values("prix_m2_moyen", ascending=True).head(top_n)
        return grouped.to_dict(orient="records")