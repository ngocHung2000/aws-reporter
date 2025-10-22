#!/bin/bash

set -e  # Exit on any error

STACK_NAME="aws-reporter-resource-cross-account"
LAMBDA_NAME="lambda-func-apse1-aws-reporter-resource-cross-account"

echo "⚠️ WARNING: This script will permanently delete AWS resources:"
echo "   - CloudFormation stack: $STACK_NAME"
echo "   - Lambda function: $LAMBDA_NAME"
read -p "❓ Are you sure you want to continue? (y/N): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "❌ Operation cancelled."
    exit 1
fi

echo ""
echo "🗑️  Deleting Lambda function: $LAMBDA_NAME ..."
aws lambda delete-function --function-name "$LAMBDA_NAME" || echo "ℹ️ Lambda not found, skipping"

echo ""
echo "🗑️  Deleting CloudFormation stack: $STACK_NAME ..."
aws cloudformation delete-stack --stack-name "$STACK_NAME"

echo "⏳ Waiting for stack deletion to complete..."
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"
echo "✅ CloudFormation stack deleted successfully!"

echo ""
echo "🎉 Cleanup completed."
