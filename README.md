# medical-data-annotator
An annotation tool for medical experts to label medical entities and relations between them in clinical narratives.

## Server
The `server` folder contains the backend code. It handles:
- API endpoints
- Business logic
- Database interactions (if applicable)

## Frontend
The `frontend` folder contains the client-side application. It includes:
- UI components
- State management
- API integrations

---

## How to run
1. In your Python virtual environment, run 

```bash
pip install fastapi uvicorn sqlmodel pydantic-settings python-multipart
```

2. At the root directory of the repo, build Docker image for UI:

```bash
make build
```

3. Start front-end UI by running

```bash
make run
```

4. Start back-end FastAPI server:

```bash
uvicorn server.main:app --reload
```

5. In any browser, navigate to `http://localhost:3000/` and start the annotation journey.

6. Select a pre-defined medical paragraph from the drop-down menu. The medical paragraph will be shown
for annotation. Then click `Create Document` button, which will create a document in the database.

7. Click any button from "Disease", "Medication", "Symptom", "Procedure" and "Anatomy", then select 
piece of text from the paragraph. You will see a corresponding JSON object in the "Annotation" area.

8. Drag and drop that JSON text component to either "Source" or "Target" area. Click "Create Source Entities"
or "Create Target Entities" accordingly. This will create the entity in the database.

9. Once a pair of source and target entities are filled, tick one item from the "Relation" checkbox, and 
clict the "Create Relation" button. A relation will be created in the database.

10. Export data: in another terminal, send the following API request. A `annotations.jsonl` file will be 
created at the root directory of the repo.

```bash
curl -X POST http://localhost:8000/api/v1/export -H "Content-Type: application/json" -d '{}' -o annotations.jsonl
```

### Demo
A screencast demo video can be found in the folder `screen_recording`.