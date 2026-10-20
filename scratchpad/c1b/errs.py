import sys, runpy
try:
    runpy.run_path(r"scratchpad/c1b/check.py", run_name="__main__")
except (TypeError, SystemExit) as e:
    import questlib
    for x in questlib.ERRORS:
        print(repr(x))
