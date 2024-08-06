#!/usr/bin/python3

import pickle

class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.total_marks = 0.0
        self.GPA = 0.0

    def calculate_marks_and_grade(self):
        if not self.courses_registered:
            self.total_marks = 0.0
            self.GPA = 0.0
        else:
            total_points = sum(course.credits * marks for course, marks in self.courses_registered)
            total_credits = sum(course.credits for course, marks in self.courses_registered)
            self.total_marks = total_points / total_credits if total_credits > 0 else 0.0
            self.GPA = self.calculate_gpa_from_marks(self.total_marks)

    def calculate_gpa_from_marks(self, marks):
        if marks >= 80:
            return 4.0  # A
        elif marks >= 70:
            return 3.0  # B
        elif marks >= 60:
            return 2.0  # C
        elif marks >= 40:
            return 1.0  # D
        elif marks >= 30:
            return 0.5  # E
        else:
            return 0.0  # F

    def register_for_course(self, course, marks):
        self.courses_registered.append((course, marks))
        self.calculate_marks_and_grade()

class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits

class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []

    def add_student(self, student):
        self.student_list.append(student)

    def add_course(self, course):
        self.course_list.append(course)

    def register_student_for_course(self, student_email, course_name, marks):
        student = next((s for s in self.student_list if s.email == student_email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        if student and course:
            student.register_for_course(course, marks)
            print("The student has been registered successfully.")
        else:
            print("Student or Course not found")

    def remove_student_from_course(self, student_email, course_name):
        student = next((s for s in self.student_list if s.email == student_email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        if student and course:
            student.courses_registered = [(c, m) for c, m in student.courses_registered if c != course]
            student.calculate_marks_and_grade()
            print(f"The student has been removed from the course '{course_name}' successfully.")
        else:
            print("Student or Course not found")

    def calculate_ranking(self):
        return sorted(self.student_list, key=lambda s: s.total_marks, reverse=True)

    def search_by_grade(self, grade):
        return [student for student in self.student_list if any(self.grade_from_marks(course_grade) == grade for course, course_grade in student.courses_registered)]

    def generate_transcript(self, student_email):
        student = next((s for s in self.student_list if s.email == student_email), None)
        if student:
            print("............................................................")
            print("                    ALU STUDENT TRANSCRIPT")
            print("............................................................")
            print(f"Student name: {'.' * (25 - len('Student name: ' + student.names))} {student.names}")
            print(f"Student email: {'.' * (25 - len('Student email: ' + student.email))} {student.email}")
            print("............................................................")
            for course, marks in student.courses_registered:
                print(f"Trimester: {'.' * (25 - len('Trimester: ' + course.trimester))} {course.trimester}")
                print(f"Course name: {'.' * (25 - len('Course name: ' + course.name))} {course.name}")
                print(f"Total marks: {'.' * (25 - len('Total marks: ' + format(student.total_marks, '.2f')))} {student.total_marks:.2f}")
                print(f"GPA: {'.' * (25 - len('GPA: ' + format(student.GPA, '.2f')))} {student.GPA:.2f}")
                grade = self.grade_from_marks(marks)
                print(f"Grade: {'.' * (25 - len('Grade: ' + grade))} {grade}")
                print("............................................................")
                print(f"{student.names} has successfully completed {course.name} Course!")
                print("............................................................")
        else:
            print("Student not found")

    def grade_from_marks(self, marks):
        if marks >= 80:
            return 'A'
        elif marks >= 70:
            return 'B'
        elif marks >= 60:
            return 'C'
        elif marks >= 40:
            return 'D'
        elif marks >= 30:
            return 'E'
        else:
            return 'F'

    def display_all_students(self):
        if not self.student_list:
            print("No students registered.")
        else:
            print("List Of Registered Students")
            print()
            print("{:<20} {:<30} {:<12} {:<15} {:<10} {:<12} {:<10} {:<6}".format(
                "Student Name", "Student Email", "Trimester", "Course", "Credits", "Total Marks", "GPA", "Grade"))
            print("=" * 121)
            for student in self.student_list:
                for course, marks in student.courses_registered:
                    grade = self.grade_from_marks(marks)
                    print("{:<20} {:<30} {:<12} {:<15} {:<10} {:<12.2f} {:<10.2f} {:<6}".format(
                        student.names, student.email, course.trimester, course.name, course.credits, student.total_marks, student.GPA, grade))

    def save_data(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.student_list, self.course_list), file)
        print("Data saved successfully.")

    def load_data(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.student_list, self.course_list = pickle.load(file)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")
        except Exception as e:
            print(f"An error occurred while loading data: {e}")

def main():
    gradebook = GradeBook()
    gradebook.load_data('gradebook_data.pkl')

    while True:
        print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("    Welcome to Yunis App    ")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Remove Student from Course")  # New option
        print("5. Calculate Ranking")
        print("6. Search by Grade")
        print("7. Generate Transcript")
        print("8. Display All Students")
        print("9. Save Data")
        print("10. Exit")  # Updated choice number
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        choice = input("Enter your choice: ")

        if choice == '1':
            email = input("Enter student's email: ")
            names = input("Enter student's name: ")
            student = Student(email, names)
            gradebook.add_student(student)
            print("The student has been added successfully.")
        elif choice == '2':
            name = input("Enter course name: ")
            trimester = input("Enter trimester: ")
            credits = float(input("Enter credits: "))
            course = Course(name, trimester, credits)
            gradebook.add_course(course)
            print("The course has been added successfully.")
        elif choice == '3':
            student_email = input("Enter student's email: ")
            course_name = input("Enter course name: ")
            marks = float(input("Enter marks: "))
            gradebook.register_student_for_course(student_email, course_name, marks)
        elif choice == '4':
            student_email = input("Enter student's email: ")
            course_name = input("Enter course name: ")
            gradebook.remove_student_from_course(student_email, course_name)  # New option
        elif choice == '5':
            ranking = gradebook.calculate_ranking()
            print("Student Rankings by Total Marks:")
            for student in ranking:
                print(f"{student.names} - Total Marks: {student.total_marks}, GPA: {student.GPA}")
        elif choice == '6':
            grade = input("Enter grade to search for: ")
            students = gradebook.search_by_grade(grade)
            print("Students with the specified grade:")
            for student in students:
                print(f"{student.names} - Email: {student.email}")
        elif choice == '7':
            student_email = input("Enter student's email: ")
            gradebook.generate_transcript(student_email)
        elif choice == '8':
            gradebook.display_all_students()
        elif choice == '9':
            gradebook.save_data('gradebook_data.pkl')
        elif choice == '10':  # Updated choice number
            print("Thank you for using Yunis's Grade Book App.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
