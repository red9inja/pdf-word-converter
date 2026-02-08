# Free PDF Tools + ATS Resume Builder

Complete online platform with 31 tools for PDF operations and professional resume building with ATS optimization.

## Features

### PDF Tools (27 Tools)

**Convert (8 tools)**
- PDF to Word - Convert PDF documents to editable Word files
- Word to PDF - Convert Word documents to PDF format
- PDF to Excel - Extract tables and data to Excel
- Excel to PDF - Convert spreadsheets to PDF
- PDF to PowerPoint - Convert PDF to editable presentations
- PowerPoint to PDF - Convert presentations to PDF
- PDF to JPG - Convert PDF pages to images
- JPG to PDF - Create PDF from images

**Organize (6 tools)**
- Merge PDF - Combine multiple PDFs into one
- Split PDF - Split PDF by pages, size, or extract individual pages
- Rotate PDF - Rotate pages 90°, 180°, or 270°
- Delete Pages - Remove specific pages from PDF
- Extract Pages - Extract specific pages to new PDF
- Organize PDF - Reorder pages in PDF

**Optimize (3 tools)**
- Compress PDF - Reduce file size (Low/Medium/High compression)
- Repair PDF - Fix corrupted PDF files
- Optimize PDF - Optimize for web and mobile

**Security (4 tools)**
- Protect PDF - Add password protection with custom permissions
- Unlock PDF - Remove password from PDF
- Sign PDF - Add digital signature
- Watermark PDF - Add text watermark (center, top, bottom, diagonal)

**Edit (6 tools)**
- Edit PDF - Modify PDF content
- Add Page Numbers - Add page numbers (bottom/top, left/center/right)
- OCR PDF - Extract text from scanned PDFs (English, Spanish, French, German, Hindi)
- PDF Reader - View PDF files online

### Resume Tools (4 Tools)

**Resume Builder (ATS Optimized)**
- Professional resume creation with ATS-friendly formatting
- Multiple sections: Personal Info, Summary, Experience, Education, Skills
- 4 templates: Modern, Professional, Minimal, Creative
- Keyword optimization for Applicant Tracking Systems
- Standard fonts and formatting
- No tables or complex layouts
- PDF output

**ATS Score Checker**
- Upload existing resume (PDF/DOC/DOCX)
- Get ATS compatibility score (0-100)
- Detailed feedback on missing sections
- Contact information validation
- Recommendations for improvement
- Section completeness analysis

**Resume Templates**
- 4 pre-designed ATS-friendly templates
- Modern - Clean and professional
- Professional - Traditional corporate style
- Minimal - Simple, content-focused
- Creative - Unique design while ATS-compatible

**Cover Letter Generator**
- Personalized cover letter creation
- Company and position-specific content
- Skills highlighting
- Professional formatting
- PDF output
- Date and greeting automation

## Architecture

```
User Browser
    
Cloudflare (DNS + DDoS Protection)
    
CloudFront (AWS CDN + SSL)
    
S3 Static Website (Frontend)
    
API Gateway (REST API)
    
Lambda Function (Processing)
    
S3 Bucket (Temporary File Storage)
```

## Technology Stack

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Responsive design
- No frameworks (lightweight)

**Backend:**
- AWS Lambda (Python 3.9)
- Serverless architecture
- Auto-scaling

**Infrastructure:**
- Terraform (Infrastructure as Code)
- GitHub Actions (CI/CD)
- AWS (Lambda, S3, API Gateway, CloudFront)
- Cloudflare (DNS, CDN, Security)

**Libraries:**
- pdf2docx - PDF to Word conversion
- PyPDF2 - PDF manipulation
- Pillow - Image processing
- ReportLab - PDF generation
- python-docx - Word document handling
- openpyxl - Excel operations
- python-pptx - PowerPoint operations

## Deployment

### Prerequisites

1. **AWS Account**
   - Create account at https://aws.amazon.com
   - Get Access Key ID and Secret Access Key

2. **Cloudflare Account**
   - Create account at https://cloudflare.com
   - Add your domain
   - Get API Token and Zone ID

