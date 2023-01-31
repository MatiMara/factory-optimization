import math

import matplotlib.pyplot as plt
import random as rd
import string
import numpy as np


class Specimen:
    def __init__(self, sectors: dict, points: float):
        self.sectors = sectors
        self.points = points

    def __repr__(self):
        return f"Specimen({self.points}, {self.sectors})"

    def __str__(self):
        return f"Specimen({self.points}, {self.sectors})"


machines_x = [15, 15, 15, 15, 15, 15, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23]
machines_y = [23, 30, 37, 44, 51, 58, 9, 16, 23, 30, 37, 44, 51, 58, 65, 72]
machine_names = ["W-41", "W-31", "W-23", "W-21", "W-13", "W-11", "M-50", "W-44",
                 "W-42", "W-32", "W-24", "W-22", "W-14", "W-12", "R-02", "R-01"]
machines_dict = {name: (machines_x[i], machines_y[i]) for i, name in enumerate(machine_names)}

fig, ax = plt.subplots()
ax.scatter(machines_x, machines_y, s=1000, marker='s')
for i, txt in enumerate(machine_names):
    ax.annotate(txt, (machines_x[i], machines_y[i]), ha='center', va='center')
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(left=0, right=38)
ax.set_ylim(bottom=0, top=90)
# plt.show()

n_sectors = 5


def gen_first_gen(n_sects, mach_names, n_first_gen) -> list:
    first_gen = []
    for i in range(n_first_gen):
        rd.shuffle(mach_names)
        letters = list(string.ascii_uppercase)[:n_sects]
        sectors = {letter: mach_names[it::n_sects] for it, letter in enumerate(letters)}
        first_gen.append(Specimen(sectors=sectors, points=0.0))
    return first_gen


def target(machines: dict, sectors: dict) -> tuple:
    """Average path"""
    avgs_of_paths = []
    for sector in sectors.keys():
        paths = []
        for i in range(len(sectors[sector])):
            cords0 = machines[sectors[sector][i-1]]
            cords1 = machines[sectors[sector][i]]
            path = math.sqrt((cords0[0] - cords1[0])**2 + (cords0[1] - cords1[1])**2)
            paths.append(path)
        avg_path = sum(paths)/len(paths)
        avgs_of_paths.append(avg_path)
    avg = sum(avgs_of_paths)/len(avgs_of_paths)
    std = float(np.std(avgs_of_paths))
    return avg, std


def fitness(avg: float, std: float) -> float:
    """The more points the better."""
    points = 1.0/(avg + std)
    return points


def selection(population: list, percentage_accepted: int) -> list:
    selected_population = population[:round(len(population) * percentage_accepted / 100)]
    return selected_population


def crossover():

    pass


def mutation():
    pass


def main() -> None:
    n_first_gen = 100
    percentage_accepted = 10
    population = gen_first_gen(n_sectors, machine_names, n_first_gen)
    print(f"population[0] = {population[0]}")
    print(f"machines = {machines_dict}")
    print(population)
    for i in range(1):  # Main loop of algorithm
        for j, specimen in enumerate(population):
            avg, std = target(machines_dict, specimen.sectors)
            population[j].points = fitness(avg, std)
        population.sort(key=lambda x: x.points, reverse=True)
        print(len(population), [specimen.points for specimen in population])
        selected_population = selection(population=population,
                                        percentage_accepted=percentage_accepted)
        print(len(selected_population), selected_population)


main()





