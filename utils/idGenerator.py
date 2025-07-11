import random
class Password:
    def __init__(self):
        self.num = []
        self.alpha = []
        self.spce = ['!', '@', '#', '$', '%', '^', '&','*', '~', '-', '+', '=']
        self.password = []
    def passw(self):
        for i in range(0, 10):
            self.num.append(str(i))
        for j in range(65, 91):
            self.alpha.append(chr(j))
        for k in range(10):
            self.password.append(random.choice(self.num))
            self.password.append(random.choice(self.alpha))
            self.password.append(random.choice(self.spce))
        random.shuffle(self.password)
        x = ''.join([str(l) for l in self.password])
        return x