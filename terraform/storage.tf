variable bucket_name {
  default = "test-lambda-1"
}

variable source_code_folder {
  default = "souce-code"
}

resource "aws_s3_bucket" "test_lambda_1" {
  bucket = var.bucket_name
  tags = {
    Name        = "Test Lambda 1 - S3 Bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_object" "source_code_folder" {
  bucket = var.bucket_name
  acl    = "private"
  key    = var.source_code_folder + "/"
  source = "/dev/null"
}