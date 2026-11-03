"""Stateless session assembly. A selection is saved by the browser and can be resumed."""
from collections import Counter
import random

from curriculum import UNITS


def public_problem(task, case_index=None):
    case_index=task.get("originalCase",0) if case_index is None else int(case_index)
    if not 0 <= case_index < len(task["cases"]):raise ValueError("Choose an available question version.")
    fields=("number","uid","set","family","paperTitle","title","method","description","scenario","task",
            "starter","cppStarter","cppReturnType","unit","tip","equations")
    result={k:task[k] for k in fields}
    result.update(example=task["cases"][case_index],caseIndex=case_index,variation=case_index!=task.get("originalCase",0),
                  diagram=task.get("diagram"),originalNumber=task["number"])
    return result


def build_session(sets, recipe):
    mode=recipe.get("mode","random")
    if mode not in ("random","midterm-random","midterm-paper","exam-random","exam-paper","unit","homework"):
        raise ValueError("Choose one of the study modes.")
    rng=random.Random()
    all_tasks=[p for meta in sets.values() for p in meta["problems"]]
    kind="midterm" if mode.startswith("midterm") else "exam"
    papers={key:meta for key,meta in sets.items() if meta["kind"]==kind}
    variation=recipe.get("variations",True) is True
    if mode.endswith("paper") or mode=="homework":
        key=recipe.get("paper","hw8" if mode=="homework" else next(iter(papers)))
        if key not in sets or (mode!="homework" and key not in papers):raise ValueError("Choose a paper from the list.")
        chosen=sets[key]["problems"]
        title=sets[key]["title"]
        variation=False
    else:
        pool=[p for p in all_tasks if not mode.endswith("random") or mode=="random" or sets[p["set"]]["kind"]==kind]
        if mode=="unit":
            unit=recipe.get("unit")
            if unit not in UNITS:raise ValueError("Choose a unit.")
            pool=[p for p in all_tasks if p["unit"]==unit]
        if not pool:raise ValueError("No questions are available for that selection.")
        if mode in ("midterm-random","exam-random") and recipe.get("format","balanced")=="balanced":
            template=recipe.get("paper") or next(iter(papers))
            if template not in papers:raise ValueError("Choose a format paper.")
            required=Counter(p["unit"] for p in papers[template]["problems"])
            chosen=[]
            used=set()
            for unit,amount in required.items():
                candidates=[p for p in pool if p["unit"]==unit]
                rng.shuffle(candidates)
                # Prefer different question types before repeating a family.
                candidates.sort(key=lambda p:p["family"] in used)
                local=[]
                for candidate in candidates:
                    if candidate["family"] not in used:
                        local.append(candidate);used.add(candidate["family"])
                        if len(local)==amount:break
                if len(local)<amount:
                    local.extend(rng.sample([p for p in candidates if p not in local],amount-len(local)))
                chosen.extend(local)
            rng.shuffle(chosen)
            title=("Midterm" if kind=="midterm" else "Final exam")+" · matched format"
        else:
            count=recipe.get("count",10)
            if type(count) is not int or not 1<=count<=len(pool):
                raise ValueError(f"Choose between 1 and {len(pool)} questions.")
            rng.shuffle(pool)
            first=[];later=[];families=set()
            for task in pool:
                (later if task["family"] in families else first).append(task)
                families.add(task["family"])
            chosen=(first+later)[:count]
            title=UNITS[recipe["unit"]] if mode=="unit" else ("Random questions" if mode=="random" else "Random "+("midterm" if kind=="midterm" else "final"))
    questions=[public_problem(task,rng.randrange(len(task["cases"])) if variation else None) for task in chosen]
    return {"title":title,"mode":mode,"recipe":recipe,"questions":questions,
            "unitCounts":dict(Counter(p["unit"] for p in questions))}
