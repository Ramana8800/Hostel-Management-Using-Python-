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


# Day 3: Student Registration
class Hostel:
    def __init__(self):
        self.rooms = {}
        self.students = {}

    def add_room(self):
        room_id = input("Enter room ID: ").strip()
        if not room_id or room_id in self.rooms:
            print("Invalid or duplicate room ID.")
            return
        print("1. Single  2. Double  3. Triple")
        choice = input("Choose room type: ").strip()
        room_types = {"1": ("Single", 1, 8000),
                      "2": ("Double", 2, 6000),
                      "3": ("Triple", 3, 5000)}
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
            print(room.room_id, room.room_type, "Capacity:", room.capacity,
                  "Available:", room.available_beds(), "Monthly fee:", room.monthly_fee)

    def register_student(self):
        student_id = input("Enter student ID: ").strip()
        if not student_id or student_id in self.students:
            print("Invalid or duplicate student ID.")
            return
        name = input("Enter name: ").strip()
        phone = input("Enter phone: ").strip()
        address = input("Enter address: ").strip()
        if not name or not phone or not address:
            print("All fields are required.")
            return
        self.students[student_id] = Student(student_id, name, phone, address)
        print("Student registered successfully.")

    def view_students(self):
        if not self.students:
            print("No students registered.")
            return
        for student in self.students.values():
            print(student.student_id, student.name, student.phone, student.address)

if __name__ == "__main__":
    hostel = Hostel()
    while True:
        print("\\n1. Add room  2. View rooms  3. Register student  4. View students  5. Exit")
        choice = input("Choose: ").strip()
        if choice == "1": hostel.add_room()
        elif choice == "2": hostel.view_rooms()
        elif choice == "3": hostel.register_student()
        elif choice == "4": hostel.view_students()
        elif choice == "5": break
        else: print("Invalid choice.")


# Day 4: Room availability, allocation and cancellation
class Hostel:
    def __init__(self):
        self.rooms = {}
        self.students = {}

    def add_room(self):
        room_id = input("Enter room ID: ").strip()
        if not room_id or room_id in self.rooms:
            print("Invalid or duplicate room ID."); return
        print("1. Single  2. Double  3. Triple")
        choice = input("Choose room type: ").strip()
        types = {"1": ("Single", 1, 8000), "2": ("Double", 2, 6000),
                 "3": ("Triple", 3, 5000)}
        if choice not in types:
            print("Invalid room type."); return
        kind, capacity, fee = types[choice]
        self.rooms[room_id] = Room(room_id, kind, capacity, fee)
        print("Room added.")

    def view_rooms(self):
        for room in self.rooms.values():
            print(room.room_id, room.room_type, "Occupied:", len(room.students),
                  "Available:", room.available_beds(), "Fee:", room.monthly_fee)

    def register_student(self):
        sid = input("Student ID: ").strip()
        if not sid or sid in self.students:
            print("Invalid or duplicate student ID."); return
        name = input("Name: ").strip()
        phone = input("Phone: ").strip()
        address = input("Address: ").strip()
        if not all([name, phone, address]):
            print("All fields are required."); return
        self.students[sid] = Student(sid, name, phone, address)
        print("Student registered.")

    def view_students(self):
        for s in self.students.values():
            print(s.student_id, s.name, s.phone, s.address,
                  "Room:", s.room_id if hasattr(s, "room_id") else "Not allocated")

    def check_availability(self):
        found = False
        for room in self.rooms.values():
            if room.available_beds() > 0:
                found = True
                print(room.room_id, room.room_type, "Available beds:", room.available_beds())
        if not found: print("No available beds.")

    def allocate_room(self):
        sid = input("Student ID: ").strip()
        if sid not in self.students:
            print("Student not found."); return
        student = self.students[sid]
        if getattr(student, "room_id", None):
            print("Student already has a room."); return
        self.check_availability()
        rid = input("Room ID: ").strip()
        if rid not in self.rooms:
            print("Room not found."); return
        room = self.rooms[rid]
        if room.available_beds() <= 0:
            print("Room is full."); return
        room.students.append(sid)
        student.room_id = rid
        student.status = "Allocated"
        print("Room allocated.")

    def cancel_allocation(self):
        sid = input("Student ID: ").strip()
        if sid not in self.students:
            print("Student not found."); return
        student = self.students[sid]
        rid = getattr(student, "room_id", None)
        if not rid:
            print("No allocation found."); return
        self.rooms[rid].students.remove(sid)
        student.room_id = None
        student.status = "Not Allocated"
        print("Allocation cancelled.")

