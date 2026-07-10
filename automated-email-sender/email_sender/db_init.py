from __future__ import annotations

from .db.models import Base
from .db.session import engine



def main() -> None:
    # Creates tables if they don't exist.
    Base.metadata.create_all(bind=engine)
    print("DB initialized (tables created if missing).")


if __name__ == "__main__":
    main()

