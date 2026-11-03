"""Compile and run C++ submissions inside the practice app's isolated process."""
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).parent))
from worker import matches


HARNESS = r'''
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <tuple>
#include <type_traits>
#include <vector>

namespace practice_detail {
void write_json(std::ostream& out, const std::string& value) {
    out << '"';
    const char* hex = "0123456789abcdef";
    for (unsigned char c : value) {
        if (c == '"') out << "\\\"";
        else if (c == '\\') out << "\\\\";
        else if (c < 32) out << "\\u00" << hex[c >> 4] << hex[c & 15];
        else out << c;
    }
    out << '"';
}
void write_json(std::ostream& out, const char* value) {
    write_json(out, std::string(value));
}
template<class T, std::enable_if_t<std::is_arithmetic_v<T>, int> = 0>
void write_json(std::ostream& out, const T& value) {
    if constexpr (std::is_same_v<T, bool>) out << (value ? "true" : "false");
    else if constexpr (std::is_floating_point_v<T>) {
        if (std::isfinite(value)) out << std::setprecision(17) << value;
        else out << "null";
    } else out << value;
}
template<class T>
void write_json(std::ostream& out, const std::vector<T>& values) {
    out << '[';
    bool first = true;
    for (const auto& value : values) {
        if (!first) out << ',';
        first = false;
        write_json(out, value);
    }
    out << ']';
}
template<class... T>
void write_json(std::ostream& out, const std::tuple<T...>& values) {
    out << '[';
    bool first = true;
    std::apply([&](const auto&... value) {
        ((out << (first ? "" : ","), first = false, write_json(out, value)), ...);
    }, values);
    out << ']';
}
}

#include "solution.cpp"

int main() {
    std::ofstream answers("/tmp/answers.json");
    answers << '[';
    // PRACTICE_CALLS
    answers << ']';
}
'''


def literal(value):
    if isinstance(value, list):
        kind = "std::vector<std::vector<double>>" if value and isinstance(value[0], list) else "std::vector<double>"
        return kind + "{" + ",".join(literal(v) for v in value) + "}"
    return repr(float(value))


def response(error=None, output="", results=None):
    return {"error": error, "output": output, "results": results or []}


def run(payload):
    Path("/tmp/solution.cpp").write_text(payload["code"])
    calls = []
    for index, case in enumerate(payload["cases"]):
        arguments = ", ".join(literal(case["input"][name]) for name in payload["arguments"])
        call = f'{payload["method"]}({arguments})'
        if index:
            calls.append("    answers << ',';")
        calls.append(f"    practice_detail::write_json(answers, {call});")
    Path("/tmp/harness.cpp").write_text(HARNESS.replace("// PRACTICE_CALLS", "\n".join(calls)))
    try:
        compile_result = subprocess.run(
            ["/usr/bin/g++", "-std=c++20", "-O0", "-fuse-ld=bfd", "-fdiagnostics-color=never", "-fmax-errors=3",
             "/tmp/harness.cpp", "-o", "/tmp/submission"],
            capture_output=True, text=True, timeout=11,
        )
    except subprocess.TimeoutExpired:
        return response("TimeoutError: C++ compilation took too long.")
    if compile_result.returncode:
        diagnostics = compile_result.stderr.replace("/tmp/solution.cpp", "solution.cpp")
        diagnostics = diagnostics.replace("/tmp/harness.cpp", "exercise")
        diagnostics = re.sub(r"^In file included from exercise:[^\n]*\n", "", diagnostics)
        return response(diagnostics.strip()[:6000] or "C++ error: Could not build this function.")

    with open("/tmp/stdout.txt", "w+") as stdout, open("/tmp/stderr.txt", "w+") as stderr:
        try:
            result = subprocess.run(["/tmp/submission"], stdout=stdout, stderr=stderr, timeout=3)
        except subprocess.TimeoutExpired:
            return response("TimeoutError: Code took too long. Check for an infinite loop.")
        stdout.seek(0)
        output = stdout.read(32000)
        stderr.seek(0)
        errors = stderr.read(4000)
    if result.returncode:
        message = errors.strip() or f"C++ stopped (exit status {result.returncode})."
        return response("RuntimeError: " + message, output)
    try:
        values = json.loads(Path("/tmp/answers.json").read_text())
    except (ValueError, OSError):
        return response("RuntimeError: C++ could not return a result.", output)
    results = []
    for case, value in zip(payload["cases"], values):
        results.append({
            "label": case["label"], "input": repr(case["input"]),
            "expected": repr(case["expected"]), "actual": repr(value)[:4000],
            "passed": matches(value, case["expected"]),
        })
    if len(values) != len(payload["cases"]):
        return response("RuntimeError: Some C++ results are missing.", output, results)
    return response(None, output, results)


if __name__ == "__main__":
    resource.setrlimit(resource.RLIMIT_CPU, (12, 13))
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    try:
        answer = run(json.load(sys.stdin))
    except BaseException as error:
        answer = response(f"RuntimeError: {type(error).__name__}: {error}")
    sys.stdout.write(json.dumps(answer, allow_nan=False))
