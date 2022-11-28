variable "lambda_package" {
  default = "test-lambda-1-1.0.0.zip"
}

variable "lambda_name" {
  default = "test-lambda-1"
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
  function_name = var.lambda_name
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

resource "aws_cloudwatch_event_rule" "sanmo_monitor_daily_trigger" {
  event_bus_name      = "default"
  is_enabled          = "true"
  name                = "${var.lambda_name}-daily-trigger"
  schedule_expression = "cron(0 10 * * ? *)"
}

resource "aws_cloudwatch_event_target" "sanmo_monitor_daily_trigger" {
  arn  = aws_lambda_function.test_lambda_1.arn
  rule = aws_cloudwatch_event_rule.sanmo_monitor_daily_trigger.name
}

resource "aws_lambda_permission" "allow_cloudwatch_to_invoke_test_lambda_1" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda_1.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.sanmo_monitor_daily_trigger.arn
}