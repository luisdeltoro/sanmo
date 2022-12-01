
variable "price_metric_emitter_lambda_name" {
  default = "test-lambda-2"
}

resource "aws_iam_role" "price_metric_emitter_lambda_iam_role" {
  name = "test-lambda-2-iam-role"

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


resource "aws_lambda_function" "price_metric_emitter" {
  function_name = var.price_metric_emitter_lambda_name
  role          = aws_iam_role.price_metric_emitter_lambda_iam_role.arn

  s3_bucket = aws_s3_bucket.price_fetcher.bucket
  s3_key    = "${aws_s3_object.price_fetcher__source_code_folder.key}${var.lambda_package}"
  handler   = "sanmo.price_metric_emitter.lambda_handler"
  runtime   = "python3.8"
  timeout   = 60

  tags = {
    Name        = "Test Lambda 2"
    Environment = "Dev"
  }
}


resource "aws_iam_role_policy_attachment" "aws_lambda_basic_execution_role_to_price_emitter_lambda" {
  role       = aws_iam_role.price_metric_emitter_lambda_iam_role.name
  policy_arn = data.aws_iam_policy.aws_lambda_basic_execution_role.arn
}

resource "aws_iam_role_policy_attachment" "star_atlas_s3_bucket_rw_to_price_emitter_lambda" {
  role       = aws_iam_role.price_metric_emitter_lambda_iam_role.name
  policy_arn = aws_iam_policy.star_atlas_s3_bucket_rw.arn
}

resource "aws_iam_policy" "cloud_watch_allow_put_metric" {
  name        = "CloudWatchAllowPutMetric"
  description = "Cloud Watch Allow Put Metric"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "cloudwatch:PutMetricData*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "cloud_watch_allow_put_metric_to_price_emitter_lambda" {
  role       = aws_iam_role.price_metric_emitter_lambda_iam_role.name
  policy_arn = aws_iam_policy.cloud_watch_allow_put_metric.arn
}

resource "aws_s3_bucket_notification" "price_metric_emitter_lambda_trigger" {
  bucket = aws_s3_bucket.star_atlas.bucket

  lambda_function {
    lambda_function_arn = aws_lambda_function.price_metric_emitter.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "sanmo_store/"
  }
}

data "aws_caller_identity" "current" {}

resource "aws_lambda_permission" "allow_s3_to_invoke_price_metric_emitter_lambda" {
  statement_id   = "AllowExecutionFromS3"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.price_metric_emitter.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.star_atlas.arn
  source_account = data.aws_caller_identity.current.account_id
}