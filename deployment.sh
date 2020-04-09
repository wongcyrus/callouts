echo "Deploy Stack"

sam build
# sam deploy

# Publish to Serverless Application Repository 
rm package.yaml
sam package --s3-bucket cyruswong-sam-repo --output-template-file package.yaml
sam publish --template package.yaml --region us-east-1