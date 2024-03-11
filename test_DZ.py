import csv
import logging
import string
import argparse
import datetime
import pytest


class Student:

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)
        logging.info(f"Инициация экземпляра студента: {self.name}, at {datetime.datetime.now()}")

    def __setattr__(self, name, value):
        if name == 'name':
            if not value.replace(' ', '').isalpha() or not value.istitle():
                raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.subjects:
            return self.subjects[name]
        else:
            raise AttributeError(f"Предмет {name} не найден")

    def __str__(self):
        return f"Студент: {self.name}\nПредметы: {', '.join(self.subjects.keys())}"

    def load_subjects(self, subjects_file):
        with open(subjects_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                subject = row[0]
                if subject not in self.subjects:
                    self.subjects[subject] = {'grades': [], 'test_scores': []}
                    logging.info(f"Добавлен предмет: {subject}, at {datetime.datetime.now()}")

    def add_grade(self, subject, grade):
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(grade, int) or grade < 2 or grade > 5:
            logging.error(f"Попытка добавить неприемлемую оценку {grade} предмету {subject}")
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        self.subjects[subject]['grades'].append(grade)
        logging.info(f"Предмету {subject} Добавлена оценка: {grade}, at {datetime.datetime.now()}")

    def add_test_score(self, subject, test_score):
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")
        self.subjects[subject]['test_scores'].append(test_score)
        logging.info(f"Предмету {subject} Добавлена оценка за тест: {test_score}, at {datetime.datetime.now()}")

    def get_average_test_score(self, subject):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        test_scores = self.subjects[subject]['test_scores']
        if len(test_scores) == 0:
            return 0
        logging.info(f"Средняя оценка за тесты по предмету: {subject}: {sum(test_scores) / len(test_scores)},"
                     f" at {datetime.datetime.now()}")
        return sum(test_scores) / len(test_scores)

    def get_average_grade(self):
        total_grades = []
        for subject in self.subjects:
            grades = self.subjects[subject]['grades']
            if len(grades) > 0:
                total_grades.extend(grades)
        if len(total_grades) == 0:
            return 0
        logging.info(f"Средняя оценка: {sum(total_grades) / len(total_grades)},"
                     f" at {datetime.datetime.now()}")
        return sum(total_grades) / len(total_grades)


parser = argparse.ArgumentParser(description='For Student parser')
parser.add_argument('file', metavar='N', type=str, nargs='*', help='write filename')
args = parser.parse_args().file[0]
print(f'Передан файл: {args}', type(args))

logging.basicConfig(filename='log_file.log', encoding='utf-8', level=logging.NOTSET, filemode='w+')


@pytest.fixture
def data():
    student = Student("Степан Геннадьевич", args)
    student.add_grade('Математика', 5)
    return student


def test_init():
    with pytest.raises(ValueError):
        Student('степа', 'subjects.cs')


def test_add_grade(data):
    assert 'Математика' in data.subjects.keys()


def test_non_existent_add_grade(data):
    with pytest.raises(ValueError):
        return data.add_grade('Математика', 1000000)


def test_get_attr(data):
    with pytest.raises(AttributeError):
        return data.imagineattr


def test_get_average_grade(data):
    assert data.get_average_grade() == 5.0


if __name__ == '__main__':
    pytest.main(['-vv'])
