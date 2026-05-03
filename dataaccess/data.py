"""Базовый класс доступа к данным: входной/выходной файл, библиотека."""


class Data:

    def __init__(self, lib=None, inp='', out=''):
        self.set_lib(lib)
        self.set_inp(inp)
        self.set_out(out)

    def set_lib(self, value):
        self.__lib = value

    def set_inp(self, value):
        self.__inp = value

    def set_out(self, value):
        self.__out = value

    def get_lib(self):
        return self.__lib

    def get_inp(self):
        return self.__inp

    def get_out(self):
        return self.__out

    def read_file(self, lib=None, filename=''):
        if lib:
            self.set_lib(lib)
        if filename:
            self.set_inp(filename)
        self.read()

    def write_file(self, lib=None, filename=''):
        if lib:
            self.set_lib(lib)
        if filename:
            self.set_out(filename)
        self.write()

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError
