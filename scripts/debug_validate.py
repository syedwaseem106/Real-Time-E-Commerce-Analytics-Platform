from src.quality.validators import EventValidator

evt = {
    "event_id": "e_902ac1f0",
    "user_id": "usr_99ac10",
    "session_id": "sess_891ac",
    "event_type": "page_view",
    "product_id": "prod_elec_001",
    "amount": 0.00,
    "timestamp": "2026-05-24 12:00:00.000",
    "event_date": "2026-05-24"
}

ok, errs = EventValidator.validate_event(evt)
print('OK:', ok)
print('Errors:', errs)
