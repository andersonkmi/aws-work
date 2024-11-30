import boto3
import logging
import os

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Default region
    region_name = os.environ['region']
    instance_id = os.environ['instance_id']
    
    if not instance_id:
        logger.error("No instance_id provided in the event.")
        return {
            "statusCode": 400,
            "body": "Error: 'instance_id' is required in the event payload."
        }
    
    try:
        # Create EC2 client
        ec2_client = boto3.client('ec2', region_name=region_name)
        
        # Start the EC2 instance
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        
        # Extract and log instance state
        starting_instance = response['StartingInstances'][0]
        current_state = starting_instance['CurrentState']['Name']
        logger.info(f"Instance {instance_id} is now {current_state}.")
        
        return {
            "statusCode": 200,
            "body": f"Instance {instance_id} is now {current_state}."
        }
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
