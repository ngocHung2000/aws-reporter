#!/bin/bash
 
set -e  # Exit on any error

STACK_NAME="aws-reporter-resource-cross-account"
LAMBDA_NAME="lambda-func-apse1-aws-reporter-resource-cross-account"
ZIP_FILE="aws-reporter.zip"

echo "🚀 This script will deploy AWS resources aws-reporter:"
echo "   - CloudFormation stack: $STACK_NAME"
echo "   - Lambda function: $LAMBDA_NAME"
read -p "❓ Are you sure you want to continue? (y/N): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "❌ Operation cancelled."
    exit 1
fi

echo ""
echo "1️⃣ Deploying Lambda aws-reporter in main account..."
aws cloudformation deploy \
    --template-file infrastructure/main-aws-reporter.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM

echo "✅ Lambda aws-reporter deployed successfully"
echo ""
 
echo "2️⃣ Packaging Lambda code..."
cd src && zip -r ../$ZIP_FILE . ../config/ > /dev/null
cd ..
 
echo "3️⃣ Updating Lambda function code..."
aws lambda update-function-code \
    --function-name $LAMBDA_NAME \
    --zip-file fileb://$ZIP_FILE > /dev/null

echo "✅ Lambda code updated successfully"
echo ""
# Cleanup
rm -f $ZIP_FILE

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Tag your instances using: ./scripts/tag-resources.sh"
echo "   2. Check CloudWatch logs: /aws/lambda/$LAMBDA_NAME"
echo "   3. Verify scheduling in 15 minutes"
echo ""
echo "📖 Documentation:"
echo "   - Tagging Guide: docs/tagging-guide.md"
echo "   - Deployment Guide: docs/deployment-guide.md"