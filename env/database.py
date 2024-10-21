from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql://StudentManagementdb_owner:zK3UCwneHv7q@ep-purple-surf-a5gp0ujp.us-east-2.aws.neon.tech/StudentManagementdb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)

    students = relationship("Student", back_populates="school")

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    level = Column(Integer, nullable=False)

    students = relationship("Student", back_populates="class_")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rollno = Column(Integer)
    age = Column(Integer)

    school_id = Column(Integer, ForeignKey("schools.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))

    school = relationship("School", back_populates="students")
    class_ = relationship("Class", back_populates="students")
Base.metadata.create_all(bind=engine)