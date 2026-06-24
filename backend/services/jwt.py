import jwt
from dotenv import load_dotenv
import os
load_dotenv()

secret_key = os.getenv("JWT_SECRET_KEY", "default_secret_key")


def create_jwt_token(data: dict) -> str:
    try:
        return jwt.encode(data, secret_key, algorithm="HS256")
    except Exception as e:
        raise ValueError(f"Error creating JWT token: {e}")


def verify_jwt_token(token: str) -> dict | None:
    try:
        user = jwt.decode_complete(token, secret_key, algorithms=["HS256"])
        if user is None:
            raise ValueError("Invalid JWT token.")
        return user
    except jwt.ExpiredSignatureError:
        raise ValueError("JWT token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid JWT token.")
