class BloqueCache:
    def __init__(self, id, state, dir, data):
        self.id = id
        self.state = state
        self.dir = dir
        self.data = data

    def obtener_estado(self):
        return self.state

class Cache:
    def __init__(self):
        self.b0 = BloqueCache(0, "none", "000", "000")
        self.b1 = BloqueCache(1, "none", "000", "000")
        self.b2 = BloqueCache(2, "none", "000", "000")
        self.b2 = BloqueCache(3, "none", "000", "000")

    def foundBloque(self):
        print("encontrar bloque")
