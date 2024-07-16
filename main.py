import sys
from src.cli import run_cli
from src.web_app import run_web_app

def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_web_app()

if __name__ == "__main__":
    main()
    