instanceId=087c643b-fd04-4b8a-b2c1-b32c1e6de399
contactFlowId=9163cea9-b9d6-4630-b315-920695e12e66
sourcePhoneNumber=+18337325078

export STACK_NAME=awscallout
export AWS_DEFAULT_REGION=us-east-1
export REGION=$AWS_DEFAULT_REGION

echo "Deploy $STACK_NAME stack at $REGION region"

sourcebucket=awscallout$UNIQUE_ID
aws s3 mb s3://$sourcebucket --region $REGION 
rm package.yaml
sam package --template-file template.yaml --s3-bucket $sourcebucket --output-template-file package.yaml

aws cloudformation deploy --stack-name $STACK_NAME --template-file package.yaml \
--region $REGION --capabilities CAPABILITY_IAM \
--parameter-overrides \
    InstanceId=$instanceId \
    ContactFlowId=$contactFlowId \
    SourcePhoneNumber=$sourcePhoneNumber

sam publish --template package.yaml --region us-east-1