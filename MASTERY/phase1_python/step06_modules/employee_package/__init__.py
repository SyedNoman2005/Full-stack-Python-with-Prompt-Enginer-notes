"""
employee_package/__init__.py

Ye file Python ko batati hai: "ye folder ek PACKAGE hai".

Yahan jo import karoge, wo package level pe available ho jaata hai.
Matlab user ko andar ki file ka naam nahi pata hona chahiye.
"""

from .models import Employee, Manager
from .utils import format_salary, calculate_tax

# __all__ define karta hai ki 'from package import *' pe kya milega
__all__ = ["Employee", "Manager", "format_salary", "calculate_tax"]

PACKAGE_VERSION = "1.0.0"
