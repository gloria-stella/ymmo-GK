from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models import User, Role

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("properties.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if User.query.filter_by(email=email).first():
            flash("Un compte existe déjà avec cet email.", "error")
            return render_template("auth/register.html")

        user = User(
            first_name=request.form.get("first_name", "").strip(),
            last_name=request.form.get("last_name", "").strip(),
            email=email,
            role=Role.CLIENT, # <-- Sécurisé : Tout le monde est client par défaut
        )
        user.set_password(request.form.get("password", ""))
        db.session.add(user)
        db.session.commit()
        flash("Compte créé avec succès, vous pouvez vous connecter.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("properties.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Bienvenue {user.first_name} !", "success")
            return redirect(request.args.get("next") or url_for("properties.index"))

        flash("Email ou mot de passe incorrect.", "error")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "success")
    return redirect(url_for("properties.index"))

@auth_bp.route("/admin/personnel", methods=["GET", "POST"])
@login_required
def manage_staff():
    # Sécurité absolue : si ce n'est pas le compte admin officiel, on bloque !
    if current_user.email != "admin@ymmo.fr":
        abort(403)
        
    if request.method == "POST":
        user_id = request.form.get("user_id")
        new_role = request.form.get("role")
        
        # On récupère l'utilisateur et on met à jour son rôle
        user_to_update = User.query.get(user_id)
        if user_to_update:
            if new_role == "agent":
                user_to_update.role = Role.AGENT
            elif new_role == "client":
                user_to_update.role = Role.CLIENT
            db.session.commit()
            flash(f"Le rôle de {user_to_update.first_name} a été mis à jour.", "success")
            
    # On récupère tous les utilisateurs pour les afficher dans le tableau
    all_users = User.query.all()
    return render_template("auth/admin_staff.html", users=all_users)