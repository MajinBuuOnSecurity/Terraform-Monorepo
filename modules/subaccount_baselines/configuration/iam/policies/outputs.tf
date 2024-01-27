output "allowlists_policy_arn" {
  description = "Service and region allowlists"
  value       = aws_iam_policy.allowlists.arn
}
