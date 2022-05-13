#!/usr/bin/python3


#global
import argparse
import time

#local
from iohandler.corpus_reader import *
from iohandler.writer import write_results
from model.ibm_model_1 import EM

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--data",
                    default="czenali.gz",
                    help="Data path (gzip format)")

parser.add_argument("-o", "--output_file",
                    default="result",
                    help="Result path")

parser.add_argument("-i", "--iterations",
                    default=10,
                    type=int,
                    help="number of iterations to perform")

parser.add_argument("-n", "--num_sentences",
                    default=2000,
                    type=int,
                    help="Number of sentences to use for training")

parser.add_argument("-v", "--verbose",
                    action="store_true",
                    default=False,
                    help="verbose flag")
                
parser.add_argument("-l", "--lowercase",
                    action="store_true",
                    default=False,
                    help="use this flag if you want all sentences to be lowercased")

def main(args):
    _reader = CorpusReader(
        max_lines=args.num_sentences,
        verbose=args.verbose,
        lowercase=args.lowercase)
    if args.verbose: print("finished reading and pre-processing the corpus")

    ibm_em = EM(
        num_iterations=args.iterations,
        reader=_reader,
        verbose=args.verbose)

    if args.verbose:
        print(f"iterating {args.iterations} times to train the model. Number of lines used = {args.num_sentences}")

    start = time.perf_counter()
    ibm_em.iterate()
    end = time.perf_counter()
    if args.verbose:
        print(f"It took {(end - start):.1f} seconds to run {args.iterations} iterations on {args.num_sentences} lines")

    if args.verbose: print(f"Writing results to {args.output_file} file...")
    write_results(_reader, ibm_em, args.output_file)
    if args.verbose: print(f"Finished writing results to {args.output_file} file")


if __name__ == "__main__":
    start = time.perf_counter()
    args = parser.parse_args()
    main(args)
    end = time.perf_counter()
    if args.verbose:
        print(f"Time it took to run the program = {(end - start):.1f} seconds")