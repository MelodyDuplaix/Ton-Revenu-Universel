# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

from fastapi.testclient import TestClient
from pytest_bdd import given, scenarios, then, when

from backend.app.main import app

scenarios("../features/simulation.feature")

client = TestClient(app)


@given("un revenu mensuel de 2000 euros", target_fixture="revenu_mensuel")
def revenu_mensuel():
    return 2000.0


@given('un statut "celibataire"', target_fixture="statut")
def statut():
    return "celibataire"

@given("un revenu mensuel de -500 euros", target_fixture="revenu_mensuel")
def revenu_mensuel_negatif():
    return -500.0

@given('un statut invalide "invalid_status"', target_fixture="statut")
def statut_invalide():
    return "invalid_status"

@given("un statut \"en couple\"", target_fixture="statut")
def statut_en_couple():
    return "en couple"

@given('un statut "  EN COUPLE  "', target_fixture="statut")
def statut_avec_espaces():
    return "  EN COUPLE  "

@given("25 enfants", target_fixture="nombre_enfants")
def beaucoup_enfants():
    return 25

@given("2 enfants", target_fixture="nombre_enfants")
def deux_enfants():
    return 2

@given("un revenu mensuel de 2500 euros", target_fixture="revenu_mensuel")
def revenu_mensuel_2500():
    return 2500.0


@given("0 enfants", target_fixture="nombre_enfants")
def nombre_enfants():
    return 0


@when("je lance la simulation", target_fixture="simulation")
def simulation(revenu_mensuel, statut, nombre_enfants):
    response = client.post(
        "/simulations/",
        json={
            "revenu_mensuel": revenu_mensuel,
            "statut": statut,
            "nombre_enfants": nombre_enfants,
        },
    )
    return response


@then("le revenu de base doit être 1000 euros", target_fixture="revenu_de_base")
def revenu_de_base(simulation):
    assert simulation.json()["revenu_de_base"] == 1000


@then("le revenu total doit être 3000 euros", target_fixture="revenu_total")
def revenu_total(simulation):
    assert simulation.json()["revenu_total"] == 3000

@then("la simulation doit échouer avec une erreur de validation")
def simulation_doit_echouer(simulation):
    assert simulation.status_code == 422, f"Expected 422, got {simulation.status_code}"
    assert "detail" in simulation.json(), "Response should contain validation errors"

@then("la simulation réussit")
def simulation_reussit(simulation):
    assert simulation.status_code == 200, f"Expected 200, got {simulation.status_code}: {simulation.json()}"
