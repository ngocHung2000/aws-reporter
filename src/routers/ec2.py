from fastapi import APIRouter, HTTPException
from services.aws_ec2_service import AWSEC2Service

# Custom router cho EC2 specific actions
router = APIRouter(prefix="/ec2", tags=["EC2"])

# Include base routes
@router.post("/{instance_id}/start")
async def start_instance(instance_id: str):
    try:
        service = AWSEC2Service()
        service.start_instance(instance_id)
        return {"message": f"Instance {instance_id} started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{instance_id}/stop")
async def stop_instance(instance_id: str):
    try:
        service = AWSEC2Service()
        service.stop_instance(instance_id)
        return {"message": f"Instance {instance_id} stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def get_ec2_instances():
    ec2 = AWSEC2Service()
    return ec2.get_resources()

@router.get("/{instance_id}")
async def get_ec2_by_id(instance_id: str):
    print(f"Get Intance by ID {instance_id}")
    return instance_id