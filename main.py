import random as rnd
import numpy as np
import prettytable

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Department:

    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self):
        return self._name

    def get_courses(self):
        return self._courses


class Class:

    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None

    def get_id(self):
        return self._id

    def get_dept(self):
        return self._dept

    def get_course(self):
        return self._course

    def get_instructor(self):
        return self._instructor

    def get_meetingTime(self):
        return self._meetingTime

    def get_room(self):
        return self._room

    def set_instructor(self, instructor):
        self._instructor = instructor

    def set_meetingTime(self, meetingTime):
        self._meetingTime = meetingTime

    def set_room(self, room):
        self._room = room

    def __str__(self) -> str:
        return str(self._dept.get_name()) + ',' + str(self._course.get_number()) + ',' + \
               str(self._room.get_number()) + ',' + str(self._instructor.get_id()) + ',' + str(
            self._meetingTime.get_id())


class Course:

    def __init__(self, number, name, instructors, maxNumberOfStudents):
        self._number = number
        self._name = name
        self._instructors = instructors
        self._maxNumberOfStudents = maxNumberOfStudents

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_instructors(self):
        return self._instructors

    def get_maxNumbOfStudents(self):
        return self._maxNumberOfStudents

    def __str__(self):
        return self._name


class Instructor:

    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name


class Room:

    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_number(self):
        return self._number

    def get_seatingCapacity(self):
        return self._seatingCapacity


class MeetingTime:

    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self):
        return self._id

    def get_time(self):
        return self._time


class Data:
    ROOMS = [['R1', 25], ['R2', 45], ['R3', 35]]
    MEETING_TIMES = [['MT1', 'MWF 09:00 - 10:00'],
                     ['MT2', 'MWF 10:00 - 11:00'],
                     ['MT3', 'TTH 09:00 - 10:30'],
                     ['MT4', 'TTH 10:30 - 12:00']]

    INSTRUCTORS = [['I1', 'Dr James Web'],
                   ['I2', 'Dr Mike Brown'],
                   ['I3', 'Dr Steve Day'],
                   ['I4', 'Dr Jane Doe']]

    def __init__(self):
        self._rooms = []
        self._meetingTimes = []
        self._instructors = []

        for i in range(len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))

        for i in range(len(self.MEETING_TIMES)):
            self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))

        for i in range(len(self.INSTRUCTORS)):
            self._instructors.append(Instructor(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))

        course1 = Course("C1", "325K", [self._instructors[0], self._instructors[1]], 25)
        course2 = Course("C2", "320K", [self._instructors[0], self._instructors[1]], 35)
        course3 = Course("C3", "462k", [self._instructors[0], self._instructors[1]], 25)
        course4 = Course("C4", "464K", [self._instructors[2], self._instructors[3]], 30)
        course5 = Course("C5", "360C", [self._instructors[3]], 35)
        course6 = Course("C6", "303K", [self._instructors[0], self._instructors[2]], 45)
        course7 = Course("C7", "303L", [self._instructors[1], self._instructors[3]], 45)

        self._courses = [course1, course2, course3, course4, course5, course6, course7]

        dept1 = Department("MATH", [course1, course3])
        dept2 = Department("EE", [course2, course4, course5])
        dept3 = Department("PHY", [course6, course7])

        self._depts = [dept1, dept2, dept3]
        self._numberOfClasses = 0

        for i in range(len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_meetingTimes(self):
        return self._meetingTimes


class Schedule:

    def __init__(self):
        self._data = data
        self._classes = []
        self._numOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numOfConflicts(self):
        return self._numOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False

        return self._fitness

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(len(depts)):
            courses = depts[i].get_courses()
            for j in range(len(courses)):
                new_class = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                new_class.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(data.get_meetingTimes()))])
                new_class.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                new_class.set_instructor(
                    courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(new_class)

        return self

    def calculate_fitness(self):
        self._numOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents():
                self._numOfConflicts += 1

            for j in range(len(classes)):
                if j >= i:
                    if \
                            classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_id() != \
                                    classes[j].get_id():
                        if classes[i].get_room() == classes[j].get_room():
                            self._numOfConflicts += 1

                        if classes[i].get_instructor() == classes[j].get_instructor():
                            self._numOfConflicts += 1

        return 1 / (1.0 * (self._numOfConflicts + 1))

    def __str__(self) -> str:
        return_value = ''
        for i in range(len(self._classes) - 1):
            return_value += str(self._classes[i]) + ', '

        return_value += str(self._classes[len(self._classes) - 1])

        return return_value


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])

        i = NUMB_OF_ELITE_SCHEDULES

        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))

            i += 1

        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])

        return population

    def _crossover_schedule(self, schedule1, schedule2):
        self.is_not_used()
        crossover_schedule = Schedule().initialize()
        for i in range(0, len(crossover_schedule.get_classes())):
            if rnd.random() > 0.5:
                crossover_schedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossover_schedule.get_classes()[i] = schedule2.get_classes()[i]

        return crossover_schedule

    def _mutate_schedule(self, mutateSchedule):
        self.is_not_used()
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        self.is_not_used()
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1

        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

        return tournament_pop

    def is_not_used(self):
        pass


