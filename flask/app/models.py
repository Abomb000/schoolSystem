from mongoengine import Document, StringField, ListField, IntField


class Student(Document):
    firstName = StringField()
    lastName = StringField(unique_with='firstName')
    email = StringField()


class Course(Document):
    name = StringField(unique_with='students')
    students = ListField(unique_with='name')


class Grade(Document):
    grade = IntField()
    student = StringField(unique_with='course')
    course = StringField(unique_with='student')
