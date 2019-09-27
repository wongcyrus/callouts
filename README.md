# AWS Callouts

This project is a tools to send out bound call reminder with AWS Connect and save the confirmation record in DynamoDB.


## Setup

1. Deploy ExcelLexBot.
2. Upload CalloutBot.xlsx to the S3 bucket for ExcelLexBot.
2. You have to create a AWS connect instance with a contact flow. https://docs.aws.amazon.com/connect/latest/adminguide/connect-contact-flows.html 
2. Import contract_flow/CallingOutContractFlow.json . https://docs.aws.amazon.com/connect/latest/adminguide/contact-flow-import-export.html
3. Deploy this project.

## Deployment with Cloud9
Update ContactFlowId, InstanceId, and SourcePhoneNumber in deployment.sh.

./setup.sh
./deployment.sh

