#global
from operator import itemgetter
import numpy as np
import pandas as pd

#local
from model.ibm_model_1 import EM
from .corpus_reader import CorpusReader

def write_results(reader : CorpusReader, ibm_em : EM, output_file : str):
    """
    for each czech word, display the top 3 most probable
    english words.

    @params reader      : CorpusReader instance
    @params ibm_em      : EM instance that contains the translation dictionary
    @params output_file : output file name
    """
    translation_table = ibm_em.to_dataframe()
    with open(output_file, "w") as file:
        for cz_word in reader.czech_words:
            #get top 3 english words that were most probable for cz_word
            best_en = translation_table[cz_word].sort_values(ascending=False)
            best_en_words = best_en[:3].index.values
            file.write(f"{cz_word}\t{' '.join(best_en_words)}\n")
