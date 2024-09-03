import uuid
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship



class Base(DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CVERecord(Base):
    __tablename__ = "cve_record"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    data: Mapped[list["CVERecordData"]] = relationship()

    cve_id: Mapped[str] = mapped_column(
        String(length=20),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )

    def __repr__(self) -> str:
        return (f"<CVERecord(id={self.id}, "
                f"data_version={self.cve_id} "
                f"title={self.title})>")



class CVERecordData(Base):
    __tablename__ = "cve_record_data"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    cve_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cve_record.id"), nullable=False,

    )

    cve: Mapped["CVERecord"] = relationship(CVERecord,
                                            cascade="all,delete"
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
        return (f"<CVERecordData"
                f"( id={self.id}, "
                f"date_published={self.date_published} "
                f"date_updated={self.date_updated} "
                f"descriptions={self.descriptions})>")