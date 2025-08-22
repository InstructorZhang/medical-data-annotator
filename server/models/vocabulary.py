import enum


# -----------------------------
# Pre-defined Vocabularies
# -----------------------------

class EntityType(str, enum.Enum):
    disease = "Disease"
    medication = "Medication"
    symptom = "Symptom"
    procedure = "Procedure"
    anatomy = "Anatomy"

class RelationType(str, enum.Enum):
    treats = "treats"
    causes = "causes"
    worsens = "worsens"
    indicates = "indicates"
    has_symptom = "has_symptom"