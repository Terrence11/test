import csv
import io
from azure.storage.filedatalake import DataLakeServiceClient


def upload_csv_to_adls(account_name, account_key, file_system_name, file_path):
    """
    Create a small CSV in memory and upload it to Azure Data Lake Storage Gen2.
    :param account_name: Name of the ADLS storage account (without domain suffix).
    :param account_key: Access key for the storage account.
    :param file_system_name: Name of the ADLS file system (container).
    :param file_path: Path (including filename) in the file system, e.g. 'sample-data/sample.csv'.
    """

    account_url = f"https://{account_name}.dfs.core.windows.net"

    # Initialize the ADLS service client
    service_client = DataLakeServiceClient(account_url=account_url, credential=account_key)

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

    # Get a client for the file system and the destination file
    file_system_client = service_client.get_file_system_client(file_system=file_system_name)
    file_client = file_system_client.get_file_client(file_path)

    # Upload CSV content (overwrite=True allows reruns)
    response = file_client.upload_data(csv_buffer.getvalue(), overwrite=True)

    print("Upload response:", response)
    print(f"Successfully uploaded {file_path} to ADLS file system {file_system_name}!")


if __name__ == "__main__":
    # Replace these with your real ADLS account details
    my_account_name = "your_storage_account_name"
    my_account_key = "your_storage_account_key"
    my_file_system = "your-file-system"
    my_file_path = "sample-data/sample.csv"

    upload_csv_to_adls(
        my_account_name,
        my_account_key,
        my_file_system,
        my_file_path,
    )
