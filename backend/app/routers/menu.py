from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..deps import get_db

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=List[schemas.MenuItemRead])
def list_menu_items(db: Session = Depends(get_db)):
    return crud.get_menu_items(db)
