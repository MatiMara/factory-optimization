import math
import time
from copy import copy

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
    points = 1.0/avg  # + std)
    # print(avg, std)
    return points


def selection(population: list, percentage_accepted: int) -> list:
    population.sort(key=lambda x: x.points, reverse=True)
    selected_population = population[:round(len(population) * percentage_accepted / 100)]
    return selected_population


def crossover(selected_population: list, new_pop_size: int, mach_names: list) -> list:
    small_sectors_len = min(len(x) for x in selected_population[0].sectors.values())
    big_sectors_len = max(len(x) for x in selected_population[0].sectors.values())
    small_sectors = []
    big_sectors = []

    for specimen in selected_population:
        for sector in specimen.sectors.values():
            if len(sector) == small_sectors_len:
                small_sectors.append(sector)
            elif len(sector) == big_sectors_len:
                big_sectors.append(sector)
            else:
                print("error")

    if not big_sectors:
        big_sectors = small_sectors

    n_sects = len(selected_population[0].sectors.keys())
    new_population = []
    for i in range(new_pop_size):
        # rd.shuffle(mach_names)
        letters = list(string.ascii_uppercase)[:n_sects]  # Remove "A" and "B"
        sectors = {}
        sector1 = rd.choice(small_sectors)
        sector2 = rd.choice(big_sectors)
        while [i for i in sector1 if i in sector2]:
            sector1 = rd.choice(small_sectors)
            sector2 = rd.choice(big_sectors)

        let1, let2 = "A", "A"
        while let1 == let2:
            let1 = rd.choice(letters)
            letters = [letter for letter in letters if letter is not let1]
            sectors[let1] = sector1
            let2 = rd.choice(letters)
            letters = [letter for letter in letters if letter is not let2]
            sectors[let2] = sector2
        used_machines = sector1 + sector2
        not_used_machines = [m_name for m_name in mach_names if m_name not in used_machines]
        other_sectors = {letter: not_used_machines[it::(n_sects-2)] for it, letter in enumerate(letters)}
        sectors.update(other_sectors)  # Mutation
        sector_keys = list(sectors.keys())
        sector_keys.sort()
        sectors = {i: sectors[i] for i in sector_keys}
        new_population.append(mutation(Specimen(sectors=sectors, points=0.0), mach_names=mach_names))
    return new_population


def mutation(specimen: Specimen, mach_names: list, chance=0.3) -> Specimen:
    if rd.random() < chance:
        rnd_sector1 = rd.choice(list(specimen.sectors.keys()))
        rnd_sector2 = rd.choice([key for key in specimen.sectors.keys() if key != rnd_sector1])
        rnd_machine1 = rd.choice(specimen.sectors[rnd_sector1])
        rnd_machine2 = rd.choice(specimen.sectors[rnd_sector2])
        specimen.sectors[rnd_sector1] = [machine for machine in specimen.sectors[rnd_sector1] if machine != rnd_machine1]
        specimen.sectors[rnd_sector2] = [machine for machine in specimen.sectors[rnd_sector2] if machine != rnd_machine2]
        specimen.sectors[rnd_sector1].append(rnd_machine2)
        specimen.sectors[rnd_sector2].append(rnd_machine1)
        rd.shuffle(specimen.sectors[rnd_sector1])
        rd.shuffle(specimen.sectors[rnd_sector2])
    # else:
    #     rd.shuffle(mach_names)
    #     n_sects = len(specimen.sectors.keys())
    #     letters = list(string.ascii_uppercase)[:n_sects]
    #     sectors = {letter: mach_names[it::n_sects] for it, letter in enumerate(letters)}
    #     specimen = Specimen(sectors=sectors, points=0.0)
    return specimen


def select_best_specimen(population) -> Specimen:
    population.sort(key=lambda x: x.points, reverse=True)
    best_specimen = population[0]
    return best_specimen


def main() -> None:
    with open("data2.txt") as f:
        lines = f.readlines()
        machines_x = [int(number) for number in lines[1].split(",")]
        machines_y = [int(number) for number in lines[3].split(",")]
        machine_names = [name for name in lines[5].split(",")]
        n_sectors = int(lines[7])

    machine_names_scopy = machine_names.copy()
    machines_dict = {name: (machines_x[i], machines_y[i]) for i, name in enumerate(machine_names)}
    colormap = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))
    factory_plot = ax.scatter(machines_x, machines_y, s=1000, marker='s')
    for j, txt in enumerate(machine_names):
        ax.annotate(txt, (machines_x[j], machines_y[j]), ha='center', va='center')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(left=min(machines_x)-10, right=max(machines_x)+10)
    ax.set_ylim(bottom=min(machines_y)-10, top=max(machines_y)+10)
    fig.canvas.draw()
    fig.canvas.flush_events()

    n_first_gen = 100
    n_next_population = 100
    percentage_accepted = 20

    population = gen_first_gen(n_sectors, machine_names, n_first_gen)

    best_ever = Specimen(sectors={}, points=9999.0)
    best_ever_previous = copy(best_ever)
    start = time.time()
    counter = 0
    for i in range(10000):  # Main loop of algorithm
        for j, specimen in enumerate(population):
            avg, std = target(machines_dict, specimen.sectors)
            population[j].points = fitness(avg, std)

        selected_population = selection(population=population, percentage_accepted=percentage_accepted)

        best_spec = select_best_specimen(selected_population)
        if best_spec.points < best_ever.points:
            best_ever = best_spec
        if best_ever.points == best_ever_previous.points:
            counter += 1
        if counter >= 150:
            break
        best_ever_previous = copy(best_ever)
        print(f"{i}. Best specimen:\n{best_spec.points}")
        # print(f"{i}. Best ever:\n{best_ever.points}")
        print(f"Time: {time.time() - start} s")

        if i % 1 == 0:
            colors_dict = {}
            for j, sector in enumerate(best_spec.sectors.keys()):
                for m_name in best_spec.sectors[sector]:
                    colors_dict[m_name] = colormap[j]
            colors_list = [colors_dict[m_name] for m_name in machine_names_scopy]
            factory_plot.set_color(colors_list)
            fig.canvas.draw()
            fig.canvas.flush_events()

        new_population = crossover(selected_population, n_next_population, machine_names)
        population = new_population
        time.sleep(0.5)

    selected_population = selection(population=population, percentage_accepted=percentage_accepted)
    best_spec = select_best_specimen(selected_population)
    if best_spec.points < best_ever.points:
        best_ever = best_spec

    # colors_dict = {}
    # for j, sector in enumerate(best_ever.sectors.keys()):
    #     for m_name in best_ever.sectors[sector]:
    #         colors_dict[m_name] = colormap[j]
    # colors_list = [colors_dict[m_name] for m_name in machine_names_scopy]
    # factory_plot.set_color(colors_list)
    # fig.canvas.draw()
    # fig.canvas.flush_events()

    input()


if __name__ == "__main__":
    main()

