#!/usr/bin/env python3
# Current Date and Time (UTC): 2025-03-22 22:08:45
# Current User's Login: eduardoconde-bit

import os
import random
import string
import datetime
import calendar
import uuid
from decimal import Decimal
from faker import Faker

class PaymentDataGenerator:
    """
    Class responsible for generating payment-related data for the Spotify database.
    Generates data for subscriptions, member_subscription, payment_methods, and orders tables.
    
    Each user will be part of EXACTLY ONE subscription (either as owner or member).
    """
    
    def __init__(self, num_users=100, output_dir='spotify_db_data'):
        """
        Initialize the PaymentDataGenerator with configuration parameters.
        
        Args:
            num_users (int): Number of users in the database
            output_dir (str): Directory to save output files
        """
        self.fake = Faker()
        self.num_users = num_users
        self.output_dir = output_dir
        
        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Files for SQL inserts
        self.plans_file = os.path.join(self.output_dir, 'insert_plans.txt')
        self.subscriptions_file = os.path.join(self.output_dir, 'insert_subscriptions.txt')
        self.member_subscription_file = os.path.join(self.output_dir, 'insert_member_subscription.txt')
        self.payment_methods_file = os.path.join(self.output_dir, 'insert_payment_methods.txt')
        self.orders_file = os.path.join(self.output_dir, 'insert_orders.txt')
        
        # Data structures to track generated entities
        self.plans = []
        self.subscriptions = []
        self.payment_methods = []
        self.member_subscriptions = []
        self.orders = []
        
        # Track which users are assigned to subscriptions
        self.user_subscription = {}  # Maps user_id to subscription data
        
        # Default plans with max_member field
        self.plans_data = [
            {'plan_id': 1, 'plan': 'Individual', 'price': 9.99, 'description': 'Music streaming for one user', 'max_member': 1},
            {'plan_id': 2, 'plan': 'Duo', 'price': 12.99, 'description': 'Music streaming for two users', 'max_member': 2},
            {'plan_id': 3, 'plan': 'Family', 'price': 14.99, 'description': 'Music streaming for up to 6 family members', 'max_member': 6},
            {'plan_id': 4, 'plan': 'Student', 'price': 4.99, 'description': 'Discounted plan for verified students', 'max_member': 1},
            {'plan_id': 5, 'plan': 'Free', 'price': 0.00, 'description': 'Free plan with advertisements', 'max_member': 1}
        ]
        
        # Credit card brands
        self.card_brands = ['Visa', 'MasterCard', 'American Express', 'Discover', 'JCB']
    
    def add_months(self, sourcedate, months):
        """
        Add a specified number of months to a date safely, handling month transitions.
        
        Args:
            sourcedate (datetime.date): The original date
            months (int): Number of months to add
            
        Returns:
            datetime.date: New date with months added
        """
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        
        # Get the last day of the target month
        last_day = calendar.monthrange(year, month)[1]
        
        # Make sure the day is valid for the new month
        day = min(sourcedate.day, last_day)
        
        return datetime.date(year, month, day)
    
    def generate_plans(self):
        """Generate plan data and write to file"""
        with open(self.plans_file, 'w') as file:
            for plan in self.plans_data:
                insert_statement = (
                    f"INSERT INTO plans (plan_id, plan, price, description, max_member) VALUES ("
                    f"{plan['plan_id']}, '{plan['plan']}', {plan['price']}, '{plan['description']}', {plan['max_member']});\n"
                )
                file.write(insert_statement)
                self.plans.append(plan)
        
        print(f"Generated {len(self.plans)} plans")
    
    def assign_users_to_subscriptions(self):
        """
        Core method that assigns users to subscription groups.
        Each user will be part of exactly one subscription (as owner or member).
        """
        print("Assigning users to subscription groups...")
        
        # Start with all users unassigned
        unassigned_users = list(range(1, self.num_users + 1))
        random.shuffle(unassigned_users)  # Randomize user order
        
        # Plan distribution weights
        plan_weights = {
            1: 0.50,  # Individual (50%)
            2: 0.15,  # Duo (15%)
            3: 0.15,  # Family (15%)
            4: 0.10,  # Student (10%)
            5: 0.10   # Free (10%)
        }
        
        # Initialize subscription ID counter
        sub_id = 1
        
        # Continue while there are unassigned users
        while unassigned_users:
            # Select a plan type based on weights
            available_plans = [p['plan_id'] for p in self.plans_data]
            weights = [plan_weights[p] for p in available_plans]
            plan_id = random.choices(available_plans, weights=weights)[0]
            
            # Get the plan details
            plan = next(p for p in self.plans_data if p['plan_id'] == plan_id)
            max_members = plan['max_member']
            
            # Calculate how many users to include in this subscription
            # This is limited by how many unassigned users we have left
            num_users_for_subscription = min(max_members, len(unassigned_users))
            
            # If we don't have enough users for a Duo or Family plan, use Individual plan instead
            if num_users_for_subscription < max_members and max_members > 1:
                # Fall back to Individual plan
                plan_id = 1  # Individual plan
                plan = next(p for p in self.plans_data if p['plan_id'] == plan_id)
                max_members = plan['max_member']
                num_users_for_subscription = 1
            
            # Skip if we can't assign any users (shouldn't happen, but just in case)
            if num_users_for_subscription <= 0:
                continue
            
            # Take users from the unassigned list
            users_for_subscription = unassigned_users[:num_users_for_subscription]
            unassigned_users = unassigned_users[num_users_for_subscription:]
            
            # The first user is the owner
            owner_id = users_for_subscription[0]
            member_ids = users_for_subscription[1:] if len(users_for_subscription) > 1 else []
            
            # Subscription start date (between 1 day and 18 months ago)
            # Convertido para inteiro (547)
            days_ago = random.randint(1, 547)  # Corrigido: 365 * 1.5 = 547.5, arredondado para 547
            date_start = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).date()
            
            # Determine if subscription is still active
            is_active = random.random() < 0.85
            
            # Determine recurrency
            recorrency = random.random() < 0.95  # 95% of subscriptions are recurring
            
            # Determine finish date if inactive
            date_finish = None
            status = 'active'
            if not is_active:
                # Inactive subscription ended between 1 day and 6 months ago
                days_inactive = random.randint(1, 180)
                date_finish = (datetime.datetime.now() - datetime.timedelta(days=days_inactive)).date()
                status = 'disabled'
            
            # Create subscription
            subscription = {
                'sub_id': sub_id,
                'date_start': date_start,
                'date_finish': date_finish,
                'recorrency': recorrency,
                'status': status,
                'plan_id': plan_id,
                'owner_id': owner_id,
                'member_ids': member_ids
            }
            
            # Track the subscription for each user
            self.user_subscription[owner_id] = {
                'sub_id': sub_id,
                'role': 'owner'
            }
            
            for member_id in member_ids:
                self.user_subscription[member_id] = {
                    'sub_id': sub_id,
                    'role': 'member'
                }
            
            self.subscriptions.append(subscription)
            sub_id += 1
        
        # Report on subscription distribution
        print(f"Created {len(self.subscriptions)} subscriptions for {self.num_users} users")
        
        plan_counts = {}
        for plan in self.plans_data:
            plan_counts[plan['plan']] = 0
        
        for sub in self.subscriptions:
            plan = next(p for p in self.plans_data if p['plan_id'] == sub['plan_id'])
            plan_counts[plan['plan']] += 1
        
        print("Subscription plan distribution:")
        for plan_name, count in plan_counts.items():
            print(f"  - {plan_name}: {count} subscriptions")
    
    def generate_payment_methods(self):
        """Generate payment methods for users and write to file"""
        with open(self.payment_methods_file, 'w') as file:
            method_id = 1
            
            for user_id in range(1, self.num_users + 1):
                # Only create payment methods for subscription owners with paid plans
                if user_id in self.user_subscription and self.user_subscription[user_id]['role'] == 'owner':
                    sub_id = self.user_subscription[user_id]['sub_id']
                    subscription = next(s for s in self.subscriptions if s['sub_id'] == sub_id)
                    plan = next(p for p in self.plans_data if p['plan_id'] == subscription['plan_id'])
                    
                    # Skip free plans
                    if plan['price'] == 0.00:
                        continue
                    
                    # Generate payment method(s) for this user
                    # 90% of paid subscription owners have a payment method
                    if random.random() < 0.90:
                        # Number of payment methods per user (1-2)
                        num_methods = random.choices([1, 2], weights=[0.8, 0.2])[0]
                        
                        for _ in range(num_methods):
                            # Method type (credit_card or google_pay)
                            method_type = random.choices(['credit_card', 'google_pay'], weights=[0.75, 0.25])[0]
                            
                            # Card brand
                            card_brand = random.choice(self.card_brands)
                            
                            # Last 4 digits
                            card_last4 = ''.join(random.choices(string.digits, k=4))
                            
                            # Expiry date (1-5 years in future)
                            current_date = datetime.datetime.now()
                            years_ahead = random.randint(1, 5)
                            expiry_date = current_date.replace(
                                year=current_date.year + years_ahead,
                                month=random.randint(1, 12),
                                day=random.randint(1, 28)
                            ).date()
                            
                            # Token (simulated payment token)
                            token = f"tok_{uuid.uuid4().hex[:20]}"
                            
                            payment_method = {
                                'method_id': method_id,
                                'user_id': user_id,
                                'method_type': method_type,
                                'card_brand': card_brand,
                                'card_last4': card_last4,
                                'expiry_date': expiry_date,
                                'token': token
                            }
                            
                            insert_statement = (
                                f"INSERT INTO payment_methods (method_id, user_id, method_type, card_brand, "
                                f"card_last4, expiry_date, token) VALUES ("
                                f"{method_id}, {user_id}, '{method_type}', '{card_brand}', "
                                f"'{card_last4}', '{expiry_date}', '{token}');\n"
                            )
                            
                            file.write(insert_statement)
                            self.payment_methods.append(payment_method)
                            method_id += 1
        
        print(f"Generated {method_id - 1} payment methods")
    
    def generate_subscriptions_file(self):
        """Write subscription data to file"""
        with open(self.subscriptions_file, 'w') as file:
            for subscription in self.subscriptions:
                date_finish_sql = f"'{subscription['date_finish']}'" if subscription['date_finish'] else "NULL"
                
                insert_statement = (
                    f"INSERT INTO subscriptions (sub_id, date_start, date_finish, "
                    f"recorrency, status, plan_id) VALUES ("
                    f"{subscription['sub_id']}, '{subscription['date_start']}', {date_finish_sql}, "
                    f"{1 if subscription['recorrency'] else 0}, '{subscription['status']}', {subscription['plan_id']});\n"
                )
                
                file.write(insert_statement)
    
    def generate_member_subscriptions(self):
        """Generate member_subscription relationships and write to file"""
        with open(self.member_subscription_file, 'w') as file:
            relationship_count = 0
            
            for subscription in self.subscriptions:
                # Add the owner
                owner_id = subscription['owner_id']
                sub_id = subscription['sub_id']
                
                insert_statement = (
                    f"INSERT INTO member_subscription (user_id, sub_id, role) VALUES ("
                    f"{owner_id}, {sub_id}, 'owner');\n"
                )
                file.write(insert_statement)
                relationship_count += 1
                
                # Add the members
                for member_id in subscription['member_ids']:
                    insert_statement = (
                        f"INSERT INTO member_subscription (user_id, sub_id, role) VALUES ("
                        f"{member_id}, {sub_id}, 'member');\n"
                    )
                    file.write(insert_statement)
                    relationship_count += 1
        
        print(f"Generated {relationship_count} member_subscription relationships")
    
    def generate_orders(self):
        """Generate order data and write to file"""
        with open(self.orders_file, 'w') as file:
            order_id = 1
            
            for subscription in self.subscriptions:
                # Skip free plans for orders
                plan = next((p for p in self.plans_data if p['plan_id'] == subscription['plan_id']), None)
                if plan['price'] == 0.00:
                    continue
                
                owner_id = subscription['owner_id']
                
                # Find payment methods for this user
                user_payment_methods = [pm for pm in self.payment_methods if pm['user_id'] == owner_id]
                
                # Skip if user has no payment method
                if not user_payment_methods:
                    continue
                
                # Select a payment method
                payment_method = random.choice(user_payment_methods)
                
                # Calculate number of months since subscription started
                start_date = subscription['date_start']
                end_date = subscription['date_finish'] or datetime.datetime.now().date()
                
                # For each month of subscription, create an order
                current_date = start_date
                
                # Limit the number of orders per subscription
                max_orders_per_subscription = 6
                order_count = 0
                
                # Generate orders until we reach end date or max limit
                while current_date <= end_date and order_count < max_orders_per_subscription:
                    # Order amount (plan price)
                    amount = plan['price']
                    
                    # Order status (mostly completed, some pending/failed)
                    status_weights = [0.03, 0.95, 0.015, 0.005]  # pending, completed, failed, refunded
                    status = random.choices(['pending', 'completed', 'failed', 'refunded'], weights=status_weights)[0]
                    
                    # Transaction ID
                    transaction_id = f"txn_{uuid.uuid4().hex[:24]}"
                    
                    # Create timestamp (a random time on the current_date)
                    hour = random.randint(0, 23)
                    minute = random.randint(0, 59)
                    second = random.randint(0, 59)
                    timestamp = datetime.datetime.combine(
                        current_date, 
                        datetime.time(hour, minute, second)
                    )
                    
                    # Order data
                    order = {
                        'order_id': order_id,
                        'user_id': owner_id,
                        'plan_id': subscription['plan_id'],
                        'method_id': payment_method['method_id'],
                        'amount': amount,
                        'status': status,
                        'transaction_id': transaction_id,
                        'created_at': timestamp
                    }
                    
                    insert_statement = (
                        f"INSERT INTO orders (order_id, user_id, plan_id, method_id, "
                        f"amount, status, transaction_id, created_at) VALUES ("
                        f"{order_id}, {owner_id}, {subscription['plan_id']}, "
                        f"{payment_method['method_id']}, {amount}, '{status}', '{transaction_id}', "
                        f"'{timestamp}');\n"
                    )
                    
                    file.write(insert_statement)
                    self.orders.append(order)
                    order_id += 1
                    order_count += 1
                    
                    # Move to next month using the safe method
                    current_date = self.add_months(current_date, 1)
        
        print(f"Generated {order_id - 1} orders")
    
    def run(self):
        """Execute the payment data generation process"""
        print(f"\n{'-'*50}")
        print("PAYMENT DATA GENERATION")
        print(f"{'-'*50}")
        
        # Generate data in the correct sequence
        self.generate_plans()
        
        # First, assign users to subscription groups (this is the core logic change)
        self.assign_users_to_subscriptions()
        
        # Then generate files in the correct order
        self.generate_subscriptions_file()
        self.generate_member_subscriptions()
        self.generate_payment_methods()
        self.generate_orders()
        
        print(f"{'-'*50}")
        print("PAYMENT DATA GENERATION COMPLETE")
        print(f"Files generated in: {self.output_dir}")
        print(f"{'-'*50}\n")


if __name__ == "__main__":
    # Create an instance of PaymentDataGenerator and run it
    generator = PaymentDataGenerator(num_users=100)
    generator.run()