import aioboto3
from contextlib import asynccontextmanager
from botocore.exceptions import ClientError
from config.settings import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET

session = aioboto3.Session(
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

@asynccontextmanager
async def get_client():
    async with session.client("s3", endpoint_url=MINIO_URL) as s3:
        yield s3

async def ensure_bucket():
    async with get_client() as s3:
        try:
            await s3.head_bucket(Bucket=MINIO_BUCKET)
        except ClientError:
            await s3.create_bucket(Bucket=MINIO_BUCKET)
            print(f"Created bucket: {MINIO_BUCKET}")

async def upload_file(filename: str, data: bytes):
    async with get_client() as s3:
        await s3.put_object(Bucket=MINIO_BUCKET, Key=filename, Body=data, ContentType="application/pdf")
        print(f"Uploaded: {filename}")

async def list_files() -> list:
    async with get_client() as s3:
        response = await s3.list_objects_v2(Bucket=MINIO_BUCKET)
        return [obj["Key"] for obj in response.get("Contents", [])]

async def download_file(filename: str) -> bytes:
    async with get_client() as s3:
        response = await s3.get_object(Bucket=MINIO_BUCKET, Key=filename)
        return await response["Body"].read()
