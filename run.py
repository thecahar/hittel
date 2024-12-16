import json
from pathlib import Path

files_dir = Path(__name__).absolute().parent / "files"
storage_file = "students.json"


LAST_ID_CONTEXT = 2


class StudentsStorage:
    def __init__(self) -> None:
        self.students = self.read_json(storage_file)

    @staticmethod
    def read_json(filename: str) -> dict:
        with open(files_dir / filename) as file:
            return json.load(file)

    @staticmethod
    def write_json(filename: str, data: dict) -> None:
        with open(files_dir / filename, mode="w") as file:
            return json.dump(data, file)

    def flush(self) -> None:
        self.write_json(storage_file, self.students)


def represent_students():
    for id_, student in StudentsStorage().students.items():
        print(f"[{id_}] {student['name']}, marks: {student['marks']}")

def add_student(student: dict) -> dict | None:
    global LAST_ID_CONTEXT
    storage = StudentsStorage()

    if len(student) != 2:
        return None
    elif not student.get("name") or not student.get("marks"):
        return None
    else:
        LAST_ID_CONTEXT += 1
        storage.students[str(LAST_ID_CONTEXT)] = student

    storage.flush()
    return student


def search_student(id_: int) -> dict | None:
    storage = StudentsStorage()
    return storage.students.get(str(id_))


def delete_student(id_: int):
    storage = StudentsStorage()

    if search_student(id_):
        del storage.students[str(id_)]
        print(f"Student with id '{id_}' is deleted")
    else:
        print(f"There is student '{id_}' in the storage")


def update_student(id_: int, payload: dict) -> dict:
    storage = StudentsStorage()
    storage.students[str(id_)] = payload
    storage.flush()

    return payload


def student_details(student: dict) -> None:
    print(f"Detailed info: [{student['name']}]...")


def parse(data: str) -> tuple[str, list[int]]:
    """Return student name and marks.

    user input template:
    'John Doe;4,5,4,5,4,5'


    def foo(*args, **kwargs):
        pass

    """

    template = "John Doe;4,5,4,5,4,5"

    items = data.split(";")

    if len(items) != 2:
        raise Exception(f"Incorrect data. Template: {template}")

    name, raw_marks = items

    try:
        marks = [int(item) for item in raw_marks.split(",")]
    except ValueError as error:
        print(error)
        raise Exception(f"Marks are incorrect. Template: {template}") from error

    return name, marks


def ask_student_payload():
    """
    Input template:
        'John Doe;4,5,4,5,4,5'

    Expected:
        John Doe:       str
        4,5,4,5,4,5:    list[int]
    """

    prompt = "Enter student's payload using next template:\n'John Doe;4,5,4,5,4,5': "

    if not (payload := parse(input(prompt))):
        return None
    else:
        name, marks = payload

    return {"name": name, "marks": marks}


def handle_management_command(command: str):
    if command == "show":
        represent_students()

    elif command == "retrieve":
        search_id = input("Enter student's id to retrieve: ")

        try:
            id_ = int(search_id)
        except ValueError as error:
            raise Exception(f"ID '{search_id}' is not correct value") from error
        else:
            if student := search_student(id_):
                student_details(student)
            else:
                print(f"There is not student with id: '{id_}'")

    elif command == "remove":
        delete_id = input("Enter student's id to remove: ")

        try:
            id_ = int(delete_id)
        except ValueError as error:
            raise Exception(f"ID '{delete_id}' is not correct value") from error
        else:
            delete_student(id_)

    elif command == "change":
        update_id = input("Enter student's id you wanna change: ")

        try:
            id_ = int(update_id)
        except ValueError as error:
            raise Exception(f"ID '{update_id}' is not correct value") from error
        else:
            if data := ask_student_payload():
                update_student(id_, data)
                print(f"Student is updated")
                if student := search_student(id_):
                    student_details(student)
                else:
                    print(f"Can not change user with data {data}")

    elif command == "add":
        data = ask_student_payload()
        if data is None:
            return None
        else:
            if not (student := add_student(data)):
                print(f"Can't create user with data: {data}")
            else:
                print(f"New student '{student['name']}' is created")
    else:
        raise SystemExit(f"Unrecognized command: '{command}'")


def handle_user_input():
    """This is an application entrypoint."""

    SYSTEM_COMMANDS = ("quit", "help")
    MANAGEMENT_COMMANDS = ("show", "add", "retrieve", "remove", "change")
    AVAILABLE_COMMANDS = SYSTEM_COMMANDS + MANAGEMENT_COMMANDS

    help_message = (
        "Welcome to the Journal application. Use the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(help_message)

    while True:
        command = input("Enter the command: ")

        if command == "quit":
            print(f"\nThanks for using Journal application. Bye!")
            break
        elif command == "help":
            print(help_message)
        elif command in MANAGEMENT_COMMANDS:
            handle_management_command(command=command)
        else:
            print(f"Unrecognized command '{command}'")


handle_user_input()