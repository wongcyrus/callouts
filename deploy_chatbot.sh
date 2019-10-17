excelbucket=$(aws cloudformation describe-stacks --stack-name excellexbot \
--query 'Stacks[0].Outputs[?OutputKey==`LexExcelBucket`].OutputValue' --output text)

aws s3 cp contract_flow/CalloutBot.xlsx s3://$excelbucket/