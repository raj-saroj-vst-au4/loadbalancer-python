# cs695_a4

## Assignment 4: Implementing a load balancer

### Team Members
- Anshika Raman (anshikaraman)
- Aman Sharma
- Kalind Karia (kalindkaria)

### Instructions to run the code
1. Run the following command to start the gateway and replicas of the frontend service:
    ```
    python3 conductor.py
    ```
    - The `docker-compose ps` should show the following services running:
        ```
        cs695_a4_frontend_1
        cs695_a4_frontend_2
        cs695_a4_frontend_3
        cs695_a4_frontend_4
        cs695_a4_gateway
        ```

2. One can run the load generator using the following command (httperf or ab [apache benchmark] can be used):
    ```
    ab -n 1000 -c 10 http://localhost:8080/
    ```

3. The logs of the gateway and replicas can be seen using the following command:
    ```
    docker-compose logs -f
    ```
    - The logs will show the requests being distributed among the replicas.
