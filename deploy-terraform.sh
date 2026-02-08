#!/bin/bash

echo "🚀 PDF to Word Converter - Terraform Deployment"
echo "================================================"
echo ""

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Installing..."
    wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
    unzip terraform_1.6.0_linux_amd64.zip
    sudo mv terraform /usr/local/bin/
    rm terraform_1.6.0_linux_amd64.zip
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI not configured. Run: aws configure"
    exit 1
fi

cd terraform

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "⚠️  terraform.tfvars not found!"
    echo ""
    echo "📝 Create terraform.tfvars with:"
    echo "   cp terraform.tfvars.example terraform.tfvars"
    echo ""
    echo "Then update with your values:"
    echo "   - cloudflare_api_token (from Cloudflare dashboard)"
    echo "   - cloudflare_zone_id (from Cloudflare dashboard)"
    echo ""
    exit 1
fi

echo "1️⃣  Initializing Terraform..."
terraform init

echo ""
echo "2️⃣  Validating configuration..."
terraform validate

echo ""
echo "3️⃣  Planning deployment..."
terraform plan -out=tfplan

echo ""
read -p "🤔 Deploy infrastructure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

echo ""
echo "4️⃣  Deploying infrastructure..."
terraform apply tfplan

echo ""
echo "5️⃣  Getting outputs..."
API_ENDPOINT=$(terraform output -raw api_endpoint)
WEBSITE_URL=$(terraform output -raw website_url)
S3_BUCKET=$(terraform output -raw s3_website_bucket)

echo ""
echo "✅ Deployment Complete!"
echo "======================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Update script.js with API endpoint:"
echo "   const API_ENDPOINT = '$API_ENDPOINT';"
echo ""
echo "2. Upload website files to S3:"
echo "   cd .."
echo "   aws s3 sync . s3://$S3_BUCKET --exclude 'terraform/*' --exclude 'lambda/*' --exclude '.git/*'"
echo ""
echo "3. Add your AdSense code in index.html"
echo ""
echo "4. Visit your website:"
echo "   $WEBSITE_URL"
echo ""
echo "💰 Estimated Cost: ₹200-500/month"
echo "📊 Monitor: AWS CloudWatch Console"
echo ""
