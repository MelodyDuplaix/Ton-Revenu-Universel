# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

from enum import Enum
from pydantic import BaseModel, Field, field_validator

class StatutEnum(str, Enum):
    CELIBATAIRE = "célibataire"
    EN_COUPLE = "en couple"

class SimulationCreate(BaseModel):
    revenu_mensuel: float = Field(..., ge=0, description="Revenu mensuel (≥ 0)")
    statut: StatutEnum = Field(..., description="Statut familial")
    nombre_enfants: int = Field(..., ge=0, le=20, description="Nombre d'enfants (0-20)")
    
    @field_validator("statut", mode='before')
    @classmethod
    def normalize_statut(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return v

class SimulationResponse(SimulationCreate):
    id: int
    revenu_de_base: float
    revenu_total: float

    class Config:
        from_attributes = True
