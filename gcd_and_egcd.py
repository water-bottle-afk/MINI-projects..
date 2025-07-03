def gcd(a, b):
    mod = max(a, b) % min(a, b)
    if mod == 0:
        return min(a, b)
    if mod == 1:
        return 1
    return gcd(b, mod)


lst_of_equations_down = []

class equation_down:
    def __init__(self, a, b):
        self.a = max(a, b)
        self.b = min(a, b)
        self.sum = self.a
        self.qoutinent = self.a // self.b
        self.reminder = self.a % self.b

    def get_and_set_gcd(self):
        self.gcd = gcd(self.a, self.b)
        return self.gcd

    def targil(self):
        lst_of_equations_down.append((self.a, self.b, self.qoutinent, self.reminder))
        print(f"{self.a} = {self.b} * ({self.qoutinent}) + {self.reminder}")

    def get_next(self):
        return self.b, self.reminder

    def print_lst(self):
        print(lst_of_equations_down)


class equation_up:
    def __init__(self):
        self.find_the_a()

    def targil(self,reminder, a,x,b,y):
        print(f"{reminder} = ({a}) * {x} + ({b}) * {y}")

    def get_next(self):
        return self.b, self.reminder

    def print_lst(self):
        print(lst_of_equations_down)

    def find_the_a(self):
        tpl = lst_of_equations_down.pop(-1)
        x,y,b,reminder = tpl
        self.x = x
        self.y = y
        self.b = b * -1
        self.reminder = reminder
        self.a = self.x // (self.b * self.y  * (-1))
        self.targil(reminder,self.a,self.x,self.b,self.y)
    def keep(self):
        tpl = lst_of_equations_down.pop(-1)
        x, y, b, reminder = tpl
        self.next_x = x
        self.next_y = y
        self.next_b = b * -1
        self.next_reminder = reminder
        self.next_a = self.next_x // (self.next_b * self.next_y * (-1))
        self.targil(self.next_reminder, self.next_a, self.next_x, self.next_b, self.next_y)

        print(lst_of_equations_down)
        self.mashup()

    def mashup(self):
        if self.x == self.next_y:
            print(f"{self.reminder} = ({self.a}) * {self.x} + ({self.b}) * ({self.next_a} * {self.next_x} + {self.next_b} * {self.next_y})")
            self.a = self.a + self.b * self.next_b
            self.y = self.next_x
            self.targil(self.reminder, self.a, self.x, self.b, self.y)
        if self.x == self. next_reminder:
            print(f"{self.reminder} = ({self.a}) * ({self.next_a} * {self.next_x} + {self.next_b} * {self.next_y})"
                  f" + ({self.b}) * ({self.y})")
            self.x = self.next_x
            self.b = self.a * self.next_b + self.b
            self.targil(self.reminder, self.a, self.x, self.b, self.y)

def rec_down(a, b, og_gcd):
    eq = equation_down(a, b)
    eq.targil()
    new_a, new_b = eq.get_next()
    if new_b == og_gcd:
        eq.print_lst()
        print()
        return
    return rec_down(new_a, new_b, og_gcd)

def ruc_up():
    eq_u = equation_up()
    while lst_of_equations_down:
        eq_u.keep()
    return eq_u.a, eq_u.b

eq_d = equation_down(26513, 32321)
og_gcd = eq_d.get_and_set_gcd()
rec_down(26513, 32321, og_gcd)
a,b = ruc_up()
print(a,b)

