from tkinter import Frame, Tk, BOTH, Button, Label, W, N, E, S, PhotoImage
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
import os
import sys

import create_docx
import log


class Example(Frame):
    """
    Класс интерфейса
    """

    def __init__(self):
        super().__init__()
        self.initUI()
        self.path_to_bd = ''
        log.add_to_log('Start program')

    def initUI(self):
        """
        Создаем и настраиваем интерфейс
        :return: None
        """
        self.master.title("Create docx result")
        self.pack(fill=BOTH, expand=True)
        try: # Умолчал явно, если запокавать в ехе, то он его теряет
            self.master.iconbitmap("icon.ico")
        except Exception as err:
            pass

        # Лейбл с путем до БД
        self.path_lable = Label(master=self, text='Path to BD: ')
        self.path_lable.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=W+N)

        # Барка для отображения выполнения кода
        self.bar = ttk.Progressbar(master=self, orient='horizontal', mode='determinate', length=100)
        self.bar.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=E+W+S+N)

        # Кнопка открытия диалога
        open_btn = Button(master=self, text='Open file', command=self.onOpen)
        open_btn.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=W+S)

        # Кнопка запуска
        create_btn = Button(master=self, text="Create docx", command=self.do_it)
        create_btn.grid(row=2, column=2, columnspan=3, padx=5, pady=5, sticky=E+S)

        # Куда сохранил файл, там, откуда запустил файл
        self.save_path_lable = Label(master=self)
        self.save_path_lable.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=W+S)

    def onOpen(self):
        """
        Диалог для выбора БД
        :return: Путь до файла БД
        """
        ftypes = [('BD файлы', '*.rtm'), ('Все файлы', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':  # Проверяем, что что-то выбрали
            self.path_to_bd = os.path.abspath(fl)
            text = self.path_lable["text"]
            self.path_lable["text"] = f"{text} {self.path_to_bd}"
            create_docx.create_empty_docx(self.path_to_bd)
            return fl

    def do_it(self):
        """
        Открываем файл, читаем его построчно и добавляем в docx данные
        :return: None
        """
        try:
            log.add_to_log(f'Open BD: {self.path_to_bd} and work')
            with open(self.path_to_bd, 'r') as f:
                try:
                    lines = f.readlines()
                    self.bar['length'] = len(lines)
                    for index, line in enumerate(lines):
                        sl = line.split('\t')

                        # for left
                        create_docx.add_result(sl[0]+' left', sl[24], sl[29:38])
                        # #for right
                        create_docx.add_result(sl[0]+' right', sl[24], sl[38:47])

                        self.bar['value'] = index * 100 / len(lines)
                        self.bar.update()
                except Exception as err:
                    print(f'Error: {err}')
                    log.add_warn(f'Error, when work with lines: {err}')
        except Exception as open_err:
            print(f'Error, when open {self.path_to_bd}: {open_err}')
            log.add_warn(f'Error, when open {self.path_to_bd}: {open_err}')

        log.add_to_log(f'Work completed!')
        showinfo(message='The progress completed!')
        self.save_path_lable["text"] = f"save as:{os.path.dirname(sys.argv[0])}{os.sep}{create_docx.NAME}.docx"
        return None


def main():
    root = Tk()
    ex = Example()
    root.mainloop()


if __name__ == '__main__':
    main()