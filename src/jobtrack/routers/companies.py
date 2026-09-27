from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from jobtrack.db import DbSession
from jobtrack.models import Company
from jobtrack.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["companies"])


def _get_or_404(db: DbSession, company_id: int) -> Company:
    company = db.get(Company, company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company


@router.post("", status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate, db: DbSession) -> CompanyRead:
    company = Company(**payload.model_dump(mode="json"))
    db.add(company)
    db.commit()
    return CompanyRead.model_validate(company)


@router.get("")
def list_companies(db: DbSession) -> list[CompanyRead]:
    companies = db.scalars(select(Company).order_by(Company.id)).all()
    return [CompanyRead.model_validate(c) for c in companies]


@router.get("/{company_id}")
def get_company(company_id: int, db: DbSession) -> CompanyRead:
    return CompanyRead.model_validate(_get_or_404(db, company_id))


@router.patch("/{company_id}")
def update_company(company_id: int, payload: CompanyUpdate, db: DbSession) -> CompanyRead:
    company = _get_or_404(db, company_id)
    for field, value in payload.model_dump(exclude_unset=True, mode="json").items():
        setattr(company, field, value)
    db.commit()
    return CompanyRead.model_validate(company)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: DbSession) -> None:
    company = _get_or_404(db, company_id)
    db.delete(company)
    db.commit()
