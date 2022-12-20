import unittest
import create_docx
import sys
import os


class TestCreateDOCX(unittest.TestCase):
    """Тест для модуля create_docx"""

    def __init__(self, *args, **kwargs):
        super(TestCreateDOCX, self).__init__(*args, **kwargs)

        """Определили переменные с которыми будем работать"""
        self.base_path = 'path_to_bd'
        self.name = 'test_docx_file'
        self.file = f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}{self.name}.docx"
        self.line = 'UID_1,2017,,,,,Name_1,sub_name,,1977,,,,,,,,,,мед организация,,,,,,Диагноз врача: норма \\ не норма \\ контроль через … месяцев и прочее,,,,34.5,34.4,33.8,34.6,33.9,34.1,34.5,34.4,33.9,34.1,33.9,34.7,34.3,34.7,34.4,34.5,34.6,34.4,34.8,34.7,32.9,32.5,32.1,33.2,32.1,32.6,32.9,32.8,32.6,32.7,32.4,33.0,32.8,33.2,33.0,33.3,33.1,33.4,33.8,33.8,0,\n'
        self.data1 = self.line.split(",")
        self.data2 = 'UID_2,2017,,,,,Name_2,sub_name,,1959,,,,,,,,,мед организация,,,,,,Диагноз врача: норма \\ не норма \\ контроль через … месяцев и прочее,,,,,36.0,35.2,35.0,35.0,34.5,34.8,35.2,35.1,34.8,34.9,34.7,34.9,35.3,35.0,34.8,34.8,34.7,35.0,34.9,35.4,34.7,34.1,33.6,33.7,33.1,33.6,34.2,33.4,33.9,33.3,32.9,33.3,34.1,33.5,33.5,33.0,33.3,33.0,33.5,33.8,0\n'.split(',')

    def setUp(self):
        """Удаляем файл, если он есть"""
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        except Exception as err:
            print(f"System can`t delete file {self.file}, {err}")

    def tearDown(self):
        """Чистим тестовые файлы"""
        try:
            os.remove(self.file)
        except FileNotFoundError:
            pass
        except Exception as err:
            print(f"System can`t delete file {self.file}, {err}")

    def test_create_empty_docx(self):
        """Тестируем создание пустого файла"""
        self.assertFalse(os.path.isfile(self.file))  # no file
        create_docx.create_empty_docx(self.base_path, self.name)  # create
        self.assertTrue(os.path.isfile(self.file))  # have empty file

    def test_average_temperature(self):
        """Проверка нахождения средней температуры"""
        self.assertEqual(create_docx.average_temperature(self.data1[29:38]), 34.23333333333333)
        self.assertEqual(create_docx.average_temperature(self.data2[29:38]), 35.06666666666667)
        # Проверка на исключение при ['','34.5', '34.4', ...]
        self.assertRaises(ValueError, create_docx.average_temperature, self.data2[28:37])

    def test_add_result(self):
        """Тестирование добавления контента"""
        create_docx.create_empty_docx(self.base_path, self.name)  # create
        size1 = os.path.getsize(self.file)
        create_docx.add_result(self.data1[0] + ' left', self.data1[24], self.data1[29:38], name=self.name)
        size2 = os.path.getsize(self.file)
        self.assertGreater(size2, size1)  # сравниваем размер файла до и после добавления


if __name__ == '__main__':
    unittest.main()


