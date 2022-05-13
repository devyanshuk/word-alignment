#global
import os
import gzip
import shutil


class CorpusReader:

    BUFFER_LEN = 1 << 16

    def __init__(self, max_lines, verbose, lowercase, czenali_gz_path="czenali.gz"):
        """
        It's best to keep the czenali.gz file in the same
        directory the main.py file is in.

        @params max_lines : maximum number of lines to read from the corpus
        @params czenali_gz_path : path of the gzip file (corpus)
        @params lowercase : bool flag that lower cases the input token if set to true.
        """
        self.max_lines = max_lines
        self.zip_path = czenali_gz_path
        self.verbose = verbose
        self.lowercase = lowercase
        self.file = czenali_gz_path.split('.')[0]
        self.english_words = {}
        self.czech_words = {}
        self.__check_extract()
        self.__preprocess()

    def __iter__(self):
        """
        returns an iterator (eng_word, cz_word) for the first self.max_lines
        lines.
        """
        return self.__read()

    def __extract(self):
        """
        extract the given corpus file (gzip format),
        for further processing later on. use the default length (65536)
        """

        with gzip.open(self.zip_path, 'rb') as src, open(self.file, 'wb') as dest:
            shutil.copyfileobj(src, dest, self.BUFFER_LEN)
        if self.verbose: print(f"finished extracting the {self.zip_path} archive as {self.file} file")


    def __preprocess(self):
        """
        read self.max_lines number of lines and store all unique english
        words and czech words in the dictionary along with it's index.
        Used later on in the translation table for correct lookup.
        """
        eng_index = 0
        cz_index = 0
        for (eng_sentence, cz_sentence) in self.__iter__():
            # store unique words in the english cache.
            for eng in eng_sentence:
                if not eng in self.english_words:
                    self.english_words[eng] = eng_index
                    eng_index += 1

            # store unique words in the czech cache.
            for cz in cz_sentence:
                if not cz in self.czech_words:
                    self.czech_words[cz] = cz_index
                    cz_index += 1
        if self.verbose: print("finished adding unique english and czech words to the english_words and the czech_words set")


    def __check_extract(self):
        if not os.path.isfile(self.file):
            if self.verbose: print(f"{self.file} file not present. extracting the {self.zip_path} archive")
            self.__extract()
        else:
            if self.verbose: print(f"The {self.file} file was present. Extracting of {self.zip_path} file not necessary")

    def __read(self):
        """
        extract and return an iterable type to functions
        requesting it.
        """
        with open(self.file, 'r', encoding="utf8") as inp_file:

            current_line = 0

            while current_line < self.max_lines:
                
                token = inp_file.readline().split('\t')

                if self.lowercase:
                    token[0] = token[0].lower()
                    token[1] = token[1].lower()

                yield (token[0].split(), token[1].split())

                current_line += 1

