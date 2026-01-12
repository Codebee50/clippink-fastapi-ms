from app.config import settings
import aiohttp


async def download_file_remote_to_local(remote_url: str, local_path: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(remote_url) as response:
            response.raise_for_status()
        
            with open(local_path, "wb") as f:
                f.write(await response.read())
    return local_path

def get_url_from_s3_key(s3_key: str) -> str:
    return f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"