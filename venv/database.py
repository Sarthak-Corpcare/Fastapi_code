from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redis import Redis

DATABASE_URL = "postgresql://StudentManagementdb_owner:zK3UCwneHv7q@ep-raspy-credit-a5z65s7i.us-east-2.aws.neon.tech/StudentManagementdb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
redis = Redis(host='localhost', port=6379, decode_responses=True)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def get_redis():
    try:
        yield redis
    finally:
        await redis.close()
