from app import app, build_index, retrieve


def test_health():
    with app.test_client() as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.get_json()["status"] == "ok"


def test_pdf_index():
    page_count, chunk_count = build_index()
    assert page_count == 101
    assert chunk_count > 100


def test_retrieve_returns_page_sources():
    build_index()
    results = retrieve("What does the Artemis program do?")
    assert results
    assert all(result["page"] >= 1 for result in results)
    assert all(result["text"] for result in results)


def test_ask_validation():
    with app.test_client() as client:
        response = client.post("/api/ask", json={"question": ""})
        assert response.status_code == 400
