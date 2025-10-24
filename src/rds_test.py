from services.aws_rds_service import AWSRDSService
from utils.logging import setup_logging
import json

logger = setup_logging()

def main():
    try:
        logger.info("Starting RDS test...")
        rds = AWSRDSService()
        
        # Get RDS instances
        response = rds.get_resources()
        instances = response.get("DBInstances", [])
        
        logger.info(f"Found {len(instances)} RDS instances")
        
        # Print instance details
        for db_instance in instances:
            logger.info(f"DB Instance: {db_instance['DBInstanceIdentifier']}")
            logger.info(f"  Status: {db_instance['DBInstanceStatus']}")
            logger.info(f"  Engine: {db_instance['Engine']}")
            logger.info(f"  Class: {db_instance['DBInstanceClass']}")
        
        # Export to JSON
        with open("../rds.json", "w") as f:
            json.dump(response, f, default=str, indent=4)
        
        logger.info("RDS data exported to rds.json")
        
    except Exception as e:
        logger.error(f"RDS test failed: {e}")
        raise

if __name__ == "__main__":
    main()