from fastapi import FastAPI, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from redis.asyncio import Redis
from database import SessionLocal
from crud import (
    create_student, get_student_by_id, update_student, delete_student,
    create_school, get_school_by_id, get_schools, update_school, delete_school,
    create_class, get_class_by_id, get_classes, update_class, delete_class
)
from redis.asyncio import Redis

app = FastAPI()
redis_client = Redis(host="localhost", port=6379, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SchoolModel(BaseModel):
    name: str
    address: Optional[str] = None

class ClassModel(BaseModel):
    name: str
    level: int

class StudentModel(BaseModel):
    name: str
    rollno: int
    age: int
    school_id: int
    class_id: int

@app.get("/")
async def check_redis_connection():
    try:
        ping_response = await redis_client.ping()
        return {"message": f"Connected to Redis: {ping_response}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not connect to Redis: {str(e)}")

@app.post("/schools/")
async def create_new_school(school: SchoolModel, db: Session = Depends(get_db)):
    return create_school(db, name=school.name, address=school.address)

@app.get("/schools/{school_id}")
async def get_school(school_id: int, db: Session = Depends(get_db)):
    school = get_school_by_id(db, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@app.get("/schools/")
async def get_all_schools(db: Session = Depends(get_db)):
    return get_schools(db)

@app.put("/schools/{school_id}")
async def update_existing_school(school_id: int, school: SchoolModel, db: Session = Depends(get_db)):
    return update_school(db, school_id, name=school.name, address=school.address)

@app.delete("/schools/{school_id}")
async def delete_existing_school(school_id: int, db: Session = Depends(get_db)):
    return delete_school(db, school_id)

@app.post("/classes/")
async def create_new_class(class_: ClassModel, db: Session = Depends(get_db)):
    return create_class(db, name=class_.name, level=class_.level)

@app.get("/classes/{class_id}")
async def get_class(class_id: int, db: Session = Depends(get_db)):
    class_ = get_class_by_id(db, class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

@app.get("/classes/")
async def get_all_classes(db: Session = Depends(get_db)):
    return get_classes(db)

@app.put("/classes/{class_id}")
async def update_existing_class(class_id: int, class_: ClassModel, db: Session = Depends(get_db)):
    return update_class(db, class_id, name=class_.name, level=class_.level)

@app.delete("/classes/{class_id}")
async def delete_existing_class(class_id: int, db: Session = Depends(get_db)):
    return delete_class(db, class_id)

@app.post("/create_student/")
async def create_new_student(student: StudentModel, db: Session = Depends(get_db)):
    return create_student(db, name=student.name, rollno=student.rollno, age=student.age, school_id=student.school_id, class_id=student.class_id)

@app.get("/get-student/{student_id}")
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/update_student/{student_id}")
async def update_existing_student(student_id: int, student: StudentModel, db: Session = Depends(get_db)):
    return update_student(db, student_id, name=student.name, rollno=student.rollno, age=student.age, school_id=student.school_id, class_id=student.class_id)

@app.delete("/delete_student/{student_id}")
async def delete_existing_student(student_id: int, db: Session = Depends(get_db)):
    return delete_student(db, student_id)


'''
@app.get("/classes/{class_id}")
async def get_class(class_id: int, db: Session = Depends(get_db)):
    class_ = get_class_by_id(db, class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

# Student routes
@app.post("/create_student/{student_id}")
async def create_new_student(student: Student, student_id: int, db: Session = Depends(get_db)):
    student_key = f"student:{student_id}"
    existing_student = await redis_client.hgetall(student_key)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student already exists in Redis")
    db_student = create_student(
        db, name=student.name, rollno=student.rollno, age=student.age,
        school_id=student.school_id, class_id=student.class_id
    )
    student_dict = {"id": db_student.id, "name": db_student.name, "rollno": db_student.rollno, "age": db_student.age, "school_id":db_student.school_id,"class_id":db_student.class_id}
    await redis_client.hset(student_key, mapping=student_dict)
    return {"message": f"Student {student_id} created successfully in both PostgreSQL and Redis"}

@app.get("/get-student/{student_id}")
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student_key = f"student:{student_id}"
    student = await redis_client.hgetall(student_key)
    if student:
        return {"source": "Redis", "student": student}
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found in PostgreSQL")
    await redis_client.hset(student_key, mapping={"id": db_student.id, "name": db_student.name, "rollno": db_student.rollno, "age": db_student.age, "school_id": db_student.school_id, "class_id": db_student.class_id})
    return {"source": "PostgreSQL", "student": db_student}

@app.put("/update_student/{student_id}")
async def update_existing_student(student: UpdateStudent, student_id: int, db: Session = Depends(get_db)):
    student_key = f"student:{student_id}"
    existing_student = await redis_client.hgetall(student_key)
    if not existing_student and not get_student_by_id(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    db_student = update_student(db, student_id, name=student.name, rollno=student.rollno, age=student.age)
    await redis_client.hset(student_key, mapping=db_student.__dict__)
    return {"message": f"Student {student_id} updated successfully"}

@app.delete("/delete_student/{student_id}")
async def delete_existing_student(student_id: int, db: Session = Depends(get_db)):
    db_student = delete_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    student_key = f"student:{student_id}"
    await redis_client.delete(student_key)
    return {"message": f"Student {student_id} deleted successfully from both PostgreSQL and Redis"}

'''