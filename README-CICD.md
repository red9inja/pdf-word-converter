# GitHub Actions CI/CD Pipeline

Automated deployment with Terraform for test, dev, and prod environments.

## Branch Strategy

```
main     → No deployment (code only)
test     → https://pdf-test.vimd.online
dev      → https://pdf-dev.vimd.online
prod     → https://pdf.vimd.online
```

## Setup

### 1. GitHub Secrets

Add these secrets in: **Settings → Secrets and variables → Actions → New repository secret**

**Required Secrets:**
```
AWS_ACCESS_KEY_ID          → Your AWS access key
AWS_SECRET_ACCESS_KEY      → Your AWS secret key
CLOUDFLARE_API_TOKEN       → Your Cloudflare API token
```

**How to get AWS keys:**
```bash
# Create IAM user with programmatic access
aws iam create-user --user-name github-actions
aws iam attach-user-policy --user-name github-actions --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam create-access-key --user-name github-actions
```

**How to get Cloudflare token:**
1. Cloudflare Dashboard → My Profile → API Tokens
2. Create Token → Edit zone DNS
3. Permissions: Zone - DNS - Edit, Zone - Zone - Read
4. Zone Resources: vimd.online
5. Copy token

### 2. Create Branches

```bash
# Create test branch
git checkout -b test
git push origin test

# Create dev branch
git checkout -b dev
git push origin dev

# Create prod branch
git checkout -b prod
git push origin prod

# Back to main
git checkout main
```

## Workflow

### Automatic Deployment

**Push to test/dev/prod branches triggers deployment:**

```bash
# Deploy to test
git checkout test
git merge main
git push origin test
# → Deploys to pdf-test.vimd.online

# Deploy to dev
git checkout dev
git merge main
git push origin dev
# → Deploys to pdf-dev.vimd.online

# Deploy to prod
git checkout prod
git merge main
git push origin prod
# → Deploys to pdf.vimd.online
```

### What Happens:

1. ✅ Checkout code
2. ✅ Setup Terraform
3. ✅ Configure AWS credentials
4. ✅ Fetch Cloudflare Zone ID automatically
5. ✅ Create/select Terraform workspace
6. ✅ Plan infrastructure changes
7. ✅ Apply changes
8. ✅ Update script.js with API endpoint
9. ✅ Upload website to S3
10. ✅ Invalidate CloudFront cache
11. ✅ Show deployment summary

### Manual Destroy

To destroy an environment:

1. Go to: **Actions → Destroy Infrastructure**
2. Click: **Run workflow**
3. Select environment: test/dev/prod
4. Type: `destroy`
5. Click: **Run workflow**

## Environment Differences

| Environment | Subdomain | Resources | Purpose |
|------------|-----------|-----------|---------|
| **test** | pdf-test.vimd.online | Separate | Testing |
| **dev** | pdf-dev.vimd.online | Separate | Development |
| **prod** | pdf.vimd.online | Separate | Production |

Each environment has:
- Own S3 buckets
- Own Lambda function
- Own API Gateway
- Own CloudFront distribution
- Own DNS record

## Monitoring Deployments

### View Workflow Runs
```
GitHub → Actions → Deploy Infrastructure
```

### Check Logs
Click on any workflow run to see detailed logs

### Deployment Summary
Each successful deployment shows:
- Environment name
- Website URL
- API endpoint
- S3 bucket name

## Cost Per Environment

**Per environment (test/dev/prod):**
- Lambda: ₹0 (free tier)
- S3: ₹50-100
- API Gateway: ₹0 (free tier)
- CloudFront: ₹100-200

**Total for 3 environments:** ₹450-900/month

**Recommendation:** Delete test/dev when not needed

## Terraform State

State is stored in:
- Workspace: test/dev/prod
- Backend: Local (in GitHub Actions runner)

**For production, use remote backend:**

Add to `terraform/providers.tf`:
```hcl
terraform {
  backend "s3" {
    bucket = "terraform-state-pdf-converter"
    key    = "state/terraform.tfstate"
    region = "us-east-1"
  }
}
```

## Troubleshooting

### Deployment Failed

**Check logs:**
1. GitHub → Actions → Failed workflow
2. Click on failed step
3. Read error message

**Common issues:**

**AWS credentials invalid:**
- Verify secrets are correct
- Check IAM user has permissions

**Cloudflare API error:**
- Verify token is valid
- Check token has DNS edit permissions

**Terraform state locked:**
- Wait for other deployment to finish
- Or manually unlock in AWS

**Zone ID not found:**
- Verify domain exists in Cloudflare
- Check domain name in workflow

### Manual Deployment

If GitHub Actions fails, deploy manually:

```bash
# Setup
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export TF_VAR_cloudflare_api_token="your-token"

# Get zone ID
ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=vimd.online" \
  -H "Authorization: Bearer $TF_VAR_cloudflare_api_token" \
  -H "Content-Type: application/json" | jq -r '.result[0].id')

# Deploy
cd terraform
terraform init
terraform workspace select test || terraform workspace new test
terraform apply \
  -var="cloudflare_zone_id=$ZONE_ID" \
  -var="subdomain=pdf-test"
```

## Security

### Secrets Protection
- ✅ Secrets never exposed in logs
- ✅ Terraform sensitive variables
- ✅ AWS credentials rotated regularly

### Branch Protection
Recommended settings for prod branch:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date

### IAM Permissions
Least privilege for GitHub Actions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "lambda:*",
        "apigateway:*",
        "cloudfront:*",
        "acm:*",
        "iam:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

## Best Practices

### Development Flow
```
1. Code changes in main branch
2. Test in test environment
3. Promote to dev
4. Final testing
5. Deploy to prod
```

### Rollback
```bash
# Revert to previous commit
git checkout prod
git revert HEAD
git push origin prod
# → Automatically redeploys previous version
```

### Monitoring
- CloudWatch logs for Lambda
- CloudFront metrics
- S3 access logs
- API Gateway logs

## Advanced

### Add Staging Environment
```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches:
      - test
      - dev
      - staging  # Add this
      - prod
```

### Slack Notifications
Add to workflow:
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Approval for Prod
Add to prod deployment:
```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://pdf.vimd.online
    # Requires manual approval in GitHub
```

## License
MIT
