#global
import numpy as np
import pandas as pd
from collections import defaultdict

#local
from iohandler.corpus_reader import CorpusReader

DEF_DEBUG = False

class EM:

    def __init__(self, reader : CorpusReader, num_iterations : int, verbose : bool):
        """
        { english_word : { cz_1 : translation_probability1, cz2 : translation_probabiltiy2 } }
        
        @params reader          : instance of the CorpusReader class
        @params num_iterations  : number of iterations to perform for the unsupervised learning
                                 process
        @params verbose         : verbose flag
        """
        self.reader = reader
        self.num_iterations = num_iterations
        self.verbose = verbose
        self.translation_table = self.__initialize_translation_table_uniformly()


    def __repr__(self):
        """
        return pandas dataframe repr when self.__repr__() is called.
        """
        return self.to_dataframe().__repr__()


    def __to_numpy_array(self):
        """
        convert the translation table to a numpy matrix for calculating the maximum probabilities faster.
        """
        translation_data = np.zeros(
            shape=[len(self.reader.english_words.keys()), len(self.reader.czech_words.keys())])

        for eng in self.reader.english_words.keys():
            cz_dict = self.translation_table[eng]
            assert isinstance(cz_dict, defaultdict)

            for cz, probability in cz_dict.items():
                eng_index = self.reader.english_words[eng]
                cz_index = self.reader.czech_words[cz]
                translation_data[eng_index][cz_index] = probability

        # ensure that the probabilities are in the right place
        if DEF_DEBUG:
            if self.verbose:
                print("Checking if the translation dictionary was properly converted to numpy array...")
            for eng_word, cz_dict in self.translation_table.items():
                for cz_word, probability in cz_dict.items():
                    en_index = self.reader.english_words[eng_word]
                    cz_index = self.reader.czech_words[cz_word]
                    assert translation_data[en_index][cz_index] == probability
            if self.verbose:
                print("Probabilities are placed in the array in correct places")

        return translation_data

    def to_dataframe(self):
        """
        represent the translation table as a pandas dataframe since it's easier to visualize
        using this library. the rows are labelled by the english words and the columns are
        labelled by czech words.
        """
        if self.verbose: print("converting translation table to pandas dataframe for better visualization...")
        translation_data = self.__to_numpy_array()
        dataframe = pd.DataFrame(
            data=translation_data,
            index=self.reader.english_words.keys(),
            columns=self.reader.czech_words.keys())
        if self.verbose: print("finished converting translation table to pandas dataframe")
        return dataframe

    def __initialize_translation_table_uniformly(self):
        """
        Initialize a translation table uniformly. Instead of using a pre-allocated
        array, we use a dynamically added dictionary for making the algorithm better
        in terms of readability.
        """
        return { 
            eng_word : defaultdict(lambda : float(1 / len(self.reader.czech_words)))
            for eng_word in self.reader.english_words.keys()
        }


    def iterate(self):
        """
        The IBM model 1 EM algorithm for word alignment.
        Performs the expectation step followed by the maximization
        step.
        """

        for epoch in range(self.num_iterations):
            # sets count, total and total_s to 0
            count = defaultdict(lambda : 0.0)
            total = defaultdict(lambda : 0.0)
            total_s = defaultdict(lambda : 0.0)

            for (eng_sentence, cz_sentence) in self.reader:

                for e_word in eng_sentence:
                    for c_word in cz_sentence:
                        total_s[e_word] += self.translation_table[e_word][c_word]
                
                for e_word in eng_sentence:
                    for c_word in cz_sentence:
                        temp = self.translation_table[e_word][c_word] / total_s[e_word]
                        count[(e_word, c_word)] += temp
                        total[c_word] += temp

            for (eng, cz) in count:
                    self.translation_table[eng][cz] = count[(eng, cz)] / total[cz]

            if self.verbose: print(f"epoch {epoch} finished.")

        if self.verbose:
           print("finished updating the translation table")

        if DEF_DEBUG:
            print(f"translation table = {self.to_dataframe().round(decimals=3)}")

                
