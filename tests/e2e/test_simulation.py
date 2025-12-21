# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

import os
from playwright.sync_api import Page
BASE_URL = os.environ.get("FRONTEND_URL", "http://frontend:8501")


def test_simulation_e2e(page: Page):
    # Ouvrir la page Streamlit
    page.goto(BASE_URL)

    # Remplir le formulaire
    page.fill('input[aria-label="Revenu mensuel actuel (€)"]', "2500")
    page.get_by_label("Statut").click()
    page.get_by_text("en couple", exact=True).click()
    page.fill('input[aria-label="Nombre d\'enfants"]', "2")

    # Cliquer sur le bouton de simulation
    page.locator('button:has-text("Lancer la simulation")').click(force=True)

    # Vérifier que les résultats s'affichent
    page.wait_for_selector("text=Revenu de base : 2100.0 €")
    page.wait_for_selector("text=Revenu total après application : 4600.0 €")
    # Vérifier que les graphiques s'affichent
    page.wait_for_selector('[data-testid="stPlotlyChart"]')


def test_stats_e2e(page: Page):
    page.goto(BASE_URL)
    page.wait_for_selector("text=Simulateur")
    # Vérifier que l'onglet "Statistiques globales" est présent
    assert page.is_visible("text=Statistiques globales")
    # Cliquer sur l'onglet
    page.click("text=Statistiques globales")
    # Vérifier que les métriques s'affichent
    page.wait_for_selector("text=Nombre total de simulations")
    assert page.is_visible("text=Revenu mensuel moyen")
