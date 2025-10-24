#!/bin/bash

# IAM Role Deployment Script for AWS Reporter
# Usage: ./iam-role-deployment.sh <source-account-id> <target-account-id>

SOURCE_ACCOUNT_ID=$1
TARGET_ACCOUNT_ID=$2
ROLE_NAME="AWSReporterRole"
POLICY_NAME="AWSReporterPolicy"

if [ -z "$SOURCE_ACCOUNT_ID" ] || [ -z "$TARGET_ACCOUNT_ID" ]; then
    echo "Usage: $0 <source-account-id> <target-account-id>"
    exit 1
fi

# Create trust policy
cat > trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::${SOURCE_ACCOUNT_ID}:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

# Create permissions policy
cat > permissions-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeRegions"
            ],
            "Resource": "*"
        }
    ]
}
EOF

# Create IAM role
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document file://trust-policy.json

# Create IAM policy
aws iam create-policy \
    --policy-name $POLICY_NAME \
    --policy-document file://permissions-policy.json

# Attach policy to role
aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn "arn:aws:iam::${TARGET_ACCOUNT_ID}:policy/${POLICY_NAME}"

# Clean up temporary files
rm trust-policy.json permissions-policy.json

echo "IAM role ${ROLE_NAME} created successfully"
echo "Role ARN: arn:aws:iam::${TARGET_ACCOUNT_ID}:role/${ROLE_NAME}"
