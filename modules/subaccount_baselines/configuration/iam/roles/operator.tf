# TODO: Fill this out
# The intention is it is like admin but less powerful
# E.g. no IAM edit permissions
resource "aws_iam_role" "operator" {
  name               = "operator"
  assume_role_policy = data.aws_iam_policy_document.human_assume_role_policy.json
}
