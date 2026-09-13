"""
================================================================
STEP 3 — OOP  🔴🔴  (SABSE IMPORTANT)
================================================================
Chalane ke liye:  python3 phase1_python/step03_oop.py

GOAL:
  Interviewer bole "Create an Employee class"
  -> tu 2 minute me bina soche likh de.

Django ke Models, Views, Serializers — SAB classes hain.
OOP kaccha = Django kaccha. Isko 3 baar padh.
================================================================
"""

from abc import ABC, abstractmethod


# ==============================================================
# 1. CLASS, OBJECT, __init__, self  — THE CORE
# ==============================================================

class Employee:
    """Ye wahi class hai jo interview me maangte hain. Ratt le."""

    # CLASS VARIABLE — sab objects me shared
    company = "TechCorp"
    total_employees = 0

    def __init__(self, name, salary):
        """
        CONSTRUCTOR — object banate hi automatically chalta hai.
        self = "ye wala object" (jo abhi ban raha hai)
        """
        # INSTANCE VARIABLES — har object ke apne alag
        self.name = name
        self.salary = salary

        Employee.total_employees += 1     # class variable update

    def display(self):
        """METHOD — class ke andar ka function. Pehla param hamesha self."""
        print(f"    {self.name} | {self.salary} | {self.company}")

    def give_raise(self, amount):
        """Object ka data badalna."""
        self.salary += amount
        return self.salary

    def annual_salary(self):
        return self.salary * 12


def core_demo():
    print("\n--- 1. CLASS / OBJECT / __init__ / self ---")

    # OBJECT banana (instantiation)
    emp = Employee("Noman", 30000)
    emp.display()

    emp2 = Employee("Ali", 45000)
    emp2.display()

    print(f"\n  emp.name          = {emp.name}")
    print(f"  emp.annual_salary = {emp.annual_salary()}")
    print(f"  give_raise(5000)  -> {emp.give_raise(5000)}")

    print(f"\n  Class variable (shared): Employee.total_employees = {Employee.total_employees}")
    print(f"  Instance variable (alag): emp.name={emp.name}, emp2.name={emp2.name}")

    print("\n  SELF KYA HAI?")
    print("    emp.display()  ko Python andar se Employee.display(emp) banata hai")
    print("    self = wahi object jispe method call hua hai")


# ==============================================================
# 2. INHERITANCE + super()
# ==============================================================

