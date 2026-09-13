"""
employee_package/models.py — classes yahan rakhte hain

Django me bhi exactly aisa hi hota hai: models.py me models.
"""


class Employee:
    def __init__(self, name, salary, dept="General"):
        self.name = name
        self.salary = salary
        self.dept = dept

    def __str__(self):
        return f"{self.name} ({self.dept}) - {self.salary}"

    def annual_salary(self):
        return self.salary * 12


class Manager(Employee):
    def __init__(self, name, salary, dept, team_size):
        super().__init__(name, salary, dept)
        self.team_size = team_size

    def __str__(self):
        return f"{self.name} (Manager, {self.dept}) - {self.salary}, team: {self.team_size}"
