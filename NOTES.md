# Command Cheatsheet
## Poetry

### One-time initialization
```
poetry install
```

### Add a project dependency
```
poetry add requests
```
### Add a dependency to a specific group
```
poetry add types-requests --group type_check
```
```
poetry add boto3 --group dev
```

### Activate poetry's virtual env
```
poetry shell
```

### Run main file
```
poetry run python3 src/sanmo/monitor.py
```

### Build package
```
poetry build
```

## Nox
### Run all checks
```
nox
```
### Execute tests
```
nox -s test -- -k prune_non_relevant_fields
```
### Code Style check
```
nox -s lint
```
### Code Formatting
```
nox -s fmt
```
```
nox -s fmt_check
```
### List dependecies' licenses
```
nox -N -s licenses
```

## Other
### Print dependency tree
```
pipdeptree
```
## Terraform
#### Initialize terraform
```
terraform init
```
### Formatting and validation
```
terraform fmt
```
```
terraform validate
```
## Materializing resources
```
terraform plan
```
```
terraform apply
```
## Cleaning up resources
```
terraform destroy
```
## Debugging AWS terraform issues
```
export TF_LOG=TRACE
```
## AWS CLI

```
LAMBDA_NAME='test-lambda-1'
LAMBDA_REGION='us-east-1'
S3_BUCKET='ldeltoro-test-lambda-1'
S3_KEY_PREFIX='source-code'
VERSION=`cat pyproject.toml | grep -E "^version =" | sed 's/^version = "\([0-9\.]*\)".*$/\1/'`


aws s3 cp dist/lambda-${VERSION}.zip s3://${S3_BUCKET}/${S3_KEY_PREFIX}/${LAMBDA_NAME}-${VERSION}.zip

aws lambda --region $LAMBDA_REGION --debug create-function --function-name $LAMBDA_NAME --role "arn:aws:iam::238035455863:role/test-lambda-1-iam-role" --runtime "python3.8" --handler "sanmo.monitor.lambda_handler" --code S3Bucket=$S3_BUCKET,S3Key=${S3_KEY_PREFIX}/${LAMBDA_NAME}-${VERSION}.zip
aws lambda --region $LAMBDA_REGION  update-function-code --function-name $LAMBDA_NAME --s3-bucket $S3_BUCKET --s3-key ${S3_KEY_PREFIX}/${LAMBDA_NAME}-${VERSION}.zip

aws lambda --region $LAMBDA_REGION  update-function-code --function-name $LAMBDA_NAME --s3-bucket $S3_BUCKET --s3-key ${S3_KEY_PREFIX}/${LAMBDA_NAME}-${VERSION}.zip
```

## DOCKER
### Open docker container in interactive mode
```
docker run --rm -v sanmo-store:/home/user/sanmo_store --interactive --tty sanmo
```

### Copy contents out of a docker volume
It can be done by using a temporary container
```
CID=$(docker run -d -v sanmo-store:/home/user/sanmo_store -w /home/user/sanmo_store sanmo true)

docker cp $CID:/home/user/sanmo_store .

docker rm $CID
```