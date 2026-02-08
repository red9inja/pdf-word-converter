# Get Cloudflare zone
data "cloudflare_zone" "domain" {
  name = var.domain_name
}

# DNS validation records for ACM certificate
resource "cloudflare_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.website.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  zone_id = var.cloudflare_zone_id
  name    = each.value.name
  value   = each.value.record
  type    = each.value.type
  ttl     = 60
}

# Main CNAME record pointing to CloudFront
resource "cloudflare_record" "website" {
  zone_id = var.cloudflare_zone_id
  name    = var.subdomain
  value   = aws_cloudfront_distribution.website.domain_name
  type    = "CNAME"
  ttl     = 1
  proxied = true

  depends_on = [aws_cloudfront_distribution.website]
}

# Cloudflare page rules for caching
resource "cloudflare_page_rule" "cache_everything" {
  zone_id  = var.cloudflare_zone_id
  target   = "${var.subdomain}.${var.domain_name}/*"
  priority = 1

  actions {
    cache_level = "cache_everything"
    edge_cache_ttl = 7200
  }
}

# Cloudflare firewall rule (optional - rate limiting)
resource "cloudflare_rate_limit" "api_limit" {
  zone_id   = var.cloudflare_zone_id
  threshold = 100
  period    = 60
  match {
    request {
      url_pattern = "${var.subdomain}.${var.domain_name}/*"
    }
  }
  action {
    mode    = "challenge"
    timeout = 86400
  }
}