class DisplayMgr:

    def print_available_data(self):
        self.is_not_used()
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()

    def print_dept(self):
        self.is_not_used()
        depts = data.get_depts()
        available_depts_table = prettytable.PrettyTable(['dept', 'courses'])

        for i in range(len(depts)):
            courses = depts.__getitem__(i).get_courses()
            temp_str = "["

            for j in range(len(courses) - 1):
                temp_str += courses[j].__str__() + ", "
            temp_str += courses[len(courses) - 1].__str__() + "]"
            available_depts_table.add_row([depts.__getitem__(i).get_name(), temp_str])

        print(available_depts_table)

    def print_course(self):
        self.is_not_used()
        available_course_table = prettytable.PrettyTable(['id', 'course', 'maxS', 'ins'])
        courses = data.get_courses()

        for i in range(len(courses)):
            instructors = courses[i].get_instructors()
            temp_str = ""

            for j in range(len(instructors) - 1):
                temp_str += instructors[j].__str__() + ", "
            temp_str += instructors[len(instructors) - 1].__str__()
            available_course_table.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), temp_str]
            )

        print(available_course_table)

    def print_room(self):
        self.is_not_used()
        availableRoomsTable = prettytable.PrettyTable(['room', 'max'])
        rooms = data.get_rooms()
        for i in range(len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])

        print(availableRoomsTable)

    def print_instructor(self):
        self.is_not_used()
        available_instructor_table = prettytable.PrettyTable(['id', 'ins'])
        instructors = data.get_instructors()

        for i in range(len(instructors)):
            available_instructor_table.add_row([instructors[i].get_id(), instructors[i].get_name()])
        print(available_instructor_table)

    def print_meeting_times(self):
        self.is_not_used()
        availableMeetingTimeTable = prettytable.PrettyTable(['id', 'mt'])
        meetingTimes = data.get_meetingTimes()

        for i in range(len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])

        print(availableMeetingTimeTable)

    def print_generation(self, population):
        self.is_not_used()
        table1 = prettytable.PrettyTable(['Schedule #', 'Fitness', '# of conflicts',
                                          'classes [dept,class,room,instructor,meeting-time]'])
        schedules = population.get_schedules()

        for i in range(len(schedules)):
            table1.add_row([str(i + 1), round(schedules[i].get_fitness(), 3), schedules[i].get_numOfConflicts(),
                            schedules[i].__str__()])

        print(table1)

    def print_schedule_as_table(self, schedule):
        self.is_not_used()
        table1 = prettytable.PrettyTable(['Class #', 'Dept', 'Courses (number, max # of students)', "Room (Capacity)",
                                          "Instructor (Id)", "Meeting Time (Id)"])
        classes = schedule.get_classes()

        for i in range(len(classes)):
            course = classes[i].get_course().get_name() + " (" + classes[i].get_course().get_number() + ", " + \
                     str(classes[i].get_course().get_maxNumbOfStudents()) + ")"
            instructor = classes[i].get_instructor().get_name() + " (" + classes[i].get_instructor().get_id() + ")"
            room = classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")"
            meeting_time = classes[i].get_meetingTime().get_time() + " (" + classes[i].get_meetingTime().get_id() + ")"

            table1.add_row(
                [classes[i].get_id(), classes[i].get_dept().get_name(), course,
                 room, instructor, meeting_time]
            )

        print(table1)

    def print_mean(self, population):
        self.is_not_used()
        schedules = population.get_schedules()
        fitness_scores = []

        for i in range(len(schedules)):
            fitness_scores.append(round(schedules[i].get_fitness(), 3))

        print("> Mean= ", np.array(fitness_scores).mean())

    def print_std(self, population):
        self.is_not_used()
        schedules = population.get_schedules()
        fitness_scores = []

        for i in range(len(schedules)):
            fitness_scores.append(round(schedules[i].get_fitness(), 3))

        print("> Standard Deviation= ", np.array(fitness_scores).std())

    def is_not_used(self):
        pass


data = Data()
display = DisplayMgr()
display.print_available_data()

generation_number = 0
print("\n> Generation #", generation_number)

population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
display.print_generation(population)
geneticAlgorithm = GeneticAlgorithm()

while population.get_schedules()[0].get_fitness() != 1.0:
    generation_number += 1
    print("\n> Generation #", generation_number)
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    display.print_generation(population)
    display.print_schedule_as_table(population.get_schedules()[0])
    display.print_mean(population)
    display.print_std(population)