3. **GitHub Account**
   - Fork or clone this repository

### Setup GitHub Secrets

Go to: **Repository  Settings  Secrets and variables  Actions**

Add these secrets:

```
AWS_ACCESS_KEY_ID           Your AWS access key
AWS_SECRET_ACCESS_KEY       Your AWS secret key
CLOUDFLARE_API_TOKEN        Your Cloudflare API token
```

**Get AWS Keys:**
```bash
# Create IAM user
aws iam create-user --user-name github-actions

# Attach admin policy
aws iam attach-user-policy \
  --user-name github-actions \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Create access key
aws iam create-access-key --user-name github-actions
```

**Get Cloudflare API Token:**
1. Cloudflare Dashboard  My Profile  API Tokens
2. Create Token  Edit zone DNS
3. Permissions:
   - Zone - DNS - Edit
   - Zone - Zone - Read
4. Zone Resources: Include  Specific zone  your-domain.com
5. Create Token  Copy token

**Get Cloudflare Zone ID:**
1. Cloudflare Dashboard
2. Select your domain
3. Overview  API section (right sidebar)
4. Copy Zone ID

### Create Branches

```bash
# Clone repository
git clone git@github.com:your-username/pdf-word-converter.git
cd pdf-word-converter

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

### Deploy

**Automatic Deployment:**

```bash
# Deploy to test environment
git checkout test
git merge main
git push origin test
#  Deploys to: https://pdf-test.your-domain.com

# Deploy to dev environment
git checkout dev
git merge main
git push origin dev
#  Deploys to: https://pdf-dev.your-domain.com

# Deploy to production
git checkout prod
git merge main
git push origin prod
#  Deploys to: https://pdf.your-domain.com
```

**What happens automatically:**
1. Terraform initializes
2. Fetches Cloudflare Zone ID
3. Creates AWS infrastructure (Lambda, S3, API Gateway, CloudFront)
4. Provisions SSL certificate
5. Configures DNS records
6. Updates frontend with API endpoint
7. Uploads website to S3
8. Invalidates CloudFront cache
9. Shows deployment summary

**Deployment time:** 5-10 minutes

### Manual Deployment (Optional)

```bash
cd terraform

# Copy example config
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
nano terraform.tfvars

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Deploy
terraform apply

# Get outputs
terraform output
```

## Google AdSense Integration

### Step 1: Apply for AdSense

1. Go to https://www.google.com/adsense
2. Sign in with Google account
3. Click "Get Started"
4. Enter your website URL: `https://pdf.your-domain.com`
5. Submit application

**Requirements:**
- Original content ( You have 31 tools)
- Privacy policy page (create one)
- About page (optional but recommended)
- At least 20-30 pages of content
- Domain must be live and accessible

### Step 2: Add AdSense Code

**After approval, you'll get:**
- Publisher ID: `ca-pub-XXXXXXXXXX`
- Ad unit codes

**Update `index.html`:**

Find these lines:
```html
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXX"
 crossorigin="anonymous"></script>
```

Replace `ca-pub-XXXXXXXXXX` with your actual Publisher ID.

**Ad Placements:**

**1. Top Banner (728x90 or responsive):**
```html
<div class="ad-banner">
    <ins class="adsbygoogle"
         style="display:inline-block;width:728px;height:90px"
         data-ad-client="ca-pub-XXXXXXXXXX"
         data-ad-slot="1234567890"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
</div>
```

**2. Sidebar (300x600 or 300x250):**
```html
<aside class="sidebar-ad">
    <ins class="adsbygoogle"
         style="display:inline-block;width:300px;height:600px"
         data-ad-client="ca-pub-XXXXXXXXXX"
         data-ad-slot="0987654321"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
</aside>
```

