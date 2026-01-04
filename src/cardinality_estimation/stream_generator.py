from argparse import ArgumentParser
from random import sample
from os import path
from numpy.random import choice

STREAM_DIR = "./synthetic_datasets"
VOCABULARY_FILE = "synthetic.dat"
STREAM_FILE = "synthetic.txt"
VOCABULARY_SIZE = 20_408
STREAM_SIZE = VOCABULARY_SIZE * 20
ALPHA = 0.6

def generate_vocabulary(output_path, vocabulary_size):
    values = sample(range(1, vocabulary_size*10), k=vocabulary_size)
    with open(output_path, "w") as out:
        out.writelines(f"{value}\n" for value in values)

def generate_stream(input_path, output_path, alpha, stream_size):
    with open(input_path, "r") as vocabulary_file:
        vocabulary = vocabulary_file.readlines()
    vocabulary_size = len(vocabulary)
    normalization_constant = 1/(sum(1/(i**alpha) for i in range(1, vocabulary_size + 1)))
    probabilities = [normalization_constant/(i**alpha) for i in range(1, vocabulary_size + 1)]
    stream = choice(a=vocabulary, p=probabilities, size=stream_size)
    with open(output_path, "w") as out:
        out.writelines(f"{value}" for value in stream)

if __name__ == '__main__':
    parser = ArgumentParser(prog="Data stream generator", description="Generate data stream or vocabularies")
    parser.add_argument("-m", "--mode", choices=["stream", "vocabulary"], default="stream")
    args = parser.parse_args()
    vocabulary_path = path.join(STREAM_DIR, VOCABULARY_FILE)
    if args.mode == "stream":
        stream_path = path.join(STREAM_DIR, STREAM_FILE)
        generate_stream(input_path=vocabulary_path, output_path=stream_path, alpha=ALPHA, stream_size=STREAM_SIZE)
    elif args.mode == "vocabulary":
        generate_vocabulary(vocabulary_path, VOCABULARY_SIZE)