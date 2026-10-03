from cli import run_cli
from config import DATA_FILE
from storage import StorageError, load_tickets


def main() -> None:
    try:
        tickets = load_tickets(DATA_FILE)
    except StorageError as exc:
        print(f"Storage error: {exc}")
        return

    run_cli(tickets)


if __name__ == "__main__":
    main()