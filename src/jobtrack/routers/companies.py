from datetime import UTC, datetime
from itertools import count

from fastapi import APIRouter, HTTPException, status

from jobtrack.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["companies"])

_companies: dict[int, CompanyRead] = {}
_ids = count(start=1)


def _get_or_404(company_id: int) -> CompanyRead:
    company = _companies.get(company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company


@router.post("", status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate) -> CompanyRead:
    company = CompanyRead(
        id=next(_ids),
        created_at=datetime.now(UTC),
        **payload.model_dump(),
    )
    _companies[company.id] = company
    return company


@router.get("")
def list_companies() -> list[CompanyRead]:
    return list(_companies.values())


@router.get("/{company_id}")
def get_company(company_id: int) -> CompanyRead:
    return _get_or_404(company_id)


@router.patch("/{company_id}")
def update_company(company_id: int, payload: CompanyUpdate) -> CompanyRead:
    company = _get_or_404(company_id)
    updates = payload.model_dump(exclude_unset=True)
    updated = company.model_copy(update=updates)
    _companies[company_id] = updated
    return updated


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int) -> None:
    _get_or_404(company_id)
    del _companies[company_id]
