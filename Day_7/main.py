import json
import os
from datetime import date

FILE_NAME = "hostel_data.txt"


class Person:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class Student(Person):
    def __init__(self, student_id, name, phone, address):
        super().__init__(name, phone)
        self.student_id = student_id
        self.address = address
        self.room_id = None
        self.check_in_date = None
        self.check_out_date = None
        self.status = "Not Allocated"


class Room:
    def __init__(self, room_id, room_type, capacity, monthly_fee):
        self.room_id = room_id
        self.room_type = room_type
        self.capacity = capacity
        self.monthly_fee = monthly_fee
        self.students = []

    def available_beds(self):
        return self.capacity - len(self.students)

    def is_available(self):
        return self.available_beds() > 0


class HostelManagement:
    def __init__(self):
        self.rooms = {}
        self.students = {}
        self.load_data()

    def save_data(self):
        data = {"rooms": {}, "students": {}}
        for rid, room in self.rooms.items():
            data["rooms"][rid] = {
                "room_type": room.room_type,
                "capacity": room.capacity,
                "monthly_fee": room.monthly_fee,
                "students": room.students
            }
        for sid, student in self.students.items():
            data["students"][sid] = {
                "name": student.name, "phone": student.phone,
                "address": student.address, "room_id": student.room_id,
                "check_in_date": student.check_in_date,
                "check_out_date": student.check_out_date,
                "status": student.status
            }
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        if not os.path.exists(FILE_NAME):
            return
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
            for rid, details in data.get("rooms", {}).items():
                room = Room(rid, details["room_type"], details["capacity"],
                            details["monthly_fee"])
                room.students = details.get("students", [])
                self.rooms[rid] = room
            for sid, details in data.get("students", {}).items():
                student = Student(sid, details["name"], details["phone"],
                                  details["address"])
                student.room_id = details.get("room_id")
                student.check_in_date = details.get("check_in_date")
                student.check_out_date = details.get("check_out_date")
                student.status = details.get("status", "Not Allocated")
                self.students[sid] = student
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print("Could not load hostel data:", error)

    @staticmethod
    def get_number(prompt, number_type=int):
        while True:
            try:
                value = number_type(input(prompt))
                if value < 0:
                    print("Enter a non-negative value.")
                    continue
                return value
            except ValueError:
                print("Enter a valid number.")

    def add_room(self):
        rid = input("Enter room ID: ").strip()
        if not rid or rid in self.rooms:
            print("Room ID cannot be empty or duplicated.")
            return
        types = {"1": ("Single", 1, 8000),
                 "2": ("Double", 2, 6000),
                 "3": ("Triple", 3, 5000)}
        print("1. Single  2. Double  3. Triple")
        choice = input("Select room type: ").strip()
        if choice not in types:
            print("Invalid room type.")
            return
        kind, capacity, default_fee = types[choice]
        fee = self.get_number(f"Monthly fee (0 for default Rs.{default_fee}): ", float)
        if fee == 0:
            fee = default_fee
        self.rooms[rid] = Room(rid, kind, capacity, fee)
        self.save_data()
        print("Room added successfully.")

    def view_rooms(self):
        if not self.rooms:
            print("No rooms available.")
            return
        print(f"{'Room ID':<12}{'Type':<12}{'Capacity':<12}{'Occupied':<12}{'Available':<12}{'Fee':<10}")
        for room in self.rooms.values():
            print(f"{room.room_id:<12}{room.room_type:<12}{room.capacity:<12}"
                  f"{len(room.students):<12}{room.available_beds():<12}{room.monthly_fee:<10.2f}")

    def register_student(self):
        sid = input("Enter student ID: ").strip()
        if not sid or sid in self.students:
            print("Student ID cannot be empty or duplicated.")
            return
        name = input("Enter name: ").strip()
        phone = input("Enter phone: ").strip()
        address = input("Enter address: ").strip()
        if not all((name, phone, address)):
            print("All student details are required.")
            return
        self.students[sid] = Student(sid, name, phone, address)
        self.save_data()
        print("Student registered successfully.")

    def view_students(self):
        if not self.students:
            print("No students registered.")
            return
        for s in self.students.values():
            print("-" * 35)
            print("ID:", s.student_id, "| Name:", s.name, "| Phone:", s.phone)
            print("Address:", s.address, "| Room:", s.room_id or "Not Allocated")
            print("Status:", s.status)

    def check_availability(self):
        found = False
        for room in self.rooms.values():
            if room.is_available():
                found = True
                print(f"Room {room.room_id} ({room.room_type}) - "
                      f"{room.available_beds()} bed(s), Rs.{room.monthly_fee}/month")
        if not found:
            print("No available beds.")

    def allocate_room(self):
        sid = input("Enter student ID: ").strip()
        if sid not in self.students:
            print("Student not found.")
            return
        student = self.students[sid]
        if student.room_id is not None:
            print("Student already has a room.")
            return
        self.check_availability()
        rid = input("Enter room ID: ").strip()
        if rid not in self.rooms:
            print("Room not found.")
            return
        room = self.rooms[rid]
        if not room.is_available():
            print("Room is full.")
            return
        room.students.append(sid)
        student.room_id = rid
        student.status = "Allocated"
        self.save_data()
        print("Room allocated successfully.")

    def cancel_allocation(self):
        sid = input("Enter student ID: ").strip()
        if sid not in self.students:
            print("Student not found.")
            return
        student = self.students[sid]
        if student.room_id is None:
            print("No room allocation found.")
            return
        if student.status == "Checked In":
            print("Check out the student before cancelling allocation.")
            return
        room = self.rooms[student.room_id]
        if sid in room.students:
            room.students.remove(sid)
        student.room_id = None
        student.status = "Not Allocated"
        self.save_data()
        print("Allocation cancelled.")

    def check_in(self):
        sid = input("Enter student ID: ").strip()
        if sid not in self.students:
            print("Student not found.")
            return
        student = self.students[sid]
        if student.room_id is None:
            print("Allocate a room first.")
            return
        if student.status == "Checked In":
            print("Student is already checked in.")
            return
        student.check_in_date = date.today().isoformat()
        student.check_out_date = None
        student.status = "Checked In"
        self.save_data()
        print("Student checked in:", student.check_in_date)

    def check_out(self):
        sid = input("Enter student ID: ").strip()
        if sid not in self.students:
            print("Student not found.")
            return
        student = self.students[sid]
        if student.status != "Checked In" or student.room_id is None:
            print("Student is not currently checked in.")
            return
        room = self.rooms[student.room_id]
        if sid in room.students:
            room.students.remove(sid)
        student.check_out_date = date.today().isoformat()
        student.room_id = None
        student.status = "Checked Out"
        self.save_data()
        print("Student checked out:", student.check_out_date)

    def calculate_charges(self):
        food = self.get_number("Food charges: Rs.", float)
        electricity = self.get_number("Electricity charges: Rs.", float)
        maintenance = self.get_number("Maintenance charges: Rs.", float)
        return food + electricity + maintenance

    def generate_bill(self):
        sid = input("Enter student ID: ").strip()
        if sid not in self.students:
            print("Student not found.")
            return
        student = self.students[sid]
        if student.room_id is None:
            print("Student has no allocated room.")
            return
        months = self.get_number("Number of months: ", int)
        if months == 0:
            print("Months must be at least 1.")
            return
        extra = self.calculate_charges()
        room_fee = self.rooms[student.room_id].monthly_fee * months
        total = room_fee + extra
        print(f"Room fee: Rs.{room_fee:.2f}")
        print(f"Additional charges: Rs.{extra:.2f}")
        print(f"Total: Rs.{total:.2f}")
        paid = self.get_number("Paid amount: Rs.", float)
        if paid > total:
            print("Paid amount cannot exceed total.")
            return
        balance = total - paid
        status = "PAID" if balance == 0 else "PENDING"
        print(f"Paid: Rs.{paid:.2f} | Balance: Rs.{balance:.2f} | {status}")
        bill_name = f"bill_{sid}.txt"
        with open(bill_name, "a", encoding="utf-8") as file:
            file.write("\\nPG HOSTEL BILL\\n")
            file.write(f"Student: {student.name} ({sid})\\n")
            file.write(f"Room: {student.room_id}\\nMonths: {months}\\n")
            file.write(f"Room fee: Rs.{room_fee:.2f}\\nAdditional charges: Rs.{extra:.2f}\\n")
            file.write(f"Total: Rs.{total:.2f}\\nPaid: Rs.{paid:.2f}\\n")
            file.write(f"Balance: Rs.{balance:.2f}\\nPayment status: {status}\\n")
            file.write(f"Date: {date.today().isoformat()}\\n")
            file.write("-" * 35 + "\\n")
        print("Bill saved to", bill_name)

    def hostel_summary(self):
        total_rooms = len(self.rooms)
        capacity = sum(room.capacity for room in self.rooms.values())
        occupied = sum(len(room.students) for room in self.rooms.values())
        allocated = sum(1 for s in self.students.values() if s.room_id is not None)
        checked_in = sum(1 for s in self.students.values() if s.status == "Checked In")
        print("Total rooms:", total_rooms)
        print("Total bed capacity:", capacity)
        print("Occupied beds:", occupied)
        print("Available beds:", capacity - occupied)
        print("Registered students:", len(self.students))
        print("Allocated students:", allocated)
        print("Checked-in students:", checked_in)

    def search_student(self):
        sid = input("Enter student ID: ").strip()
        if sid not in self.students:
            print("Student not found.")
            return
        s = self.students[sid]
        print("ID:", s.student_id, "| Name:", s.name, "| Phone:", s.phone)
        print("Address:", s.address, "| Room:", s.room_id or "Not Allocated")
        print("Status:", s.status)

    def menu(self):
        actions = {
            "1": self.add_room, "2": self.view_rooms,
            "3": self.register_student, "4": self.view_students,
            "5": self.check_availability, "6": self.allocate_room,
            "7": self.cancel_allocation, "8": self.check_in,
            "9": self.check_out, "10": self.generate_bill,
            "11": self.hostel_summary, "12": self.search_student
        }
        while True:
            print("\\n===== PG HOSTEL MANAGEMENT SYSTEM =====")
            print("1 Add Room       2 View Rooms")
            print("3 Register       4 View Students")
            print("5 Availability   6 Allocate Room")
            print("7 Cancel         8 Check-in")
            print("9 Check-out      10 Generate Bill")
            print("11 Hostel Summary 12 Search Student")
            print("13 Exit")
            choice = input("Enter choice: ").strip()
            try:
                if choice == "13":
                    self.save_data()
                    print("Thank you for using the system.")
                    break
                if choice in actions:
                    actions[choice]()
                else:
                    print("Choose a number from 1 to 13.")
            except (ValueError, KeyError, OSError) as error:
                print("Operation could not be completed:", error)


if __name__ == "__main__":
    HostelManagement().menu()
