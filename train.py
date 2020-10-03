import sys
import re
import argparse
import glob
import pickle


def parse():
    parser = argparse.ArgumentParser(description='Create a model.')
    parser.add_argument('--input-dir', dest='inp', default='stdin', help='input a path to the directory (else stdin)')
    parser.add_argument('--model', dest='mo', required=True, help='input a path to the file with model')
    parser.add_argument('--lc', action='store_true', default=False, help='converts text to lowercase')
    args = parser.parse_args()
    return args


def split_words(line, lowercase):    # разбиваем строку на слова, опционально приводим к нижнему регистру
    if lowercase:
        line = line.lower
    line = re.sub(r'[^A-Za-zА-Яа-яЁё ]+', '', line)
    line = re.sub(r'\s+', ' ', line)
    line = line.strip()
    words = line.split(' ')
    return words


def create_dict(words, dictionary, ending_word):    # создаем словарь {слово1 : {слово2 : частота}} для строки
    for i in range(1, len(words)):
        word2 = words[i]
        if i == 1:
            word1 = ending_word
        elif i == len(words) - 1:
            word1 = words[i-1]
            ending_word = word2
        else:
            word1 = words[i-1]
        if word1 != "":
            if dictionary.get(word1) is not None:
                if dictionary.get(word1).get(word2) is not None:
                    dictionary.get(word1)[word2] += 1
                else:
                    dictionary.get(word1).setdefault(word2, 1)
            else:
                default = {word2: 1}
                dictionary.setdefault(word1, default)
    return dictionary, ending_word


def create_model(input_stream, dictionary):    # словарь для файла
    ending_word = ''
    first_file_flag = 0
    for line in input_stream:
        words = split_words(line, parse().lc)
        if first_file_flag == 0:
            ending_word = words[0]
        dictionary, ending_word = create_dict(words, dictionary, ending_word)
        first_file_flag += 1
    return dictionary


def model_from_files():    # создаем модель при считывании из папки
    dictionary = dict()
    path = parse().inp + '*'
    files = glob.glob(pathname=path)   # извлекаем все файлы из указанной директории (из-за этого не могу создать
    for name in files:                 # общую переменную input_stream - для работы с файлами надо еще их извлечь
        input_stream = open(name, encoding='utf-8')    # из папки, причем до того, как создам переменную)
        dictionary = create_model(input_stream, dictionary)
    return dictionary


def model_from_stdin():    # создаем модель при считывании из stdin
    dictionary = dict()
    ending_word = ''
    for line in sys.stdin:
        words = split_words(line, parse().lc)
        dictionary = create_dict(words, dictionary, ending_word)
    return dictionary


def train():
    if parse().inp != 'stdin':
        dictionary = model_from_files()
    else:
        dictionary = model_from_stdin()
    save_model(dictionary)


def save_model(dictionary):
    model = parse().mo
    with open(model, 'wb') as t:    # сохраняем словарь в указанный файл
        pickle.dump(dictionary, t)


train()
