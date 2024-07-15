#!/usr/bin/python3

class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.gpa = 0.0
        self.total_marks = 0.0


    def calculate_GPA(self):
        if not self.courses_registered:
            return 0.0
        total_grades = sum(course['grade'] for course in self.courses_registered)
        total_credits = sum(course['credits'] for course in self.courses_registered)
        self.gpa = total_grades / total_credits
        return self.gpa


    def register_for_course(self, course_name, trimester, credits, grade):
        self.courses_registered.append({'name': course_name, 'trimester': trimester, 'credits': credits, 'grade': grade})
        self.calculate_GPA()
        self.total_marks += grade


class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits


class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []


    def add_student(self, email, names):
        student = Student(email, names)
        self.student_list.append(student)
        print(f"Student {names} added successfully!")


    def add_course(self, name, trimester, credits):
        course = Course(name, trimester, credits)
        self.course_list.append(course)
        print(f"Course {name} added successfully!")


    def register_student_for_course(self, student_email, course_name, trimester, grade):
        student = next((s for s in self.student_list if s.email == student_email), None)
        course = next((c for c in self.course_list if c.name == course_name and c.trimester == trimester), None)
        if student and course:
            student.register_for_course(course.name, course.trimester, course.credits, grade)
            print("Student registered for the course successfully!")
        else:
            print("Student or course not found!")


    def calculate_GPA(self):
        for student in self.student_list:
            student.calculate_GPA()


    def calculate_ranking(self):
        ranked_students = sorted(self.student_list, key=lambda s: s.gpa, reverse=True)
        for rank, student in enumerate(ranked_students, 1):
            print(f"{rank}. {student.email}: {student.gpa:.2f}")


    def search_by_grade(self, min_grade, max_grade):
        filtered_students = [s for s in self.student_list if min_grade <= s.gpa <= max_grade]
        if filtered_students:
            print(f"Students with GPA between {min_grade} and {max_grade}:")
            for student in filtered_students:
                print(f"{student.names} ({student.email}): {student.gpa:.2f}")
        else:
            print(f"No students found with GPA between {min_grade} and {max_grade}")


    def generate_transcript(self, student_email):
        student = next((s for s in self.student_list if s.email == student_email), None)
        if student:
            print("*" * 60)
            print(" " * 20 + "ALU STUDENT TRANSCRIPT")
            print("*" * 60)
            print(f"Student name:  {student.names}")
            print(f"Student email: {student.email}")
            for course in student.courses_registered:
                print("*" * 60)
                print(f"Trimester:     {course['trimester']}")
                print(f"Course name:   {course['name']}")
                print(f"Total marks:   {course['grade']:.2f}")
                grade = self.grade_from_marks(course['grade'])
                print(f"GPA:           {student.gpa:.2f}")
                print(f"Grade:         {grade}")
                print("*" * 60)
                print(f"{student.names} has successfully completed {course['name']}!")
            print("*" * 60)
        else:
            print("Student not found!")


    def grade_from_marks(self, marks):
        if marks >= 90:
            return 'A'
        elif marks >= 80:
            return 'B'
        elif marks >= 70:
            return 'C'
        elif marks >= 60:
            return 'D'
        else:
            return 'F'


    def display_all_students(self):
        if not self.student_list:
            print("No students registered.")
        else:
            print("List Of Registered Students")
            print()
            print("{:<15} {:<25} {:<12} {:<15} {:<8} {:<12} {:<5} {:<5}".format(
                "Student Name", "Student Email", "Trimester", "Course", "Credits", "Total Marks", "GPA", "Grade"))
            print("=" * 104)
            for student in self.student_list:
                for course in student.courses_registered:
                    grade = self.grade_from_marks(course['grade'])
                    print("{:<15} {:<25} {:<12} {:<15} {:<8} {:<12.2f} {:<5.2f} {:<5}".format(
                        student.names, student.email, course['trimester'], course['name'], course['credits'], course['grade'], student.gpa, grade))


def main():
    gradebook = GradeBook()
    while True:
        print("\n" + "=" * 30)
        print("    Welcome to Grade Book")
        print("=" * 30)
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Calculate Ranking")
        print("5. Search by Grade")
        print("6. Generate Transcript")
        print("7. Display All Students")
        print("8. Exit")
        print("=" * 30)
        choice = input("Enter your choice: ")


        if choice == "1":
            email = input("Enter student email: ")
            names = input("Enter student names: ")
            gradebook.add_student(email, names)
        elif choice == "2":
            name = input("Enter course name: ")
            trimester = input("Enter course trimester: ")
            credits = int(input("Enter course credits: "))
            gradebook.add_course(name, trimester, credits)
        elif choice == "3":
            student_email = input("Enter student email: ")
            course_name = input("Enter course name: ")
            trimester = input("Enter course trimester: ")
            grade = float(input("Enter grade received: "))
            gradebook.register_student_for_course(student_email, course_name, trimester, grade)
        elif choice == "4":
            gradebook.calculate_ranking()
        elif choice == "5":
            min_grade = float(input("Enter minimum GPA: "))
            max_grade = float(input("Enter maximum GPA: "))
            gradebook.search_by_grade(min_grade, max_grade)
        elif choice == "6":
            student_email = input("Enter student email: ")
            gradebook.generate_transcript(student_email)
        elif choice == "7":
            gradebook.display_all_students()
        elif choice == "8":
            print("Thank you for using Grade Book! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()




