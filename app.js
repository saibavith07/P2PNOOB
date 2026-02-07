const landing = document.getElementById("landing");
const app = document.getElementById("app");
const startBtn = document.getElementById("startBtn");
const generateBtn = document.getElementById("generateBtn");

const outputDiv = document.getElementById("output");
const loadingDiv = document.getElementById("loading");

startBtn.onclick = () => {
  landing.classList.add("hidden");
  app.classList.remove("hidden");
};

generateBtn.onclick = async () => {
  const topic = document.getElementById("topic").value.trim();
  if (!topic) {
    alert("Please enter a topic.");
    return;
  }

  const payload = {
    topic,
    domain: document.getElementById("domain").value,
    outputType: document.getElementById("outputType").value,
    depth: document.getElementById("depth").value
  };

  outputDiv.innerHTML = "";
  loadingDiv.classList.remove("hidden");

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    renderOutput(data.output);
  } catch (err) {
    outputDiv.innerHTML = "<p class='text-red-400'>Something went wrong.</p>";
  } finally {
    loadingDiv.classList.add("hidden");
  }
};

function renderOutput(text) {
  const sections = text.split("\n\n");

  sections.forEach(sec => {
    const card = document.createElement("div");
    card.className = "bg-slate-800 p-4 rounded-lg";
    card.textContent = sec;
    outputDiv.appendChild(card);
  });
}
