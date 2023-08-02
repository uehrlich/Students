from __future__ import annotations
import typing 
import strawberry
import datetime
from grades.models import Test
from grades.models import Student



@strawberry.type(name ="Student")
class StudentGQL:
     id : strawberry.ID
     name :str
     birthDate : datetime.date
     test : list["TestGQL"]

     @classmethod
     def from_orm(cls, student: Student) -> StudentGQL:
        return StudentGQL(
            id= student.id,
            name= student.name,
            birthDate= student.birth_date,
            test=[TestGQL.from_orm(t) for t in student.test_set.all()]
        )

@strawberry.type(name="Test")
class TestGQL:
    subject: str
    grade : int

    @classmethod
    def from_orm(cls, tst: Test) -> TestGQL:
        return TestGQL(
            subject = tst.subject,
            grade = tst.grade )

@strawberry.type
class Query:
    @strawberry.field
    def students(root) -> list[StudentGQL]:
        students_list = []
        students = Student.objects.all()    
        for student in students:    
            students_list.append(StudentGQL.from_orm(student))
        return students_list
    # @strawberry.field
    # def tests(root) -> list["Test"]:
    #     test_list = []
    #     tests = Test.objects.all()    
    #     for test in tests:    
    #         test_list.append(TestGQL.from_orm(
    #             TestGQL,test))
    #     return test_list

@strawberry.type
class Mutation:
    @strawberry.field
    def add_student(self,name:str,birth: datetime.date)->Student:
        return Student(name= name , birthDate= birth)
    @strawberry.field
    def submitTestResults(self, studentID :id, subject:str, grade:int )->Student:
        return Student(id = studentID , test= TestGQL(subject=subject, grade= grade))
    

schema = strawberry.Schema(query=Query)
