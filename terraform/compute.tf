variable "lambda_package" {
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


resource "aws_lambda_function" "test_lambda_1" {
  function_name = "test-lambda-1"
  role          = aws_iam_role.test_lambda_1_iam_role.arn

  s3_bucket = aws_s3_bucket.test_lambda_1.bucket
  s3_key    = "${aws_s3_object.source_code_folder.key}${var.lambda_package}"
  handler   = "sanmo.monitor.lambda_handler"
  runtime   = "python3.8"
  timeout   = 60

  tags = {
    Name        = "Test Lambda 1"
    Environment = "Dev"
  }
}

resource "aws_iam_role_policy_attachment" "star_atlas_s3_bucket_rw_to_test_lambda_1" {
  role       = aws_iam_role.test_lambda_1_iam_role.name
  policy_arn = aws_iam_policy.star_atlas_s3_bucket_rw.arn
}