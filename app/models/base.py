"""
Mixin commun à plusieurs modèles (principe DRY).
Ajoute automatiquement les dates de création/mise à jour.
"""
from datetime import datetime
from ..extensions import db


class TimestampMixin:
    """Ajoute les colonnes created_at et updated_at à un modèle."""

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )