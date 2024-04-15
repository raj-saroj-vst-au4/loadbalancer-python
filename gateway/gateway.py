
# This script defines a Flask application that acts as a gateway to route incoming requests to two different services.

# default imports
# from flask import Flask, request, jsonify
from flask import jsonify
from fastapi import FastAPI
import requests
import os

# app = Flask(__name__)
app = FastAPI()

# Define service endpoints
SERVICE_ENDPOINTS = {
    "container_a": os.environ.get("CONTAINERA_ENDPOINT"),
    "container_b": os.environ.get("CONTAINERB_ENDPOINT")
}

# Initialize request count
req_count = 0

# Define a route to accept incoming requests
# @app.route('/', methods=['GET'])
@app.get("/")
def gateway():
    global req_count

    # Increment request count
    req_count += 1

    # Determine which container to route the request to based on request count
    service_name = "container_a" if req_count % 2 != 0 else "container_b"
    print(f"Routing request to {service_name}")

    # Get the endpoint for the selected container
    service_endpoint = SERVICE_ENDPOINTS.get(service_name)

    # Make a request to the specified service endpoint
    try:
        response = requests.get(service_endpoint)
        response.elapsed.total_seconds()
        return str(response.status_code)
    except Exception as e:
        return jsonify({'error': f'Failed to connect to service "{service_name}": {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
