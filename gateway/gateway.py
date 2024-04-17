
# This script defines a Flask application that acts as a gateway to route incoming requests to two different services.

# default imports
# from flask import Flask, request, jsonify
# from flask import jsonify
from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests

# app = Flask(__name__)
app = FastAPI()

class ContainerDetails(BaseModel):
    name: str
    ip: str
    port: int
    status: str

# Define service endpoints
FRONTEND_DTLS = {}
POLICY = "LEAST_RESPONSE_TIME"
response_time = {}

# Initialize request count
req_count = 0

# define route to accept details about frontend services
@app.post("/register")
def register_frontend(container: ContainerDetails):
    global FRONTEND_DTLS, response_time

    for service_name in FRONTEND_DTLS:
        response_time[service_name] = 0

    # add the details of the frontend service to the dictionary
    if container.status == "active":
        FRONTEND_DTLS[container.name] = f"http://{container.ip}:{container.port}"
        return {'message': f'Registered frontend service "{container.name}"'}

    elif container.status == "inactive":
        if container.name in FRONTEND_DTLS:
            del FRONTEND_DTLS[container.name]
            return {'message': f'Removed frontend service "{container.name}"'}

    print(FRONTEND_DTLS)

# define a route to decide the balancing policy
# @app.post("/policy")
# def policy(policy: Query[str]):
#     return {'message': 'Policy set to ' + policy}

# define a route to accept incoming requests
@app.get("/")
def load_balancer():
    global FRONTEND_DTLS, req_count, response_time

    # Increment request count
    req_count += 1

    # if policy is round-robin
    if POLICY == "ROUND_ROBIN":
        service_name = list(FRONTEND_DTLS.keys())[(req_count - 1) % len(FRONTEND_DTLS)]
        service_endpoint = FRONTEND_DTLS[service_name]

        try:
            response = requests.get(service_endpoint)
            return {'message': f'Hello from the gateway! Request count: {req_count}. Request served at {service_name}', 'response': response.json()}
        except Exception as e:
            return {'error': f'Failed to connect to service "{service_name}": {str(e)}'}, 500

    # if policy is least response time
    elif POLICY == "LEAST_RESPONSE_TIME":
        min_service_name = None
        min_time = min(response_time.values())

        for service_name, service_endpoint in FRONTEND_DTLS.items():

            try:
                if response_time[service_name] == min_time:
                    min_service_name = service_name

                    response = requests.get(FRONTEND_DTLS[min_service_name])
                    response_time = response.elapsed.total_seconds()
                    response_time[service_name] = response_time

                return {'message': f'Response time: {response_time}. Request served at {min_service_name}', 'response': response.json()}

            except Exception as e:
                return {'error': f'Failed to connect to service "{service_name}": {str(e)}'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# TODO:
# - test the least respoonse time policy and figure out how to get number of active connections to a container
# - build the resoruce based policy
#   - add constraints on the containers and determine their current usage to choose the next best container
# - testing of above policies for the correctness
# - determine the metric to measure the performance and cost w.r.t. the different workloads
#   - check performance with and without the load balancer
# - auto-scaling the containers
# - generate the different behaviors of workload to test
