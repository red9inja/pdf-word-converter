# AWS Lambda PDF to Word Converter

Complete AWS-based PDF to Word converter with your own infrastructure.

## Architecture

```
User Browser
    ↓
S3 Static Website (index.html, css, js)
    ↓
API Gateway
    ↓
Lambda Function (Python)
    ↓
S3 Bucket (Converted files)
```

## Features
- ✅ Complete AWS infrastructure
- ✅ Serverless (pay per use)
- ✅ Google AdSense integrated
- ✅ Your own code, your control
- ✅ Scalable automatically

## Cost Estimate

**Free Tier (First 12 months):**
- Lambda: 1M requests/month FREE
- S3: 5GB storage FREE
- API Gateway: 1M requests FREE

**After Free Tier:**
- Lambda: ₹0.0000002 per request
- S3: ₹1.5 per GB/month
- API Gateway: ₹0.003 per request
- **Total: ₹200-500/month** (for moderate traffic)

## Deployment Steps

### Prerequisites
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1), Output (json)
```

### Deploy to AWS
```bash
# Run deployment script
./deploy-aws.sh
```

This will:
1. Create S3 bucket for file storage
2. Create IAM role for Lambda
3. Package and deploy Lambda function
4. Create API Gateway
5. Configure permissions
6. Return API endpoint URL

### Update Frontend
After deployment, update `script.js`:
```javascript
const API_ENDPOINT = 'YOUR-API-ENDPOINT-FROM-DEPLOY-SCRIPT';
```

### Host Frontend

**Option 1: S3 Static Website (Recommended)**
```bash
# Create bucket for website
aws s3 mb s3://pdf.vimd.online

# Enable static website hosting
aws s3 website s3://pdf.vimd.online --index-document index.html

# Upload files
aws s3 sync . s3://pdf.vimd.online --exclude "lambda/*" --exclude "*.sh"

# Make public
aws s3api put-bucket-policy --bucket pdf.vimd.online --policy file://bucket-policy.json
```

**Option 2: CloudFront + S3 (Better performance)**
- Create CloudFront distribution
- Point to S3 bucket
- Add custom domain: pdf.vimd.online
- Free SSL certificate

### Domain Setup (pdf.vimd.online)

**Route 53:**
```bash
# Create hosted zone
aws route53 create-hosted-zone --name vimd.online --caller-reference $(date +%s)

# Add A record pointing to CloudFront/S3
```

**Or use your existing DNS:**
- CNAME: pdf → your-cloudfront-url.cloudfront.net
- Or A record → S3 website endpoint

## Google AdSense Setup

1. Apply for AdSense: https://www.google.com/adsense
2. Get your Publisher ID (ca-pub-XXXXXXXXXX)
3. Update `index.html`:
   - Replace `ca-pub-XXXXXXXXXX` with your ID
   - Replace ad slot IDs after approval

## File Structure

```
pdf-word-converter/
├── index.html              # Frontend with AdSense
├── style.css               # Styling
├── script.js               # API calls to Lambda
├── lambda/
│   ├── convert.py          # Lambda function
│   └── requirements.txt    # Python dependencies
├── deploy-aws.sh           # Deployment script
└── README-AWS.md           # This file
```

## Testing

```bash
# Test Lambda function
aws lambda invoke \
  --function-name pdf-to-word-converter \
  --payload '{"body": "{\"file\": \"base64-encoded-pdf\"}"}' \
  response.json

# Test API Gateway
curl -X POST https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/convert \
  -H "Content-Type: application/json" \
  -d '{"file": "base64-pdf-content"}'
```

## Monitoring

```bash
# View Lambda logs
aws logs tail /aws/lambda/pdf-to-word-converter --follow

# Check S3 usage
aws s3 ls s3://your-bucket-name --recursive --summarize

# API Gateway metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiId,Value=YOUR-API-ID
```

## Scaling

Lambda automatically scales:
- 0 to 1000 concurrent executions
- No configuration needed
- Pay only for what you use

## Security

- Files auto-delete after 1 hour (presigned URL expires)
- CORS enabled for your domain only
- IAM roles with minimal permissions
- S3 bucket not public (presigned URLs only)

## Troubleshooting

**Lambda timeout:**
- Increase timeout: `aws lambda update-function-configuration --function-name pdf-to-word-converter --timeout 300`

**Memory issues:**
- Increase memory: `aws lambda update-function-configuration --function-name pdf-to-word-converter --memory-size 2048`

**CORS errors:**
- Check API Gateway CORS settings
- Ensure Lambda returns proper headers

## Revenue Optimization

1. **SEO:**
   - Add blog posts about PDF conversion
   - Create landing pages for different use cases
   - Use keywords in content

2. **AdSense Placement:**
   - Top banner: 728x90
   - Sidebar: 300x600
   - In-article ads for blog posts

3. **Traffic Sources:**
   - Google search (organic)
   - Social media
   - Reddit, Quora answers
   - YouTube tutorials

## Estimated Revenue

**With 10,000 visitors/month:**
- AdSense: ₹5,000-15,000
- AWS Cost: ₹200-500
- **Net Profit: ₹4,500-14,500**

**With 100,000 visitors/month:**
- AdSense: ₹50,000-150,000
- AWS Cost: ₹2,000-5,000
- **Net Profit: ₹45,000-145,000**

## Support

For issues:
1. Check CloudWatch logs
2. Test Lambda function directly
3. Verify S3 permissions
4. Check API Gateway configuration

## License
MIT
