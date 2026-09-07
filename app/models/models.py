from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from pgvector.sqlalchemy import Vector
import uuid
from sqlalchemy import Boolean
from sqlalchemy import Computed
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import Index
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    filename = Column(String, nullable=False)
    num_pages = Column(Integer)
    status = Column(String, default="processing")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer)
    embedding = Column(Vector(384))
    content_tsv = Column(TSVECTOR, Computed("to_tsvector('english', content)", persisted=True))

    document = relationship("Document", back_populates="chunks")


Index('chunks_content_tsv_idx', Chunk.content_tsv, postgresql_using='gin')



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())