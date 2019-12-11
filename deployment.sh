echo "Deploy Stack"

sam build
sam deploy

# sourcebucket=cyruswong-sam-repo
# aws s3 mb s3://$sourcebucket --region $REGION 
# rm package.yaml
# sam package --template-file template.yaml --s3-bucket $sourcebucket --output-template-file package.yaml

# aws cloudformation deploy --stack-name $STACK_NAME --template-file package.yaml \
# --region $REGION --capabilities CAPABILITY_IAM \
# --parameter-overrides \
#     InstanceId=$instanceId \
#     ContactFlowId=$contactFlowId \
#     SourcePhoneNumber=$sourcePhoneNumber

# sam publish --template package.yaml --region us-east-1