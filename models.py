from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime
import uuid

class Device(Base):
    __tablename__ = "devices"

    device_id = Column(String, primary_key=True, index=True)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)
    device_model = Column(String, nullable=True)

    records = relationship("AudioRecord", back_populates="device")

class AudioRecord(Base):
    __tablename__ = "audio_records"

    audio_id = Column(String, primary_key=True, index=True, default=lambda: f"A{uuid.uuid4().hex[:8].upper()}")
    device_id = Column(String, ForeignKey("devices.device_id"), index=True)
    file_path = Column(String)
    transcription = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    device = relationship("Device", back_populates="records")