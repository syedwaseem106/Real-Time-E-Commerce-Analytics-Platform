import pytest
from src.event_generator.generator import EcommerceEventGenerator
from src.event_generator.config import EVENT_TYPES, CATEGORIES

class TestEventGenerator:
    @pytest.fixture
    def generator(self):
        return EcommerceEventGenerator(num_users=20)

    def test_init_users_pool(self, generator):
        assert len(generator.users) == 20
        user = generator.users[0]
        assert 'user_id' in user
        assert 'username' in user
        assert 'email' in user
        assert 'device' in user

    def test_generate_single_event(self, generator):
        event = generator.generate_event()
        assert event is not None
        assert 'event_id' in event
        assert 'session_id' in event
        assert 'event_type' in event
        assert 'product_id' in event
        assert event['event_type'] in EVENT_TYPES
        assert event['category'] in CATEGORIES

    def test_funnel_progression_logic(self, generator):
        # View transitions
        assert generator.determine_next_event_type("purchase") == "payment"
        assert generator.determine_next_event_type("payment") == "page_view"
        assert generator.determine_next_event_type("remove_from_cart") == "product_view"

    def test_generate_batch(self, generator):
        batch = generator.generate_batch(count=15)
        assert len(batch) == 15
        for evt in batch:
            assert 'event_id' in evt
