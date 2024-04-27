
# default imports
from locust import HttpUser, task, constant

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")

    wait_time = constant(0.5)