**3. In-content ads (optional):**
```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-format="fluid"
     data-ad-layout-key="-fb+5w+4e-db+86"
     data-ad-client="ca-pub-XXXXXXXXXX"
     data-ad-slot="1122334455"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

### Step 3: Create Required Pages

**Create `privacy.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Privacy Policy</title>
</head>
<body>
    <h1>Privacy Policy</h1>
    <p>Last updated: [Date]</p>
    
    <h2>Information We Collect</h2>
    <p>We do not collect personal information. Files uploaded are:</p>
    <ul>
        <li>Processed temporarily</li>
        <li>Automatically deleted after 1 hour</li>
        <li>Not stored permanently</li>
        <li>Not shared with third parties</li>
    </ul>
    
    <h2>Cookies</h2>
    <p>We use cookies for:</p>
    <ul>
        <li>Google AdSense (advertising)</li>
        <li>Analytics (optional)</li>
    </ul>
    
    <h2>Third-Party Services</h2>
    <p>We use:</p>
    <ul>
        <li>Google AdSense for advertising</li>
        <li>AWS for file processing</li>
        <li>Cloudflare for CDN</li>
    </ul>
    
    <h2>Contact</h2>
    <p>Email: contact@your-domain.com</p>
</body>
</html>
```

Upload to S3:
```bash
aws s3 cp privacy.html s3://pdf.your-domain.com/
```

### Step 4: Optimize Ad Placement

**Best practices:**
- Place ads above the fold (visible without scrolling)
- Don't place too many ads (3-4 per page max)
- Use responsive ad units for mobile
- Test different placements
- Monitor performance in AdSense dashboard

**Recommended layout:**
```
[Header]
[Top Banner Ad - 728x90]
[Tool Selector]
[Tool Interface]  [Sidebar Ad - 300x600]
[Features]
[Footer]
```

### Step 5: AdSense Approval Tips

**Content Requirements:**
-  31 unique tools (good!)
-  Original functionality
-  User-friendly interface
-  Mobile responsive
-  Fast loading

**Add more content:**
- Blog posts about PDF tips
- How-to guides for each tool
- Resume writing tips
- ATS optimization guide

**Create blog pages:**
```
/blog/how-to-compress-pdf.html
/blog/ats-resume-tips.html
/blog/pdf-to-word-guide.html
```

### Step 6: Monitor Revenue

**AdSense Dashboard:**
- Daily earnings
- Page RPM (Revenue per 1000 impressions)
- Click-through rate (CTR)
- Top performing pages

**Optimization:**
- Test ad positions
- Try different ad sizes
- A/B test layouts
- Monitor user experience

## Revenue Estimates

### Traffic-Based Projections

**10,000 visitors/month:**
- Page views: ~30,000 (3 pages per visitor)
- RPM: ₹100-300 (average)
- Revenue: ₹3,000-9,000/month

**50,000 visitors/month:**
- Page views: ~150,000
- RPM: ₹100-300
- Revenue: ₹15,000-45,000/month

**100,000 visitors/month:**
- Page views: ~300,000
- RPM: ₹100-300
- Revenue: ₹30,000-90,000/month

**Factors affecting revenue:**
- Geographic location of visitors (US/UK = higher RPM)
- Niche (Resume tools = higher CPC)
- Ad placement
- User engagement
- Click-through rate

### Cost Breakdown

**AWS Costs (per month):**
- Lambda: ₹200-400 (3GB memory, 15min timeout)
- S3: ₹50-100 (storage + requests)
- API Gateway: ₹100-200 (requests)
- CloudFront: ₹100-200 (data transfer)
- **Total: ₹450-900/month**

**Cloudflare:**
- Free plan: ₹0
- Pro plan (optional): $20/month (₹1,600)

**Domain:**
- ₹500-1,000/year

**Net Profit Examples:**

**10K visitors:**
- Revenue: ₹3,000-9,000
- Costs: ₹450-900
- Profit: ₹2,500-8,000

**50K visitors:**
- Revenue: ₹15,000-45,000
- Costs: ₹600-1,200
- Profit: ₹14,000-44,000

**100K visitors:**
- Revenue: ₹30,000-90,000
- Costs: ₹800-1,500
- Profit: ₹29,000-89,000

## SEO Optimization

### Keywords to Target

**PDF Tools:**
- free pdf converter
- pdf to word online
- merge pdf free
- compress pdf online
- pdf tools free

**Resume Tools:**
- free resume builder
- ats resume checker
- resume templates free
- ats optimized resume
- cover letter generator

### On-Page SEO

**Already implemented:**
-  Descriptive title tags
-  Meta descriptions
-  Semantic HTML
-  Mobile responsive
-  Fast loading

**Add:**
- Sitemap.xml
- Robots.txt
- Schema markup
- Open Graph tags

**Create sitemap.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://pdf.your-domain.com/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://pdf.your-domain.com/privacy.html</loc>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Content Marketing

**Create blog posts:**
1. "How to Create an ATS-Friendly Resume in 2026"
2. "10 Best Free PDF Tools for Students"
3. "Complete Guide to PDF Compression"
4. "Resume Keywords That Get You Hired"
5. "How to Pass ATS Screening"

**Social media:**
- Share on LinkedIn (resume tools)
- Reddit (r/resumes, r/jobs)
- Twitter/X
- Facebook groups

## Monitoring

### CloudWatch Logs

```bash
# View Lambda logs
aws logs tail /aws/lambda/pdf-converter --follow

