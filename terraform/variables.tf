variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "pdf-word-converter"
}

variable "domain_name" {
  description = "Domain name"
  type        = string
  default     = "vimd.online"
}

variable "subdomain" {
  description = "Subdomain"
  type        = string
  default     = "pdf"
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type        = string
  sensitive   = true
}

variable "cloudflare_zone_id" {
  description = "Cloudflare zone ID for domain"
  type        = string
}