if __name__ == "__main__":
    hostel = Hostel()
    while True:
        print("\\n1 Add room 2 View rooms 3 Register student 4 View students")
        print("5 Availability 6 Allocate 7 Cancel allocation 8 Exit")
        c = input("Choose: ").strip()
        if c == "1": hostel.add_room()
        elif c == "2": hostel.view_rooms()
        elif c == "3": hostel.register_student()
        elif c == "4": hostel.view_students()
        elif c == "5": hostel.check_availability()
        elif c == "6": hostel.allocate_room()
        elif c == "7": hostel.cancel_allocation()
        elif c == "8": break
        else: print("Invalid choice.")


# Day 5: Student check-in and check-out
from datetime import date

class Hostel:
    def __init__(self):
        self.rooms = {}
        self.students = {}

    def add_room(self):
        rid = input("Room ID: ").strip()
        if not rid or rid in self.rooms: print("Invalid/duplicate room."); return
        print("1 Single 2 Double 3 Triple")
        types = {"1": ("Single", 1, 8000), "2": ("Double", 2, 6000),
                 "3": ("Triple", 3, 5000)}
        choice = input("Room type: ").strip()
        if choice not in types: print("Invalid type."); return
        kind, cap, fee = types[choice]
        self.rooms[rid] = Room(rid, kind, cap, fee)
        print("Room added.")

    def view_rooms(self):
        for r in self.rooms.values():
            print(r.room_id, r.room_type, "Available:", r.available_beds(), "Fee:", r.monthly_fee)

    def register_student(self):
        sid = input("Student ID: ").strip()
        if not sid or sid in self.students: print("Invalid/duplicate ID."); return
        name, phone, address = input("Name: ").strip(), input("Phone: ").strip(), input("Address: ").strip()
        if not all([name, phone, address]): print("All fields required."); return
        s = Student(sid, name, phone, address)
        s.room_id, s.status, s.check_in_date, s.check_out_date = None, "Not Allocated", None, None
        self.students[sid] = s
        print("Student registered.")

    def view_students(self):
        for s in self.students.values():
            print(s.student_id, s.name, s.phone, s.address,
                  "Room:", s.room_id or "Not Allocated", "Status:", s.status)

    def check_availability(self):
        available = [r for r in self.rooms.values() if r.available_beds() > 0]
        if not available: print("No available beds.")
        for r in available: print(r.room_id, r.room_type, "Beds:", r.available_beds())

    def allocate_room(self):
        sid = input("Student ID: ").strip()
        if sid not in self.students: print("Student not found."); return
        s = self.students[sid]
        if s.room_id: print("Student already allocated."); return
        self.check_availability()
        rid = input("Room ID: ").strip()
        if rid not in self.rooms: print("Room not found."); return
        r = self.rooms[rid]
        if r.available_beds() <= 0: print("Room full."); return
        r.students.append(sid); s.room_id = rid; s.status = "Allocated"
        print("Room allocated.")

    def cancel_allocation(self):
        sid = input("Student ID: ").strip()
        if sid not in self.students: print("Student not found."); return
        s = self.students[sid]
        if not s.room_id: print("No allocation."); return
        if s.status == "Checked In": print("Check out before cancelling."); return
        self.rooms[s.room_id].students.remove(sid)
        s.room_id, s.status = None, "Not Allocated"
        print("Allocation cancelled.")

    def check_in(self):
        sid = input("Student ID: ").strip()
        if sid not in self.students: print("Student not found."); return
        s = self.students[sid]
        if not s.room_id: print("Allocate a room first."); return
        if s.status == "Checked In": print("Already checked in."); return
        s.check_in_date = date.today().isoformat()
        s.check_out_date = None
        s.status = "Checked In"
        print("Checked in on", s.check_in_date)

    def check_out(self):
        sid = input("Student ID: ").strip()
        if sid not in self.students: print("Student not found."); return
        s = self.students[sid]
        if s.status != "Checked In": print("Student is not checked in."); return
        rid = s.room_id
        self.rooms[rid].students.remove(sid)
        s.check_out_date = date.today().isoformat()
        s.room_id = None
        s.status = "Checked Out"
        print("Checked out on", s.check_out_date)

if __name__ == "__main__":
    hostel = Hostel()
    while True:
        print("\\n1 Add room 2 View rooms 3 Register student 4 View students")
        print("5 Availability 6 Allocate 7 Cancel 8 Check-in 9 Check-out 10 Exit")
        c = input("Choose: ").strip()
        actions = {"1": hostel.add_room, "2": hostel.view_rooms, "3": hostel.register_student,
                   "4": hostel.view_students, "5": hostel.check_availability,
                   "6": hostel.allocate_room, "7": hostel.cancel_allocation,
                   "8": hostel.check_in, "9": hostel.check_out}
        if c == "10": break
        elif c in actions: actions[c]()
        else: print("Invalid choice.")
