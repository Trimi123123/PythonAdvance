from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self._weight = weight
        self._height = height


    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self._weight = value
        else:
            raise ValueError("Weight must be positive")


    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value > 0:
            self._height = value
        else:
            raise ValueError("Height must be positive")

    @abstractmethod
    def calculate_bmi(self):
        pass

    @abstractmethod
    def get_bmi_category(self):
        pass

    def print_info(self):
        bmi = self.calculate_bmi()
        category = self.get_bmi_category()
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"BMI: {bmi:.2f}")
        print(f"Category: {category}")
        print("-" * 30)


class Adult(Person):

    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "Underweight"
        elif bmi < 24.9:
            return "Normal weight"
        elif bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"


class Child(Person):

    def calculate_bmi(self):
        return (self.weight / (self.height ** 2)) * 1.3

    def get_bmi_category(self):
        bmi = self.calculate_bmi()

        if bmi < 14:
            return "Underweight"
        elif bmi < 18:
            return "Normal weight"
        elif bmi < 24:
            return "Overweight"
        else:
            return "Obese"



class BMIApp:
    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def collect_user_data(self):
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        weight = float(input("Enter weight (kg): "))
        height = float(input("Enter height (m): "))

        if age >= 18:
            person = Adult(name, age, weight, height)
        else:
            person = Child(name, age, weight, height)

        self.add_person(person)

    def print_results(self):
        print("\nBMI RESULTS")
        print("=" * 30)
        for person in self.people:
            person.print_info()

    def run(self):
        while True:
            self.collect_user_data()
            choice = input("Add another person? (y/n): ").lower()
            if choice != 'y':
                break

        self.print_results()



if __name__ == "__main__":
    app = BMIApp()
    app.run()