import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.warehouse.models import Base, DimUser, DimProduct, DimTime, FactEvent, FactOrder

class TestWarehouseModels:
    @pytest.fixture
    def in_memory_db(self):
        # Build local isolated in-memory Sqlite engine to test SQLAlchemy model mapping quickly
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine

    def test_orm_mapping_success(self, in_memory_db):
        Session = sessionmaker(bind=in_memory_db)
        session = Session()
        
        # 1. DimUser model check
        user = DimUser(
            user_id="usr_test001",
            username="test_dev",
            email="test@company.com",
            segment="VIP"
        )
        session.add(user)
        session.commit()
        
        fetched_user = session.query(DimUser).filter_by(user_id="usr_test001").first()
        assert fetched_user is not None
        assert fetched_user.username == "test_dev"
        assert fetched_user.segment == "VIP"
        
        # 2. DimProduct model check
        prod = DimProduct(
            product_id="prod_test001",
            product_name="Dev Product",
            category="Books",
            base_price=39.99
        )
        session.add(prod)
        session.commit()
        
        fetched_prod = session.query(DimProduct).filter_by(product_id="prod_test001").first()
        assert fetched_prod is not None
        assert fetched_prod.base_price == 39.99
        
        session.close()
