variable "lambda_bucket_name" {
  default = "ldeltoro-test-lambda-1"
}

variable "storage_bucket" {
  default = "star-atlas"
}

variable "source_code_folder" {
  default = "source-code"
}

variable "sanmo_storage_folder" {
  default = "sanmo_store"
}

resource "aws_s3_bucket" "test_lambda_1" {
  bucket = var.lambda_bucket_name
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

resource "aws_s3_bucket" "star_atlas" {
  bucket = var.storage_bucket
  tags = {
    Name        = "Star Atlas - S3 Bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_object" "sanmo_store_folder" {
  bucket = aws_s3_bucket.star_atlas.bucket
  acl    = "private"
  key    = "${var.sanmo_storage_folder}/"
  source = "/dev/null"
}

resource "aws_iam_policy" "star_atlas_s3_bucket_rw" {
  name        = "StarAtlasS3BucketRW"
  path        = "/"
  description = "Allows to read and write to star atlas bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:GetObject",
          "s3:GetObjectAcl",
          "s3:AbortMultipartUpload",
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.star_atlas.arn,
          "${aws_s3_bucket.star_atlas.arn}/*"
        ]
      },
    ]
  })
}