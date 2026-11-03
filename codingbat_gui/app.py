#!/usr/bin/env python3
"""Local physics practice GUI. Run this file, then open its printed address."""
import argparse
import ast
import hmac
import json
import os
from pathlib import Path
import secrets
import signal
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from midterms import FALL, SPRING
from question_bank import add_papers, UNITS
from curriculum import enrich, sheet, practice_sheet
from study import build_session, public_problem

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent
TOKEN = secrets.token_urlsafe(32)
RUN_LOCK = threading.BoundedSemaphore(1)
EDITOR_ASSETS = {
    "/vendor/codemirror/" + name: ("vendor/codemirror/" + name,
                                  "text/css; charset=utf-8" if name.endswith(".css") else "text/javascript; charset=utf-8")
    for name in ("lib/codemirror.js", "lib/codemirror.css", "mode/python/python.js", "mode/clike/clike.js",
                 "addon/hint/show-hint.js", "addon/hint/show-hint.css", "addon/edit/matchbrackets.js")
}


def add_starters(problem):
    arguments = problem["arguments"]
    problem["starter"] = (
        "import math\n\n\ndef " + problem["method"] + "(" + ", ".join(arguments) + "):\n"
        "    return None\n"
    )

    def cpp_type(value):
        if isinstance(value, list):
            return "vector<vector<double>>" if value and isinstance(value[0], list) else "vector<double>"
        return "double"

    example = problem["cases"][0]["input"]
    parameters = ", ".join(f"{cpp_type(example[name])} {name}" for name in arguments)
    result_type = problem["cppReturnType"]
    placeholder = '{0.0, "", ""}' if result_type.startswith("tuple<") else "{}"
    problem["cppStarter"] = (
        "#include <cmath>\n#include <vector>\n#include <string>\n#include <tuple>\n"
        "#include <iostream>\nusing namespace std;\n\n"
        f"{result_type} {problem['method']}({parameters}) {{\n"
        f"    return {placeholder};\n}}\n"
    )


def load_problems():
    cases = json.loads((SOURCE / "physics_leetcode_cases.json").read_text())
    tree = ast.parse((SOURCE / "physics_leetcode.py").read_text())
    solution = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Solution")
    methods = {n.name: n for n in solution.body if isinstance(n, ast.FunctionDef)}
    for problem in cases:
        node = methods[problem["method"]]
        arguments = [a.arg for a in node.args.args if a.arg != "self"]
        problem["arguments"] = arguments
        problem["description"] = ast.get_docstring(node).split("\n", 1)[1].strip()
        problem["cppReturnType"] = "tuple<double, string, string>" if problem["number"] == 3 else "vector<double>"
        add_starters(problem)
    return cases


PROBLEMS = load_problems()
for midterm_problem in SPRING + FALL:
    add_starters(midterm_problem)
SETS = {
    "hw8": {"title": "Homework 8", "problems": PROBLEMS,
            "file": "PH-UY 1013 F26 HW8 - PH-UY 1013_ MECHANICS (F26), Fall 2026 _ WebAssign.pdf"},
    "midterm-s26": {"title": "Midterm · Spring 2026", "problems": SPRING, "file": "1013X1aS26.pdf"},
    "midterm-f25": {"title": "Midterm · Fall 2025", "problems": FALL, "file": "1013X1aF25.pdf"},
}
add_papers(SETS)
for paper in SETS.values():
    for task in paper["problems"]:
        enrich(task)
        add_starters(task)
for directory in ("latex", "katex"):
    for asset in (ROOT / "vendor" / directory).rglob("*"):
        if asset.is_file() and asset.suffix in (".js", ".css", ".woff2"):
            suffix_types={".js":"text/javascript", ".css":"text/css", ".woff2":"font/woff2"}
            relative=asset.relative_to(ROOT).as_posix()
            EDITOR_ASSETS["/"+relative]=(relative,suffix_types[asset.suffix])


def catalog():
    papers=[{"id":key,"title":value["title"],"count":len(value["problems"]),
             "kind":value["kind"],"semester":value["semester"],"year":value["year"],"version":value["version"],
             "source":"/sources/"+key+".pdf" if (SOURCE/value["file"]).is_file() else None,
             "unitCounts":{unit:sum(p["unit"]==unit for p in value["problems"]) for unit in UNITS}}
            for key,value in SETS.items()]
    questions=[{k:p[k] for k in ("uid","set","number","unit","family","title")} for s in SETS.values() for p in s["problems"]]
    return {"papers":papers,"units":[{"id":key,"title":title} for key,title in UNITS.items()],
            "questions":questions,"equations":sheet(),"practiceSheet":practice_sheet(),"constants":{"g":9.8,"G":6.67e-11,"earthMass":5.97e24,"earthRadiusKm":6370},
            "sources":[{"file":s["file"],"paper":key} for key,s in SETS.items()]+
                      [{"file":"midterm.pdf","contains":[key for key,s in SETS.items() if s["kind"]=="midterm"]},
                       {"file":"final.pdf","contains":[key for key,s in SETS.items() if s["kind"]=="exam"]}]}


