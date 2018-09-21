class x:
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def hello(self):
        print (self.a)
z = x(2,3)
z.a = 3
print(z.a)

