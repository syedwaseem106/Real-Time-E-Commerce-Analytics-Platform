import re
from datetime import datetime
from src.event_generator.config import EVENT_TYPES

class EventValidator:
    """
    Implements single event validation rules to filter corrupt, malformed,
    or outlier clickstream events prior to warehouse ingestion.
    """
    REQUIRED_FIELDS = ['event_id', 'user_id', 'session_id', 'event_type', 'product_id', 'timestamp']

    @staticmethod
    def validate_schema(event: dict) -> tuple[bool, list[str]]:
        """Verifies that all required fields are present in the payload."""
        errors = []
        for field in EventValidator.REQUIRED_FIELDS:
            if field not in event:
                errors.append(f"Missing required field: {field}")
        return len(errors) == 0, errors

    @staticmethod
    def check_nulls(event: dict) -> tuple[bool, list[str]]:
        """Ensures critical operational values are not null/empty."""
        errors = []
        for field in EventValidator.REQUIRED_FIELDS:
            val = event.get(field)
            if val is None or str(val).strip() == "":
                errors.append(f"Null or blank value in field: {field}")
        return len(errors) == 0, errors

    @staticmethod
    def validate_types(event: dict) -> tuple[bool, list[str]]:
        """Asserts correct data types for e-commerce amounts and quantities."""
        errors = []
        amount = event.get('amount')
        quantity = event.get('quantity')
        
        if amount is not None:
            try:
                float(amount)
            except ValueError:
                errors.append(f"Amount {amount} is not a valid decimal")
                
        if quantity is not None:
            try:
                int(quantity)
            except ValueError:
                errors.append(f"Quantity {quantity} is not a valid integer")
                
        return len(errors) == 0, errors

    @staticmethod
    def validate_business_rules(event: dict) -> tuple[bool, list[str]]:
        """Validates logical business metrics such as negative costs or future dates."""
        errors = []
        
        # Validate event type
        event_type = event.get('event_type')
        if event_type not in EVENT_TYPES:
            errors.append(f"Invalid event_type: {event_type}")
            
        # Ensure transaction amounts are positive
        amount = event.get('amount', 0)
        if event_type in ['purchase', 'payment'] and (amount is None or float(amount) <= 0):
            errors.append(f"Transaction event type '{event_type}' has invalid amount: {amount}")
            
        # Ensure timestamp is not in the future
        timestamp_str = event.get('timestamp')
        if timestamp_str:
            try:
                # Handle formats with or without fractional seconds
                if '.' in timestamp_str:
                    evt_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    evt_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    
                if evt_time > datetime.utcnow() + timedelta(minutes=5): # 5 min tolerance
                    errors.append(f"Event timestamp {timestamp_str} is in the future")
            except Exception as e:
                errors.append(f"Timestamp parsing error: {str(e)}")
                
        return len(errors) == 0, errors

    @staticmethod
    def validate_event(event: dict) -> tuple[bool, list[str]]:
        """Aggregates all schema, null, type, and business rule validations."""
        all_errors = []
        
        # 1. Schema Check
        ok, errs = EventValidator.validate_schema(event)
        all_errors.extend(errs)
        if not ok: return False, all_errors # Stop if schema is completely broken
        
        # 2. Null Check
        _, errs = EventValidator.check_nulls(event)
        all_errors.extend(errs)
        
        # 3. Type Check
        _, errs = EventValidator.validate_types(event)
        all_errors.extend(errs)
        
        # 4. Business Rules Check
        _, errs = EventValidator.validate_business_rules(event)
        all_errors.extend(errs)
        
        return len(all_errors) == 0, all_errors

from datetime import timedelta

class BatchValidator:
    """
    Validates batch datasets (e.g. Pandas DataFrames or lists of events) 
    for duplicates and global DQ metrics.
    """
    @staticmethod
    def find_duplicates(events: list, key='event_id') -> list:
        """Finds any duplicated keys in the batch."""
        seen = set()
        duplicates = []
        for e in events:
            val = e.get(key)
            if val in seen:
                duplicates.append(val)
            else:
                seen.add(val)
        return duplicates

    @staticmethod
    def compute_quality_metrics(events: list) -> dict:
        """Computes critical operational quality metrics over the event stream."""
        total = len(events)
        if total == 0:
            return {"total_count": 0, "pass_rate": 100.0}
            
        valid_count = 0
        null_fields = 0
        schema_failures = 0
        rule_violations = 0
        
        for e in events:
            ok, errs = EventValidator.validate_event(e)
            if ok:
                valid_count += 1
            else:
                # Classify errors
                err_str = " ".join(errs).lower()
                if "missing" in err_str:
                    schema_failures += 1
                if "null" in err_str:
                    null_fields += 1
                if "invalid" in err_str or "future" in err_str:
                    rule_violations += 1
                    
        return {
            "total_count": total,
            "valid_count": valid_count,
            "invalid_count": total - valid_count,
            "pass_rate": round((valid_count / total) * 100.0, 2),
            "schema_failures": schema_failures,
            "null_fields": null_fields,
            "rule_violations": rule_violations
        }
