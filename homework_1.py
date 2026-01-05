import json

PATH_TO_DB = "students.json"


class Student:
    # Инициализируем объект студента с параметрами
    def __init__(
        self, id_: int, name: str, subjects: dict | None = None
    ):  # id, имя студента, предметы
        self.name = name
        self.id = id_
        self.subjects = subjects or {}  # либо переданный НЕ пустой словарь, либо пустой

    # Добавление предмета для ученика
    def add_subject(self, name_subject):  # принимаем имя предмета
        name_subject = (
            name_subject.lower()
        )  # приводим к нижнему регистру, чтобы корректно отработало
        if (
            name_subject not in self.subjects
        ):  # проверка, что предмета еще нет у ученика
            self.subjects[name_subject] = []
        else:
            print(
                "У ученика уже существует этот предмет!"
            )  # не выбрасываем исключение, потому что не влияет на логику

    # Добавление оценки для ученика по предмету
    def add_grade(self, name_subject: str, grade: int):  # имя предмета, оценка
        name_subject = name_subject.lower()

        if (
            name_subject not in self.subjects
        ):  # проверка, есть ли у ученика этот предмет
            raise ValueError(
                "У ученика отсутствует этот предмет!"
            )  # возбуждаем исключение, если нет такого предмета
        if not 1 <= grade <= 5:
            raise ValueError("Можно передать только цифру от 1 до 5")

        self.subjects[name_subject].append(
            grade
        )  # корректно обновляем список с оценками по предмету

    # Удаление предмета у ученика
    def remove_subject(self, name_subject):  # имя предмета
        name_subject = name_subject.lower()  #
        if (
            name_subject not in self.subjects
        ):  # проверка, есть ли у ученика такой предмет
            raise ValueError(
                "У ученика нет этого предмета, чтобы его можно было удалить!"
            )  # выкидываем ошибку, если нет
        self.subjects.pop(name_subject)  # удаляем предмет из словаря

    # Расчёт среднего балла
    def get_gpa(self):
        if not self.subjects:  # проверка, если еще нет предметов и вызвали метод
            return 0.0  # возвращаем нули
        total = sum(
            sum(grades) for grades in self.subjects.values()
        )  # считаем сумму оценок по всем предметам
        return round(
            total / len(self.subjects), 2
        )  # делим сумму оценок на кол-во предметов и округляем

    # Метод для преобразования в словарь из Student
    def to_dict(self) -> dict:
        res = {"id": self.id, "name": self.name.capitalize(), "subjects": self.subjects}
        return res

    # Метод для преобразования из словаря в Student
    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(id_=data["id"], name=data["name"], subjects=data.get("subjects", {}))

    # Строковое представление ученика
    def __str__(self):
        pretty_subjects = []
        for key, value in self.subjects.items():
            pretty_subjects.append(
                f"\n{key.capitalize()}: {', '.join(map(str, value))}"
            )
        pretty_subjects = "".join(pretty_subjects)

        res_str = (
            f"Ученик {self.name.capitalize()}, его оценки по предметам: {pretty_subjects}\n"
            f"Средний бал по всем предметам равен {self.get_gpa()}"
        )
        return res_str


# Решил вынести работу с данными в отдельный класс
class JsonStudentHelper:
    # Загрузка из json
    @staticmethod
    def load(filepath=PATH_TO_DB) -> list:
        with open(filepath, encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
            except (
                json.decoder.JSONDecodeError
            ):  # обрабатываем исключения, если записей еще нет
                return []  # возвращаем пустой список, если нет записей
        return data  # иначе возвращаем заполненный список

    # Метод для сохранения в json
    @staticmethod
    def save(data: list[dict], filepath=PATH_TO_DB) -> None:
        with open(
            filepath, "w", encoding="utf-8"
        ) as json_file:  # полностью перезаписываем json
            json.dump(data, json_file, ensure_ascii=False, indent=4)


# Класс для управления работой со студентами
class StudentManager:
    def __init__(self):
        students = (
            JsonStudentHelper.load()
        )  # не наследуемся от JsonStudentHelper и внедряем просто зависимость
        students = [
            Student.from_dict(student) for student in students
        ]  # создаем экземпляры класса Student сразу при объявлении менеджера
        self.students = students

    # Добавляем студента
    def add_student(self, name: str):
        _id = self._next_id()
        student = Student(_id, name)
        self.students.append(student)
        return student

    # Получить следующий id, защищённый метод т.к. публичный доступ не нужен, а используется только внутри класса
    def _next_id(self):
        if not self.students:
            return 1
        return max(student.id for student in self.students) + 1

    # Сохранение изменений для менеджера
    def save(self):
        data = [student.to_dict() for student in self.students]
        JsonStudentHelper.save(data)
