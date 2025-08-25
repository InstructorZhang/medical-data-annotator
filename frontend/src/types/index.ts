export type EntityType =
  | "Disease"
  | "Medication"
  | "Symptom"
  | "Procedure"
  | "Anatomy";

export const ENTITY_TYPES: EntityType[] = [
  "Disease",
  "Medication",
  "Symptom",
  "Procedure",
  "Anatomy",
];

export type Annotation = {
  id: number;
  text: string;
  start: number;
  end: number;
  label: EntityType;
};

export type RelationType = "treats" | "causes" | "worsens" | "indicates";

export const RELATIONS: RelationType[] = [
  "treats",
  "causes",
  "worsens",
  "indicates",
];
