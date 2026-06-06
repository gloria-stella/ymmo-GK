from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models import PropertyType, PropertyStatus, Transaction
from ..services.property_service import PropertyService
from .decorators import agent_required

properties_bp = Blueprint("properties", __name__)

@properties_bp.route("/")
def index():
    filters = {
        "city": request.args.get("city"),
        "property_type": request.args.get("property_type"),
        "max_price": request.args.get("max_price"),
        "min_rooms": request.args.get("min_rooms"),
    }
    filters = {k: v for k, v in filters.items() if v}
    biens = PropertyService.list_available(filters)
    return render_template("properties/index.html", biens=biens, types=PropertyType, filters=filters)

@properties_bp.route("/biens/<int:property_id>")
def detail(property_id):
    prop = PropertyService.get(property_id)
    if not prop: abort(404)
    return render_template("properties/detail.html", bien=prop)

@properties_bp.route("/biens/nouveau", methods=["GET", "POST"])
@login_required
@agent_required
def create():
    if request.method == "POST":
        PropertyService.create(_form_to_dict(request.form), current_user.id)
        flash("Bien publié avec succès.", "success")
        return redirect(url_for("properties.index"))
    return render_template("properties/form.html", bien=None, types=PropertyType, statuses=PropertyStatus)

@properties_bp.route("/biens/<int:property_id>/modifier", methods=["GET", "POST"])
@login_required
@agent_required
def edit(property_id):
    prop = PropertyService.get(property_id)
    if not prop: abort(404)

    if request.method == "POST":
        PropertyService.update(prop, _form_to_dict(request.form))
        flash("Bien mis à jour.", "success")
        return redirect(url_for("properties.detail", property_id=prop.id))
    return render_template("properties/form.html", bien=prop, types=PropertyType, statuses=PropertyStatus)

@properties_bp.route("/biens/<int:property_id>/supprimer", methods=["POST"])
@login_required
@agent_required
def delete(property_id):
    prop = PropertyService.get(property_id)
    if not prop: abort(404)
    PropertyService.delete(prop)
    flash("Bien supprimé.", "success")
    return redirect(url_for("properties.index"))

@properties_bp.route("/biens/<int:property_id>/offre", methods=["POST"])
@login_required
def make_offer(property_id):
    prop = PropertyService.get(property_id)
    if not prop: abort(404)
    
    # Un agent ne doit pas pouvoir postuler à sa propre plateforme
    if current_user.role.name.lower() == "agent":
        abort(403)

    try:
        offer_price = float(request.form.get("offer_price", 0))
    except ValueError:
        offer_price = 0

    if offer_price <= 0:
        flash("Le montant de l'offre est invalide.", "error")
        return redirect(url_for("properties.detail", property_id=prop.id))

    offre = Transaction(offer_price=offer_price, property_id=prop.id, buyer_id=current_user.id)
    db.session.add(offre)
    db.session.commit()
    flash("Votre offre a bien été envoyée à l'agence.", "success")
    return redirect(url_for("properties.detail", property_id=prop.id))

def _form_to_dict(form) -> dict:
    return {
        "title": form.get("title", "").strip(),
        "description": form.get("description", "").strip(),
        "property_type": form.get("property_type"),
        "status": form.get("status"),
        "price": float(form.get("price") or 0),
        "surface": int(form.get("surface") or 0),
        "rooms": int(form.get("rooms") or 1),
        "city": form.get("city", "").strip(),
        "postal_code": form.get("postal_code", "").strip(),
    }