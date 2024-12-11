import boto3
import logging
import os

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # Default region
    region_name = os.environ['region']
    start_instance_id = os.environ['start_instance_id']
    stop_instance_id = os.environ['stop_instance_id']
    allocation_id = os.environ['allocation_id']

    if not start_instance_id:
        logger.error("No start_instance_id provided in the event.")
        return {
            "statusCode": 400,
            "body": "Error: 'start_instance_id' is required in the event payload."
        }

    if not stop_instance_id:
        logger.error("No stop_instance_id provided in the event.")
        return {
            "statusCode": 400,
            "body": "Error: 'stop_instance_id' is required in the event payload."
        }

    try:
        # Create EC2 client
        ec2_client = boto3.client('ec2', region_name=region_name)
        ec2_waiter = ec2_client.get_waiter('instance_running')

        # Start the EC2 instance
        ec2_client.start_instances(InstanceIds=[start_instance_id])

        # Wait until the instance is running
        logger.info(f"Waiting for instance {start_instance_id} to enter 'running' state.")
        ec2_waiter.wait(InstanceIds=[start_instance_id])

        # Extract and log instance state
        logger.info(f"Instance {start_instance_id} is now running.")

        # Associate the EIP
        eip_association_response = ec2_client.associate_address(InstanceId=start_instance_id, AllocationId=allocation_id,
                                                                AllowReassociation=True)
        print(f"Elastic IP associated successfully: {eip_association_response['AssociationId']}")

        # Stop the other EC2 instance
        stop_response = ec2_client.stop_instances(InstanceIds=[stop_instance_id])
        stopping_instance = stop_response['StoppingInstances'][0]
        current_state = stopping_instance['CurrentState']['Name']
        logger.info(f"Instance {stop_instance_id} is now {current_state}.")

        return {
            "statusCode": 200,
            "body": f"Instance {start_instance_id} is now running."
        }

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
