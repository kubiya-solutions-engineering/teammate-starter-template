import boto3
import argparse

def list_s3_buckets(profile_name):
    # Create a session using the specified profile
    session = boto3.Session(profile_name=profile_name)

    # Create an S3 client
    s3_client = session.client('s3')

    # List all S3 buckets
    response = s3_client.list_buckets()

    # Print the names of all buckets
    print("Buckets:")
    for bucket in response['Buckets']:
        print(f"  {bucket['Name']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List all S3 buckets.')
    parser.add_argument('--profile', type=str, required=True, help='AWS CLI profile name')

    args = parser.parse_args()
    list_s3_buckets(args.profile)
