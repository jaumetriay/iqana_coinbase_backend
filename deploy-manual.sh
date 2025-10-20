#!/bin/bash
set -e

# Configuration
ENVIRONMENT=${1:-dev}
REGION="us-east-1"
PROFILE="coinbase-dev"
BASE_STACK_NAME="coinbase-base-${ENVIRONMENT}"
SERVICE_STACK_NAME="coinbase-service-${ENVIRONMENT}"
GITHUB_REPO="https://github.com/jaumetriay/iqana_coinbase_backend"
GITHUB_BRANCH="main"

echo "🚀 Manual deployment for environment: ${ENVIRONMENT}"

echo "☁️  Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file deployment/cloudformation/template.yaml \
    --stack-name ${SERVICE_STACK_NAME} \
    --parameter-overrides \
        Environment=${ENVIRONMENT} \
        BaseStackName=${BASE_STACK_NAME} \
        GitHubRepo=${GITHUB_REPO} \
        GitHubBranch=${GITHUB_BRANCH} \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --region ${REGION} \
    --profile ${PROFILE}

echo "✅ Deployment complete!"

# Get the URLs
APP_RUNNER_URL=$(aws cloudformation describe-stacks \
    --stack-name ${SERVICE_STACK_NAME} \
    --query 'Stacks[0].Outputs[?OutputKey==`AppRunnerServiceUrl`].OutputValue' \
    --output text \
    --region ${REGION} \
    --profile ${PROFILE})

CLOUDFRONT_URL=$(aws cloudformation describe-stacks \
    --stack-name ${SERVICE_STACK_NAME} \
    --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontURL`].OutputValue' \
    --output text \
    --region ${REGION} \
    --profile ${PROFILE})

echo ""
echo "🌐 URLs:"
echo "App Runner (direct): ${APP_RUNNER_URL}"
echo "CloudFront (protected): ${CLOUDFRONT_URL}"
