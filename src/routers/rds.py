from fastapi import APIRouter
from services.aws_rds_service import AWSRDSService

router = APIRouter(tags=["RDS"])

@router.get("/rds")
async def get_rds_instances():
    rds = AWSRDSService()
    return rds.get_resources()

@router.get("/rds/{instance_id}")
async def find_instance_by_id(instance_id: str):
    # rds = AWSRDSService()
    print("Get Intance by ID {}", instance_id)
    return instance_id