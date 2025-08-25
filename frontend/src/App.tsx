import React, { useState } from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { createDocument } from "./services/api";
import { Annotation, EntityType, RelationType, RELATIONS, ENTITY_TYPES } from "./types";
import { API_BASE } from "./services/api";
import "./App.css";

// Predefined texts
const MEDICAL_TEXTS = [
  {
    id: 1,
    text: "The patient was diagnosed with pneumonia and was prescribed amoxicillin.",
  },
  { id: 2, text: "Diabetes can cause kidney failure if left untreated." },
  { id: 3, text: "Aspirin treats headaches but may worsen stomach ulcers." },
  {
    id: 4,
    text: "The surgery procedure helped relieve the patient's chronic back pain.",
  },
  { id: 5, text: "Hypertension indicates an increased risk of stroke." },
];

// ----------------- Draggable Annotation Card -----------------
const DraggableCard: React.FC<{ annotation: Annotation }> = ({
  annotation,
}) => {
  const [, drag] = useDrag(() => ({
    type: "ANNOTATION",
    item: { annotation },
  }));

  return (
    <div
      ref={(el) => {
        drag(el);
      }}
      style={{
        padding: "10px",
        margin: "5px",
        border: "1px solid #888",
        borderRadius: "6px",
        background: "#f0faff",
        cursor: "grab",
      }}
    >
      <pre style={{ margin: 0, fontSize: "12px" }}>
        {JSON.stringify(annotation, null, 2)}
      </pre>
    </div>
  );
};

// ----------------- Drop Zone -----------------
const DropZone: React.FC<{
  title: string;
  onDrop: (annotation: Annotation) => void;
  annotations: Annotation[];
}> = ({ title, onDrop, annotations }) => {
  const [{ isOver }, drop] = useDrop(
    () => ({
      accept: "ANNOTATION",
      drop: (item: { annotation: Annotation }) => {
        onDrop(item.annotation);
      },
      collect: (monitor) => ({
        isOver: monitor.isOver(),
      }),
    }),
    [onDrop]
  );

  return (
    <div
      ref={(el) => {
        drop(el);
      }}
      style={{
        flex: 1,
        minHeight: "200px",
        border: "2px dashed #ccc",
        borderRadius: "6px",
        padding: "10px",
        margin: "0 10px",
      }}
    >
      <h3>{title}</h3>
      {annotations.map((a) => (
        <DraggableCard key={a.id} annotation={a} />
      ))}
    </div>
  );
};

// ----------------- Relation Checklist -----------------
const RelationChecklist: React.FC<{
  relationState: Record<RelationType, boolean>;
  setRelationState: (state: Record<RelationType, boolean>) => void;
}> = ({ relationState, setRelationState }) => {
  const toggle = (rel: RelationType) => {
    setRelationState({ ...relationState, [rel]: !relationState[rel] });
  };

  return (
    <div
      style={{ padding: "10px", border: "1px solid #ddd", borderRadius: "6px" }}
    >
      <h4>Relations</h4>
      {RELATIONS.map((rel) => (
        <label key={rel} style={{ display: "block" }}>
          <input
            type="checkbox"
            checked={relationState[rel]}
            onChange={() => toggle(rel)}
          />
          {rel}
        </label>
      ))}
    </div>
  );
};

