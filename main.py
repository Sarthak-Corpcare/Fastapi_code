from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from redis import Redis

from . import crud, models, Schemas
from .database import get_db, get_redis, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.post("/documents/", response_model=Schemas.DocumentResponse)
async def create_document(document: Schemas.DocumentCreate, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    return await crud.create_document(db=db, redis=redis, document=document)

@app.get("/documents/search/")
async def search_documents(query: str, redis: Redis = Depends(get_redis)):
    results = await crud.search_documents(redis, query)
    if not results:
        raise HTTPException(status_code=404, detail="No documents found")
    return results

@app.on_event("startup")
async def on_startup():
    redis = Redis(host='localhost', port=6379, decode_responses=True)
    await crud.create_redis_index(redis)
    await redis.close()


'''
@app.post("/documents")
async def create_document(doc:DocumentCreate):
    document=store_document(redis_client, doc.title,doc.content)
    return {"message ": "Document Stored", "docuemnt":document}
'''