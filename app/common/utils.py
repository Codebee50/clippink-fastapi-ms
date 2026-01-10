from app.config import settings

def get_url_from_s3_key(s3_key: str) -> str:
    return f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"