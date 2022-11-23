variable "bucket_name" {
  default = "ldeltoro-test-lambda-1"
}

variable "source_code_folder" {
  default = "source-code"
}

resource "aws_s3_bucket" "test_lambda_1" {
  bucket = var.bucket_name
  tags = {
    Name        = "Test Lambda 1 - S3 Bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_object" "source_code_folder" {
  bucket = aws_s3_bucket.test_lambda_1.bucket
  acl    = "private"
  key    = "${var.source_code_folder}/"
  source = "/dev/null"
}