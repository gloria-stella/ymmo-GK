"""
Modèle Transaction : représente une offre d'achat / une vente
faite par un client (buyer) sur un bien (property).
"""
import enum
from ..extensions import db
from .base import TimestampMixin


class TransactionStatus(enum.Enum):
    """Cycle de vie d'une offre d'achat."""

    EN_ATTENTE = "en_attente"
    ACCEPTEE = "acceptee"
    REFUSEE = "refusee"
    FINALISEE = "finalisee"


class Transaction(TimestampMixin, db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    offer_price = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(
        db.Enum(TransactionStatus),
        default=TransactionStatus.EN_ATTENTE,
        nullable=False,
    )

    property_id = db.Column(
        db.Integer, db.ForeignKey("properties.id"), nullable=False
    )
    property = db.relationship("Property", back_populates="transactions")

    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    buyer = db.relationship("User", back_populates="purchases")

    def __repr__(self) -> str:
        return f"<Transaction #{self.id} {self.offer_price}€ ({self.status.value})>"