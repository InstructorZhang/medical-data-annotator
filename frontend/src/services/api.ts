export const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api/v1";

export async function createDocument(docId: number, text: string) {
  await fetch(`${API_BASE}/documents`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: docId, text: text }),
  });
  alert("Document created!");
}

export async function createEntity(docId: number, entity: any) {
  return fetch(`${API_BASE}/documents/${docId}/entities`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(entity),
  }).then((res) => res.json());
}

export async function createRelation(docId: number, rel: any) {
  return fetch(`${API_BASE}/documents/${docId}/relations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(rel),
  }).then((res) => res.json());
}
