from .base import Base

from sqlalchemy import create_engine, Column, Integer, BigInteger, TEXT, Float, DateTime, Numeric, Boolean, text, func, Sequence, Index, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, TEXT

class discoms(Base):
    __tablename__ = 'discoms'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('discoms_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    unitNumber = Column(Integer, nullable=False)
    power = Column(Float, nullable=False)

class energy_export(Base):
    __tablename__ = 'energy_export'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('energy_export_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    unitNumber = Column(Integer, nullable=False)
    power = Column(Float, nullable=False)

class energy_import(Base):
    __tablename__ = 'energy_import'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('energy_import_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    unitNumber = Column(Integer, nullable=False)
    power = Column(Float, nullable=False)

class frequency(Base):
    __tablename__ = 'frequency'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('frequency_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    frequency = Column(Float, nullable=False)

class plants_centre(Base):
    __tablename__ = 'plants_centre'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('plants_centre_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    unitNumber = Column(Integer, nullable=False)
    power = Column(Float, nullable=False)

class plants_state(Base):
    __tablename__ = 'plants_state'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('plants_state_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    unitNumber = Column(Integer, nullable=False)
    power = Column(Float, nullable=False)

class states(Base):
    __tablename__ = 'states'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('states_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    unitNumber = Column(Integer, nullable=False)
    power = Column(Float, nullable=False)

class substations(Base):
    __tablename__ = 'substations'
    __table_args__ = {'schema': 'edata'}

    serialNumber = Column(BigInteger, Sequence('substations_serialNumber_seq', schema='edata'), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    unitNumber = Column(Integer, nullable=False)
    power = Column(Float, nullable=False)
