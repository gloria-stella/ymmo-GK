"""
Routes du tableau de bord d'analyse de données.
Réservé aux agents/admins (décisions stratégiques d'achat/vente).
"""
import io
from datetime import datetime
from flask import Blueprint, render_template, send_file
from flask_login import login_required
from fpdf import FPDF
from ..services.analytics_service import AnalyticsService
from .decorators import agent_required

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analyses")
@login_required
@agent_required
def dashboard():
    return render_template(
        "analytics/dashboard.html",
        summary=AnalyticsService.global_summary(),
        by_city=AnalyticsService.stats_by_city(),
        popular_types=AnalyticsService.popular_types(),
        best_cities=AnalyticsService.best_cities_to_buy(),
    )


@analytics_bp.route("/analyses/export-pdf")
@login_required
@agent_required
def export_pdf():
    # 1. Collecte des données Pandas réelles
    summary = AnalyticsService.global_summary()
    by_city = AnalyticsService.stats_by_city()
    best_cities = AnalyticsService.best_cities_to_buy()
    
    # 2. Construction de la structure PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    
    # En-tête Corporate
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, "YMMO - RAPPORT D'ANALYSE IMMOBILIERE", ln=True, align="C")
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 10, f"Edite le {datetime.now().strftime('%d/%m/%Y')} - Document confidentiel Agent", ln=True, align="C")
    pdf.ln(10)
    
    # Section 1 : Résumé Global
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, "1. Indicateurs Globaux du Catalogue", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f" - Nombre total de biens actifs : {summary['total_biens']}", ln=True)
    pdf.cell(0, 7, f" - Prix de vente moyen du catalogue : {summary['prix_moyen']:,.0f} EUR".replace(',', ' '), ln=True)
    pdf.cell(0, 7, f" - Prix moyen au metre carre : {summary['prix_m2_moyen']:,.0f} EUR/m2".replace(',', ' '), ln=True)
    pdf.cell(0, 7, f" - Surface moyenne des biens : {summary['surface_moyenne']:,.0f} m2".replace(',', ' '), ln=True)
    pdf.ln(10)
    
    # Section 2 : Tableau des villes
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "2. Synthese Detaillee par Ville", ln=True)
    pdf.ln(2)
    
    # En-tête Tableau
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(50, 8, "Ville", border=1, fill=True)
    pdf.cell(30, 8, "Biens", border=1, fill=True, align="C")
    pdf.cell(55, 8, "Prix Moyen", border=1, fill=True, align="C")
    pdf.cell(55, 8, "Prix Moyen / m2", border=1, fill=True, align="C")
    pdf.ln()
    
    # Lignes du tableau
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    for row in by_city:
        pdf.cell(50, 8, str(row['city']), border=1)
        pdf.cell(30, 8, str(row['nb_biens']), border=1, align="C")
        pdf.cell(55, 8, f"{row['prix_moyen']:,.0f} EUR".replace(',', ' '), border=1, align="R")
        pdf.cell(55, 8, f"{row['prix_m2_moyen']:,.0f} EUR/m2".replace(',', ' '), border=1, align="R")
        pdf.ln()
        
    pdf.ln(10)
    
    # Section 3 : Opportunités d'achat
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, "3. Opportunites d'Investissement Rentables", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "Classement des secteurs prioritaires (prix au m2 le plus bas) :", ln=True)
    pdf.ln(2)
    
    for idx, row in enumerate(best_cities, 1):
        pdf.cell(0, 7, f" {idx}. {row['city']} : {row['prix_m2_moyen']:,.0f} EUR/m2 ({row['nb_biens']} biens dispo)".replace(',', ' '), ln=True)
        
    # 3. Envoi du flux binaire en téléchargement direct et propre
    pdf_bytes = pdf.output()
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="Ymmo_Rapport_Marche.pdf"
    )