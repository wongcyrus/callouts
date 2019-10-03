export STACK_NAME=it114115callout
export AWS_DEFAULT_REGION=us-east-1
export REGION=$AWS_DEFAULT_REGION

echo "Deploy $STACK_NAME stack at $REGION region"

sourcebucket=cywong$STACK_NAME
aws s3 mb s3://$sourcebucket --region $REGION 
rm package.yaml
sam package --template-file template.yaml --s3-bucket $sourcebucket --output-template-file package.yaml

aws cloudformation deploy --stack-name $STACK_NAME --template-file package.yaml \
--region $REGION --capabilities CAPABILITY_IAM \
--parameter-overrides \
    InstanceArn="arn:aws:connect:us-east-1:467005446488:instance/3af3242c-de99-472b-914c-060e914f844b" \
    ContactFlowArn="arn:aws:connect:us-east-1:467005446488:instance/3af3242c-de99-472b-914c-060e914f844b/contact-flow/5647fbab-8265-4a7d-bedb-3811f597c906" \
    SourcePhoneNumber="+12569639465" 