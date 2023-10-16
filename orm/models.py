from sqlalchemy import (
    Column,
    Integer,
    DECIMAL,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    String,
    Table,
    Text,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT, BIT, INTEGER
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class FrPotatoApi(Base):
    __tablename__ = 'fr_potato_api_input'

    id = Column(BIGINT(20), primary_key=True)
    Province = Column(String(255))
    District = Column(String(255))
    AEZ = Column(String(255))
    Season = Column(String(255))
    refYieldClass = Column(String(255))
    longitude = Column(String(255))
    latitude = Column(String(255))
    Urea = Column(DECIMAL(5, 2))
    DAP = Column(DECIMAL(5, 2))
    NPK = Column(DECIMAL(5, 2))
    expectedYieldReponse = Column(DECIMAL(10, 2))
    totalFertilizerCost = Column(DECIMAL(10, 2))
    netRevenue = Column(DECIMAL(10, 2))
