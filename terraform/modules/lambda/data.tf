data "aws_ecr_image" "app" {
  repository_name = var.repository_name
  image_tag       = var.image_version
}

data "aws_ecr_repository" "image_registry" {
  name = var.repository_name
}

data "aws_iam_role" "lambda_role" {
  name = "LabRole"
}

#Permissions for the lambda function
data "aws_iam_policy_document" "lambda_permissions" {
  # disabled for academical reasons
  #checkov:skip=CKV_AWS_111: "Ensure IAM policies does not allow write access without constraints"
  #checkov:skip=CKV_AWS_356: "Ensure no IAM policies documents allow "*" as a statement's resource for restrictable actions"

  #Permissions to record logs on CloudWatch
  statement {
    sid = "LambdaLogsCreatePutLogsPolicy"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect = "Allow"
    #TODO: wildcard must be removed
    resources = ["*"]
  }

  #Permissions to pull image from ECR
  statement {
    sid = "LambdaECRImageCrossAccountRetrievalPolicy"
    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer"
    ]
    effect = "Allow"
    #TODO: wildcard must be removed
    resources = [data.aws_ecr_repository.image_registry.arn]
  }
}