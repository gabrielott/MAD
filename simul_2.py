#!/usr/bin/env python3

from numpy.random import exponential as randexp
from functools import reduce

import sys

ARRIVAL = 0
DEPARTURE = 1

class E():
    def __init__(self, k, t):
        self.k = k
        self.t = t

    def __str__(self):
        return f"({self.k}, {self.t})"

class C():
    def __init__(self, a, s):
        self.a = a
        self.s = s

    def __str__(self):
        return f"({self.a}, {self.s})"

def append_sort(l, e):
    l.append(e)
    l.sort(key=lambda a: a.t, reverse=True)

def run():

    inv_lambda = float(sys.argv[1])
    inv_mi = float(sys.argv[2])

    FULL = 3
    EMPTY = 0

    n = 0
    events = []

    for _ in range(FULL + 1):
        events.append(E(ARRIVAL, 0))

    clients = []
    clients_index = 0
    sum_client_average = 0
    last_t = 0
    graph_data = []

    last_full = None
    full_intervals = []

    for _ in range(400):
        e = events.pop()
        graph_data.append((last_t, n))
        graph_data.append((e.t, n))
        sum_client_average += n * (e.t - last_t)

        if e.k == ARRIVAL:
            n += 1
            clients.append(C(e.t, None))
            append_sort(events, E(ARRIVAL, e.t + randexp(inv_lambda)))
            if n == 1:
                clients[clients_index].s = e.t
                clients_index += 1
                append_sort(events, E(DEPARTURE, e.t + randexp(inv_mi)))

            if last_full is None and n == FULL:
                print(f"comecou a contar {n}")
                last_full = e.t

        elif e.k == DEPARTURE:
            n -= 1
            if n > 0:
                clients[clients_index].s = e.t
                clients_index += 1
                append_sort(events, E(DEPARTURE, e.t + randexp(inv_mi)))

            if last_full is not None and n == EMPTY:
                print(f"parou de contar {n}")
                full_intervals.append(e.t - last_full)
                last_full = None

        last_t = e.t

    for i in clients:
        print(i)

    filtered_clients = filter(lambda x: x.s is not None, clients)
    average_wait = reduce(lambda total, x: total + (x.s - x.a), filtered_clients, 0) / len(clients)
    average_clients = sum_client_average / e.t
    average_full = sum(full_intervals) / len(full_intervals)
    print(f"Média tempo de espera: {average_wait}")
    print(f"Média clientes no sistema: {average_clients}")
    print(f"Média cheio {average_full}")

    with open("saida.csv", "w") as f:
        for d in graph_data:
            f.write(str(d)[1:-1] + "\n")

def main():
    while True:
        try:
            print("comecou")
            run()
            break
        except ZeroDivisionError:
            pass

if __name__ == "__main__":
    main()
