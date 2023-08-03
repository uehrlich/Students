from __future__ import annotations
import typing 
import strawberry
import datetime
from grades.models import Test
from grades.models import Student
import uuid



@strawberry.type(name ="Student")
class StudentGQL:
     id : strawberry.ID
     name :str
     birthDate : datetime.datetime
     test : list["TestGQL"]

     @classmethod
     def from_orm(cls, student: Student) -> StudentGQL:
        return cls(
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
    @strawberry.mutation
    def add_student(self,name:str,birth: datetime.date)->StudentGQL:
        stud = Student(name = name, birth_date = birth )
        stud.save(force_insert= True)
        # stu =Student.objects.create(name =name , birth_date = birth)
        return StudentGQL.from_orm(stud)

    @strawberry.mutation
    def submitTestResults(self, studentID :int, subject:str, grade:int )->StudentGQL:
        stu = Student.objects.get(id = studentID)
        t =Test.objects.filter( subject = subject).filter(student = stu).update(grade = grade)
        return StudentGQL.from_orm(stu)
    

schema = strawberry.Schema(query=Query, mutation=Mutation)
