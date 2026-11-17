# Day 1: Classes and Objects
class Person:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

class Student(Person):
    def __init__(self, student_id, name, phone, address):
        super().__init__(name, phone)
        self.student_id = student_id
        self.address = address

class Room:
    def __init__(self, room_id, room_type, capacity, monthly_fee):
        self.room_id = room_id
        self.room_type = room_type
        self.capacity = capacity
        self.monthly_fee = monthly_fee
        self.students = []

    def available_beds(self):
        return self.capacity - len(self.students)

room = Room("101", "Single", 1, 6000)
student = Student("S101", "Ramana", "9876543210", "Anakapalli")

print("PG Hostel Management System - Day 1")
print("Room:", room.room_id, room.room_type)
print("Available beds:", room.available_beds())
print("Student:", student.name)
