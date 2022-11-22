variable lambda_package {
  default = "test-lambda-1-1.0.0.zip"
}

resource "aws_iam_role" "test_lambda_1_iam_role" {
  name = "test-lambda-1-iam-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_s3_bucket" "test_lambda_1" {
  bucket = var.bucket_name
}

resource "aws_lambda_function" "test_lambda_1" {
  function_name = "lambda_function_name"
  role          = aws_iam_role.test_lambda_1_iam_role.arn

  s3_bucket = data.aws_s3_bucket.test_lambda_1
  s3_key = var.source_code_folder + "/" + var.lambda_package
  handler       = "monitor.lambda_handler"
  runtime = "python3.8"

  tags = {
    Name        = "Test Lambda 1"
    Environment = "Dev"
  }
}