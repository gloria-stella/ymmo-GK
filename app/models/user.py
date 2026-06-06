"""
Modèle Utilisateur et gestion des rôles.

On distingue trois rôles métier inspirés du brief Ymmo :
- CLIENT  : un particulier qui achète/vend
- AGENT   : un commercial d'agence qui publie et gère des biens
- ADMIN   : administrateur de la plateforme (siège)
"""
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..extensions import db, login_manager
from .base import TimestampMixin


class Role(enum.Enum):
    """Rôles disponibles sur la plateforme."""

    CLIENT = "client"
    AGENT = "agent"
    ADMIN = "admin"


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.CLIENT, nullable=False)

    # Biens publiés par un agent (relation 1-N)
    properties = db.relationship("Property", back_populates="agent", lazy="dynamic")
    # Transactions où l'utilisateur est l'acheteur
    purchases = db.relationship("Transaction", back_populates="buyer", lazy="dynamic")

    # --- Méthodes métier (POO / encapsulation) ---
    def set_password(self, password: str) -> None:
        """Hache et stocke le mot de passe (jamais en clair)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Vérifie un mot de passe en clair contre le hash stocké."""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def is_agent(self) -> bool:
        return self.role in (Role.AGENT, Role.ADMIN)

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"


@login_manager.user_loader
def load_user(user_id: str):
    """Callback requis par Flask-Login pour recharger l'utilisateur en session."""
    return db.session.get(User, int(user_id))