"""
Service de gestion des biens immobiliers.
Centralise les opérations CRUD et la recherche filtrée.
"""
from ..extensions import db
from ..models import Property, PropertyStatus, PropertyType


class PropertyService:
    @staticmethod
    def list_available(filters: dict | None = None):
        """Retourne les biens disponibles, avec filtres optionnels."""
        query = Property.query.filter_by(status=PropertyStatus.DISPONIBLE)
        filters = filters or {}

        if filters.get("city"):
            query = query.filter(Property.city.ilike(f"%{filters['city']}%"))
        if filters.get("property_type"):
            query = query.filter(Property.property_type == PropertyType(filters["property_type"]))
        if filters.get("max_price"):
            query = query.filter(Property.price <= filters["max_price"])
        if filters.get("min_rooms"):
            query = query.filter(Property.rooms >= filters["min_rooms"])

        return query.order_by(Property.created_at.desc()).all()

    @staticmethod
    def get(property_id: int) -> Property | None:
        return db.session.get(Property, property_id)

    @staticmethod
    def create(data: dict, agent_id: int) -> Property:
        prop = Property(
            title=data["title"],
            description=data.get("description"),
            property_type=PropertyType(data["property_type"]),
            price=data["price"],
            surface=data["surface"],
            rooms=data.get("rooms", 1),
            city=data["city"],
            postal_code=data["postal_code"],
            agent_id=agent_id,
        )
        db.session.add(prop)
        db.session.commit()
        return prop

    @staticmethod
    def update(prop: Property, data: dict) -> Property:
        prop.title = data["title"]
        prop.description = data.get("description")
        prop.property_type = PropertyType(data["property_type"])
        prop.price = data["price"]
        prop.surface = data["surface"]
        prop.rooms = data.get("rooms", 1)
        prop.city = data["city"]
        prop.postal_code = data["postal_code"]
        if data.get("status"):
            prop.status = PropertyStatus(data["status"])
        db.session.commit()
        return prop

    @staticmethod
    def delete(prop: Property) -> None:
        db.session.delete(prop)
        db.session.commit()