class Person:
    """PARENT / BASE class"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"Main {self.name} hoon, umar {self.age}"

    def show(self):
        return f"Person: {self.name}"


class Developer(Person):
    """CHILD class — Person se sab kuch inherit karti hai"""

    def __init__(self, name, age, language):
        super().__init__(name, age)     # parent ka __init__ chalao
        self.language = language        # apna extra field

    def show(self):                     # METHOD OVERRIDING
        return f"Developer: {self.name} ({self.language})"

    def code(self):                     # apna naya method
        return f"{self.name} {self.language} me code likh raha hai"


class SeniorDeveloper(Developer):
    """MULTI-LEVEL inheritance: Person -> Developer -> SeniorDeveloper"""

    def __init__(self, name, age, language, team_size):
        super().__init__(name, age, language)
        self.team_size = team_size

    def show(self):
        return f"Senior Dev: {self.name} ({self.language}), team of {self.team_size}"


def inheritance_demo():
    print("\n--- 2. INHERITANCE + super() ---")

    p = Person("Aslam", 40)
    d = Developer("Noman", 21, "Python")
    s = SeniorDeveloper("Sara", 30, "Django", 5)

    print(f"  {p.show()}")
    print(f"  {d.show()}")
    print(f"  {s.show()}")

    print(f"\n  Inherited method (Person se aaya): {d.introduce()}")
    print(f"  Own method:                       {d.code()}")
    print(f"  Multi-level (Person ka method):   {s.introduce()}")

    print(f"\n  isinstance(d, Person)    = {isinstance(d, Person)}")
    print(f"  issubclass(Developer, Person) = {issubclass(Developer, Person)}")

    print("\n  super() kya karta hai?")
    print("    Parent class ka method call karta hai.")
    print("    super().__init__() = parent ka constructor chalao.")

    print("\n  INHERITANCE TYPES:")
    print("    Single       : A -> B")
    print("    Multi-level  : A -> B -> C")
    print("    Multiple     : class C(A, B)")
    print("    Hierarchical : A -> B, A -> C")


# ==============================================================
# 3. ENCAPSULATION — data ko chhupana
# ==============================================================

class BankAccount:
    """Private data + getter/setter. Ye encapsulation hai."""

    def __init__(self, owner, balance):
        self.owner = owner             # PUBLIC
        self._account_type = "Savings" # PROTECTED (convention: mat chhedo)
        self.__balance = balance       # PRIVATE (name mangling)

    # GETTER
    def get_balance(self):
        return self.__balance

    # SETTER with VALIDATION — yahi encapsulation ka faida hai
    def deposit(self, amount):
        if amount <= 0:
            return "Amount positive hona chahiye"
        self.__balance += amount
        return f"Deposited {amount}. Balance: {self.__balance}"

    def withdraw(self, amount):
        if amount > self.__balance:
            return "Insufficient balance"
        self.__balance -= amount
        return f"Withdrew {amount}. Balance: {self.__balance}"


class Product:
    """@property — modern Pythonic getter/setter"""

    def __init__(self, name, price):
        self.name = name
        self.__price = price

    @property
    def price(self):
        """Getter — ab obj.price likho, obj.get_price() nahi"""
        return self.__price

    @price.setter
    def price(self, value):
        """Setter with validation"""
        if value < 0:
            raise ValueError("Price negative nahi ho sakta")
        self.__price = value

    @property
    def price_with_gst(self):
        """Computed property — store nahi hoti, calculate hoti hai"""
        return round(self.__price * 1.18, 2)


def encapsulation_demo():
    print("\n--- 3. ENCAPSULATION ---")

    acc = BankAccount("Noman", 10000)
    print(f"  Owner: {acc.owner}")
    print(f"  {acc.deposit(5000)}")
    print(f"  {acc.withdraw(3000)}")
    print(f"  {acc.withdraw(999999)}")
    print(f"  {acc.deposit(-100)}   <- validation ne roka")

    print("\n  Private access try karo:")
    try:
        print(acc.__balance)
    except AttributeError as e:
        print(f"    AttributeError: {e}")
    print(f"    Sahi tareeka -> acc.get_balance() = {acc.get_balance()}")
    print(f"    (Name mangling se ye kaam karta hai, par mat karo: {acc._BankAccount__balance})")

    print("\n  @property demo:")
    p = Product("Laptop", 50000)
    print(f"    p.price          = {p.price}")
    print(f"    p.price_with_gst = {p.price_with_gst}")
    p.price = 55000
    print(f"    p.price = 55000  -> {p.price}")
    try:
        p.price = -100
    except ValueError as e:
        print(f"    p.price = -100   -> ValueError: {e}")


# ==============================================================
# 4. POLYMORPHISM — ek naam, alag behaviour
# ==============================================================

class Shape:
    def area(self):
        return 0

    def name(self):
        return "Shape"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return round(3.14159 * self.radius ** 2, 2)

    def name(self):
        return "Circle"


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def name(self):
        return "Rectangle"


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def name(self):
        return "Square"


def polymorphism_demo():
    print("\n--- 4. POLYMORPHISM ---")

    shapes = [Circle(5), Rectangle(4, 6), Square(3)]

    print("  Same method call, alag alag result:")
    for s in shapes:
        print(f"    {s.name():<10} area = {s.area()}")

    print("\n  DUCK TYPING (Python ka special):")
    print("    'Agar duck jaisa chalta hai aur duck jaisa bolta hai, to duck hai'")
    print("    Python inheritance nahi dekhta, bas method hai ya nahi ye dekhta hai.")

    class Dog:
        def speak(self):
            return "Bhow Bhow"

    class Cat:
        def speak(self):
            return "Meow"

    class Robot:
        def speak(self):
            return "Beep Boop"

    for animal in [Dog(), Cat(), Robot()]:
        print(f"    {type(animal).__name__:<7} -> {animal.speak()}")

    print("\n  OPERATOR OVERLOADING bhi polymorphism hai:")
    print(f"    5 + 3        = {5 + 3}        (addition)")
    print(f"    'a' + 'b'    = {'a' + 'b'}       (concatenation)")
    print(f"    [1] + [2]    = {[1] + [2]}     (merge)")


# ==============================================================
# 5. ABSTRACTION — blueprint, implementation chhupao
# ==============================================================

class Vehicle(ABC):
    """ABSTRACT CLASS — iska object nahi bana sakte, sirf inherit kar sakte ho."""

    def __init__(self, brand):
        self.brand = brand

    @abstractmethod
    def start_engine(self):
        """Har child ko ye method likhna HI padega."""
        pass

    @abstractmethod
    def fuel_type(self):
        pass

    def describe(self):
        """Concrete method — sab children ko free me milta hai."""
        return f"{self.brand} runs on {self.fuel_type()}"


class Car(Vehicle):
    def start_engine(self):
        return f"{self.brand} car: Vroom!"

    def fuel_type(self):
        return "Petrol"


class ElectricCar(Vehicle):
    def start_engine(self):
        return f"{self.brand} EV: Silent start"

    def fuel_type(self):
        return "Electricity"


def abstraction_demo():
    print("\n--- 5. ABSTRACTION ---")

    for v in [Car("Maruti"), ElectricCar("Tata")]:
        print(f"  {v.start_engine()}")
        print(f"    -> {v.describe()}")

    print("\n  Abstract class ka object banane ki koshish:")
    try:
        Vehicle("Generic")
    except TypeError as e:
        print(f"    TypeError: {e}")

    print("\n  Faida: Contract ban jaata hai. Jo bhi Vehicle banayega,")
    print("  usko start_engine() aur fuel_type() likhna HI padega.")


# ==============================================================
# 6. DUNDER / MAGIC METHODS
# ==============================================================

class Money:
    """__str__, __repr__, __add__, __eq__, __len__ — ye poochhte hain."""

    def __init__(self, amount, currency="INR"):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        """print(obj) — user ke liye"""
        return f"{self.currency} {self.amount:,}"

    def __repr__(self):
        """Debugging ke liye — developer ke liye"""
        return f"Money({self.amount}, '{self.currency}')"

    def __add__(self, other):
        """obj1 + obj2 kaam karega"""
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        """obj1 == obj2"""
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        """obj1 < obj2 — sorting ke liye"""
        return self.amount < other.amount


def dunder_demo():
    print("\n--- 6. DUNDER / MAGIC METHODS ---")

    a = Money(30000)
    b = Money(45000)

    print(f"  print(a)   -> {a}          (__str__)")
    print(f"  repr(a)    -> {repr(a)}   (__repr__)")
    print(f"  a + b      -> {a + b}          (__add__)")
    print(f"  a == b     -> {a == b}              (__eq__)")
    print(f"  a < b      -> {a < b}               (__lt__)")
    print(f"  sorted     -> {[str(m) for m in sorted([b, a])]}")

    print("\n  Django me tu ye roz likhega:")
    print("    class Employee(models.Model):")
    print("        def __str__(self):")
    print("            return self.name       <- admin panel me naam dikhega")


# ==============================================================
# 7. STATIC / CLASS / INSTANCE METHODS
# ==============================================================

class MathHelper:
    pi = 3.14159

    def __init__(self, value):
        self.value = value

    def instance_method(self):
        """self leta hai — object ka data chahiye"""
        return f"Instance method, value = {self.value}"

    @classmethod
    def class_method(cls):
        """cls leta hai — class ka data chahiye, object nahi"""
        return f"Class method, pi = {cls.pi}"

    @classmethod
    def from_string(cls, text):
        """ALTERNATIVE CONSTRUCTOR — ye pattern bahut use hota hai"""
        return cls(int(text))

    @staticmethod
    def static_method(a, b):
        """Na self, na cls — bas ek utility function"""
        return a + b


def methods_demo():
    print("\n--- 7. STATIC / CLASS / INSTANCE METHODS ---")

    obj = MathHelper(10)
    print(f"  {obj.instance_method()}")
    print(f"  {MathHelper.class_method()}")
    print(f"  MathHelper.static_method(3, 4) = {MathHelper.static_method(3, 4)}")

    alt = MathHelper.from_string("99")
    print(f"  Alternative constructor: MathHelper.from_string('99').value = {alt.value}")

    print("\n  Kab kya use karein?")
    print("    instance -> object ka data chahiye       (self)")
    print("    class    -> class ka data chahiye        (cls)")
    print("    static   -> kuch nahi chahiye, bas utility")


# ==============================================================
# INTERVIEW — RATTA MAAR LO
# ==============================================================
INTERVIEW = """
Q1. OOP ke 4 pillars?
    1. Encapsulation — data + methods ek jagah, private data chhupao
    2. Inheritance   — parent ka code child me reuse
    3. Polymorphism  — ek naam, alag behaviour
    4. Abstraction   — kya karta hai dikhao, kaise karta hai chhupao

