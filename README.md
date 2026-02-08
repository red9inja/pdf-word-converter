# PDF to Word Converter

Free online PDF to Word converter with complete AWS infrastructure and CI/CD.

## 🚀 Quick Start

### For Development (Main Branch)
```bash
git clone git@github.com:red9inja/pdf-word-converter.git
cd pdf-word-converter
```

**Main branch:** Code only, no deployment

### For Deployment

**Setup GitHub Secrets:**
1. Go to: Settings → Secrets → Actions
2. Add secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `CLOUDFLARE_API_TOKEN`

**Deploy to environments:**
```bash
# Test environment
git checkout test
git merge main
git push origin test
→ Deploys to: https://pdf-test.vimd.online

# Dev environment
git checkout dev
git merge main
git push origin dev
→ Deploys to: https://pdf-dev.vimd.online

# Production
git checkout prod
git merge main
git push origin prod
→ Deploys to: https://pdf.vimd.online
```

## 📁 Project Structure

```
pdf-word-converter/
├── index.html              # Frontend with AdSense
├── style.css               # Styling
├── script.js               # API integration
├── lambda/
│   ├── convert.py          # PDF to Word conversion
│   └── requirements.txt    # Python dependencies
├── terraform/
│   ├── providers.tf        # AWS + Cloudflare
│   ├── s3.tf              # Storage
│   ├── lambda.tf          # Serverless function
│   ├── api-gateway.tf     # REST API
│   ├── cloudfront.tf      # CDN + SSL
│   └── cloudflare.tf      # DNS automation
├── .github/workflows/
│   ├── deploy.yml         # Auto deployment
│   └── destroy.yml        # Cleanup
└── README*.md             # Documentation
```

## 🌟 Features

- ✅ **Serverless Architecture** - AWS Lambda
- ✅ **Infrastructure as Code** - Terraform
- ✅ **CI/CD Pipeline** - GitHub Actions
- ✅ **Auto DNS Setup** - Cloudflare API
- ✅ **Multi-Environment** - test/dev/prod
- ✅ **CDN** - CloudFront + Cloudflare
- ✅ **SSL/HTTPS** - Auto-provisioned
- ✅ **AdSense Ready** - Revenue optimized

## 🏗️ Architecture

```
User
  ↓
Cloudflare (DNS + DDoS)
  ↓
CloudFront (CDN + SSL)
  ↓
S3 Static Website
  ↓
API Gateway
  ↓
Lambda (PDF Converter)
  ↓
S3 (File Storage)
```

## 📚 Documentation

- **[README-TERRAFORM.md](README-TERRAFORM.md)** - Manual Terraform deployment
- **[README-CICD.md](README-CICD.md)** - GitHub Actions pipeline
- **[README-AWS.md](README-AWS.md)** - AWS CLI deployment

## 💰 Cost Estimate

**Per Environment:**
- Lambda: ₹0 (free tier: 1M requests)
- S3: ₹50-100/month
- API Gateway: ₹0 (free tier)
- CloudFront: ₹100-200/month
- **Total: ₹150-300/month**

**Revenue Potential:**
- 10K visitors: ₹5,000-15,000/month
- 100K visitors: ₹50,000-150,000/month

## 🔧 Local Development

```bash
# Install dependencies
cd lambda
pip install -r requirements.txt

# Test Lambda locally
python convert.py

# Preview website
python -m http.server 8000
# Visit: http://localhost:8000
```

## 🚀 Deployment Methods

### 1. GitHub Actions (Recommended)
- Push to test/dev/prod branches
- Automatic deployment
- Zero configuration

### 2. Terraform CLI
```bash
cd terraform
terraform init
terraform apply
```

### 3. AWS CLI
```bash
./deploy-aws.sh
```

## 🔐 Security

- AWS credentials in GitHub Secrets
- Cloudflare API token encrypted
- Zone ID auto-fetched
- IAM least privilege
- CORS configured
- Rate limiting enabled

## 📊 Monitoring

**CloudWatch Logs:**
```bash
aws logs tail /aws/lambda/pdf-word-converter --follow
```

**GitHub Actions:**
- Actions tab → View workflow runs
- Deployment summaries
- Error logs

## 🎯 Environments

| Branch | URL | Purpose |
|--------|-----|---------|
| main | - | Development (no deploy) |
| test | pdf-test.vimd.online | Testing |
| dev | pdf-dev.vimd.online | Development |
| prod | pdf.vimd.online | Production |

## 🔄 Workflow

```
1. Code in main branch
2. Merge to test → Auto deploy
3. Test features
4. Merge to dev → Auto deploy
5. Final testing
6. Merge to prod → Auto deploy
7. Live! 🎉
```

## 🛠️ Customization

**Change domain:**
```yaml
# .github/workflows/deploy.yml
env:
  DOMAIN_NAME: your-domain.com
  SUBDOMAIN: pdf
```

**Add environment:**
```yaml
on:
  push:
    branches:
      - staging  # Add new environment
```

**Increase Lambda memory:**
```hcl
# terraform/lambda.tf
memory_size = 2048
timeout     = 600
```

## 📝 AdSense Setup

1. Apply: https://www.google.com/adsense
2. Get Publisher ID
3. Update `index.html`:
   - Replace `ca-pub-XXXXXXXXXX`
   - Add ad slot IDs

## 🐛 Troubleshooting

**Deployment failed:**
- Check GitHub Actions logs
- Verify secrets are set
- Check AWS/Cloudflare credentials

**Website not loading:**
- Wait 5-10 minutes for DNS
- Check CloudFront distribution
- Verify S3 bucket policy

**Lambda timeout:**
- Increase timeout in terraform/lambda.tf
- Check CloudWatch logs

## 🤝 Contributing

1. Fork the repo
2. Create feature branch
3. Make changes
4. Test in test environment
5. Create pull request

## 📄 License

MIT

## 🔗 Links

- **GitHub:** https://github.com/red9inja/pdf-word-converter
- **Production:** https://pdf.vimd.online
- **Test:** https://pdf-test.vimd.online
- **Dev:** https://pdf-dev.vimd.online

## 💡 Tips

- Use test environment for experiments
- Keep main branch clean
- Delete unused environments to save cost
- Monitor CloudWatch for errors
- Enable CloudFront caching for better performance

---

**Made with ❤️ for learning AWS + Terraform + CI/CD**
