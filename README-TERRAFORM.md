# Terraform Deployment Guide

Complete infrastructure as code deployment with Terraform + Cloudflare.

## Architecture

```
User → Cloudflare (DNS + CDN)
       ↓
    CloudFront (AWS CDN)
       ↓
    S3 Static Website
       ↓
    API Gateway
       ↓
    Lambda Function
       ↓
    S3 (File Storage)
```

## Prerequisites

### 1. Install Terraform
```bash
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
terraform --version
```

### 2. AWS CLI Setup
```bash
aws configure
# Enter: Access Key, Secret Key, us-east-1, json
```

### 3. Cloudflare API Token

**Get API Token:**
1. Login to Cloudflare: https://dash.cloudflare.com
2. My Profile → API Tokens → Create Token
3. Use template: "Edit zone DNS"
4. Permissions:
   - Zone - DNS - Edit
   - Zone - Zone - Read
5. Zone Resources: Include - Specific zone - vimd.online
6. Create Token → Copy token

**Get Zone ID:**
1. Cloudflare Dashboard
2. Select domain: vimd.online
3. Overview → API section (right side)
4. Copy Zone ID

## Deployment Steps

### 1. Configure Variables
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

Update with your values:
```hcl
cloudflare_api_token = "your-token-here"
cloudflare_zone_id   = "your-zone-id-here"
```

### 2. Deploy Infrastructure
```bash
cd /root/pdf-word-converter
./deploy-terraform.sh
```

This will:
- ✅ Create S3 buckets (website + files)
- ✅ Deploy Lambda function
- ✅ Setup API Gateway
- ✅ Create CloudFront distribution
- ✅ Configure SSL certificate
- ✅ Setup Cloudflare DNS
- ✅ Enable CDN and caching

### 3. Update Frontend
After deployment, update `script.js`:
```javascript
const API_ENDPOINT = 'OUTPUT_FROM_TERRAFORM';
```

### 4. Upload Website
```bash
aws s3 sync . s3://pdf.vimd.online \
  --exclude 'terraform/*' \
  --exclude 'lambda/*' \
  --exclude '.git/*' \
  --exclude '*.sh'
```

### 5. Add AdSense
Update `index.html` with your AdSense code:
- Replace `ca-pub-XXXXXXXXXX` with your Publisher ID
- Replace ad slot IDs after approval

## Manual Terraform Commands

```bash
cd terraform

# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply

# Destroy (cleanup)
terraform destroy

# Show outputs
terraform output

# Show specific output
terraform output api_endpoint
```

## Infrastructure Components

### AWS Resources Created:
- **S3 Buckets:** 2 (website + files)
- **Lambda Function:** PDF converter
- **API Gateway:** HTTP API
- **CloudFront:** CDN distribution
- **ACM Certificate:** SSL/TLS
- **IAM Roles:** Lambda execution
- **CloudWatch:** Logs

### Cloudflare Resources:
- **DNS Record:** CNAME for subdomain
- **SSL Certificate Validation:** DNS records
- **Page Rules:** Caching optimization
- **Rate Limiting:** DDoS protection

## Cost Breakdown

### AWS (Monthly):
- Lambda: ₹0 (free tier: 1M requests)
- S3: ₹50-100 (storage + requests)
- API Gateway: ₹0 (free tier: 1M requests)
- CloudFront: ₹100-200 (data transfer)
- **Total: ₹150-300/month**

### Cloudflare:
- Free plan: ₹0
- Pro plan (optional): $20/month (₹1600)

## Features

✅ **Infrastructure as Code**
- Version controlled
- Reproducible
- Easy to modify

✅ **Auto SSL**
- Free SSL certificate
- Auto-renewal
- HTTPS enforced

✅ **CDN**
- CloudFront (AWS)
- Cloudflare (DNS level)
- Global edge locations

✅ **Security**
- Rate limiting
- DDoS protection
- CORS configured
- IAM least privilege

✅ **Monitoring**
- CloudWatch logs
- API Gateway metrics
- Lambda insights

## Customization

### Change Region
Edit `terraform/variables.tf`:
```hcl
variable "aws_region" {
  default = "ap-south-1"  # Mumbai
}
```

### Increase Lambda Memory
Edit `terraform/lambda.tf`:
```hcl
memory_size = 2048  # 2GB
timeout     = 600   # 10 minutes
```

### Add More Domains
Edit `terraform/cloudflare.tf`:
```hcl
resource "cloudflare_record" "website2" {
  zone_id = var.cloudflare_zone_id
  name    = "convert"
  value   = aws_cloudfront_distribution.website.domain_name
  type    = "CNAME"
}
```

## Troubleshooting

### Certificate Validation Stuck
```bash
# Check DNS records
dig _acm-challenge.pdf.vimd.online

# Force validation
terraform taint aws_acm_certificate_validation.website
terraform apply
```

### Lambda Timeout
```bash
# Increase timeout
terraform apply -var="lambda_timeout=600"
```

### S3 Upload Failed
```bash
# Check bucket policy
aws s3api get-bucket-policy --bucket pdf.vimd.online

# Sync with public-read
aws s3 sync . s3://pdf.vimd.online --acl public-read
```

### Cloudflare DNS Not Working
```bash
# Verify zone ID
terraform output cloudflare_record

# Check Cloudflare dashboard
# Ensure proxy is enabled (orange cloud)
```

## Monitoring

### View Lambda Logs
```bash
aws logs tail /aws/lambda/pdf-word-converter --follow
```

### API Gateway Metrics
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiId,Value=YOUR_API_ID \
  --start-time 2026-02-08T00:00:00Z \
  --end-time 2026-02-08T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

### S3 Usage
```bash
aws s3 ls s3://pdf.vimd.online --recursive --summarize
```

## Cleanup

To destroy all resources:
```bash
cd terraform
terraform destroy
```

This will remove:
- All AWS resources
- Cloudflare DNS records
- SSL certificates

**Note:** S3 buckets with files may need manual deletion.

## Updates

### Update Lambda Code
```bash
# Modify lambda/convert.py
cd terraform
terraform apply
```

### Update Website
```bash
# Modify HTML/CSS/JS
aws s3 sync . s3://pdf.vimd.online
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

## Support

**Terraform Issues:**
- Check: `terraform validate`
- Debug: `TF_LOG=DEBUG terraform apply`

**AWS Issues:**
- CloudWatch Logs
- AWS Support Center

**Cloudflare Issues:**
- Cloudflare Dashboard → Analytics
- Support tickets (Pro plan)

## License
MIT
