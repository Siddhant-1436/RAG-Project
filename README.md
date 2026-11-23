# NASA Report RAG

A local Flask retrieval-augmented-generation app for
`NASA_100_Page_Report_Siddhant_Kumar.pdf`.

## Run

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe app.py
```

Open `http://localhost:5000`.

## Optional LLM

Without an API key, the app returns extractive answers with page references.
To enable an OpenAI-compatible model, set `LLM_API_KEY`, `OPENAI_BASE_URL`,
and `LLM_MODEL` in `.env`.

## Test

```powershell
& .\.venv\Scripts\python.exe -m pytest -q
```
