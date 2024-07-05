from t import A

class B:
    def __init__(self, name, a: A):
        self.name = name
        self.a = a

    def show(self):
        print(self.name)