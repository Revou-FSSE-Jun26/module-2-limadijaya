from locust import HttpUser, task, between, SequentialTaskSet


class UserJourney(SequentialTaskSet):
    """
    Simulates a sequential user journey:
    1. GET all products
    2. GET a single product by ID
    3. POST a new order
    4. GET the created order
    """

    product_id = None
    order_id = None
    user_id = 1  # Assuming a user with ID 1 exists

    @task
    def get_all_products(self):
        """Step 1: Browse all products."""
        with self.client.get('/products', catch_response=True) as response:
            if response.status_code == 200:
                products = response.json()
                if products and len(products) > 0:
                    self.product_id = products[0]['id']
                response.success()
            else:
                response.failure(f"Failed to get products: {response.status_code}")

    @task
    def get_single_product(self):
        """Step 2: View a single product by ID."""
        if self.product_id is None:
            self.product_id = 1

        with self.client.get(f'/products/{self.product_id}', catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to get product: {response.status_code}")

    @task
    def create_order(self):
        """Step 3: Place a new order."""
        if self.product_id is None:
            self.product_id = 1

        order_data = {
            "user_id": self.user_id,
            "items": [
                {
                    "product_id": self.product_id,
                    "quantity": 2
                }
            ]
        }

        with self.client.post('/orders', json=order_data, catch_response=True) as response:
            if response.status_code == 201:
                self.order_id = response.json().get('id')
                response.success()
            else:
                response.failure(f"Failed to create order: {response.status_code}")

    @task
    def get_created_order(self):
        """Step 4: View the order just created."""
        if self.order_id is None:
            return

        with self.client.get(f'/orders/{self.order_id}', catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to get order: {response.status_code}")

        # Restart the journey
        self.interrupt()


class RevoShopUser(HttpUser):
    """
    Simulated RevoShop user.
    Run with: locust -f locustfile.py --host=http://localhost:5001
    Start with 50 users, ramp up to 200.
    """
    tasks = [UserJourney]
    wait_time = between(1, 3)
