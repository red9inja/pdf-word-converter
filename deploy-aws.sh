#!/bin/bash

# AWS Lambda Deployment Script
# Run this script to deploy your Lambda function

echo "🚀 Starting AWS Lambda Deployment..."

# Variables - UPDATE THESE
FUNCTION_NAME="pdf-to-word-converter"
REGION="us-east-1"
S3_BUCKET="pdf-converter-files-$(date +%s)"
ROLE_NAME="lambda-pdf-converter-role"

# Create S3 bucket for file storage
echo "📦 Creating S3 bucket..."
aws s3 mb s3://$S3_BUCKET --region $REGION

# Create IAM role for Lambda
echo "🔐 Creating IAM role..."
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document file://trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Wait for role to be ready
echo "⏳ Waiting for IAM role to propagate..."
sleep 10

# Package Lambda function
echo "📦 Packaging Lambda function..."
cd lambda
pip install -r requirements.txt -t .
zip -r ../lambda-package.zip .
cd ..

# Get role ARN
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)

# Create Lambda function
echo "🚀 Creating Lambda function..."
aws lambda create-function \
  --function-name $FUNCTION_NAME \
  --runtime python3.9 \
  --role $ROLE_ARN \
  --handler convert.lambda_handler \
  --zip-file fileb://lambda-package.zip \
  --timeout 300 \
  --memory-size 1024 \
  --environment Variables="{S3_BUCKET=$S3_BUCKET}" \
  --region $REGION

# Create API Gateway
echo "🌐 Creating API Gateway..."
API_ID=$(aws apigatewayv2 create-api \
  --name pdf-converter-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:$REGION:$(aws sts get-caller-identity --query Account --output text):function:$FUNCTION_NAME \
  --region $REGION \
  --query 'ApiId' \
  --output text)

# Add Lambda permission for API Gateway
aws lambda add-permission \
  --function-name $FUNCTION_NAME \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:$REGION:$(aws sts get-caller-identity --query Account --output text):$API_ID/*" \
  --region $REGION

# Get API endpoint
API_ENDPOINT="https://$API_ID.execute-api.$REGION.amazonaws.com/convert"

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📝 Update these values in your code:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "API Endpoint: $API_ENDPOINT"
echo "S3 Bucket: $S3_BUCKET"
echo ""
echo "📋 Next Steps:"
echo "1. Update script.js with API_ENDPOINT"
echo "2. Upload index.html, style.css, script.js to S3 or hosting"
echo "3. Add your AdSense code in index.html"
echo "4. Point pdf.vimd.online to your hosting"
echo ""
echo "💰 Estimated Monthly Cost:"
echo "- Lambda: Free tier (1M requests)"
echo "- S3: ~₹50-200 (depending on usage)"
echo "- API Gateway: Free tier (1M requests)"
echo ""