// ----------------- Main App -----------------
function App() {
  const [selectedType, setSelectedType] = useState<EntityType | null>(null);
  const [annotations, setAnnotations] = useState<Annotation[]>([]);
  const [sources, setSources] = useState<Annotation[]>([]);
  const [targets, setTargets] = useState<Annotation[]>([]);
  const [relationState, setRelationState] = useState<
    Record<RelationType, boolean>
  >({
    treats: false,
    causes: false,
    worsens: false,
    indicates: false,
  });
  const [docIndex, setDocIndex] = useState(0);

  const currentDoc = MEDICAL_TEXTS[docIndex];

  const handleMouseUp = () => {
    if (!selectedType) return;
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);
    const selectedText = selection.toString();
    if (!selectedText) return;

    const startOffset = range.startOffset;
    const endOffset = range.endOffset;

    const newAnnotation: Annotation = {
      id: Math.floor(Math.random() * 10000),
      text: selectedText,
      start: startOffset,
      end: endOffset,
      label: selectedType,
    };

    setAnnotations([...annotations, newAnnotation]);
    selection.removeAllRanges();
  };

  const addToSource = (annotation: Annotation) => {
    if (!sources.find((a) => a.id === annotation.id)) {
      setSources([...sources, annotation]);
    }
  };

  const addToTarget = (annotation: Annotation) => {
    if (!targets.find((a) => a.id === annotation.id)) {
      setTargets([...targets, annotation]);
    }
  };

  const handleCreateDocument = createDocument.bind(
    null,
    currentDoc.id,
    currentDoc.text
  );

  const handleCreateEntities = async (column: "source" | "target") => {
    const anns = column === "source" ? sources : targets;
    for (const ann of anns) {
      await fetch(
        `${API_BASE}/documents/${currentDoc.id}/entities`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ...ann, document_id: currentDoc.id, annotator: "Zhiyu" }),
        }
      );
    }
    alert(`${anns.length} entities created in ${column}.`);
  };

  const handleCreateRelations = async () => {
    const sourceId = sources.map((s) => s.id)[0];
    const targetId = targets.map((t) => t.id)[0];
    const relations = Object.entries(relationState)
      .filter(([_, enabled]) => enabled)
      .map(([predicate]) => ({
        source_entity_id: sourceId,
        target_entity_id: targetId,
        predicate,
        annotator: "Zhiyu",
      }));

    for (const relation of relations) {
      await fetch(
        `${API_BASE}/documents/${currentDoc.id}/relations`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(relation),
        }
      );
    }
    alert(`${relations.length} relations created.`);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div
        className="App"
        style={{ padding: "20px", fontFamily: "sans-serif" }}
      >
        <h2 style={{ fontSize: '36px' }}>Medical Text Annotation Tool</h2>

        {/* Entity type selector */}
        <div style={{ display: "flex", gap: "10px", margin: "20px 0" }}>
          {ENTITY_TYPES.map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              style={{
                padding: "10px 20px",
                borderRadius: "8px",
                border:
                  selectedType === type ? "2px solid blue" : "1px solid gray",
                background: selectedType === type ? "#e0f0ff" : "white",
                cursor: "pointer",
              }}
            >
              {type}
            </button>
          ))}
        </div>

        {/* Dropdown for medical text selection */}
        <div style={{ marginBottom: "10px" }}>
          <label>Select Document: </label>
          <select
            value={docIndex}
            onChange={(e) => {
              setDocIndex(Number(e.target.value));
              setAnnotations([]);
              setSources([]);
              setTargets([]);
            }}
          >
            {MEDICAL_TEXTS.map((doc, idx) => (
              <option key={doc.id} value={idx}>
                Medical Text {doc.id}
              </option>
            ))}
          </select>
          <button
            onClick={handleCreateDocument}
            style={{
              marginLeft: "10px",
              padding: "5px 10px",
              border: "1px solid #888",
              borderRadius: "6px",
              background: "#e0f0ff",
            }}
          >
            Create Document
          </button>
        </div>

        {/* Paragraph */}
        <div
          style={{
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "8px",
            marginBottom: "20px",
            background: "#fafafa",
          }}
          onMouseUp={handleMouseUp}
        >
          {currentDoc.text}
        </div>

        {/* Annotation list (draggables) */}
        <div style={{ marginBottom: "20px" }}>
          <h3>Annotations</h3>
          <div style={{ display: "flex", flexWrap: "wrap" }}>
            {annotations.map((a) => (
              <DraggableCard key={a.id} annotation={a} />
            ))}
          </div>
          <button
            onClick={() => {
              setAnnotations([]);
              setSources([]);
              setTargets([]);
            }}
            style={{
              marginBottom: "10px",
              border: "1px solid #888",
              borderRadius: "6px",
              padding: "5px 10px",
            }}
          >
            Clear All
          </button>
        </div>

        {/* Relation editor */}
        <div style={{ display: "flex", gap: "20px" }}>
          <DropZone title="Source" annotations={sources} onDrop={addToSource} />
          <DropZone title="Target" annotations={targets} onDrop={addToTarget} />
          <div style={{ flex: 1 }}>
            <RelationChecklist
              relationState={relationState}
              setRelationState={setRelationState}
            />
          </div>
        </div>

        {/* Create entities for source and target */}
        <div style={{ marginTop: "20px" }}>
          <button
            onClick={() => handleCreateEntities("source")}
            style={{
              marginRight: "10px",
              padding: "5px 10px",
              border: "1px solid #888",
              borderRadius: "6px",
              background: "#e0f0ff",
            }}
          >
            Create Source Entities
          </button>
          <button
            onClick={() => handleCreateEntities("target")}
            style={{
              padding: "5px 10px",
              border: "1px solid #888",
              borderRadius: "6px",
              background: "#e0f0ff",
            }}
          >
            Create Target Entities
          </button>
          <button
            onClick={handleCreateRelations}
            style={{
              marginLeft: "80px",
              padding: "5px 10px",
              border: "1px solid #888",
              borderRadius: "6px",
              background: "#e0f0ff",
            }}
          >
            Create Relation
          </button>
        </div>
      </div>
    </DndProvider>
  );
}

export default App;
