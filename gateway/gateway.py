
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
POLICY = "ROUND_ROBIN"

# Initialize request count
req_count = 0

# define route to accept details about frontend services
@app.post("/register")
def register_frontend(container: ContainerDetails):
    global FRONTEND_DTLS

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
# def policy(policy: str = Query(None)):
#     return {'message': 'Policy set to ' + policy}

# define a route to accept incoming requests
@app.get("/")
def load_balancer():
    global FRONTEND_DTLS
    global req_count

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
