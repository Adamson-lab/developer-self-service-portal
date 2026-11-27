from fastapi import APIRouter, HTTPException

from core.catalog import load_catalog

router = APIRouter(prefix="/catalog", tags=["catalog"])
CATALOG = load_catalog()


@router.get("")
def list_catalog():
    return CATALOG


@router.get("/{name}")
def get_template(name: str):
    if name not in CATALOG:
        raise HTTPException(404, f"unknown template '{name}'")
    return CATALOG[name]
