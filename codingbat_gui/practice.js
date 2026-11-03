"use strict";
const $ = id => document.getElementById(id);
const previewMode = new URLSearchParams(location.search).has("preview");
const globalPrefix = previewMode ? "physics-study-preview-" : "physics-study-";
const cache = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key,value) { try { localStorage.setItem(key,value); } catch {} },
  json(key,fallback) { try { return JSON.parse(this.get(key)) ?? fallback; } catch { return fallback; } }
};
const codePrefix = set => "physics-" + set + (previewMode ? "-preview-" : "-v1-");
let catalog, session, selected, position = 0, running = false, request, generation = 0;
let language = cache.get(globalPrefix + "language") || cache.get(codePrefix("hw8") + "language") || "python";
let progress = cache.json(globalPrefix + "progress", {});
const token = document.querySelector('meta[name="practice-token"]').content;
const draftKey = (p,lang=language) => codePrefix(p.set) + (lang === "cpp" ? "code-cpp-" : "code-") + p.originalNumber;
const doneKey = (p,lang=language) => codePrefix(p.set) + (lang === "cpp" ? "done-cpp-" : "done-") + (p.originalNumber ?? p.number);
const editor = window.createPracticeEditor($("code"), {
  run: () => run(), change: value => { if (selected) cache.set(draftKey(selected),value); }
});
const paper = id => catalog.papers.find(p => p.id === id);
const unitName = id => catalog.units.find(u => u.id === id)?.title || id;
const mode = () => document.querySelector('input[name="mode"]:checked').value;
const randomModes = new Set(["random","midterm-random","exam-random","unit"]);

