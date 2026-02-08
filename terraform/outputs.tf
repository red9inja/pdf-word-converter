output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = "${aws_apigatewayv2_api.converter_api.api_endpoint}/prod/convert"
}

output "website_url" {
  description = "Website URL"
  value       = "https://${var.subdomain}.${var.domain_name}"
}

output "cloudfront_url" {
  description = "CloudFront distribution URL"
  value       = aws_cloudfront_distribution.website.domain_name
}

output "s3_website_bucket" {
  description = "S3 website bucket name"
  value       = aws_s3_bucket.website.id
}

output "s3_files_bucket" {
  description = "S3 files bucket name"
  value       = aws_s3_bucket.converter_files.id
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.converter.function_name
}

output "cloudflare_record" {
  description = "Cloudflare DNS record"
  value       = cloudflare_record.website.hostname
}
