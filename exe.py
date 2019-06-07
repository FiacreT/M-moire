
class Exe:
    myVar = ""
    @staticmethod
    def method_t(name):
        Exe.myVar = name
    def hello(self, name):
        #print("hello")
        #global myVar
        #return "hello"'''
        pass

'''if __name__ == '__main__':
    hello()'''

#print(myVar)

e = Exe()
e.method_t("hello")
print(e.myVar)
e.method_t("salut")
print(e.myVar)
m=Exe()
print(m.myVar)