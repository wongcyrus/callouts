contactFlowArn=arn:aws:connect:us-east-1:467005446488:instance/087c643b-fd04-4b8a-b2c1-b32c1e6de399/contact-flow/9163cea9-b9d6-4630-b315-920695e12e66
sourcePhoneNumber=+18337325078

export STACK_NAME=aws_callout
export AWS_DEFAULT_REGION=us-east-1
export REGION=$AWS_DEFAULT_REGION

echo "Deploy $STACK_NAME stack at $REGION region"

sourcebucket=awscallout$STACK_NAME
aws s3 mb s3://$sourcebucket --region $REGION 
rm package.yaml
sam package --template-file template.yaml --s3-bucket $sourcebucket --output-template-file package.yaml


instanceArn="$(echo $contactFlowArn | cut -d '/' -f1)/$(echo $contactFlowArn | cut -d '/' -f2)"

aws cloudformation deploy --stack-name $STACK_NAME --template-file package.yaml \
--region $REGION --capabilities CAPABILITY_IAM \
--parameter-overrides \
    InstanceArn=$instanceArn \
    ContactFlowArn=$contactFlowArn \
    SourcePhoneNumber=$sourcePhoneNumber