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


# data "aws_iam_policy_document" "human_assume_role_policy" {
#   statement {
#     actions = ["sts:AssumeRole"]

#     principals {
#       type        = "AWS"
#       # TODO: Could change this, to have Identity Hub account ID be passed in
#       identifiers = ["arn:aws:iam::152001638181:root"]
#     }
#   }
# }

resource "aws_iam_role" "admin" {
  name               = "admin"
  assume_role_policy = data.aws_iam_policy_document.human_assume_role_policy.json
}
