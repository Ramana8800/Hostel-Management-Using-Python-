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


# Day 2: Room Management using a dictionary
class Hostel:
    def __init__(self):
        self.rooms = {}

    def add_room(self):
        room_id = input("Enter room ID: ").strip()
        if not room_id or room_id in self.rooms:
            print("Invalid or duplicate room ID.")
            return

        print("1. Single  2. Double  3. Triple")
        choice = input("Choose room type: ").strip()
        room_types = {
            "1": ("Single", 1, 8000),
            "2": ("Double", 2, 6000),
            "3": ("Triple", 3, 5000)
        }
        if choice not in room_types:
            print("Invalid room type.")
            return

        room_type, capacity, fee = room_types[choice]
        self.rooms[room_id] = Room(room_id, room_type, capacity, fee)
        print("Room added successfully.")

    def view_rooms(self):
        if not self.rooms:
            print("No rooms added.")
            return
        for room in self.rooms.values():
            print(room.room_id, room.room_type,
                  "Capacity:", room.capacity,
                  "Available:", room.available_beds(),
                  "Monthly fee:", room.monthly_fee)

if __name__ == "__main__":
    hostel = Hostel()
    hostel.add_room()
    hostel.view_rooms()
