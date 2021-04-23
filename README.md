# aws-lambda-libpostal-example

This repository contains sample code that uses the libpostal library to parse addresses into parts.  The code is deployed as a Lambda function and is packaged as a Docker container.  The image size is over 2GB in size because the libpostal library contains NLP models that are more than 2GB.

## Usage

```

export AWS_REGION=us-east-2

# Get AWS account ID for later use
ACCOUNT_ID=`aws sts get-caller-identity |jq -r .Account`

# Create ECR repository
aws ecr create-repository --repository-name libpostal-demo

# Package the Docker image
docker build -t libpostal-demo:latest .

# Get ECR Docker login
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Tag image
docker tag libpostal-demo:latest ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/libpostal-demo:latest

# Push image
docker push ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/libpostal-demo:latest

# Create the CloudFormation stack
aws cloudformation deploy           \
    --template template.yaml        \
    --stack-name libpostal-example  \
    --parameter-overrides           \
        ImageName=${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/libpostal-demo  \
        ImageTag=latest             \
    --capabilities CAPABILITY_IAM

```


## Testing

```
# Get the Lambda function name created by CloudFormation
LAMBDA_FUNCTION=`aws cloudformation describe-stacks --stack-name libpostal-example --query "Stacks[0].Outputs[?OutputKey=='FunctionName'].OutputValue" --output text`

# Sample input address
PAYLOAD='{ "address" : "123 33rd St, New York City, NY 10001"}'
PAYLOAD_BASE64=`echo $PAYLOAD |base64`

# Invoke the function and redirect the output to a file named 'output'
aws lambda invoke --function-name $LAMBDA_FUNCTION --payload $PAYLOAD_BASE64 output

# View the output
cat output
```

Output:
```
{
  "house_number": "123",
  "road": "33rd st",
  "city": "new york city",
  "state": "ny",
  "postcode": "10001"
}
```
