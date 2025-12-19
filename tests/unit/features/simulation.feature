# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

Feature: Simulation de revenu de base
  Scenario: Calculer le revenu de base pour un célibataire sans enfant
    Given un revenu mensuel de 2000 euros
    And un statut "celibataire"
    And 0 enfants
    When je lance la simulation
    Then le revenu de base doit être 1000 euros
    And le revenu total doit être 3000 euros

  Scenario: Rejeter un revenu mensuel négatif
    Given un revenu mensuel de -500 euros
    And un statut "celibataire"
    And 0 enfants
    When je lance la simulation
    Then la simulation doit échouer avec une erreur de validation
  
  Scenario: Rejeter un statut invalide
    Given un revenu mensuel de 2000 euros
    And un statut invalide "invalid_status"
    And 0 enfants
    When je lance la simulation
    Then la simulation doit échouer avec une erreur de validation
  
  Scenario: Rejeter un nombre d'enfants supérieur à 20
    Given un revenu mensuel de 2000 euros
    And un statut "en couple"
    And 25 enfants
    When je lance la simulation
    Then la simulation doit échouer avec une erreur de validation
  
  Scenario: Normaliser le statut avec espaces et majuscules
    Given un revenu mensuel de 2500 euros
    And un statut "  EN COUPLE  "
    And 2 enfants
    When je lance la simulation
    Then la simulation réussit
