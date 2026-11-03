"""Execute one practice submission inside the isolated Python process."""
import contextlib
import copy
import io
import json
import math
import resource
import sys
import traceback


class Output(io.StringIO):
    def write(self, value):
        if self.tell() + len(value) > 32000:
            raise RuntimeError("Output limit reached; check for a printing loop.")
        return super().write(value)


def matches(actual, expected):
    if isinstance(expected, str):
        return isinstance(actual, str) and actual == expected
    if isinstance(expected, list):
        return isinstance(actual, (list, tuple)) and len(actual) == len(expected) and all(
            matches(a, e) for a, e in zip(actual, expected)
        )
    return isinstance(actual, (int, float)) and not isinstance(actual, bool) and math.isclose(
        actual, expected, rel_tol=1e-6, abs_tol=1e-6
    )


def python_error(error):
    if isinstance(error, SyntaxError):
        return "".join(traceback.format_exception_only(type(error), error)).rstrip()
    frames = traceback.extract_tb(error.__traceback__)
    frames = [f for f in frames if f.filename == "solution.py"]
    detail = "".join(traceback.format_exception_only(type(error), error)).rstrip()
    if frames:
        return f'File "solution.py", line {frames[-1].lineno}\n{detail}'
    return detail


def run(payload):
    output = Output()
    results = []
    try:
        compiled = compile(payload["code"], "solution.py", "exec")
        namespace = {"__name__": "__practice__"}
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            exec(compiled, namespace)
            name = payload["method"]
            function = namespace.get(name)
            if not callable(function):
                raise NameError(f"Define a function named {name}.")
            for case in payload["cases"]:
                value = function(**copy.deepcopy(case["input"]))
                results.append({
                    "label": case["label"],
                    "input": repr(case["input"]),
                    "expected": repr(case["expected"]),
                    "actual": repr(value)[:4000],
                    "passed": matches(value, case["expected"]),
                })
        return {"output": output.getvalue(), "results": results, "error": None}
    except BaseException as error:
        return {"output": output.getvalue(), "results": results, "error": python_error(error)}


if __name__ == "__main__":
    resource.setrlimit(resource.RLIMIT_CPU, (2, 3))
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    payload = json.load(sys.stdin)
    response = run(payload)
    sys.stdout.write(json.dumps(response, allow_nan=False))
