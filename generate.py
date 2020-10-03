import random
import argparse
import pickle


def parse():
    parser = argparse.ArgumentParser(description='Generate a text.')
    parser.add_argument('--model', dest='mo', required=True, help='input a path to the file with model')
    parser.add_argument('--seed', dest='seed', default='0', help='input the first word (else random)')
    parser.add_argument('--length', dest='len', required=True, help='input length')
    parser.add_argument('--output', dest='out', default='stdout', help='input a path to the directory (else stdout)')
    args = parser.parse_args()
    return args


def first_word(seed, dictionary):    # определяем первое слово
    if seed == '0':
        list_of_keys = [i for i in dictionary.keys()]
        initial_word = random.choice(list_of_keys)
    else:
        initial_word = seed
    return initial_word


def probabilities(i, dictionary, result):    # преобразуем частоты в вероятности
    sum_ = 0
    for j in dictionary[result[i]].values():
        sum_ += int(j)
    list_of_prob = [int(j) / sum_ for j in dictionary[result[i]].values()]
    return list_of_prob


def generate_chain(dictionary):
    seed = parse().seed
    length = int(parse().len)
    initial_word = first_word(seed, dictionary)
    result = list()
    result.append(initial_word)  # закинули первое слово
    for i in range(length):  # на основе имеющегося слова выбираем следующее...
        list_of_prob = probabilities(i, dictionary, result)
        list_of_values = [j for j in dictionary[result[i]].keys()]
        new_word = random.choices(list_of_values, weights=list_of_prob, k=1)
        result.append(new_word[0])  # ...закидываем его в результат, чтобы выбирать дальше уже на основе него
    result = ' '.join(result)
    return result


def open_model():
    model = parse().mo
    with open(model, 'rb') as k:
        dictionary = pickle.load(k)
    return dictionary


def save_result(result):
    output = parse().out
    if output == 'stdout':
        print(result)
    else:
        with open(output, 'w', encoding='utf-8') as k:
            print(f'{result}', file=k)


def main():
    dictionary = open_model()
    result = generate_chain(dictionary)
    save_result(result)


main()
