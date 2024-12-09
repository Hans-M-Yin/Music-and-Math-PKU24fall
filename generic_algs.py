from music21 import *

class stream_with_score:
    def __init__(self, strm, scre):
        self.stream = stream
        self.score = scre
    def __lt__(self, other):
        return self.score < other.score

def fitness_function (melody:stream) -> float:
    return 0.0

def run_generic_algorithm(melodies:list[stream.Stream]) -> stream:
    return stream.Stream()