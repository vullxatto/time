class libWidget:

    def __init__(self, library=None, conf=None):
        self.__library = library
        self.__conf = conf

    def getLibrary(self):
        return self.__library

    def getConf(self):
        return self.__conf
