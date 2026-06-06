"""
Modèles de données (POO).

Chaque entité du domaine Ymmo est représentée par une classe Python
qui correspond à une table MySQL. On applique le principe DRY avec
une classe de base `TimestampMixin` factorisant les colonnes communes.
"""
from .user import User, Role
from .property import Property, PropertyType, PropertyStatus
from .transaction import Transaction, TransactionStatus

__all__ = [
    "User",
    "Role",
    "Property",
    "PropertyType",
    "PropertyStatus",
    "Transaction",
    "TransactionStatus",
]