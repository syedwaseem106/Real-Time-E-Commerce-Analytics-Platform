import pytest
from src.quality.validators import EventValidator, BatchValidator

class TestEventValidator:
    @pytest.fixture
    def valid_event(self):
        return {
            "event_id": "e_902ac1f0",
            "user_id": "usr_99ac10",
            "session_id": "sess_891ac",
            "event_type": "page_view",
            "product_id": "prod_elec_001",
            "amount": 0.00,
            "timestamp": "2026-05-24 12:00:00.000",
            "event_date": "2026-05-24"
        }

    def test_schema_valid_event(self, valid_event):
        ok, errs = EventValidator.validate_event(valid_event)
        assert ok is True
        assert len(errs) == 0

    def test_missing_required_fields(self, valid_event):
        invalid_evt = valid_event.copy()
        del invalid_evt["event_id"]
        ok, errs = EventValidator.validate_event(invalid_evt)
        assert ok is False
        assert any("Missing required field" in e for e in errs)

    def test_negative_purchase_amount(self, valid_event):
        invalid_evt = valid_event.copy()
        invalid_evt["event_type"] = "purchase"
        invalid_evt["amount"] = -150.00
        ok, errs = EventValidator.validate_event(invalid_evt)
        assert ok is False
        assert any("invalid amount" in e.lower() for e in errs)

    def test_invalid_event_type(self, valid_event):
        invalid_evt = valid_event.copy()
        invalid_evt["event_type"] = "user_login" # Not in config event list
        ok, errs = EventValidator.validate_event(invalid_evt)
        assert ok is False
        assert any("Invalid event_type" in e for e in errs)
