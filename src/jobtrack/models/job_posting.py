from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Identity, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jobtrack.models.base import Base

if TYPE_CHECKING:
    from jobtrack.models.company import Company


class JobPosting(Base):
    __tablename__ = "job_postings"
    __table_args__ = (CheckConstraint("length(trim(title)) > 0", name="title_not_blank"),)

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("companies.id", ondelete="RESTRICT"),
        index=True,
    )
    title: Mapped[str] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(Text)
    seniority: Mapped[str | None] = mapped_column(Text)
    extracted_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    company: Mapped[Company] = relationship(back_populates="job_postings")
