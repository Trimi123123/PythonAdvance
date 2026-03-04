class DigitalSchool:
    def __init__(self, name, city, state, courses):
        self.__name = name
        self.__city = city
        self.__state = state
        self.__courses = courses


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value


    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value


    @property
    def courses(self):
        return self.__courses

    @courses.setter
    def courses(self, value):
        self.__courses = value

    def show_school_info(self):
        return {
            "name": self.__name,
            "city": self.__city,
            "state": self.__state,
            "courses": self.__courses
        }

    def organize_hackathon(self):
        print("Hackathon details will be announced soon.")


class DS_Prishtina(DigitalSchool):
    def __init__(self, name, city, state, courses, student_number):
        super().__init__(name, city, state, courses)
        self.__student_number = student_number

    @property
    def student_number(self):
        return self.__student_number

    @student_number.setter
    def student_number(self, value):
        self.__student_number = value

    def SCF(self):
        print("Spring Code Fest (SCF) is organized by DS_Prishtina every year!")

    def organize_hackathon(self):
        print("DS_Prishtina is organizing a 24-hour coding hackathon for all students!")



ds_prishtina = DS_Prishtina(
    name="Digital School Prishtina",
    city="Prishtina",
    state="Kosovo",
    courses=["Python", "Web Development", "Data Science"],
    student_number=350
)


ds_prishtina.SCF()
ds_prishtina.organize_hackathon()

print(f"The number of students in DS_Prishtina is {ds_prishtina.student_number}")


print(ds_prishtina.show_school_info())


