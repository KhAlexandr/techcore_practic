students = [
    {
        "Name": "Саша",
        "avg_grade": 3.2,
    },
    {
        "Name": "Маша",
        "avg_grade": 4.1
    },
    {
        "Name": "Миша",
        "avg_grade": 4.8
    },
]


def filter_students(s):
    filtered_students = []
    for student in s:
        if student["avg_grade"] > 4.0:
            filtered_students.append(student)
    return filtered_students


print(filter_students(students))
