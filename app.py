import os
import re
from pathlib import Path

import httpx
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from pypdf import PdfReader
from rank_bm25 import BM25Okapi

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
PDF_PATH = BASE_DIR / "NASA_100_Page_Report_Siddhant_Kumar.pdf"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 180

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

index = {
    "chunks": [],
    "pages": [],
    "bm25": None,
}


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def split_text(text, page_number):
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return

    for start in range(0, len(clean), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk = clean[start:start + CHUNK_SIZE].strip()
        if len(chunk) >= 80:
            index["chunks"].append(chunk)
            index["pages"].append(page_number)
        if start + CHUNK_SIZE >= len(clean):
            break


def build_index():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    index["chunks"].clear()
    index["pages"].clear()

    reader = PdfReader(str(PDF_PATH))
    for page_number, page in enumerate(reader.pages, start=1):
        split_text(page.extract_text() or "", page_number)

    if not index["chunks"]:
        raise ValueError("No searchable text could be extracted from the PDF.")

    index["bm25"] = BM25Okapi([tokenize(chunk) for chunk in index["chunks"]])
    return len(reader.pages), len(index["chunks"])


def retrieve(question, limit=5):
    if index["bm25"] is None:
        build_index()

    scores = index["bm25"].get_scores(tokenize(question))
    ranked = sorted(
        range(len(index["chunks"])),
        key=lambda position: scores[position],
        reverse=True,
    )
    results = []
    for position in ranked[:limit]:
        if scores[position] <= 0:
            continue
        results.append({
            "text": index["chunks"][position],
            "page": index["pages"][position],
            "score": round(float(scores[position]), 4),
        })
    return results


def extractive_answer(question, results):
    if not results:
        return "I could not find relevant text in the report."

    question_tokens = set(tokenize(question))
    scored_sentences = []
    for result in results:
        sentences = re.split(r"(?<=[.!?])\s+", result["text"])
        for sentence in sentences:
            tokens = set(tokenize(sentence))
            overlap = len(question_tokens & tokens)
            if overlap:
                scored_sentences.append((overlap, len(sentence), sentence, result["page"]))

    if not scored_sentences:
        return results[0]["text"][:700].rstrip() + ("..." if len(results[0]["text"]) > 700 else "")

    scored_sentences.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    seen = set()
    answer_lines = []
    for _, _, sentence, page in scored_sentences:
        sentence = sentence.strip()
        if sentence and sentence not in seen:
            seen.add(sentence)
            answer_lines.append(f"{sentence} (Page {page})")
        if len(answer_lines) == 4:
            break

    return "\n".join(answer_lines)


def generate_llm_answer(question, results):
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if not api_key:
        return extractive_answer(question, results)

    context = "\n\n".join(
        f"[Page {item['page']}]\n{item['text']}" for item in results
    )
    system_prompt = (
        "Answer only from the supplied report context. "
        "If the context does not contain the answer, say that clearly. "
        "Include page references for factual claims."
    )
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
    }

    try:
        response = httpx.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError):
        return extractive_answer(question, results)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/ask")
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    if not question:
        return jsonify({"error": "Please enter a question."}), 400
    if len(question) > 1000:
        return jsonify({"error": "Question is too long."}), 400

    try:
        results = retrieve(question)
    except (FileNotFoundError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 500

    answer = generate_llm_answer(question, results)
    sources = [
        {
            "page": item["page"],
            "score": item["score"],
            "excerpt": item["text"][:350].strip(),
        }
        for item in results
    ]
    return jsonify({"answer": answer, "sources": sources})


@app.post("/api/reindex")
def reindex():
    try:
        page_count, chunk_count = build_index()
        return jsonify({"pages": page_count, "chunks": chunk_count})
    except (FileNotFoundError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "pdf": PDF_PATH.name,
        "indexed": index["bm25"] is not None,
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "0") == "1")
