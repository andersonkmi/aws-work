import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def stop_ec2_instance(instance_id, region_name='us-east-1'):
    """
    Starts an EC2 instance with the specified instance ID.
    
    :param instance_id: The ID of the EC2 instance to start.
    :param region_name: The AWS region where the EC2 instance resides.
    """
    try:
        # Create an EC2 client
        ec2_client = boto3.client('ec2', region_name=region_name)
        
        # Start the instance
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        
        # Extract and print instance state
        for instance in response['StoppingInstances']:
            print(f"Instance {instance['InstanceId']} is now {instance['CurrentState']['Name']}.")
    
    except NoCredentialsError:
        print("AWS credentials not found.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials configuration.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your instance ID and region
    INSTANCE_ID = "i-056c8b8f33ebd212f"
    REGION = "us-east-1"
    stop_ec2_instance(INSTANCE_ID, REGION)