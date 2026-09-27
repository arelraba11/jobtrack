from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Identity, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jobtrack.models.base import Base

if TYPE_CHECKING:
    from jobtrack.models.job_posting import JobPosting


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (CheckConstraint("length(trim(name)) > 0", name="name_not_blank"),)

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    website: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    job_postings: Mapped[list[JobPosting]] = relationship(
        back_populates="company",
        passive_deletes="all",
    )
