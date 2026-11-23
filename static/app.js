const form = document.getElementById("questionForm");
const questionInput = document.getElementById("question");
const submitButton = document.getElementById("submitButton");
const answerArea = document.getElementById("answerArea");
const reindexButton = document.getElementById("reindexButton");

function escapeHtml(value) {
  const element = document.createElement("div");
  element.textContent = value;
  return element.innerHTML;
}

async function askQuestion(question) {
  submitButton.disabled = true;
  reindexButton.disabled = true;
  answerArea.innerHTML = '<p class="question-answer">Searching the report...</p>';

  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "The request failed.");
    }

    const sources = data.sources.map((source) =>
      `<article class="source"><strong>Page ${source.page}</strong>${escapeHtml(source.excerpt)}</article>`
    ).join("");

    answerArea.innerHTML =
      '<div class="question-answer"><h2>Answer</h2>' +
      escapeHtml(data.answer).replace(/\n/g, "<br>") +
      "</div>" +
      '<div class="sources"><strong style="grid-column:1/-1">Sources</strong>' +
      sources +
      "</div>";
  } catch (error) {
    answerArea.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
  } finally {
    submitButton.disabled = false;
    reindexButton.disabled = false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (question) {
    askQuestion(question);
  }
});

document.querySelectorAll("[data-question]").forEach((button) => {
  button.addEventListener("click", () => {
    questionInput.value = button.dataset.question;
    askQuestion(button.dataset.question);
  });
});

reindexButton.addEventListener("click", async () => {
  reindexButton.disabled = true;
  reindexButton.textContent = "Rebuilding...";
  try {
    const response = await fetch("/api/reindex", { method: "POST" });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Reindex failed.");
    }
    answerArea.innerHTML =
      `<p class="question-answer">Index rebuilt: ${data.pages} pages, ${data.chunks} chunks.</p>`;
  } catch (error) {
    answerArea.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
  } finally {
    reindexButton.disabled = false;
    reindexButton.textContent = "Rebuild index";
  }
});
