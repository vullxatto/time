class entity:

    def __init__(self, code=0):
        self.setCode(code)

    def setCode(self, value):
        self.__code = value

    def getCode(self):
        return self.__code
