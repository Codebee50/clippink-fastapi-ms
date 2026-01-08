from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "scene" ADD "mood" VARCHAR(20);
        ALTER TABLE "scene" ADD "narration" TEXT;
        ALTER TABLE "scene" ADD "visual_prompt" TEXT;
        ALTER TABLE "scene" ADD "duration_seconds" INT NOT NULL DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "scene" DROP COLUMN "mood";
        ALTER TABLE "scene" DROP COLUMN "narration";
        ALTER TABLE "scene" DROP COLUMN "visual_prompt";
        ALTER TABLE "scene" DROP COLUMN "duration_seconds";"""


MODELS_STATE = (
    "eJztmG1PIjEQx78K2Vde4hlEUHO5XIKAJ6fCRdAzGrMp2wKNu+3a7arE8N2v7T4vXU7wCX"
    "K+UZjpsDO/Ttv/9slwKES2t9WzEEHGt9KTQYAjP2QdmyUDuG5ilgYOBrYa6cVDBh5nwOLC"
    "OAS2h4QJIs9i2OWYEmElvm1LI7XEQExGickn+M5HJqcjxMeICcf1jTBjAtEj8qKv7q05xM"
    "iGmUQxlM9WdpNPXGU7P283D9VI+biBaVHbd0gy2p3wMSXxcN/HcEvGSN9IVMMARzBVhswy"
    "LDcyBRkLA2c+ilOFiQGiIfBtCcP4PvSJJRmU1JPkn+oPYwE8FiUSLSZcsniaBlUlNSurIR"
    "/VOKqfbezsflFVUo+PmHIqIsZUBQIOglDFNQFJGUTMJL4zEBMwg7RNuJ5oPizHVuS8DNXI"
    "kGBNWiriWl6eoMhH/Pta2a7uVfd3dqv7YohKJLbszYHc7vQVy9RqQRCDoOYZco0xYHp02a"
    "gcOJHuW4EzsANG6AUNaDjg0bQRGfGxZFaew+qifqZ6slJWPUnFBhFsG53QU1GuLE4CmKhZ"
    "JjVDs48eCxoxE7QUzHDlLsQyYvbqK7nfuuzLnB3Pu7PTwDZO65eKpTMJPSfdzs9oeApw46"
    "R7kAML/QCR6SGRCfQWWOe60P9yrd9jzwe26TLquHyRBp0J/GxSbZM6lGrO9DnbaDh+TXC+"
    "9eZ5jyGi5mKyKB3zmuLoQ5vzH1pIKsrhrVYKKRyz/A4pQ3hEjtFEUWyLRACxdId3qJ4vot"
    "9ZWW6JNVkLDDzEOjvTGaJAURbiwXqs9xr1ZstQHAfAun0ADJoZoNJDKzRnicfOupyKk7cA"
    "IqQKDMuQSWfQat5YYubFbyzx9H6+saz1G0uQyiJHcBLxfmp7vQ5fsaVxX6MLi4/fJOId32"
    "BcRKDEtrrHsMWQLNoEmgZtCg/HDtIDzUbmoMIwdCv6sJpta4gaYJfYk3B7mdfG7dNWr18/"
    "/Z3p5Wa935KeSqaPI+vGbm4m4h8p/Wn3j0rya+mq22nld5V4XP/KkDkBn1OT0AcTwNROGF"
    "kjMJmJ9V245MRmIz8n9kMnViU/owGLxUz62BGzotkiD8K4w+MzZBfdROTvVVdvhouU4fQt"
    "5VwdMWyNdXou9MwVdCAZszKKrvAiRSvoNFcnYcu+TMm9cLG/ytVJsYC7R8zT3vIVq41UyL"
    "pIuJzSqNWeIzVqtWKtIX1ZsSGXxgIQw+HrCXC7/BytJkYVAlS+nFqjhCOiOdF/9bqdApmW"
    "hORAnhNR4DXEFt8s2djjN6uJdQ5FWfX8V4v8W0TuOJY/cKC7ZHnP24LpX/7fQhg="
)
