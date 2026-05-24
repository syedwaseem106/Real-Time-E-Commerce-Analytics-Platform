import random
import uuid
import time
from datetime import datetime, timedelta
from faker import Faker
from src.event_generator.config import EVENT_TYPES, EVENT_WEIGHTS, PRODUCTS, CATEGORIES, NUM_USERS, EVENTS_PER_SECOND

class EcommerceEventGenerator:
    """
    Simulates real-world, realistic e-commerce clickstream user sessions and interactions.
    Maintains session state (users remain in active sessions for ~25 mins) and outputs JSON payloads.
    """
    def __init__(self, num_users=NUM_USERS):
        self.faker = Faker()
        self.num_users = num_users
        self.users = self._init_users()
        self.products = PRODUCTS
        self.active_sessions = {}  # user_id -> {"session_id": uuid, "expires_at": datetime, "last_event_type": str}

    def _init_users(self):
        """Pre-generates a pool of simulated user profiles to ensure user continuity in analytics."""
        user_pool = []
        devices = ['mobile', 'desktop', 'tablet']
        browsers = ['Chrome', 'Safari', 'Firefox', 'Edge']
        
        # Pre-seed users with unique devices/browsers/locations to build high-quality dim tables
        for _ in range(self.num_users):
            user_pool.append({
                "user_id": f"usr_{uuid.uuid4().hex[:10]}",
                "username": self.faker.user_name(),
                "email": self.faker.email(),
                "city": self.faker.city(),
                "country": self.faker.country(),
                "device": random.choice(devices),
                "browser": random.choice(browsers),
                "segment": random.choice(['regular', 'frequent_buyer', 'VIP', 'bargain_hunter'])
            })
        return user_pool

    def get_or_create_session(self, user):
        """Maintains stateful user sessions over a rolling 25-minute window."""
        user_id = user["user_id"]
        now = datetime.utcnow()
        
        # Check if session exists and is active
        if user_id in self.active_sessions:
            session_info = self.active_sessions[user_id]
            if now < session_info["expires_at"]:
                # Extend session
                session_info["expires_at"] = now + timedelta(minutes=25)
                return session_info["session_id"], session_info["last_event_type"]
                
        # Initialize new session
        new_session_id = f"sess_{uuid.uuid4().hex[:12]}"
        self.active_sessions[user_id] = {
            "session_id": new_session_id,
            "expires_at": now + timedelta(minutes=25),
            "last_event_type": "page_view"
        }
        return new_session_id, "page_view"

    def determine_next_event_type(self, last_event_type):
        """
        Calculates user progression along the shopping funnel.
        Users shouldn't leap from page_view directly to purchase without checkout.
        """
        # Funnel transitions:
        # page_view -> product_view -> add_to_cart -> checkout -> purchase -> payment
        if last_event_type == 'page_view':
            return random.choice(['page_view', 'product_view'])
        elif last_event_type == 'product_view':
            return random.choices(['product_view', 'add_to_cart', 'page_view'], weights=[30, 50, 20])[0]
        elif last_event_type == 'add_to_cart':
            return random.choices(['add_to_cart', 'remove_from_cart', 'checkout', 'page_view'], weights=[20, 10, 50, 20])[0]
        elif last_event_type == 'remove_from_cart':
            return 'product_view'
        elif last_event_type == 'checkout':
            return random.choices(['checkout', 'purchase', 'page_view'], weights=[20, 70, 10])[0]
        elif last_event_type == 'purchase':
            return 'payment'
        elif last_event_type == 'payment':
            return 'page_view' # Session loops back
        return 'page_view'

    def generate_event(self):
        """Generates a highly contextual single e-commerce event."""
        # Pick a random user
        user = random.choice(self.users)
        user_id = user["user_id"]
        
        # Get active session state
        session_id, last_event_type = self.get_or_create_session(user)
        event_type = self.determine_next_event_type(last_event_type)
        
        # Keep track of state
        self.active_sessions[user_id]["last_event_type"] = event_type
        
        # Choose product based on category random weights
        product_id = random.choice(list(self.products.keys()))
        product = self.products[product_id]
        
        # Construct realistic numeric variations for amount & qty
        amount = 0.0
        quantity = None
        
        # Event type pricing and details
        if event_type in ['add_to_cart', 'checkout', 'purchase', 'payment']:
            # Base price with slight variation (±10% to look realistic)
            variation = random.uniform(-0.1, 0.1)
            amount = round(product["base_price"] * (1 + variation), 2)
            quantity = random.randint(1, 3)
        elif event_type == 'product_view':
            # Viewing might display the catalog price, no transaction
            amount = product["base_price"]
            
        now = datetime.utcnow()
        
        event = {
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "username": user["username"],
            "email": user["email"],
            "session_id": session_id,
            "event_type": event_type,
            "product_id": product_id,
            "product_name": product["name"],
            "category": product["category"],
            "amount": amount,
            "quantity": quantity,
            "device": user["device"],
            "browser": user["browser"],
            "city": user["city"],
            "country": user["country"],
            "timestamp": now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            "event_date": now.strftime('%Y-%m-%d')
        }
        
        return event

    def generate_batch(self, count=100):
        """Returns a batch of events"""
        return [self.generate_event() for _ in range(count)]

    def stream_events(self, events_per_second=EVENTS_PER_SECOND):
        """Generator that continuously yields simulated clickstream events"""
        delay = 1.0 / events_per_second
        while True:
            yield self.generate_event()
            time.sleep(delay)
