from src.quality.validators import EventValidator

def filter_invalid_events(events: list) -> tuple[list, list]:
    """
    Splits a raw ingestion batch of dictionary events into high-fidelity
    valid events and dead-letter invalid events.
    """
    valid = []
    invalid = []
    
    for e in events:
        ok, errs = EventValidator.validate_event(e)
        if ok:
            valid.append(e)
        else:
            # Capture structural error context along with the event
            invalid_record = e.copy()
            invalid_record["dq_errors"] = errs
            invalid.append(invalid_record)
            
    return valid, invalid

def filter_by_event_type(events: list, event_types: list) -> list:
    """Isolates specific e-commerce actions (e.g. only purchases)."""
    return [e for e in events if e.get('event_type') in event_types]

def remove_duplicates(events: list, key='event_id') -> list:
    """Filters duplicate event payloads based on a unique identifier key."""
    seen = set()
    deduped = []
    for e in events:
        val = e.get(key)
        if val not in seen:
            seen.add(val)
            deduped.append(e)
    return deduped

def filter_outlier_amounts(events: list, max_amount=10000.0) -> list:
    """Protects down-stream reports from extreme payment glitches (e.g. negative costs or $10k+ buys)."""
    clean = []
    for e in events:
        try:
            amt = float(e.get('amount', 0))
            if 0 <= amt <= max_amount:
                clean.append(e)
        except (ValueError, TypeError):
            pass
    return clean
