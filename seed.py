"""
Script d'initialisation de la base de données.

- Crée toutes les tables (si elles n'existent pas)
- Insère un jeu de données de démonstration (utilisateurs + biens)

À lancer une seule fois :  python seed.py
"""
from app import create_app
from app.extensions import db
from app.models import User, Role, Property, PropertyType, PropertyStatus

app = create_app()


def run_seed():
    with app.app_context():
        db.create_all()

        if User.query.first():
            print("La base contient déjà des données. Seed ignoré.")
            return

        # --- Utilisateurs ---
        admin = User(
            first_name="Admin", last_name="Ymmo",
            email="admin@ymmo.fr", role=Role.ADMIN,
        )
        admin.set_password("admin123")

        agent = User(
            first_name="Sophie", last_name="Martin",
            email="agent@ymmo.fr", role=Role.AGENT,
        )
        agent.set_password("agent123")

        client = User(
            first_name="Lucas", last_name="Bernard",
            email="client@ymmo.fr", role=Role.CLIENT,
        )
        client.set_password("client123")

        db.session.add_all([admin, agent, client])
        db.session.commit()

        # --- Biens immobiliers de démonstration ---
        biens = [
            Property(title="Appartement T3 lumineux", description="Proche centre-ville, balcon.",
                     property_type=PropertyType.APPARTEMENT, price=285000, surface=68, rooms=3,
                     city="Aix-en-Provence", postal_code="13100", agent_id=agent.id),
            Property(title="Maison familiale avec jardin", description="4 chambres, garage.",
                     property_type=PropertyType.MAISON, price=540000, surface=140, rooms=5,
                     city="Marseille", postal_code="13008", agent_id=agent.id),
            Property(title="Studio étudiant rénové", description="Idéal investissement locatif.",
                     property_type=PropertyType.APPARTEMENT, price=125000, surface=25, rooms=1,
                     city="Aix-en-Provence", postal_code="13090", agent_id=agent.id),
            Property(title="Local commercial centre-ville", description="Belle vitrine, fort passage.",
                     property_type=PropertyType.LOCAL_PRO, price=320000, surface=90, rooms=2,
                     city="Lyon", postal_code="69002", agent_id=agent.id),
            Property(title="Maison de campagne", description="Au calme, grand terrain.",
                     property_type=PropertyType.MAISON, price=410000, surface=160, rooms=6,
                     city="Marseille", postal_code="13011", agent_id=agent.id,
                     status=PropertyStatus.DISPONIBLE),
            Property(title="Terrain constructible", description="800 m² viabilisé.",
                     property_type=PropertyType.TERRAIN, price=180000, surface=800, rooms=0,
                     city="Lyon", postal_code="69009", agent_id=agent.id),
        ]
        db.session.add_all(biens)
        db.session.commit()

        print("Seed terminé avec succès.")
        print("Comptes de test :")
        print("  admin@ymmo.fr  / admin123")
        print("  agent@ymmo.fr  / agent123")
        print("  client@ymmo.fr / client123")


if __name__ == "__main__":
    run_seed()