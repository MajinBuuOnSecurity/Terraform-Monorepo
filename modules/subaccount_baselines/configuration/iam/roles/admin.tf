# Note:
#   I decided not to TF the following policies, 
#   and only require `terraform import` of the role, and not these 4 policies too.
#   (That are added in iam.py of create_aws_account)
#     IAMFullAccess
#     ReadOnlyAccess
#     SecurityAudit
#     ViewOnlyAccess
resource "aws_iam_role" "admin" {
  name               = "admin"
  assume_role_policy = data.aws_iam_policy_document.human_assume_role_policy.json
}
