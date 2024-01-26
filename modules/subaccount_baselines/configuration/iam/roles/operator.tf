# IAM Role
# ./Policies maybe?

# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": ""
#             },
#             "Action": [
#                 "sts:AssumeRole",
#                 "sts:SetSourceIdentity"
#             ]
#         }
#     ]
# }



# IAMFullAccess AWS managed 1
# ReadOnlyAccess  AWS managed - job function  1
# SecurityAudit AWS managed - job function  1
# ViewOnlyAccess  AWS managed - job function  1

resource "aws_iam_role" "operator" {
  name               = "operator"
  assume_role_policy = data.aws_iam_policy_document.human_assume_role_policy.json
}
