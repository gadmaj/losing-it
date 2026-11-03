"use strict";
const $ = (id) => document.getElementById(id);
const token = document.querySelector('meta[name="practice-token"]').content;
const preview = new URLSearchParams(location.search).has("preview");
let setId = new URLSearchParams(location.search).get("set") || "hw8";
const setPrefix = id => "physics-" + id + (preview ? "-preview-" : "-v1-");
let prefix = setPrefix(setId);
let practiceSets = [];
let problems = [];
let selected;
let running = false;
let request;
let generation = 0;
let setGeneration = 0;
let language = storageLanguage();
const editor = window.createPracticeEditor($("code"), {
  run: () => run(),
  change: value => { if (selected) storage.set(codeKey(selected.number), value); }
});

function storageLanguage() {
  try {
    const saved = localStorage.getItem(prefix + "language") ?? localStorage.getItem(setPrefix("hw8") + "language");
    return saved === "cpp" ? "cpp" : "python";
  }
  catch { return "python"; }
}

const languageName = () => language === "cpp" ? "C++" : "Python";
const codeKey = number => language === "cpp" ? "code-cpp-" + number : "code-" + number;
const doneKey = number => language === "cpp" ? "done-cpp-" + number : "done-" + number;
const starterCode = problem => language === "cpp" ? problem.cppStarter : problem.starter;

const diagrams = {
  1: `<svg viewBox="0 0 600 270" role="img" aria-labelledby="box-title box-desc">
    <title id="box-title">A box pushed along a frictionless floor</title>
    <desc id="box-desc">A 4 kilogram box moves 6.8 meters to the right. A 16 newton force acts 30 degrees below horizontal. The dashed box shows its later position.</desc>
    <defs>
      <marker id="box-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="currentColor"/></marker>
    </defs>
    <g class="diagram-rule" fill="none" stroke-width="1.5">
      <path d="M35 200 H565"/>
      <path d="M75 74 H175" stroke-dasharray="4 4"/>
      <rect x="400" y="120" width="85" height="80" stroke-dasharray="6 5"/>
      <path d="M172.5 210 V243 M442.5 210 V243"/>
    </g>
    <rect class="diagram-box" x="130" y="120" width="85" height="80" stroke-width="2"/>
    <g class="diagram-accent" fill="none" stroke-width="2">
      <path d="M75 74 L160 123" marker-end="url(#box-arrow)"/>
      <path d="M120 74 A45 45 0 0 1 114 96.5"/>
    </g>
    <path class="diagram-ink" d="M175 231 H440" fill="none" stroke-width="1.5" marker-start="url(#box-arrow)" marker-end="url(#box-arrow)"/>
    <g class="diagram-label">
      <text x="48" y="55">F = 16.0 N</text>
      <text x="127" y="99">30°</text>
      <text x="172.5" y="165" text-anchor="middle">4.00 kg</text>
      <text x="307.5" y="257" text-anchor="middle">d = 6.80 m</text>
      <text x="385" y="184">→</text>
    </g>
  </svg><figcaption>Homework setup: a constant push, 30° below horizontal.</figcaption>`,
  4: `<svg viewBox="0 0 620 325" role="img" aria-labelledby="graph-title graph-desc">
    <title id="graph-title">Homework force versus position graph</title>
    <desc id="graph-desc">Straight lines connect A at zero meters and zero newtons, B at ten meters and six newtons, C at twenty meters and zero newtons, D at twenty-five meters and negative three newtons, and E at thirty meters and zero newtons.</desc>
    <defs>
      <marker id="graph-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="currentColor"/></marker>
    </defs>
    <g class="diagram-rule" fill="none" stroke-width="0.7">
      <path d="M70 40 H550 M70 65 H550 M70 90 H550 M70 115 H550 M70 140 H550 M70 165 H550 M70 215 H550 M70 240 H550 M70 265 H550"/>
      <path d="M150 40 V265 M230 40 V265 M310 40 V265 M390 40 V265 M470 40 V265 M550 40 V265"/>
    </g>
    <g class="diagram-ink" fill="none" stroke-width="1.4">
      <path d="M70 287 V20" marker-end="url(#graph-arrow)"/>
      <path d="M60 190 H582" marker-end="url(#graph-arrow)"/>
    </g>
    <polyline class="diagram-accent" points="70,190 230,40 390,190 470,265 550,190" fill="none" stroke-width="3" stroke-linejoin="round"/>
    <g class="diagram-points">
      <circle cx="70" cy="190" r="3.5"/><circle cx="230" cy="40" r="3.5"/>
      <circle cx="390" cy="190" r="3.5"/><circle cx="470" cy="265" r="3.5"/><circle cx="550" cy="190" r="3.5"/>
    </g>
    <g class="diagram-label" text-anchor="middle">
      <text x="70" y="310">0</text><text x="150" y="310">5</text>
      <text x="230" y="310">10</text><text x="310" y="310">15</text>
      <text x="390" y="310">20</text><text x="470" y="310">25</text>
      <text x="550" y="310">30</text>
      <text x="51" y="46">6</text><text x="51" y="96">4</text>
      <text x="51" y="146">2</text><text x="51" y="196">0</text>
      <text x="47" y="246">−2</text><text x="47" y="271">−3</text>
      <text x="42" y="23">Fₓ (N)</text><text x="588" y="179">x (m)</text>
      <text x="85" y="178">A</text><text x="230" y="27">B</text>
      <text x="404" y="178">C</text><text x="470" y="288">D</text>
      <text x="558" y="178">E</text>
    </g>
  </svg><figcaption>The homework graph, including the negative-force section from 20 m to 30 m.</figcaption>`
};