function el(tag,text,className) {
  const node=document.createElement(tag);
  if (text != null) node.textContent=text;
  if (className) node.className=className;
  return node;
}
function math(node,latex,display=false) {
  window.katex.render(latex,node,{throwOnError:false,trust:false,displayMode:display,output:"htmlAndMathml"});
}
function number(value) {
  if (!Number.isFinite(value)) return String(value);
  if (value === 0) return "0";
  const abs=Math.abs(value);
  if (abs >= 1e5 || abs < .0001) {
    const [coefficient,power]=value.toExponential(5).split("e");
    return Number(coefficient)+"\\times10^{"+Number(power)+"}";
  }
  return String(Number(value.toPrecision(7)));
}
function valueLatex(value) {
  if (!Array.isArray(value)) return typeof value === "number" ? number(value) : "\\text{"+String(value).replace(/[{}\\]/g,"")+"}";
  const rows=Array.isArray(value[0]) ? value : [value];
  return "\\begin{bmatrix}"+rows.map(row=>row.map(number).join("&")).join("\\\\")+"\\end{bmatrix}";
}
function unitsFor(name) {
  if (/Ratio|Multiple|Coefficient|Fraction|children|revolutions/.test(name)) return "";
  if (/Degrees/.test(name)) return "^{\\circ}";
  if (name === "G") return "\\;\\mathrm{m^3\,kg^{-1}\,s^{-2}}";
  if (name === "g" || /gravityEarth|gravityPlanet/.test(name)) return "\\;\\mathrm{m/s^2}";
  if (/[Mm]ass/.test(name)) return "\\;\\mathrm{kg}";
  if (/Km$/.test(name)) return "\\;\\mathrm{km}";
  if (/Cm$/.test(name)) return "\\;\\mathrm{cm}";
  if (/inertia|Inertia/.test(name)) return "\\;\\mathrm{kg\,m^2}";
  if (/angularAcceleration/.test(name)) return "\\;\\mathrm{rad/s^2}";
  if (/ax|ay/.test(name) && name.length===2 || /accelerationDown|tangentialAcceleration/.test(name)) return "\\;\\mathrm{m/s^2}";
  if (/torque/.test(name)) return "\\;\\mathrm{N\,m}";
  if (/springConstant/.test(name)) return "\\;\\mathrm{N/m}";
  if (/energy|Work/.test(name)) return "\\;\\mathrm J";
  if (/force|Force|tension|Tension|Normal/.test(name)) return Array.isArray(selected.example.input[name]) ? "\\;\\mathrm N" : "\\;\\mathrm N";
  if (/Speed|speed|Velocity|velocity|soundSpeed/.test(name)) return "\\;\\mathrm{m/s}";
  if (/time|Time|period|Period|duration|delay/.test(name)) return "\\;\\mathrm s";
  if (/height|Height|radius|Radius|distance|Distance|length|Length|width|stretch|Stretch|targetX|Position|Separation|Compression|displacement/.test(name) && !Array.isArray(selected.example.input[name])) return "\\;\\mathrm m";
  return "";
}
function setOptions(select,values,preferred) {
  const previous=preferred ?? select.value;
  select.replaceChildren(...values.map(value=>{
    const option=el("option",typeof value === "object" ? value.label : value);
    option.value=typeof value === "object" ? value.value : value;
    return option;
  }));
  if ([...select.options].some(o=>o.value===String(previous))) select.value=String(previous);
}
function matchingPapers() {
  return catalog.papers.filter(p=>p.kind === (mode().startsWith("midterm") ? "midterm" : "exam"));
}
function chosenPaper() {
  return matchingPapers().find(p=>p.semester === $("paper-semester").value && p.year === Number($("paper-year").value) && p.version === $("paper-version").value);
}
function updatePaperFields(level=0) {
  const papers=matchingPapers();
  if (level===0) setOptions($("paper-semester"),[...new Set(papers.map(p=>p.semester))],"Spring");
  const semesters=papers.filter(p=>p.semester === $("paper-semester").value);
  if (level<=1) setOptions($("paper-year"),[...new Set(semesters.map(p=>p.year))].sort((a,b)=>b-a));
  const years=semesters.filter(p=>p.year === Number($("paper-year").value));
  setOptions($("paper-version"),years.map(p=>p.version));
  $("version-field").hidden=years.length<=1;
}
function updateSettings(level=0) {
  if (!catalog) return;
  const current=mode(), randomized=current === "midterm-random" || current === "exam-random";
  const isPaper=current.endsWith("paper");
  $("format-field").hidden=!randomized;
  $("paper-fields").hidden=!(isPaper || randomized && $("random-format").value === "balanced");
  if (isPaper || randomized) updatePaperFields(level);
  $("unit-field").hidden=current !== "unit";
  $("count-field").hidden=isPaper || randomized && $("random-format").value === "balanced";
  $("question-count").disabled=$("count-field").hidden;
  $("variation-field").hidden=!randomModes.has(current);
  const pool=catalog.questions.filter(q=>current === "unit" ? q.unit === $("study-unit").value : randomized ? paper(q.set).kind === (current.startsWith("midterm") ? "midterm" : "exam") : true);
  $("question-count").max=pool.length;
  if (Number($("question-count").value)>pool.length) $("question-count").value=pool.length;
  const active=chosenPaper();
  const count=$("count-field").hidden ? active?.count : Number($("question-count").value);
  let summary=`${count || 0} questions`;
  if (randomized && $("random-format").value === "balanced" && active) {
    summary+=` · the same unit mix as ${active.semester} ${active.year}, version ${active.version}`;
  } else if (isPaper && active) summary+=` · ${active.semester} ${active.year}, version ${active.version}`;
  else if (current === "unit") summary+=" · "+unitName($("study-unit").value);
  else summary+=" · shuffled, with a mix of question types";
  $("session-preview").textContent=summary+".";
}
function recipe() {
  return {mode:mode(),format:$("random-format").value,paper:chosenPaper()?.id,
    unit:$("study-unit").value,count:Number($("question-count").value),variations:$("use-variations").checked};
}
function saveSession() {
  if (!session) return;
  session.position=position;
  cache.set(globalPrefix+"session",JSON.stringify(session));
}
function saveDraft() { if (selected) cache.set(draftKey(selected),editor.value); }
function home() {
  saveDraft();saveSession();request?.abort();generation++;running=false;
  $("home").hidden=false;$("workspace").hidden=true;
  $("resume").hidden=!cache.get(globalPrefix+"session");
  const url=new URL(location.href);url.searchParams.delete("set");url.searchParams.delete("study");url.hash="";history.replaceState(null,"",url);
  window.scrollTo({top:0});
}
async function start(recipeValue) {
  saveDraft();request?.abort();const current=++generation;
  $("start-study").disabled=true;$("start-study").textContent="Preparing…";$("home-error").hidden=true;
  try {
    const response=await fetch("/api/session",{method:"POST",headers:{"Content-Type":"application/json","X-Practice-Token":token},body:JSON.stringify(recipeValue)});
    const value=await response.json();
    if (current!==generation) return;
    if (!response.ok) throw new Error(value.error || "Could not create this session.");
    session=value;openSession(0);
  } catch(error) {
    $("home-error").textContent=error.message;$("home-error").hidden=false;
  } finally { $("start-study").disabled=false;$("start-study").textContent="Start studying"; }
}
function solved(p) { return progress[p.uid]?.solved || cache.get(doneKey(p,"python")) === "true" || cache.get(doneKey(p,"cpp")) === "true"; }
function markProgress() {
  if (!session) return;
  let complete=0;
  session.questions.forEach((p,i)=>{
    const button=document.querySelector(`[data-question="${i}"]`);
    if (!button) return;
    const done=solved(p);if(done)complete++;
    button.replaceChildren(el("span",`${i+1}. ${p.title}`));
    if(done)button.append(el("small","Solved","done"));
  });
  $("progress").textContent=`${complete} / ${session.questions.length} solved`;
}
function openSession(index) {
  $("home").hidden=true;$("workspace").hidden=false;$("skills-panel").hidden=true;$("show-skills").setAttribute("aria-expanded","false");
  $("session-title").textContent=session.title;
  $("problem-list").replaceChildren();$("problem-picker").replaceChildren();
  session.questions.forEach((p,i)=>{
    const button=el("button");button.type="button";button.dataset.question=i;button.addEventListener("click",()=>choose(i));
    const li=el("li");li.append(button);$("problem-list").append(li);
    const option=el("option",`${i+1}. ${p.title}`);option.value=i;$("problem-picker").append(option);
  });
  choose(Math.min(index,session.questions.length-1));markProgress();
  requestAnimationFrame(()=>editor.refresh());
}
function clearOutput() {
  $("status").textContent="Run your function to check the original and general cases.";$("status").className="";
  $("console").hidden=true;$("console").textContent="";$("results").replaceChildren();document.querySelector(".results-wrap").hidden=true;
}
function renderEquations() {
  const recommended=new Set(selected.equations);
  const list=$("equations");list.replaceChildren();
  const render=(equations,target)=>{
    for(const equation of equations) {
      const row=el("div",null,"equation-row"+(recommended.has(equation.id)?" recommended":""));
      row.append(el("div",equation.title,"equation-title"));
      const formula=el("div",null,"formula");math(formula,equation.latex,true);row.append(formula);target.append(row);
    }
  };
  const original=el("section",null,"practice-equation-sheet");
  original.append(el("h3","PH1013 Equation Sheet"));
  const constants=el("div",null,"sheet-constants");
  math(constants,"g=9.8\\,\\mathrm{m/s^2}\\quad G=6.67\\times10^{-11}\\,\\mathrm{N\\,m^2/kg^2}\\quad M_E=5.97\\times10^{24}\\,\\mathrm{kg}\\quad R_E=6370\\,\\mathrm{km}");
  original.append(constants);
  const columns=el("div",null,"sheet-columns");
  for(const entries of catalog.practiceSheet) {
    const column=el("div",null,"sheet-column");
    for(const equation of entries) {
      const useful=equation.ids.some(id=>recommended.has(id));
      const row=el("div",null,"sheet-formula"+(useful?" recommended":""));
      if(useful)row.setAttribute("aria-label","Useful for this question");
      math(row,equation.latex,true);column.append(row);
    }
    columns.append(column);
  }
  original.append(columns);list.append(original);
  const all=el("details");all.append(el("summary","Additional reference equations"));
  render(catalog.equations,all);list.append(all);
  const source=paper("midterm-s26")?.source;
  if(source){const link=el("a","Open the original equation-sheet PDF");link.href=source+"#page=3";link.target="_blank";link.rel="noopener";list.append(link);}
  $("equation-count").textContent=`· ${recommended.size} useful here`;
}
function choose(index,skipSave=false) {
  if(!skipSave)saveDraft();request?.abort();generation++;running=false;position=index;selected=session.questions[index];
  $("run").disabled=false;$("run").textContent="Run";editor.readOnly=false;
  const origin=paper(selected.set);
  $("title").textContent=selected.title;
  $("problem-meta").textContent=unitName(selected.unit)+" · "+origin.title+" · Q"+selected.originalNumber+(selected.variation?" · new numbers":"");
  $("source").hidden=!origin.source;if(origin.source)$("source").href=origin.source;
  const scenario=selected.scenario.split(/\nChoices:/)[0];
  $("description").replaceChildren();
  if(selected.variation) {
    $("description").append(el("p","A number variation of the original problem. Use the quantities below for the same physical setup."));
    const original=el("details");original.append(el("summary","Read the original scenario"),el("p",scenario));$("description").append(original);
  } else for(const paragraph of scenario.split(/\n\s*\n/))$("description").append(el("p",paragraph));
  $("givens").replaceChildren();
  for(const [name,value] of Object.entries(selected.example.input)) {
    const item=el("div",null,"given");const term=el("dt");term.append(el("code",name));
    const definition=el("dd");math(definition,valueLatex(value)+unitsFor(name));item.append(term,definition);$("givens").append(item);
  }
  $("task").textContent=selected.task.replace(/\nUse degrees for angle inputs and return an unrounded number\. Use the supplied g where present\.$/,"");
  $("tip").textContent=selected.tip;$("tip-details").open=false;
  window.renderPhysicsDiagram($("diagram"),selected);
  renderEquations();
  $("example").textContent="Input: "+JSON.stringify(selected.example.input,null,2)+"\n\nExpected: "+JSON.stringify(selected.example.expected);
  $("example-details").open=false;
  editor.setLanguage(language);editor.value=cache.get(draftKey(selected)) ?? (language==="cpp"?selected.cppStarter:selected.starter);
  $("language").value=language;$("code-label").textContent=(language==="cpp"?"C++":"Python")+" code";
  $("language-help").hidden=language!=="cpp";$("language-help").textContent="C++20 · Write the function; no main() needed. Return "+selected.cppReturnType+".";
  $("problem-picker").value=index;
  for(const button of document.querySelectorAll("[data-question]")) {
    if(Number(button.dataset.question)===index)button.setAttribute("aria-current","page");else button.removeAttribute("aria-current");
  }
  $("previous-question").disabled=index===0;
  $("next-question").textContent=index===session.questions.length-1?"Finish session":"Next question";
  $("question-position").textContent=`${index+1} of ${session.questions.length}`;
  const url=new URL(location.href);url.searchParams.set("study","session");url.searchParams.delete("set");url.hash=String(index+1);history.replaceState(null,"",url);
  saveSession();clearOutput();markProgress();
}
async function run() {
  if(!selected || running)return;
  saveDraft();const current=++generation;const task=selected;request=new AbortController();running=true;
  $("run").disabled=true;$("run").textContent="Running…";editor.readOnly=true;clearOutput();$("status").textContent="Checking your function…";
  try {
    const response=await fetch("/api/run",{method:"POST",signal:request.signal,headers:{"Content-Type":"application/json","X-Practice-Token":token},body:JSON.stringify({set:task.set,problem:task.originalNumber,language,code:editor.value})});
    const data=await response.json();if(current!==generation)return;
    const results=data.results || [], passed=results.filter(r=>r.passed).length;
    if(data.error){$("status").textContent="Fix the error below and run again.";$("status").className="error";}
    else {
      const done=results.length>0 && passed===results.length;
      $("status").textContent=`${passed} of ${results.length} cases passed.`;$("status").className=done?"success":"";
      cache.set(doneKey(task),String(done));
      progress[task.uid]={attempts:(progress[task.uid]?.attempts||0)+1,solved:progress[task.uid]?.solved||done,lastRun:Date.now()};
      cache.set(globalPrefix+"progress",JSON.stringify(progress));markProgress();renderSkills();
    }
    const output=[data.output,data.error].filter(Boolean).join("\n");$("console").textContent=output;$("console").hidden=!output;$("console").className=data.error?"error":"";
    for(const result of results) {
      const row=el("tr");
      const label=el("td");label.append(el("strong",result.label),el("pre",result.input));row.append(label);
      for(const value of [result.expected,result.actual]){const cell=el("td");cell.append(el("pre",value));row.append(cell);}
      row.append(el("td",result.passed?"Pass":"Try again",result.passed?"pass":"fail"));$("results").append(row);
    }
    document.querySelector(".results-wrap").hidden=!results.length;
  } catch(error) {
    if(error.name!=="AbortError" && current===generation){$("status").textContent="The app is not responding. Open Start Physics Practice and try again.";$("status").className="error";}
  } finally {if(current===generation){running=false;editor.readOnly=false;$("run").disabled=false;$("run").textContent="Run";}}
}
function renderSkills() {
  if(!catalog)return;
  $("skill-chart").replaceChildren();
  for(const unit of catalog.units) {
    const questions=catalog.questions.filter(p=>p.unit===unit.id);
    const families=new Set(questions.map(p=>p.family));
    const done=new Set(questions.filter(solved).map(p=>p.family));
    const attempted=new Set(questions.filter(p=>progress[p.uid]?.attempts || solved(p)).map(p=>p.family));
    const row=el("button",null,"skill-row");row.type="button";
    row.append(el("span",unit.title,"skill-name"));
    const track=el("span",null,"skill-track");const fill=el("span",null,"skill-fill");fill.style.width=(families.size?100*done.size/families.size:0)+"%";track.append(fill);row.append(track);
    row.append(el("span",`${done.size} / ${families.size}`,"skill-count"));
    row.title=`${done.size} solved, ${attempted.size} attempted, ${families.size} available question types`;
    row.addEventListener("click",()=>{home();document.querySelector('input[value="unit"]').checked=true;$("study-unit").value=unit.id;updateSettings();$("skills-panel").hidden=true;$("show-skills").setAttribute("aria-expanded","false");$("start-study").focus({preventScroll:true});});
    $("skill-chart").append(row);
  }
}
$("study-form").addEventListener("submit",e=>{e.preventDefault();start(recipe());});
$("mode-options").addEventListener("change",()=>updateSettings());
$("paper-semester").addEventListener("change",()=>updateSettings(1));
$("paper-year").addEventListener("change",()=>updateSettings(2));
for(const id of ["paper-version","random-format","question-count","study-unit"])$(id).addEventListener("input",()=>updateSettings(3));
$("home-link").addEventListener("click",e=>{e.preventDefault();home();});$("change-study").addEventListener("click",home);
$("open-homework").addEventListener("click",()=>start({mode:"homework",paper:"hw8"}));
$("resume").addEventListener("click",()=>{const previous=cache.json(globalPrefix+"session",null);if(previous?.questions?.length){session=previous;openSession(previous.position||0);}});
$("show-skills").addEventListener("click",()=>{const open=$("skills-panel").hidden;$("skills-panel").hidden=!open;$("show-skills").setAttribute("aria-expanded",String(open));if(open){renderSkills();$("skills-panel").scrollIntoView({block:"start"});}});
$("close-skills").addEventListener("click",()=>{$("skills-panel").hidden=true;$("show-skills").setAttribute("aria-expanded","false");$("show-skills").focus();});
$("problem-picker").addEventListener("change",e=>choose(Number(e.target.value)));
$("previous-question").addEventListener("click",()=>choose(position-1));
$("next-question").addEventListener("click",()=>{if(position<session.questions.length-1)choose(position+1);else{home();renderSkills();$("skills-panel").hidden=false;$("show-skills").setAttribute("aria-expanded","true");}});
$("language").addEventListener("change",e=>{saveDraft();language=e.target.value;cache.set(globalPrefix+"language",language);if(selected)choose(position,true);});
$("run").addEventListener("click",run);
$("reset").addEventListener("click",()=>{if(!selected || !confirm("Reset this function to the starter code?"))return;editor.value=language==="cpp"?selected.cppStarter:selected.starter;saveDraft();clearOutput();editor.focus();});
$("code-label").addEventListener("click",()=>editor.focus());
window.addEventListener("pagehide",()=>{saveDraft();saveSession();});

fetch("/api/catalog").then(r=>{if(!r.ok)throw new Error("Could not load the question bank.");return r.json();}).then(async value=>{
  catalog=value;
  setOptions($("study-unit"),catalog.units.map(u=>({value:u.id,label:u.title})));
  const papers=catalog.papers.filter(p=>p.kind!=="homework");
  $("bank-summary").textContent=`${catalog.questions.length} questions from ${papers.length} papers and Homework 8. Pick a starting point.`;
  $("mode-options").disabled=false;$("start-study").disabled=false;$("resume").hidden=!cache.get(globalPrefix+"session");
  updateSettings();renderSkills();
  const params=new URLSearchParams(location.search);
  if(params.has("set")) {
    const id=params.get("set"),meta=paper(id);
    if(meta)await start({mode:meta.kind==="homework"?"homework":meta.kind+"-paper",paper:id});
  } else if(params.get("study")==="session") {
    const previous=cache.json(globalPrefix+"session",null);if(previous?.questions?.length){session=previous;openSession(previous.position||0);}
  }
}).catch(error=>{$("bank-summary").textContent="Open Start Physics Practice, then refresh this page.";$("home-error").textContent=error.message;$("home-error").hidden=false;});
