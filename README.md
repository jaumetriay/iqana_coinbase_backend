# Coinbase Holdings API

A FastAPI service that retrieves Coinbase account holdings using the Coinbase Advanced Trade API with JWT authentication.

## Features

- 🔐 **Secure Authentication**: Uses Coinbase CDP SDK with JWT tokens
- 🛡️ **Rate Limiting**: Built-in protection against spam requests
- 🐳 **Docker Support**: Containerized deployment
- ☁️ **AWS Deployment**: Automated deployment with CloudFormation and GitHub Actions
- 🔒 **WAF Protection**: CloudFront + WAF for DDoS and attack protection


## Prerequisites

### Local Development
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose
- AWS CLI configured

### AWS Deployment
- AWS Account with appropriate permissions
- GitHub repository with secrets configured

## Local Development Setup

### Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

### Install project dependencies
uv sync

### Configure AWS CLI with your credentials
aws configure

### Source your environment

source deployment/envs/<env>/<env>.env

### Set your AWS profile (if using named profiles)
export AWS_PROFILE=your-profile-name

### Run the FastAPI server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

### API will be available at:
#### http://localhost:8000

### Navigate to docker directory
cd docker

### Start the service
docker-compose up --build

### API will be available at:
#### http://localhost:8000

## Run linting
uv run ruff check .
uv run black --check .
uv run mypy .

## Run pre-commit hooks
pre-commit run --all-files
