from music21 import *

class stream_with_score:
    def __init__(self, strm):
        self.stream = strm
        self.score = fitness_function(strm)
    

def fitness_function (melody:stream) -> float:
    return 0.0

def call_operator (melody:stream) -> stream.Stream:
    return stream.Stream()

def run_generic_algorithm(melodies:list[stream.Stream], iterations = 100, criteria = 1.0, total = 20, fraction = 0.5) -> stream:
    iter = 0
    best_performance = 100.0

    population = []
    for strm in melodies:
        population.append(stream_with_score(strm))
    while iter < iterations and best_performance > criteria:
        population = sorted(population, key=lambda x: x.score)
        population = population[:total]
        best_performance = population[0].score

        for i in range(int(total*fraction)):
            n_strm = call_operator(population[i])
            population.append(stream_with_score(n_strm))

    return population[0].stream