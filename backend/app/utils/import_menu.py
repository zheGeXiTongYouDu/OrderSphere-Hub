import json
from pathlib import Path
from sqlalchemy.orm import Session
from ..database import SessionLocal, Base, engine
from ..models import MenuItem

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "foodMsg.json"


def init_db():
    Base.metadata.create_all(bind=engine)


def import_menu_from_json(db: Session, json_path: Path = DATA_PATH):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for raw_key, item in data.items():
        # 避免重复导入
        exists = db.query(MenuItem).filter(MenuItem.raw_key == raw_key).first()
        if exists:
            continue

        price = float(item.get("price", 0))
        category = ",".join(item.get("category", [])) if isinstance(item.get("category"), list) else item.get("category")
        type_ = ",".join(item.get("type", [])) if isinstance(item.get("type"), list) else item.get("type")

        menu_item = MenuItem(
            raw_key=raw_key,
            name=raw_key,  # 直接使用 JSON 键名作为展示名称
            price=price,
            category=category,
            type=type_,
            description=item.get("description", ""),
            region=item.get("region", ""),
        )
        db.add(menu_item)

    db.commit()


if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        import_menu_from_json(db)
        print("Menu imported successfully.")
    finally:
        db.close()
