# AWS Reporter for Cross Account

A Python-based tool for reporting AWS resources across multiple accounts using cross-account role assumption.

## Features

- Cross-account AWS resource reporting
- EC2 instance discovery and reporting
- Configurable account management
- JSON output support
- Comprehensive logging

## Project Structure

```
aws-reporter/
├── src/
│   ├── models/
│   │   ├── aws_instance.py    # EC2 instance operations
│   │   ├── aws_sts.py         # STS role assumption
│   │   └── config.py          # Configuration management
│   ├── utils/
│   │   └── logging.py         # Logging utilities
│   ├── lambda_function.py     # Main Lambda function
│   └── ec2_instance_test.py   # Test script
├── config/
│   └── accounts.json          # Account configuration
├── infrastructure/
│   └── main-aws-reporter.yaml # CloudFormation template
└── scripts/                   # Deployment scripts
```

## Prerequisites

- Python 3.8+
- AWS CLI configured
- Appropriate IAM permissions for cross-account access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aws-reporter
```

2. Install dependencies:
```bash
pip install boto3
```

3. Configure AWS credentials:
```bash
aws configure
```

## Configuration

### Account Configuration

Edit `config/accounts.json` to add your AWS accounts:

```json
{
    "accounts": [
        {
            "account_name": "production",
            "account_id": "123456789012",
            "role_arn": "arn:aws:iam::123456789012:role/AWSReporterRole",
            "region": "ap-southeast-1"
        }
    ]
}
```

### IAM Role Setup

Create an IAM role in each target account with the following trust policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::SOURCE-ACCOUNT-ID:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

Attach the following policy for EC2 read access:

```json
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
```

## Usage

### Basic EC2 Instance Reporting

```bash
cd src
python3 ec2_instance_test.py
```

This will:
- Load account configuration
- Connect to AWS using default credentials
- Retrieve EC2 instances
- Output results to `instances_output.json`

### Lambda Function

Deploy and run the Lambda function:

```bash
python3 src/lambda_function.py
```

### Programmatic Usage

```python
from models.aws_instance import AwsInstance
from models.config import Config

# Load configuration
config = Config.load_config("config/accounts.json")

# Initialize AWS instance client
aws_instance = AwsInstance()

# Get instances
instances = aws_instance.get_instances()

# Process results
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance ID: {instance['InstanceId']}")
        print(f"State: {instance['State']['Name']}")
        print(f"Type: {instance['InstanceType']}")
```

## API Reference

### AwsInstance Class

#### `__init__(session=None)`
Initialize the AwsInstance client.
- `session`: Optional boto3 session. If None, uses default credentials.

#### `get_instances()`
Retrieve all EC2 instances in the configured region.
- Returns: EC2 describe_instances response

### Config Class

#### `load_config(file_path)`
Load account configuration from JSON file.
- `file_path`: Path to configuration file
- Returns: Configuration dictionary

### AwsSts Class

#### `assume_role(role_arn, region)`
Assume an IAM role for cross-account access.
- `role_arn`: ARN of the role to assume
- `region`: AWS region
- Returns: boto3 session with assumed role credentials

## Output Format

The tool outputs EC2 instance data in JSON format with datetime objects converted to ISO format strings.

Example output structure:
```json
{
    "Reservations": [
        {
            "Instances": [
                {
                    "InstanceId": "i-1234567890abcdef0",
                    "InstanceType": "t3.micro",
                    "State": {
                        "Name": "running"
                    },
                    "LaunchTime": "2023-10-22T10:30:00"
                }
            ]
        }
    ]
}
```

## Logging

Logs are written to the `logs/` directory with timestamps. Log level can be configured in `utils/logging.py`.

## Troubleshooting

### Common Issues

1. **"Unable to locate credentials"**
   - Ensure AWS credentials are configured
   - Check AWS_PROFILE environment variable

2. **"Access Denied" when assuming role**
   - Verify IAM role trust policy
   - Check role permissions

3. **"TypeError: Object of type datetime is not JSON serializable"**
   - Use the datetime handler in JSON serialization
   - Already handled in `ec2_instance_test.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]
