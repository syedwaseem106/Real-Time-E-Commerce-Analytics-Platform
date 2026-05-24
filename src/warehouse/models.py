from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Numeric, Boolean, DateTime, Date, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from src.utils.config import get_postgres_uri

Base = declarative_base()

class DimUser(Base):
    __tablename__ = 'dim_users'
    __table_args__ = {'schema': 'warehouse'}

    user_key = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    device_preference = Column(String(30))
    segment = Column(String(50), default='regular')
    first_seen_date = Column(Date)
    last_seen_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    events = relationship("FactEvent", back_populates="user")
    orders = relationship("FactOrder", back_populates="user")

    def __repr__(self):
        return f"<DimUser(user_id='{self.user_id}', username='{self.username}', segment='{self.segment}')>"

class DimProduct(Base):
    __tablename__ = 'dim_products'
    __table_args__ = {'schema': 'warehouse'}

    product_key = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(50), unique=True, nullable=False)
    product_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    brand = Column(String(100))
    base_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    events = relationship("FactEvent", back_populates="product")
    orders = relationship("FactOrder", back_populates="product")

    def __repr__(self):
        return f"<DimProduct(product_id='{self.product_id}', product_name='{self.product_name}')>"

class DimTime(Base):
    __tablename__ = 'dim_time'
    __table_args__ = {'schema': 'warehouse'}

    time_key = Column(Integer, primary_key=True, autoincrement=True)
    full_date = Column(Date, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    month_name = Column(String(20), nullable=False)
    week_of_year = Column(Integer, nullable=False)
    day_of_month = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    day_name = Column(String(20), nullable=False)
    is_weekend = Column(Boolean, nullable=False)
    is_holiday = Column(Boolean, default=False)
    fiscal_year = Column(Integer)
    fiscal_quarter = Column(Integer)

    events = relationship("FactEvent", back_populates="time")
    orders = relationship("FactOrder", back_populates="time")

    def __repr__(self):
        return f"<DimTime(date='{self.full_date}', day_name='{self.day_name}')>"

class FactEvent(Base):
    __tablename__ = 'fact_events'
    __table_args__ = {'schema': 'warehouse'}

    event_key = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(String(50), unique=True, nullable=False)
    user_key = Column(Integer, ForeignKey('warehouse.dim_users.user_key'))
    product_key = Column(Integer, ForeignKey('warehouse.dim_products.product_key'))
    time_key = Column(Integer, ForeignKey('warehouse.dim_time.time_key'))
    session_id = Column(String(50), nullable=False)
    event_type = Column(String(30), nullable=False)
    amount = Column(Numeric(10, 2), default=0.00)
    quantity = Column(Integer, default=1)
    device = Column(String(30))
    browser = Column(String(30))
    event_timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime)

    user = relationship("DimUser", back_populates="events")
    product = relationship("DimProduct", back_populates="events")
    time = relationship("DimTime", back_populates="events")

    def __repr__(self):
        return f"<FactEvent(event_id='{self.event_id}', type='{self.event_type}')>"

class FactOrder(Base):
    __tablename__ = 'fact_orders'
    __table_args__ = {'schema': 'warehouse'}

    order_key = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(String(50), unique=True, nullable=False)
    user_key = Column(Integer, ForeignKey('warehouse.dim_users.user_key'))
    product_key = Column(Integer, ForeignKey('warehouse.dim_products.product_key'))
    time_key = Column(Integer, ForeignKey('warehouse.dim_time.time_key'))
    session_id = Column(String(50), nullable=False)
    order_amount = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    device = Column(String(30))
    browser = Column(String(30))
    order_timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime)

    user = relationship("DimUser", back_populates="orders")
    product = relationship("DimProduct", back_populates="orders")
    time = relationship("DimTime", back_populates="orders")

    def __repr__(self):
        return f"<FactOrder(order_key={self.order_key}, amount={self.order_amount})>"

class StagingEvent(Base):
    __tablename__ = 'stg_events'
    __table_args__ = {'schema': 'staging'}

    event_id = Column(String(50), primary_key=True)
    user_id = Column(String(50))
    session_id = Column(String(50))
    event_type = Column(String(30))
    product_id = Column(String(50))
    product_name = Column(String(200))
    category = Column(String(100))
    amount = Column(Numeric(10, 2))
    quantity = Column(Integer)
    device = Column(String(30))
    browser = Column(String(30))
    city = Column(String(100))
    country = Column(String(100))
    event_timestamp = Column(DateTime)
    event_date = Column(Date)
    loaded_at = Column(DateTime)

    def __repr__(self):
        return f"<StagingEvent(event_id='{self.event_id}', type='{self.event_type}')>"

def get_engine(conn_string=None):
    """Factory method to construct SQLAlchemy Connection Engine."""
    if not conn_string:
        conn_string = get_postgres_uri()
    return create_engine(conn_string)

def create_all_tables(engine):
    """Creates operational schemas and provisions tables defined inside ORM metadata."""
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS warehouse;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics;"))
        conn.commit()
    Base.metadata.create_all(engine)
