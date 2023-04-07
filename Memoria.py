class BloqueMem:
    def __init__(self, id, data, dir):
        self.id = id
        self.data = data
        self.dir = dir

class Memoria:
    def __init__(self):
        self.b0 = BloqueMem(0, "none", "000")
        self.b1 = BloqueMem(1, "none", "001")
        self.b2 = BloqueMem(1, "none", "010")
        self.b3 = BloqueMem(1, "none", "011")
        self.b4 = BloqueMem(1, "none", "100")
        self.b5 = BloqueMem(1, "none", "101")
        self.b6 = BloqueMem(1, "none", "110")
        self.b7 = BloqueMem(1, "none", "111")
