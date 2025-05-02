import sys
import subprocess
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py [app|admin]")
        sys.exit(1)

    command = sys.argv[1].lower()
    root_dir = os.path.dirname(os.path.abspath(__file__))

    if command == "app":
        subprocess.run([sys.executable, "app/app.py"], cwd=root_dir)
    elif command == "admin":
        subprocess.run([sys.executable, "app/admin.py"], cwd=root_dir)
    else:
        print("Invalid argument. Use 'app' or 'admin'.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("app")
    main()