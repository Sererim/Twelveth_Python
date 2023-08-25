from csv import reader

chars = list(map(chr, range(97, 123)))

class CheckStudentName:
    
    def __get__(self, instance, owner):
        return getattr(instance)
    
    def __set__(self, instance, name: str):
        lst_name = name.split()
        self.validate(lst_name)   
    
    def validate(self, name):
        if len(name) != 2:
            raise TypeError(f"{name} must have two strings in it.")
        for i, j in enumerate(name):
            for x in j:
                if x.lower() not in chars:
                    raise TypeError(f"{name[i]}  letter {x} is not a string.")
        if not name[0].istitle():
            raise TypeError(f"{name[0]} name must start with an uppercase letter.")
        

class CheckNums:
    def __init__(self, min_value: int = None, max_value: int = None) -> None:
        self.min = min_value
        self.max = max_value
    
    def __get(self, instance):
        return getattr(instance)
    
    def __set__(self, instance, value):
        self.validate(value)
    
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Value must be an integer.")
        if self.min is not None and value < self.min:
            raise ValueError(f"Value {value} must be bigger than {self.min}")
        if self.max is not None and value > self.max:
            raise ValueError(f"Value {value} must be smaller than {self.max}")


class Student:
    """Student class that reads subjects from csv file
    and allows to enter marks for student.
    """
    __marks = {}
    __tests = {}
    __file_name: str = "students.csv"
    
    fullname = CheckStudentName()
    _mark = CheckNums(2, 5 )
    _test = CheckNums(0, 100)
    _grade = CheckNums(1, 12)
    _age = CheckNums(5, 19)
        
    def __init__(self, fullname, age, grade) -> None:
        self.fullname = fullname
        self.age = age
        self.grade = grade
    
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        with open(Student.__file_name, '+r') as file:
            subjects = reader(file)
            for home in subjects:
                for subject in home:
                    instance.__marks[subject] = 0
                    instance.__tests[subject] = 0
        return instance
    
    def get_mark(self, mark, subject: str):
        self._mark = mark
        if subject in self.__marks.keys():
            self.__marks[subject] = mark
        else:
            raise NameError(f"No subject named {subject}")
        
    def get_test(self, test, subject: str):
        self._test = test
        if subject in self.__marks.keys():
            self.__tests[subject] = test
        else:
            raise NameError(f"No subject named {subject}")
        
    def get_average_test(self) -> float:
        average: float = 0.0
        count = 0
        for _, j in self.__tests.items():
            average += j
            if j != 0:
                count += 1
        average /= count + 1
        return average.__round__(2)
    
    def get_average_mark(self) -> float:
        average: float = 0.0
        count = 0
        for _, j in self.__marks.items():
            average += j
            if j != 0:
                count += 1
        average /= count + 1
        return average.__round__(2)

if __name__ == "__main__":
    std = Student("Mike Wazovcki", 16, 8)
    std.get_mark(5, 'Physics')
    std.get_mark(5, "Biology")
    std.get_test(99, "Physics")
    std.get_test(100, "Biology")
    print(std.get_average_mark())
    print(std.get_average_test())    
