from sqlalchemy.orm import Session
from database import School, Class, Student

def create_school(db: Session, name: str, address: str):
    new_school = School(name=name, address=address)
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school

def get_school_by_id(db: Session, school_id: int):
    return db.query(School).filter(School.id == school_id).first()

def get_schools(db: Session):
    return db.query(School).all()

def update_school(db: Session, school_id: int, name: str = None, address: str = None):
    school = get_school_by_id(db, school_id)
    if not school:
        return None
    if name is not None:
        school.name = name
    if address is not None:
        school.address = address
    db.commit()
    db.refresh(school)
    return school

def delete_school(db: Session, school_id: int):
    school = get_school_by_id(db, school_id)
    if school:
        db.delete(school)
        db.commit()
        return school
    return None


# CRUD Operations for Class
def create_class(db: Session, name: str, level: int):
    new_class = Class(name=name, level=level)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

def get_class_by_id(db: Session, class_id: int):
    return db.query(Class).filter(Class.id == class_id).first()

def get_classes(db: Session):
    return db.query(Class).all()

def update_class(db: Session, class_id: int, name: str = None, level: int = None):
    class_ = get_class_by_id(db, class_id)
    if not class_:
        return None
    if name is not None:
        class_.name = name
    if level is not None:
        class_.level = level
    db.commit()
    db.refresh(class_)
    return class_

def delete_class(db: Session, class_id: int):
    class_ = get_class_by_id(db, class_id)
    if class_:
        db.delete(class_)
        db.commit()
        return class_
    return None

# CRUD Operations for Student (with School and Class)
def create_student(db: Session, name: str, rollno: int, age: int, school_id: int, class_id: int):
    new_student = Student(name=name, rollno=rollno, age=age, school_id=school_id, class_id=class_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session):
    return db.query(Student).all()

def update_student(db: Session, student_id: int, name: str = None, rollno: int = None, age: int = None, school_id: int = None, class_id: int = None):
    student = get_student_by_id(db, student_id)
    if not student:
        return None
    if name is not None:
        student.name = name
    if rollno is not None:
        student.rollno = rollno
    if age is not None:
        student.age = age
    if school_id is not None:
        student.school_id = school_id
    if class_id is not None:
        student.class_id = class_id
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if student:
        db.delete(student)
        db.commit()
        return student
    return None