def execute(code, problem, language="python"):
    worker_name = "cpp_worker.py" if language == "cpp" else "worker.py"
    command = [
        "/usr/bin/bwrap", "--unshare-all", "--die-with-parent", "--new-session",
        "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib64", "/lib64",
        "--symlink", "usr/lib", "/lib", "--proc", "/proc", "--dev", "/dev",
        "--tmpfs", "/tmp", "--dir", "/work", "--ro-bind", str(ROOT / "worker.py"),
        "/work/worker.py", "--ro-bind", str(ROOT / "cpp_worker.py"), "/work/cpp_worker.py",
        "--chdir", "/work", "/usr/bin/python3", "-I", "-S", "/work/" + worker_name,
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True,
                               env={"LANG": "C.UTF-8", "PATH": "/usr/bin"})
    payload = json.dumps({"code": code, "method": problem["method"], "cases": problem["cases"],
                          "arguments": problem["arguments"]})
    name = "C++" if language == "cpp" else "Python"
    try:
        stdout, stderr = process.communicate(payload, timeout=16 if language == "cpp" else 3)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        return {"error": "TimeoutError: Code took too long. Check for an infinite loop.",
                "output": "", "results": []}
    if process.returncode:
        return {"error": f"RuntimeError: {name} stopped. Check for an infinite loop or excessive memory use.",
                "output": "", "results": []}
    try:
        return json.loads(stdout)
    except ValueError:
        return {"error": f"RuntimeError: {name} could not return a result.", "output": "", "results": []}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, status, body, content_type="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlsplit(self.path)
        route = url.path
        if route == "/api/catalog":
            return self.send(200,catalog())
        if route == "/api/sets":
            return self.send(200, [{"id": key, "title": value["title"], "count": len(value["problems"]),
                                    "source": "/sources/" + key + ".pdf" if (SOURCE / value["file"]).is_file() else None}
                                   for key, value in SETS.items()])
        if route == "/api/problems":
            set_id = parse_qs(url.query).get("set", ["hw8"])[0]
            if set_id not in SETS:
                return self.send(404, {"error": "Choose a practice set."})
            public = [public_problem(p) for p in SETS[set_id]["problems"]]
            return self.send(200, public)
        for set_id, practice_set in SETS.items():
            if route == "/sources/" + set_id + ".pdf":
                source_file = SOURCE / practice_set["file"]
                if not source_file.is_file():
                    return self.send(404, {"error": "Original PDF is not installed on this computer."})
                return self.send(200, source_file.read_bytes(), "application/pdf")
        diagram_names = {p["diagram"]["src"] for p in SPRING + FALL if p.get("diagram")}
        if route == "/diagrams/bowl.svg":
            return self.send(200,(ROOT/"diagrams/bowl.svg").read_text(),"image/svg+xml")
        if route in diagram_names:
            return self.send(200, (ROOT / "diagrams" / Path(route).name).read_bytes(), "image/png")
        assets = {"/": ("index.html", "text/html; charset=utf-8"),
                  "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                  "/syntax.js": ("syntax.js", "text/javascript; charset=utf-8"),
                  "/editor.js": ("editor.js", "text/javascript; charset=utf-8"),
                  "/diagrams.js": ("diagrams.js", "text/javascript; charset=utf-8"),
                  "/practice.js": ("practice.js", "text/javascript; charset=utf-8"),
                  "/tokens.css": ("tokens.css", "text/css; charset=utf-8"),
                  "/style.css": ("style.css", "text/css; charset=utf-8")}
        assets.update(EDITOR_ASSETS)
        if route not in assets:
            return self.send(404, {"error": "Not found"})
        name, content_type = assets[route]
        content = (ROOT / name).read_bytes() if name.endswith(".woff2") else (ROOT / name).read_text()
        if name == "index.html":
            content = content.replace("__PRACTICE_TOKEN__", TOKEN)
        self.send(200, content, content_type)

    def do_POST(self):
        if self.path not in ("/api/run","/api/session"):
            return self.send(404, {"error": "Not found"})
        token = self.headers.get("X-Practice-Token", "")
        if not hmac.compare_digest(token, TOKEN):
            return self.send(403, {"error": "Refresh the page and try again."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 65536:
                return self.send(400, {"error": "Code is too long."})
            payload = json.loads(self.rfile.read(length))
            if self.path == "/api/session":
                if not isinstance(payload,dict):raise ValueError()
                try:
                    return self.send(200,build_session(SETS,payload))
                except (ValueError,KeyError,TypeError) as error:
                    return self.send(400,{"error":str(error) or "Choose a study mode and try again."})
            number = payload["problem"]
            code = payload["code"]
            language = payload.get("language", "python")
            set_id = payload.get("set", "hw8")
            if not isinstance(set_id, str) or set_id not in SETS:
                raise ValueError()
            problems = SETS[set_id]["problems"]
            if type(number) is not int or not 1 <= number <= len(problems) or not isinstance(code, str):
                raise ValueError()
            if language not in ("python", "cpp"):
                raise ValueError()
        except (ValueError, KeyError, TypeError):
            return self.send(400, {"error": "Choose a problem and enter code."})
        if not RUN_LOCK.acquire(blocking=False):
            return self.send(409, {"error": "Code is still running. Try again in a moment."})
        try:
            result = execute(code, problems[number - 1], language)
        except OSError:
            result = {"error": "The code runner could not start. Restart the practice app.",
                      "output": "", "results": []}
        finally:
            RUN_LOCK.release()
        self.send(200, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Physics practice: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
