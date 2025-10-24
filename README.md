# AWS Reporter for Cross Account

A FastAPI-based REST API for managing and reporting AWS resources across multiple accounts using cross-account role assumption.

## Features

- **FastAPI REST API** with automatic OpenAPI documentation
- **Cross-account AWS resource management** using STS role assumption
- **EC2 instance operations**: List, start, stop, and tag instances
- **RDS instance operations**: List, start, stop DB instances
- **Configurable account management** via JSON configuration
- **Comprehensive logging** with structured log files
- **CORS support** for web integration
- **Modular service architecture** with base classes

## Project Structure

```
aws-reporter/
├── src/
│   ├── routers/
│   │   ├── ec2.py             # EC2 API endpoints
│   │   ├── rds.py             # RDS API endpoints
│   │   └── base.py            # Base router utilities
│   ├── services/
│   │   ├── aws_ec2_service.py # EC2 service layer
│   │   ├── aws_rds_service.py # RDS service layer
│   │   ├── aws_aurora_service.py # Aurora service layer
│   │   ├── aws_sts_service.py # STS role assumption
│   │   └── aws_base_service.py # Base service class
│   ├── utils/
│   │   ├── logging.py         # Logging utilities
│   │   └── config.py          # Configuration management
│   ├── main.py                # FastAPI application entry point
│   ├── lambda_function.py     # Lambda function (legacy)
│   └── *_test.py              # Test scripts
├── config/
│   └── accounts.json          # Account configuration
├── infrastructure/
│   └── main-aws-reporter.yaml # CloudFormation template
├── scripts/                   # Deployment scripts
├── logs/                      # Application logs
└── requirements.txt           # Python dependencies
```

## Prerequisites

- Python 3.8+
- AWS CLI configured with appropriate credentials
- IAM permissions for cross-account access (if using cross-account features)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aws-reporter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
aws configure
```

## Configuration

### Account Configuration

Edit `config/accounts.json` to add your AWS accounts for cross-account access:

```json
{
    "accounts": [
        {
            "account_name": "production",
            "account_id": "123456789012",
            "role_arn": "arn:aws:iam::123456789012:role/AWSReporterRole",
            "region": "ap-southeast-1"
        },
        {
            "account_name": "staging",
            "account_id": "123456789013",
            "role_arn": "arn:aws:iam::123456789013:role/AWSReporterRole",
            "region": "us-east-1"
        }
    ]
}
```

### IAM Role Setup (for Cross-Account Access)

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

Attach policies for required AWS services:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:CreateTags",
                "rds:DescribeDBInstances",
                "rds:StartDBInstance",
                "rds:StopDBInstance"
            ],
            "Resource": "*"
        }
    ]
}
```

## Usage

### Running the FastAPI Server

Start the API server:
```bash
cd src
python3 main.py
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### API Endpoints

#### General Endpoints
- `GET /` - API information and version
- `GET /health` - Health check endpoint

#### EC2 Endpoints
- `GET /api/v1/ec2/list` - List all EC2 instances
- `GET /api/v1/ec2/{instance_id}` - Get specific EC2 instance details
- `POST /api/v1/ec2/{instance_id}/start` - Start an EC2 instance
- `POST /api/v1/ec2/{instance_id}/stop` - Stop an EC2 instance

#### RDS Endpoints
- `GET /api/v1/rds` - List all RDS instances
- `GET /api/v1/rds/{instance_id}` - Get specific RDS instance details

### Testing Individual Services

Run EC2 service test:
```bash
cd src
python3 ec2_instance_test.py
```

Run RDS service test:
```bash
cd src
python3 rds_test.py
```

Run Aurora service test:
```bash
cd src
python3 aurora_test.py
```

### Programmatic Usage

#### Using EC2 Service
```python
from services.aws_ec2_service import AWSEC2Service

# Initialize EC2 service
ec2_service = AWSEC2Service()

# Get all EC2 instances
instances = ec2_service.get_resources()

# Start an instance
ec2_service.start_instance("i-1234567890abcdef0")

# Stop an instance
ec2_service.stop_instance("i-1234567890abcdef0")

# Tag a resource
ec2_service.tag_resource("i-1234567890abcdef0", {"Environment": "Production"})
```

#### Using RDS Service
```python
from services.aws_rds_service import AWSRDSService

# Initialize RDS service
rds_service = AWSRDSService()

# Get all RDS instances
db_instances = rds_service.get_resources()

# Start a DB instance
rds_service.start_db_instance("my-database")

# Stop a DB instance
rds_service.stop_db_instance("my-database")
```

#### Using Cross-Account Access
```python
from services.aws_sts_service import AWSSTSService
from services.aws_ec2_service import AWSEC2Service

# Assume role in another account
session = AWSSTSService.assume_role(
    role_arn="arn:aws:iam::123456789012:role/AWSReporterRole",
    region="ap-southeast-1"
)

# Use the assumed role session
ec2_service = AWSEC2Service(session=session)
instances = ec2_service.get_resources()
```

## Architecture

### Service Layer Architecture

The application follows a modular service-oriented architecture:

- **AWSBaseService**: Abstract base class providing common functionality
- **AWSEC2Service**: Handles EC2 operations (list, start, stop, tag)
- **AWSRDSService**: Handles RDS operations (list, start, stop)
- **AWSSTSService**: Handles cross-account role assumption
- **Config**: Manages configuration loading from JSON files

### Router Layer

FastAPI routers organize endpoints by AWS service:
- **EC2 Router**: `/api/v1/ec2/*` endpoints
- **RDS Router**: `/api/v1/rds/*` endpoints

## Output Format

API responses return AWS service data in JSON format with proper error handling.

Example EC2 response:
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
                    "LaunchTime": "2023-10-22T10:30:00+00:00"
                }
            ]
        }
    ]
}
```

## Logging

- Logs are written to the `logs/` directory with timestamps
- Log files follow the pattern: `app_YYYYMMDD_HHMMSS.log`
- Structured logging includes service operations and error details
- Log level can be configured in `utils/logging.py`

## Troubleshooting

### Common Issues

1. **"Unable to locate credentials"**
   - Ensure AWS credentials are configured: `aws configure`
   - Check `AWS_PROFILE` environment variable

2. **"Access Denied" when assuming role**
   - Verify IAM role trust policy includes your source account
   - Check role permissions for required AWS services

3. **"Module not found" errors**
   - Ensure you're running from the `src/` directory
   - Install all dependencies: `pip install -r requirements.txt`

4. **FastAPI server won't start**
   - Check if port 8000 is available
   - Verify all router modules have the `router` attribute defined

## Development

### Adding New Services

1. Create a new service class inheriting from `AWSBaseService`
2. Implement the `get_resources()` method
3. Add service-specific methods
4. Create corresponding router endpoints
5. Update `main.py` to include the new router

### Running Tests

Execute individual test files:
```bash
cd src
python3 ec2_instance_test.py
python3 rds_test.py
python3 aurora_test.py
```

## Dependencies

- `boto3>=1.26.0` - AWS SDK for Python
- `fastapi>=0.104.0` - Modern web framework
- `uvicorn>=0.24.0` - ASGI server
- `python-dateutil>=2.8.0` - Date utilities

## License

[Add your license information here]
