
---

## Классы

### `Student`
Представляет одного студента.  

Методы:

- `add_subject(name_subject)` — добавить предмет  
- `remove_subject(name_subject)` — удалить предмет  
- `add_grade(name_subject, grade)` — добавить оценку по предмету (от 1 до 5)  
- `get_gpa()` — средний балл по всем предметам  
- `to_dict()` — конвертировать объект в словарь для JSON  
- `from_dict(data)` — создать объект из словаря  
- `__str__()` — красиво вывести студента и его оценки  

---

### `JsonStudentHelper`
Работа с JSON-файлом (`students.json`):  

Методы:

- `load(filepath=PATH_TO_DB)` — загрузка данных из JSON, возвращает список словарей  
- `save(data, filepath=PATH_TO_DB)` — сохранение списка студентов в JSON  

---

### `StudentManager`
Менеджер студентов, хранит объекты `Student` и управляет ними.  

Методы:

- `add_student(name)` — создать нового студента и вернуть объект  
- `save()` — сохранить текущие изменения в JSON  

Защищённый метод:

- `_next_id()` — возвращает следующий доступный ID студента  

---

## Пример использования

```python
from main import StudentManager

# Создаём менеджера
manager = StudentManager()

# Добавляем студентов
student1 = manager.add_student("Мирослав")
student1.add_subject("Математика")
student1.add_grade("Математика", 5)
student1.add_grade("Математика", 4)

student2 = manager.add_student("Аня")
student2.add_subject("Физика")
student2.add_grade("Физика", 5)

# Сохраняем все изменения
manager.save()

# Выводим информацию о студентах
for student in manager.students:
    print(student)