Q2. Class vs Object?
    Class  = blueprint / naksha (ghar ka design)
    Object = actual instance (asli ghar)

Q3. self kya hai?
    Current object ka reference. Har instance method ka pehla parameter.
    obj.method() ko Python Class.method(obj) banata hai.

Q4. __init__ kya hai?
    Constructor. Object banate hi automatically chalta hai.
    Instance variables initialize karta hai.

Q5. super() kya karta hai?
    Parent class ka method call karta hai.
    Zyadatar super().__init__() ke liye use hota hai.

Q6. Method Overriding vs Overloading?
    Overriding  -> child parent ka method dobara likhe.  Python me HOTA HAI.
    Overloading -> same naam, alag parameters.  Python me NAHI HOTA
                   (default args / *args se kaam chalate hain).

Q7. Public vs Protected vs Private?
    name    -> public     (koi bhi use kare)
    _name   -> protected  (convention: mat chhedo, par technically accessible)
    __name  -> private    (name mangling: _ClassName__name)
    Python me sach me kuch private nahi hota — sab convention hai.

Q8. Abstract class kya hai?
    ABC se inherit karti hai, @abstractmethod hote hain.
    Iska object nahi banta. Child ko abstract methods likhna hi padta hai.

Q9. @staticmethod vs @classmethod?
    staticmethod -> na self na cls. Utility function.
    classmethod  -> cls leta hai. Class-level data ya alternative constructor.

