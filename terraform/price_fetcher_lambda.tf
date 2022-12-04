variable "lambda_package" {
  default = "test-lambda-1-1.0.0.zip"
}

variable "price_fetcher_lambda_name" {
  default = "test-lambda-1"
}

resource "aws_iam_role" "price_fetcher_lambda_iam_role" {
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


resource "aws_lambda_function" "price_fetcher" {
  function_name = var.price_fetcher_lambda_name
  role          = aws_iam_role.price_fetcher_lambda_iam_role.arn

  s3_bucket = aws_s3_bucket.price_fetcher.bucket
  s3_key    = "${aws_s3_object.price_fetcher__source_code_folder.key}${var.lambda_package}"
  handler   = "sanmo.price_fetcher.lambda_handler"
  runtime   = "python3.8"
  timeout   = 60

  tags = {
    Name        = "Test Lambda 1"
    Environment = "Dev"
  }
}

resource "aws_iam_role_policy_attachment" "aws_lambda_basic_execution_role_to_price_fetcher_lambda" {
  role       = aws_iam_role.price_fetcher_lambda_iam_role.name
  policy_arn = data.aws_iam_policy.aws_lambda_basic_execution_role.arn
}

resource "aws_iam_role_policy_attachment" "star_atlas_s3_bucket_rw_to_price_fetcher_lambda" {
  role       = aws_iam_role.price_fetcher_lambda_iam_role.name
  policy_arn = aws_iam_policy.star_atlas_s3_bucket_rw.arn
}

resource "aws_cloudwatch_event_rule" "price_fetcher_lambda_trigger" {
  event_bus_name      = "default"
  is_enabled          = "true"
  name                = "${var.price_fetcher_lambda_name}-trigger"
  schedule_expression = "cron(0 * * * ? *)"
}

resource "aws_cloudwatch_event_target" "price_fetcher_lambda" {
  arn  = aws_lambda_function.price_fetcher.arn
  rule = aws_cloudwatch_event_rule.price_fetcher_lambda_trigger.name
}

resource "aws_lambda_permission" "allow_cloudwatch_to_invoke_price_fetcher_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.price_fetcher.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.price_fetcher_lambda_trigger.arn
}