const storage = {
  get(key) { try { return localStorage.getItem(prefix + key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(prefix + key, value); } catch {} }
};

function markProgress() {
  let complete = 0;
  for (const problem of problems) {
    const done = storage.get(doneKey(problem.number)) === "true";
    if (done) complete++;
    const button = document.querySelector(`[data-problem="${problem.number}"]`);
    button.textContent = `${problem.number}. ${problem.title}`;
    if (done) {
      const text = document.createElement("span");
      text.className = "done";
      text.textContent = "Complete";
      button.append(text);
    }
  }
  $("progress").textContent = `${complete} of ${problems.length} complete`;
}

function clearOutput() {
  $("status").className = "";
  $("status").textContent = "Run your code to see results.";
  $("console").hidden = true;
  $("console").textContent = "";
  $("results").replaceChildren();
  document.querySelector(".results-wrap").hidden = true;
}

function choose(number) {
  const problem = problems.find(p => p.number === number) || problems[0];
  request?.abort();
  generation++;
  selected = problem;
  running = false;
  $("run").disabled = false;
  $("run").textContent = "Run";
  editor.readOnly = false;
  $("title").textContent = `${problem.number}. ${problem.title}`;
  $("description").textContent = problem.description;
  $("diagram").replaceChildren();
  if (problem.diagram) {
    const image = document.createElement("img");
    image.src = problem.diagram.src;
    image.alt = problem.diagram.alt;
    const caption = document.createElement("figcaption");
    caption.textContent = "Diagram from the original midterm.";
    $("diagram").append(image, caption);
  } else if (setId === "hw8") $("diagram").innerHTML = diagrams[problem.number] || "";
  $("diagram").hidden = !problem.diagram && !(setId === "hw8" && diagrams[problem.number]);
  $("example").textContent = "Input: " + JSON.stringify(problem.example.input, null, 2)
    + "\n\nExpected: " + JSON.stringify(problem.example.expected);
  $("example-details").open = false;
  editor.setLanguage(language);
  editor.value = storage.get(codeKey(problem.number)) ?? starterCode(problem);
  $("language").value = language;
  $("code-label").textContent = languageName() + " code";
  $("language-help").hidden = language !== "cpp";
  $("language-help").textContent = "C++20 · Write the function below; no main() needed. Return " + problem.cppReturnType + ".";
  $("problem-picker").value = problem.number;
  for (const button of document.querySelectorAll("[data-problem]")) {
    if (Number(button.dataset.problem) === problem.number) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  }
  history.replaceState(null, "", "#" + problem.number);
  clearOutput();
}

function resultCell(text, pre = false) {
  const cell = document.createElement("td");
  if (pre) {
    const code = document.createElement("pre");
    code.textContent = text;
    cell.append(code);
  } else cell.textContent = text;
  return cell;
}

async function run() {
  if (!selected || running) return;
  storage.set(codeKey(selected.number), editor.value);
  const current = ++generation;
  request = new AbortController();
  running = true;
  $("run").disabled = true;
  $("run").textContent = "Running…";
  editor.readOnly = true;
  clearOutput();
  $("status").textContent = "Running " + languageName() + "…";
  try {
    const response = await fetch("/api/run", {
      method: "POST", signal: request.signal,
      headers: { "Content-Type": "application/json", "X-Practice-Token": token },
      body: JSON.stringify({ set: setId, problem: selected.number, code: editor.value, language })
    });
    const data = await response.json();
    if (current !== generation) return;
    const results = data.results || [];
    const passed = results.filter(r => r.passed).length;
    if (data.error) {
      $("status").textContent = "Fix the " + languageName() + " error below and run again.";
      $("status").className = "error";
    } else {
      $("status").textContent = `${passed} of ${results.length} tests passed.`;
      $("status").className = passed === results.length ? "success" : "";
      storage.set(doneKey(selected.number), String(results.length > 0 && passed === results.length));
      markProgress();
    }
    const output = [data.output, data.error].filter(Boolean).join("\n");
    $("console").textContent = output;
    $("console").hidden = !output;
    $("console").className = data.error ? "error" : "";
    for (const result of results) {
      const row = document.createElement("tr");
      const label = resultCell("");
      const name = document.createElement("span");
      name.className = "test-name";
      name.textContent = result.label;
      const input = document.createElement("pre");
      input.textContent = result.input;
      label.append(name, input);
      const status = resultCell(result.passed ? "Pass" : "Try again");
      status.className = result.passed ? "pass" : "fail";
      row.append(label, resultCell(result.expected, true), resultCell(result.actual, true), status);
      $("results").append(row);
    }
    document.querySelector(".results-wrap").hidden = results.length === 0;
  } catch (error) {
    if (error.name !== "AbortError" && current === generation) {
      $("status").textContent = "The practice app is not running. Open Start Physics Practice and try again.";
      $("status").className = "error";
    }
  } finally {
    if (current === generation) {
      running = false;
      editor.readOnly = false;
      $("run").disabled = false;
      $("run").textContent = "Run";
    }
  }
}

$("run").addEventListener("click", run);
$("reset").addEventListener("click", () => {
  if (!selected || !confirm("Reset the code for this problem?")) return;
  editor.value = starterCode(selected);
  storage.set(codeKey(selected.number), editor.value);
  storage.set(doneKey(selected.number), "false");
  markProgress(); clearOutput(); editor.focus();
});
$("problem-picker").addEventListener("change", e => choose(Number(e.target.value)));
$("language").addEventListener("change", e => {
  if (selected) storage.set(codeKey(selected.number), editor.value);
  language = e.target.value === "cpp" ? "cpp" : "python";
  storage.set("language", language);
  if (selected) choose(selected.number);
  markProgress();
});

async function loadSet(id, number = 1) {
  if (selected) storage.set(codeKey(selected.number), editor.value);
  request?.abort();
  generation++;
  const current = ++setGeneration;
  selected = undefined;
  problems = [];
  running = false;
  $("run").disabled = true;
  $("run").textContent = "Run";
  editor.readOnly = true;
  $("practice-set").disabled = true;
  $("problem-picker").disabled = true;
  $("problem-list").replaceChildren();
  $("problem-picker").replaceChildren();
  $("title").textContent = "Loading problems…";
  $("description").textContent = "";
  $("diagram").hidden = true;
  clearOutput();
  setId = id;
  prefix = setPrefix(id);
  storage.set("language", language);
  const active = practiceSets.find(s => s.id === id);
  $("practice-set").value = id;
  if (active.source) $("source").href = active.source;
  else $("source").removeAttribute("href");
  $("source").hidden = !active.source;
  document.title = "Physics practice · " + active.title;
  $("progress").textContent = "0 of " + active.count + " complete";
  const url = new URL(location.href);
  url.searchParams.set("set", id);
  url.hash = String(number);
  history.replaceState(null, "", url);
  try {
    const response = await fetch("/api/problems?set=" + encodeURIComponent(id));
    if (!response.ok) throw new Error("Could not load the practice set.");
    const data = await response.json();
    if (current !== setGeneration) return;
    problems = data;
    for (const problem of problems) {
      const li = document.createElement("li");
      const button = document.createElement("button");
      button.dataset.problem = problem.number;
      button.addEventListener("click", () => choose(problem.number));
      li.append(button); $("problem-list").append(li);
      const option = document.createElement("option");
      option.value = problem.number;
      option.textContent = `${problem.number}. ${problem.title}`;
      $("problem-picker").append(option);
    }
    markProgress();
    choose(number);
    $("problem-picker").disabled = false;
  } catch {
    if (current !== setGeneration) return;
    $("title").textContent = "Could not load the problems";
    $("description").textContent = "Open Start Physics Practice, then refresh this page.";
  } finally {
    if (current === setGeneration) $("practice-set").disabled = false;
  }
}

$("practice-set").addEventListener("change", e => loadSet(e.target.value));

fetch("/api/sets").then(r => {
  if (!r.ok) throw new Error("Could not load practice sets.");
  return r.json();
}).then(data => {
  practiceSets = data;
  $("practice-set").replaceChildren();
  for (const set of practiceSets) {
    const option = document.createElement("option");
    option.value = set.id;
    option.textContent = set.title;
    $("practice-set").append(option);
  }
  if (!practiceSets.some(s => s.id === setId)) setId = "hw8";
  return loadSet(setId, Number(location.hash.slice(1)) || 1);
}).catch(() => {
  $("title").textContent = "Could not load the problems";
  $("description").textContent = "Open Start Physics Practice, then refresh this page.";
});