Q10. Multiple inheritance aur MRO?
    class C(A, B) — dono se inherit.
    MRO = Method Resolution Order. C.__mro__ se dekh sakte ho.
    Python C3 linearization use karta hai.

Q11. __str__ vs __repr__?
    __str__  -> print() ke liye, user-friendly
    __repr__ -> debugging ke liye, developer-friendly, unambiguous

Q12. Class variable vs Instance variable?
    Class variable    -> sab objects me shared (ClassName.var)
    Instance variable -> har object ka apna (self.var)
"""


PRACTICE = """
1.  Employee class — name, salary, display() method. (MUST)
2.  Student class — marks list lo, average nikalo, grade do.
3.  BankAccount — private balance, deposit(), withdraw() with validation.
4.  Animal parent class, Dog/Cat child — speak() override karo.
5.  Shape abstract class, Circle/Rectangle child — area() implement karo.
6.  Car class me __str__ likho jo "Brand Model (Year)" print kare.
7.  Money class me __add__ likho taaki m1 + m2 chale.
8.  Manager class banao jo Employee se inherit kare + team_size add kare.
9.  @property use karke Product class me price validation karo.
10. Library system: Book, Member, Library classes — issue/return books.
"""


if __name__ == "__main__":
    print("=" * 62)
    print("STEP 3 — OOP  (sabse important step)")
    print("=" * 62)

    core_demo()
    inheritance_demo()
    encapsulation_demo()
    polymorphism_demo()
    abstraction_demo()
    dunder_demo()
    methods_demo()

    print("\n" + "=" * 62)
    print("INTERVIEW QUESTIONS — ratta maar lo")
    print("=" * 62)
    print(INTERVIEW)

    print("=" * 62)
    print("PRACTICE")
    print("=" * 62)
    print(PRACTICE)
