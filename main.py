
import os
import sys
from itertools import zip_longest


def file_to_list(filename, file_location):
    l_list = []

    file_path = os.path.join(file_location, filename)

    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            l_list.append(line.strip())

    return l_list


def local_file_to_list(filename):
    script_dir = os.path.dirname(__file__)
    return file_to_list(filename, script_dir)


class FrequentWordLoader:

    def __init__(self):
        self.m_word_list = []

    def load_word_list(self):
        self.m_word_list = local_file_to_list("words2.txt")

    def get_word_list(self):
        return self.m_word_list


class Word:

    def __init__(self):
        self.word = ""
        self.meaningful_ngrams = []

    def set_word(self, word):
        self.word = word

    def add_meaningful_ngram(self, ngram):
        print("adding_meaningful_ngram '", ngram, "' to word '", self.word, "'")
        self.meaningful_ngrams.append(ngram)

    def get_word(self):
        return self.word


class NgramsLoader:

    def __init__(self):
        self.ngrams = []
        self.bigrams = []
        self.trigrams = []
        self.tetragrams = []

    def load_bigrams(self):
        self.bigrams = local_file_to_list("bigrams.txt")

    def load_trigrams(self):
        self.trigrams = local_file_to_list("trigrams.txt")

    def load_tetragrams(self):
        self.tetragrams = local_file_to_list("tetragrams.txt")

    def load_ngrams(self):
        self.load_bigrams()
        self.load_trigrams()
        self.load_tetragrams()
        if not self.bigrams or not self.trigrams or not self.tetragrams:
            print("At least one of the lists is empty. Exiting script.")
            sys.exit(1)

        self.ngrams = [item for sublist in zip_longest(
            self.bigrams, self.trigrams, self.tetragrams) for item in sublist if item is not None]
        print(self.ngrams)

    def get_sorted_ngrams(self):
        return self.ngrams


class Algorithm:

    def __init__(self):
        self.ngrams = []
        self.words_sorted_by_freq = []
        self.resulting_word_objs = []
        self.meaningful_ngrams = []
        self.resulting_words = []

    def set_sorted_ngrams(self, ngrams):
        self.ngrams = ngrams

    def set_sorted_word_list(self, words):
        self.words_sorted_by_freq = words

    def get_result_words_list(self):
        return self.resulting_words

    def get_meaningful_ngrams_list(self):
        return self.meaningful_ngrams

    def run(self):
        while len(self.resulting_word_objs) < 200:
            curr_ngram = self.ngrams.pop(0)
            print("curr_ngram: '", curr_ngram, "'")
            self.meaningful_ngrams.append(curr_ngram)
            self.add_ngram_to_word_list(curr_ngram)
        self.translate_word_objs_list_to_words_list()

    def add_ngram_to_word_list(self, ngram):
        print("add_ngram_to_word_list: '", ngram, "'")
        if not any(ngram in obj.word for obj in self.resulting_word_objs):
            self.add_word_with_ngram_to_word_list(ngram)
        else:
            print("Ngram: '", ngram, "' already exists in resulting_word_objs")
            for word_obj in self.resulting_word_objs:
                if ngram in word_obj.word:
                    print("Adding ngram '", ngram, "' to word '", word_obj.word, "'")
                    word_obj.add_meaningful_ngram(ngram)

    def find_word_with_ngram(self, ngram):
        print("find_word_with_ngram: '", ngram, "'")
        for word in self.words_sorted_by_freq:
            if ngram in word:
                print("Found word: '", word, "'")
                return word
        print("Fatal, could not find a word with ngram '", ngram, "'")
        sys.exit(1)

    def add_word_with_ngram_to_word_list(self, ngram):
        print("add_word_with_ngram_to_word_list: ", ngram)
        new_word_obj = Word()
        word = self.find_word_with_ngram(ngram)
        new_word_obj.set_word(word)
        print("Creating new word_obj with the word '", word, "'")
        for ngram in self.meaningful_ngrams:
            if ngram in new_word_obj.word:
                print("Adding ngram '", ngram, "' to new_word_obj '", new_word_obj.word, "'")
                new_word_obj.add_meaningful_ngram(ngram)
        for word_obj in self.resulting_word_objs:
            if set(word_obj.meaningful_ngrams) <= set(new_word_obj.meaningful_ngrams):
                print(word_obj.meaningful_ngrams, "is a subset of ", new_word_obj.meaningful_ngrams)
                print("Removing word '", word_obj.word, "' from resulting_word_obj")
                self.resulting_word_objs.remove(word_obj)
        print("Adding the word '", new_word_obj.word, "' to resulting_word_objs")
        self.resulting_word_objs.append(new_word_obj)

    def translate_word_objs_list_to_words_list(self):
        for word_obj in self.resulting_word_objs:
            self.resulting_words.append(word_obj.get_word())


class FileWriter:

    def __init__(self):
        self.word_list = []
        self.ngram_list = []

    def set_word_list(self, word_list):
        print("FileWriter : set_word_list")
        print(word_list)
        self.word_list = word_list

    def set_ngram_list(self, ngram_list):
        print("FileWriter : set_ngram_list")
        print(ngram_list)
        self.ngram_list = ngram_list

    def write_word_list_to_file(self, filename, separator):
        print("FileWriter : write_word_list_to_file")
        with open(filename, "w") as file:
            file.write(separator.join(map(str, self.word_list)))

    def write_ngram_list_to_file(self, filename, separator):
        print("FileWriter : write_ngram_list_to_file")
        with open(filename, "w") as file:
            file.write(separator.join(map(str, self.ngram_list)))


class Main:

    def __init__(self):
        self.frequent_words_loader = FrequentWordLoader()
        self.ngrams_loader = NgramsLoader()
        self.main_algorithm = Algorithm()
        self.file_writer = FileWriter()

    def run(self):
        self.frequent_words_loader.load_word_list()
        self.ngrams_loader.load_ngrams()
        self.main_algorithm.set_sorted_word_list(self.frequent_words_loader.get_word_list())
        self.main_algorithm.set_sorted_ngrams(self.ngrams_loader.get_sorted_ngrams())
        self.main_algorithm.run()
        self.file_writer.set_word_list(self.main_algorithm.get_result_words_list())
        self.file_writer.set_ngram_list(self.main_algorithm.get_meaningful_ngrams_list())
        self.file_writer.write_word_list_to_file("output.txt", " ")
        self.file_writer.write_ngram_list_to_file("output_ngram.txt", " ")


if __name__ == '__main__':
    main = Main()
    main.run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
