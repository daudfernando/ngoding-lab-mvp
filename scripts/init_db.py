import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from core.database import get_db, init_db  # noqa: E402
from core.seed import seed_if_empty  # noqa: E402


def main():
    init_db()
    db = get_db()
    try:
        seed_if_empty(db)
        print("Database siap. Seed default sudah tersedia jika database sebelumnya kosong.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
