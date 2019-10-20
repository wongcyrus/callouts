excelbucket=$(aws cloudformation describe-stacks --stack-name excellexbot \
--query 'Stacks[0].Outputs[?OutputKey==`LexExcelBucket`].OutputValue' --output text)

aws s3 cp contract_flow/CalloutBot.xlsx s3://$excelbucket/
aws s3 cp contract_flow/CalloutBotDate.xlsx s3://$excelbucket/
aws s3 cp contract_flow/CalloutBotNumber.xlsx s3://$excelbucket/
aws s3 cp contract_flow/CalloutBotTime.xlsx s3://$excelbucket/