import boto3
import csv
import io

def upload_csv_to_s3(bucket_name, object_key):
    """
    Create a small CSV in memory and upload it to S3.
    :param bucket_name: Name of the S3 bucket.
    :param object_key: Path (including filename) in the bucket, e.g. 'folder/sample.csv'.
    """

    # Initialize the S3 client (make sure AWS credentials are configured)
    s3_client = boto3.client('s3', region_name='us-east-1')  # Change region if needed

    # Create CSV data in memory using StringIO
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)

    # Write header row
    writer.writerow(["Name", "Age", "City"])

    # Write sample rows
    writer.writerow(["Alice", 30, "New York"])
    writer.writerow(["Bob", 25, "London"])
    writer.writerow(["Charlie", 35, "Sydney"])

    # Reset buffer position to the start
    csv_buffer.seek(0)

    # Upload the CSV data to S3
    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=csv_buffer.getvalue()
    )

    # Optionally print response or return it
    print("Upload response:", response)
    print(f"Successfully uploaded {object_key} to {bucket_name}!")


if __name__ == "__main__":
    # Replace these with your real bucket name and desired object key
    my_bucket = "lzbucket0226"
    my_object_key = "sample-data/sample.csv"

    upload_csv_to_s3(my_bucket, my_object_key)
