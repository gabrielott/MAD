#!/usr/bin/env python3

from numpy.random import exponential as randexp
from functools import reduce

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
    n = 0
    events = [E(ARRIVAL, randexp(1))]
    clients = []
    clients_index = 0
    sum_client_average = 0
    last_t = 0

    for _ in range(40):
        e = events.pop()
        sum_client_average += n * (e.t - last_t)

        if e.k == ARRIVAL:
            n += 1
            clients.append(C(e.t, None))
            append_sort(events, E(ARRIVAL, e.t + randexp(1)))
            if n == 1:
                clients[clients_index].s = e.t
                clients_index += 1
                append_sort(events, E(DEPARTURE, e.t + randexp(1)))

        elif e.k == DEPARTURE:
            n -= 1
            if n > 0:
                clients[clients_index].s = e.t
                clients_index += 1
                append_sort(events, E(DEPARTURE, e.t + randexp(1)))

        last_t = e.t

    for i in clients:
        print(i)

    filtered_clients = filter(lambda x: x.s is not None, clients)
    average_wait = reduce(lambda total, x: total + (x.s - x.a), filtered_clients, 0) / len(clients)
    average_clients = sum_client_average / e.t
    print(f"Média tempo de espera: {average_wait}")
    print(f"Média clientes no sistema: {average_clients}")

def main():
    run()

if __name__ == "__main__":
    main()
