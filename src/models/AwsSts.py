import boto3
from utils.logging import setup_logging

logger = setup_logging()

class AwsSts:
    @staticmethod
    def assume_role(role_arn: str,region: str):
        """Assume role cross-account and return session credentials"""
        try:
            sts_client = boto3.client('sts')
            response = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName="ResourceScheduler"
            )
            logger.info(f"Assumed role {role_arn} successfully.")
            return boto3.Session(
                aws_access_key_id=response['Credentials']['AccessKeyId'],
                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                aws_session_token=response['Credentials']['SessionToken'],
                region_name=region
            )
        except Exception as e:
            logger.error(f"Failed to assume role {role_arn}: {str(e)}")
            raise