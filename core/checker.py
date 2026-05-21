import ast
import base64
import subprocess
import sys


BLOCKED_IMPORTS = {"os", "sys", "subprocess", "pathlib", "socket", "requests", "shutil", "glob"}
BLOCKED_BUILTINS = {"open", "eval", "exec", "compile", "__import__", "input"}
ALLOWED_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "print": print,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
}


class CodeSafetyError(Exception):
    pass


def _validate_ast(code: str) -> None:
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        raise CodeSafetyError(f"Syntax error: {exc.msg}") from exc

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name.split(".")[0] for alias in getattr(node, "names", [])]
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module.split(".")[0])
            blocked = sorted(set(names) & BLOCKED_IMPORTS)
            if blocked:
                raise CodeSafetyError(f"Import tidak diizinkan: {', '.join(blocked)}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_BUILTINS:
                raise CodeSafetyError(f"Fungsi tidak diizinkan: {node.func.id}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise CodeSafetyError("Akses atribut internal tidak diizinkan.")
        if isinstance(node, ast.While):
            raise CodeSafetyError("Loop while belum diizinkan di MVP1.")


def run_safe_python(code, input_data="", timeout=2):
    timeout = min(int(timeout or 2), 2)
    _validate_ast(code)

    encoded_code = base64.b64encode((code or "").encode("utf-8")).decode("ascii")
    wrapper = f"""
import base64

code = base64.b64decode({encoded_code!r}).decode("utf-8")

def _controlled_input(prompt=""):
    try:
        return input()
    except EOFError:
        return ""

safe_builtins = {{
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "print": print,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "input": _controlled_input,
}}

exec(compile(code, "<student_code>", "exec"), {{"__builtins__": safe_builtins}}, {{}})
"""
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-c", wrapper],
            input=input_data or "",
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"status": "error", "output": "", "error": "Program terlalu lama berjalan."}

    if result.returncode != 0:
        error_lines = (result.stderr or "").strip().splitlines()
        error = error_lines[-1] if error_lines else "Kode error."
        return {"status": "error", "output": (result.stdout or "").strip(), "error": error}

    return {"status": "success", "output": (result.stdout or "").strip(), "error": ""}


def check_multiple_choice(correct_option_ids, selected_option_ids):
    return set(map(int, correct_option_ids)) == set(map(int, selected_option_ids))


def _normalize_output(text: str) -> str:
    return (text or "").strip().replace("\r\n", "\n")


def check_coding_output(code, expected_output, test_cases=None):
    test_cases = test_cases or []
    try:
        if test_cases:
            details = []
            for case in test_cases:
                result = run_safe_python(code, case.get("input_data", ""))
                expected = _normalize_output(case.get("expected_output", ""))
                actual = _normalize_output(result.get("output", ""))
                if result["status"] != "success":
                    return False, "error", result.get("error", "Kode error.")
                if actual != expected:
                    details.append(f"Expected: {expected} | Output: {actual}")
            if details:
                return False, "incorrect", details[0]
            return True, "correct", "Semua test case benar."

        result = run_safe_python(code)
        if result["status"] != "success":
            return False, "error", result.get("error", "Kode error.")
        actual = _normalize_output(result.get("output", ""))
        expected = _normalize_output(expected_output)
        if actual == expected:
            return True, "correct", "Output benar."
        return False, "incorrect", f"Output belum tepat. Expected: {expected} | Output: {actual}"
    except CodeSafetyError as exc:
        return False, "error", str(exc)
