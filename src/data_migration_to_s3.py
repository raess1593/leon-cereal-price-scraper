import sqlite3
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

def migrate_db_to_cloud(local_path: str, bucket: str) -> None:
    s3_client = boto3.client('s3')

    try:
        conn = sqlite3.connect(local_path)
        df_silver = pd.read_sql_query("SELECT * FROM crop_prices_clean", conn)
        conn.close()

        try:
            s3_client.create_bucket(Bucket=bucket)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ['BucketAlreadyOwnedByYou', 'BucketAlreadyExists']: pass
            else: print(e)

        silver_path = f"s3://{bucket}/silver/lonja.csv"
        print("Uploading data to silver")
        df_silver.to_csv(silver_path, index=False)

        try:
            s3_client.put_object_tagging(
                Bucket=bucket,
                Key="silver/lonja.csv",
                Tagging={
                    'TagSet': [
                        {'Key': 'Source', 'Value': 'Leon_Cereal_Price_ScraperBot'},
                        {'Key': 'Status', 'Value': 'Ready'}
                    ]
                }
            )
        except Exception as e: print(e)

        try:
            s3_client.put_bucket_versioning(
                Bucket=bucket,
                VersioningConfiguration={
                    'Status': 'Enabled'
                }
            )
        except Exception as e: print(e)

        print("Data has been uploaded successfully")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    local_path="data/lonja.db"
    BUCKET="leon-cereal-price-data"

    migrate_db_to_cloud(local_path, BUCKET)