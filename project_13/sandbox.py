# sandbox.py

import io
import contextlib
import traceback


def run_code(code, tests):
    """
    Runs AI-generated Python code together with hidden tests.

    Returns:
        success: True/False
        output: captured output
        error: traceback/error message
    """

    # Create a namespace where the generated function will live
    namespace = {}

    # Combine generated code and hidden tests
    complete_code = code + "\n\n" + tests

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    try:
        # Execute the generated code and tests
        with contextlib.redirect_stdout(stdout_capture):
            with contextlib.redirect_stderr(stderr_capture):
                exec(complete_code, namespace)

        return {
            "success": True,
            "output": stdout_capture.getvalue(),
            "error": ""
        }

    except Exception:
        return {
            "success": False,
            "output": stdout_capture.getvalue(),
            "error": traceback.format_exc()
        }