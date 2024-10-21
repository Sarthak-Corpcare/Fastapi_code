from redis import Redis
import uuid
from sqlalchemy.orm import Session
from TextSearchApp.models import Document
from typing import List
from .Schemas import DocumentCreate


async def create_redis_index(redis: Redis):
    await redis.execute_command(
        'FT.CREATE', 'doc_index',
        'SCHEMA', 'title', 'TEXT', 'content', 'TEXT'
    )

async def create_document(db: Session, redis: Redis, document: DocumentCreate):
    # Insert document into PostgreSQL
    db_doc = Document(title=document.title, content=document.content)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
# Inserted document into Redis with full-text search
    doc_id = f'doc:{db_doc.id}'
    await redis.hset(doc_id, mapping={
        'title': document.title,
        'content': document.content
    })
    return db_doc

async def search_documents(redis: Redis, query: str):
    search_result = await redis.execute_command('FT.SEARCH', 'doc_index', query)
    return [search_result[i] for i in range(1, len(search_result), 2)]


'''
def store_document(redis_client:Redis, title:str, content:str):
    doc_id-str(uuid.uuid4())
    document=Document(doc_id=doc_id,title=title,content=content)
    redis_client.hset(f"doc:{doc_id}", mapping={"title": title, "content": content})
    redis_client.sadd("doc_index",f"{title} {content}")
    return document

def search_document(redis_client:Redis, query:str)->List[Document]:
    matching_docs=[]
    all_docs=redis_client.smembers("doc_index")
    for doc in all_docs:
        doc= await redis.hgetall(f"doc:{doc_id}")
        if query.lower() in doc.lower():
            matching_docs.append(doc)
    return matching_docs
'''