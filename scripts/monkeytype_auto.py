import os
import subprocess
import sys


def run_monkeytype_trace():
    print("[🐒] Tracing tests with monkeytype run...")
    subprocess.run(
        ["monkeytype", "run", "scripts/run_tests_for_monkeytype.py"], check=True
    )


def list_traced_modules():
    print("[📦] Listing traced modules...")
    subprocess.run(["monkeytype", "list-modules"], check=True)


def apply_type_annotations(module):
    print(f"[✍️] Applying annotations to {module}...")
    subprocess.run(["monkeytype", "apply", module], check=True)


def rerun_pytest():
    print("[🧪] Rerunning tests after applying annotations...")
    subprocess.run(["python", "-m", "pytest"], check=True)


def main():
    if len(sys.argv) < 2:
        print("❗ Usage: python scripts/monkeytype_auto.py <module_name>")
        sys.exit(1)

    module = sys.argv[1]
    os.environ["PYTHONPATH"] = os.getcwd()

    run_monkeytype_trace()
    list_traced_modules()
    apply_type_annotations(module)
    rerun_pytest()


if __name__ == "__main__":
    main()
