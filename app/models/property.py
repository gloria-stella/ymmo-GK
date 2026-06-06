"""
Modèle Bien immobilier (Property).
Entité centrale de la plateforme Ymmo : un bien à vendre/acheter.
"""
import enum
from ..extensions import db
from .base import TimestampMixin


class PropertyType(enum.Enum):
    """Type de bien immobilier."""

    APPARTEMENT = "appartement"
    MAISON = "maison"
    LOCAL_PRO = "local_professionnel"
    TERRAIN = "terrain"


class PropertyStatus(enum.Enum):
    """Statut de mise en vente."""

    DISPONIBLE = "disponible"
    SOUS_COMPROMIS = "sous_compromis"
    VENDU = "vendu"


class Property(TimestampMixin, db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    property_type = db.Column(
        db.Enum(PropertyType), default=PropertyType.APPARTEMENT, nullable=False
    )
    status = db.Column(
        db.Enum(PropertyStatus), default=PropertyStatus.DISPONIBLE, nullable=False
    )

    price = db.Column(db.Numeric(12, 2), nullable=False)   # prix en euros
    surface = db.Column(db.Integer, nullable=False)        # surface en m²
    rooms = db.Column(db.Integer, default=1, nullable=False)
    city = db.Column(db.String(100), nullable=False, index=True)
    postal_code = db.Column(db.String(10), nullable=False)

    # Agent (commercial) qui a publié le bien
    agent_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    agent = db.relationship("User", back_populates="properties")

    transactions = db.relationship(
        "Transaction", back_populates="property", lazy="dynamic"
    )

    @property
    def price_per_m2(self) -> float:
        """Prix au m² : utile pour les analyses et l'affichage."""
        if self.surface and self.surface > 0:
            return round(float(self.price) / self.surface, 2)
        return 0.0

    @property
    def is_available(self) -> bool:
        return self.status == PropertyStatus.DISPONIBLE

    def __repr__(self) -> str:
        return f"<Property {self.title} - {self.city} - {self.price}€>"