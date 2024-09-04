import uuid
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from .db import Base

class CVERecord(Base):
    __tablename__ = "cve_record"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    cve_id: Mapped[str] = mapped_column(
        String(length=20),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )

    date_published: Mapped[str] = mapped_column(
        DateTime(),
        nullable=True,
    )
    date_updated: Mapped[str] = mapped_column(
        DateTime(),
        nullable=True,
    )

    descriptions: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )

    def __repr__(self) -> str:
        return (f"<CVERecord(id={self.id}, "
                f"data_version={self.cve_id} "
                f"title={self.title})>")

