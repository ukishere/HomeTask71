import psycopg2 as psy


def create_db():
    cursor.execute('''CREATE TABLE student (
        id INT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        gpa NUMERIC(10,2),
        birth TIMESTAMP
        );''')

    cursor.execute('''CREATE TABLE course (
        id INT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL
        );''')

    cursor.execute('''CREATE TABLE student_course (
        s_id INT REFERENCES student(id),
        c_id INT REFERENCES course(id),
        CONSTRAINT sc_primkey PRIMARY KEY(s_id, c_id)
        );''')

def get_students(course_id):
    cursor.execute(
        'SELECT id, name FROM student join student_course on student.id = student_course.s_id WHERE c_id = (%s);',
        (course_id))
    print(f'Студенты, зачисленные на курс {course_id}:\n {cursor.fetchall()}')

def add_students(course_id, students):
    for student in students.items():
        cursor.execute('INSERT INTO student(id, name, gpa, birth) VALUES (%s, %s, %s, %s)',
                       (student[0], student[1]['name'], student[1]['gpa'], student[1]['birth']))
        cursor.execute('INSERT INTO student_course(s_id, c_id) VALUES (%s, %s)', (student[0], course_id))

def add_courses(courses):
    for course in courses.items():
        cursor.execute('INSERT INTO course(id, name) VALUES (%s, %s)', (course[0], course[1]))

def add_student(student):
    student = list(student.items())
    cursor.execute('INSERT INTO student(id, name, gpa, birth) VALUES (%s, %s, %s, %s)',
                   (student[0][0], student[0][1]['name'], student[0][1]['gpa'], student[0][1]['birth']))
    cursor.execute('INSERT INTO student_course(s_id, c_id) VALUES (%s, %s)', (student[0][0], '2'))

def get_student(student_id):
    cursor.execute('SELECT name FROM student WHERE id = (%s)', (student_id))
    print(f'Студента под номером {student_id} зовут {cursor.fetchall()[0][0]}')

with psy.connect(database='hometasku711', user='hometasku711', password='1234') as connection:
    students = {
        '1': {'name': 'Alex',
                'gpa': '1.0',
                'birth': '10/01/2010'
            },
        '2': {'name': 'Max',
                'gpa': '1.1',
                'birth': '11/01/2010'
            },
        '3': {'name': 'Mike',
                'gpa': '2.2',
                'birth': '12/01/2010'
            }
    }
    courses = {
        '1': 'First course',
        '2': 'Second course'
    }
    student = {'4': {'name': 'Igor', 'gpa': '3.3', 'birth': '9/01/2010'}}
    cursor = connection.cursor()
    # create_db()
    # add_courses(courses)
    # add_students('1', students)
    # add_student(student)
    # get_student('1')
    # get_students('1')