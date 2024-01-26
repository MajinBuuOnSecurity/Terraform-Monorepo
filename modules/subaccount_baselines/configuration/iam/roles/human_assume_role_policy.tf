data "aws_iam_policy_document" "human_assume_role_policy" {
  statement {
    actions = [
      "sts:AssumeRole",
      "sts:SetSourceIdentity",
    ]

    principals {
      type        = "AWS"
      # TODO: Could change this, to have Identity Hub account ID be passed in
      identifiers = ["arn:aws:iam::152001638181:root"]
    }
  }
}
