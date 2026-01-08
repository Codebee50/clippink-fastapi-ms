from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "video" (
    "id" UUID NOT NULL PRIMARY KEY,
    "script" TEXT NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'pending',
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "scene" (
    "id" UUID NOT NULL PRIMARY KEY,
    "order_number" INT NOT NULL DEFAULT 0,
    "media_type" VARCHAR(20) NOT NULL DEFAULT 'image',
    "video_id" UUID NOT NULL REFERENCES "video" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmOtP4kAQwP8V0k9e4hlE8MzlckkFPDkVLlI9ozHN0h1gY7tb261KDP/77S590xLwwW"
    "HiFx7zaGd+O7sz7bPmMAy2v9O3gIL2vfKsUeTIH1nFdkVDrpuIpYCjga0s/dhk4HMPWVwI"
    "h8j2QYgw+JZHXE4YFVIa2LYUMksYEjpKRAEl9wGYnI2Aj8ETiptbISYUwxP40V/3zhwSsH"
    "EmUILlvZXc5BNXyS4uOq0jZSlvNzAtZgcOTazdCR8zGpsHAcE70kfqRiIbD3HAqTRklGG6"
    "kWgWsRBwL4A4VJwIMAxRYEsY2o9hQC3JoKLuJD/qP7UV8FiMSrSEcsnieTrLKslZSTV5q+"
    "axfr61t/9FZcl8PvKUUhHRpsoRcTRzVVwTkMzD4Jk0cAZiAeaQdigvJpp3y7EVMb+EaiRI"
    "sCYlFXGtvpygiEd8fa3t1r/VD/b26wfCRAUSS74tgNzpGoplarcAJmiW8xy55hh5xeiyXj"
    "lwItz3AqcRB43gFQWoOejJtIGO+Fgyqy5gdamfq5qsVVVNMnFAzI6NbqipKVUW5wPBwMzV"
    "dnba5y339zJAI3Dr3s7yUBzeFe5mhWOe3xHzgIzoCUwUxY4IBFGrqP7CBnAZXWdjuSXS5P"
    "D10GPcKjKVIRIUaQGf7Uy939RbbU1xHCDr7hF52MwAlRpWYzlJbDuvcmpOXoKo2G04TEMG"
    "nUFb0HRj5uVNN17ez6b7oZvuLJR5mAY8lfTbxGN9DePdzjejfWXIoB3fv7fTXWHrTL9SPJ"
    "1JqDntdX9F5qku0jztHea6hzjSeOCv0ogTjzU2YRcoltg2tw1bHsikTVRQoC2h4cSBYqBZ"
    "zxxUHLruRD82s2w1kQPuUXsSHi+Lyrhz1u4b+tmfTC23dKMtNbVMHUfSrf3cSsQXqfztGM"
    "cV+bdy3eu286dKbGdcazImFHBmUvZoIpw6CSNpBCazsIGLX7iwWc/Phf2vC6uCn5sBy4eZ"
    "dNsRq1JwRB6Gfkcn52AjBbZ0MoxfDWzeCpdNhtP3HOd08Ig1LprnQs3CgQ4lNhsz0ZU+8x"
    "cOdAVP+mHJvm6Se+Vmf5Mn/fIB7gE8P9wmy04bKZePMsLlJo1GY5lRo9EonzWkLjtsyK2x"
    "AsTQ/GMC3K0uM6sJq1KASpeb1hjlQAs6+u9+r1sypiUuOZAXVCR4g4nFtys28fntZmJdQF"
    "FmvfjRIv8UkWvH8gKHRS9Z1vm2YPoPnnmWXA=="
)
