from services.aws_aurora_service import AwsAurora

aurora = AwsAurora()
for db_instance in aurora.get_resources().get("DBClusters", []):
    print("DB Cluster Identifier:", db_instance["DBClusterIdentifier"])