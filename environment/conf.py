import json
import os

class conf:

    def __init__(self, confile='conf.json'):
        self.__confile = confile
        self.__dataDir = './data/'
        self.readfile()

    def readfile(self):
        possible_paths = [self.__confile, os.path.join(os.path.dirname(__file__), self.__confile), os.path.join(os.getcwd(), self.__confile)]
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.__dataDir = data.get('datadir', './data/')
                        self.__imgDir = data.get('imgdir', './public/img/')
                    return
                except Exception:
                    continue
        print(f'Предупреждение: conf.json не найден. Используются значения по умолчанию.')

    def getDataDir(self):
        return self.__dataDir

    def getImgDir(self):
        return self.__imgDir
