"""
Point d'entrée de l'application Ymmo.
Lancer avec :  python run.py
"""
from app import create_app
from app.extensions import db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Rend les objets disponibles dans `flask shell`."""
    return {"db": db}


if __name__ == "__main__":
    app.run(debug=True)