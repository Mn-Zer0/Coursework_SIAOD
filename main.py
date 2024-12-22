# Метод в лоб
PEAK_HOURS = [(7, 9), (17, 19)]
WORK_DURATION = 9
LONG_BREAK = 1
SHORT_BREAK = 0.25
BREAK_INTERVAL = 3

drivers = [
    {"name": "Водитель 1", "start_time": 6, "category": "A"},
    {"name": "Водитель 2", "start_time": 7, "category": "A"},
    {"name": "Водитель 3", "start_time": 8, "category": "B"},
    {"name": "Водитель 4", "start_time": 10, "category": "A"},
    {"name": "Водитель 5", "start_time": 11, "category": "B"},
    {"name": "Водитель 6", "start_time": 13, "category": "B"},
    {"name": "Водитель 7", "start_time": 16, "category": "A"},
    {"name": "Водитель 8", "start_time": 18, "category": "B"},
]


def is_rush_hour(hour):
    return any(start <= hour < end for start, end in PEAK_HOURS)


def breaks_distribution(work_hours, driver_type):
    breaks = []
    non_peak_hours = [hour for hour in work_hours if not is_rush_hour(hour)]

    if driver_type == "A":
        for i, hour in enumerate(work_hours):
            if hour in non_peak_hours and i >= 4:
                breaks.append(hour)
                break
    elif driver_type == "B":
        first_break, second_break = None, None
        for i, hour in enumerate(work_hours):
            if hour in non_peak_hours and i >= 2:
                if first_break is None:
                    first_break = hour
                elif (hour - first_break) % 24 >= BREAK_INTERVAL:
                    second_break = hour
                    break
        if first_break:
            breaks.append(first_break)
        if second_break:
            breaks.append(second_break)
    return breaks


def get_driver_schedule(driver):
    schedule = {}
    work_start = driver['start_time']
    work_end = (work_start + WORK_DURATION) % 24
    work_hours = [(work_start + i) % 24 for i in range(WORK_DURATION)]
    breaks = breaks_distribution(work_hours, driver['category'])

    for hour in work_hours:
        if hour == work_hours:
            schedule[hour] = 'Начало смены'
        elif hour in breaks:
            schedule[hour] = 'Перерыв'
        elif is_rush_hour(hour):
            schedule[hour] = 'Поездка (час пик)'
        else:
            schedule[hour] = 'Поездка'

    schedule[work_end] = 'Окончание смены'
    return schedule


def create_schedule():
    all_schedules = {}
    for driver in drivers:
        all_schedules[driver['name']] = get_driver_schedule(driver)
    return all_schedules


def display_schedule(schedule):
    for driver, hours in schedule.items():
        print(f"\nТаблица для {driver}:")
        for hour, activity in sorted(hours.items()):
            print(f"{hour:02d}:00 - {activity}")


if __name__ == "__main__":
    schedule = create_schedule()
    print(schedule)
    display_schedule(schedule)


# Генетический алгоритм
import random
import copy

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1


def create_driver_schedule(driver):
    schedule = {}
    shift_start = driver['start']
    shift_end = (shift_start + WORK_DURATION) % 24
    shift_hours = [(shift_start + i) % 24 for i in range(WORK_DURATION)]
    breaks = [shift_hours[4]]

    for hour in shift_hours:
        if hour == shift_start:
            schedule[hour] = 'Начало смены'
        elif hour in breaks:
            schedule[hour] = 'Перерыв'
        elif is_rush_hour(hour):
            schedule[hour] = 'Поездка (час пик)'
        else:
            schedule[hour] = 'Поездка'

    schedule[shift_end] = 'Окончание смены'
    return schedule


def generate_random_schedule():
    random_schedule = []
    for driver in drivers:
        shift_start = random.randint(6, 18)
        driver_copy = copy.deepcopy(driver)
        driver_copy['start'] = shift_start
        random_schedule.append(driver_copy)
    return random_schedule


def fitness(schedule):
    penalty = 0
    peak_hours_coverage = 0

    for driver in schedule:
        shift = get_driver_schedule(driver)
        for hour, task in shift.items():
            if is_rush_hour(hour) and task == 'Поездка (час пик)':
                peak_hours_coverage += 1
            if task == 'Перерыв' and is_rush_hour(hour):
                penalty += 10

    return peak_hours_coverage - penalty


def crossover(parent1, parent2):
    child = []
    for d1, d2 in zip(parent1, parent2):
        if random.random() > 0.5:
            child.append(copy.deepcopy(d1))
        else:
            child.append(copy.deepcopy(d2))
    return child


def mutate(schedule):
    for driver in schedule:
        if random.random() < MUTATION_RATE:
            driver['start'] = random.randint(6, 18)
    return schedule


def genetic_algorithm():
    population = [generate_random_schedule() for _ in range(POPULATION_SIZE)]

    for generation in range(GENERATIONS):
        population.sort(key=lambda s: -fitness(s))
        print(f"Generation {generation}, Best Fitness: {fitness(population[0])}")

        new_population = population[:10]

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:20], 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

    best_schedule = population[0]
    return best_schedule


if __name__ == "__main__":
    best_solution = genetic_algorithm()
    print("Лучшее расписание:")
    for driver in best_solution:
        print(f"\nТаблица для {driver['name']}: Начало смены в {driver['start']}:00")

        # Вывод расписания для каждого водителя
        driver_schedule = get_driver_schedule(driver)
        for hour in sorted(driver_schedule.keys()):
            print(f"{hour:02d}:00 - {driver_schedule[hour]}")
