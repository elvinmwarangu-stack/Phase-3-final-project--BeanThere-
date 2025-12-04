# beanthere/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Many-to-many association table
drink_flavor = Table(
    "drink_flavor",
    Base.metadata,
    Column("drink_id", Integer, ForeignKey("drinks.id"), primary_key=True),
    Column("flavor_id", Integer, ForeignKey("flavors.id"), primary_key=True),
)

class Bean(Base):
    __tablename__ = "beans"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    origin = Column(String, nullable=False)
    roaster = Column(String, default="Local Roaster")
    process = Column(String)                    # washed, natural, etc.
    cost_per_kg = Column(Float, default=90.0)   # USD
    grams_in_stock = Column(Float, default=0.0)

    drinks = relationship("Drink", back_populates="bean")

class Flavor(Base):
    __tablename__ = "flavors"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    drinks = relationship("Drink", secondary=drink_flavor, back_populates="flavors")

class Drink(Base):
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True)
    bean_id = Column(Integer, ForeignKey("beans.id"))
    grams_used = Column(Float, nullable=False)
    price_paid = Column(Float, nullable=False)
    rating = Column(Integer)        # 1–5
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    bean = relationship("Bean", back_populates="drinks")
    flavors = relationship("Flavor", secondary=drink_flavor, back_populates="drinks")