# View API Gateway logs
aws logs tail /aws/apigateway/pdf-converter-api --follow
```

### Metrics

**Lambda:**
- Invocations
- Duration
- Errors
- Throttles

**API Gateway:**
- Request count
- Latency
- 4XX/5XX errors

**S3:**
- Storage used
- Requests
- Data transfer

### Alerts

Set up CloudWatch alarms for:
- Lambda errors > 10/hour
- API Gateway 5XX errors > 5%
- High costs

## Troubleshooting

### Common Issues

**1. Deployment Failed**
- Check GitHub Actions logs
- Verify AWS credentials
- Check Cloudflare API token
- Ensure domain exists in Cloudflare

**2. Lambda Timeout**
- Increase timeout in `terraform/lambda.tf`
- Increase memory (more memory = faster CPU)
- Optimize code

**3. CORS Errors**
- Check API Gateway CORS settings
- Verify Lambda response headers
- Check CloudFront configuration

**4. File Upload Failed**
- Check file size limits
- Verify S3 bucket permissions
- Check Lambda memory

**5. AdSense Not Showing**
- Wait 24-48 hours after adding code
- Check browser ad blockers
- Verify Publisher ID is correct
- Check AdSense account status

### Support

**AWS Issues:**
- CloudWatch Logs
- AWS Support (if on paid plan)

**Cloudflare Issues:**
- Cloudflare Dashboard  Analytics
- Community forums

**AdSense Issues:**
- AdSense Help Center
- AdSense Community Forum

## Scaling

### Traffic Growth

**Current setup handles:**
- 100K requests/month easily
- Auto-scales with Lambda
- CloudFront caching reduces load

**For higher traffic:**
- Enable CloudFront caching (already configured)
- Use Lambda reserved concurrency
- Implement rate limiting
- Add CloudWatch alarms

### Cost Optimization

**Reduce costs:**
- Enable S3 lifecycle policies (already configured)
- Use CloudFront caching aggressively
- Optimize Lambda memory/timeout
- Delete unused environments (test/dev)

## Security

**Implemented:**
-  HTTPS only (SSL certificate)
-  CORS configured
-  Files auto-deleted after 1 hour
-  No user data stored
-  IAM least privilege
-  Cloudflare DDoS protection
-  Rate limiting

**Best practices:**
- Rotate AWS keys regularly
- Monitor CloudWatch logs
- Keep dependencies updated
- Review IAM permissions

## Maintenance

### Regular Tasks

**Weekly:**
- Check error logs
- Monitor costs
- Review AdSense performance

**Monthly:**
- Update dependencies
- Review and optimize
- Backup Terraform state
- Check SSL certificate expiry

**Quarterly:**
- Security audit
- Performance optimization
- Content updates
- SEO review

## License

MIT License - Free to use and modify

## Support

For issues or questions:
- GitHub Issues: [repository-url]/issues
- Email: contact@your-domain.com

---

**Built with  for learning AWS, Terraform, and building profitable side projects**
