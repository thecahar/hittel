COMMANDS = ("quit", "show", "retrieve", "add")

students = [
    {
        "name": "John Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 y.o. Hobbies: music",
    },
    {
        "name": "Marry Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "John is 23 y.o. Hobbies: football",
    },
]


def find_student(name: str) -> dict | None:
    for student in students:
        if student["name"] == name:
            return student

    return None


def show_students() -> None:
    print("=" * 20)
    print("The list of students:\n")
    for student in students:
        print(f"{student['name']}. Marks: {student['marks']}")

    print("=" * 20)


def show_student(name: str) -> None:
    student: dict | None = find_student(name)

    if not student:
        print(f"There is no student {name}")
        return

    print("Detailed about student:\n")
    print(
        f"{student['name']}. Marks: {student['marks']}\n"
        f"Details: {student['info']}\n"
    )


def add_student(student_name: str):
    instance = {"name": student_name, "marks": [], "info": None}
    students.append(instance)

    return instance


def main():
    print(f"Welcome to the Digital journal!\nAvailable commands: {COMMANDS}")
    while True:
        user_input = input("Enter the command: ")

        if user_input not in COMMANDS:
            print(f"Command {user_input} is not available.\n")
            continue

        if user_input == "quit":
            print("See you next time.")
            break

        try:
            if user_input == "show":
                show_students()
            elif user_input == "retrieve":
                student_name = input("Enter student name you are looking for: ")
                show_student(student_name)
            elif user_input == "add":
                name = input("Enter student's name: ")
                add_student(name)
        except NotImplementedError as error:
            print(f"Feature '{error}' is not ready for live.")
        except Exception as error:
            print(error)


main()