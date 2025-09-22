# Finure App Gateway

## 1. Overview
App Gateway is the API gateway for the Finure platform, acting as the main entry point for credit card application submissions. It exposes a FastAPI endpoint that receives application data from frontend clients, validates and serializes it, and streams it securely to Kafka for downstream processing. The gateway is designed to run as a Kubernetes Deployment and is managed via Helm charts for configuration and scaling.

## 2. Features
- **REST API Endpoint:** FastAPI-based `/api/apply` endpoint for credit card application intake
- **Kafka Integration:** Securely streams validated application data to Kafka using SSL
- **CORS Support:** Allows cross-origin requests from frontend clients
- **Kubernetes Native:** Runs as a Deployment in a k8s cluster, with Helm charts for deployment and configuration
- **Health Checks:** Includes a Kafka readiness probe script for liveness/readiness checks
- **Environment Configuration:** Supports environment-specific values for flexible deployments

## 3. Prerequisites
- Kubernetes cluster bootstrapped ([Finure Terraform](https://github.com/finure/terraform))
- Infrastructure setup via Flux ([Finure Kubernetes](https://github.com/finure/kubernetes))

If running locally for development/testing:
- Docker 
- Python 3.12+ 
- Kafka broker 

## 4. File Structure
```
app-gateway/
├── app/
│   └── requirements.txt       # Python dependencies
│   ├── kafka-check.py         # Kafka readiness/liveness probe script
│   ├── main.py                # FastAPI gateway source code
├── k8s/
│   ├── environments/
│   │   └── production/
│   │       └── values.yaml    # Production environment values
│   ├── helm-charts/
│   │   └── app-gateway/
│   │       ├── .helmignore
│   │       ├── Chart.yaml     # Helm chart metadata
│   │       ├── values.yaml    # Default Helm values
│   │       └── templates/
│   │           ├── _helpers.tpl      # Helm template helpers
│   │           ├── deployment.yaml   # Kubernetes Deployment manifest
│   │           ├── hpa.yaml          # Horizontal Pod Autoscaler
│   │           ├── service.yaml      # Service definition
│   │           └── serviceaccount.yaml # Service account for gateway
│   └── scripts/
│       └── istio.sh           # Istio graceful exit script
├── Dockerfile                 # Container build file
├── .dockerignore              # Docker ignore rules
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
```

## 5. How to Run Manually
1. Install Python dependencies:
	```bash
	cd app-gateway/app
	pip install -r requirements.txt
	```
2. Prepare required environment variables and secrets:
   - `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker address (e.g., `localhost:9092`)
   - `KAFKA_TOPIC`: Kafka topic to stream application data
3. Run the gateway service:
	```bash
	python main.py
	```
3. Start the FastAPI gateway:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```
   The API will be available at `http://localhost:8080/api/apply` and will stream received application data to Kafka

## 6. k8s Folder Significance

The `k8s` folder contains all Kubernetes-related resources:
- **Helm Charts:** Used to deploy the gateway as a Kubernetes Deployment in the cluster. Not intended for standalone or local use.
- **Environment Values:** Customize deployments for different environments (e.g., production)
- **Scripts:** Utility scripts for cluster setup (e.g., Istio service mesh, readiness/liveness probes)

> **Important:** The resources in `k8s` are designed to be consumed by the Kubernetes cluster during automated deployments. They are not meant for manual execution outside the cluster context.

## Additional Information

This repo is primarily designed to be used in the Finure project. While the gateway can be adapted for other use cases, it is recommended to use it as part of the Finure platform for full functionality and support.