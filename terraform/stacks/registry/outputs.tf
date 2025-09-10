output "repository_arns" {
  description = "ARNs of all repositories"
  value       = { for k, m in module.ecr_instances : k => m.repository_arn }
}

output "repository_urls" {
  description = "URLs of all repositories"
  value       = { for k, m in module.ecr_instances : k => m.repository_url }
}
