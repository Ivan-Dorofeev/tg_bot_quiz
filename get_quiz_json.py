import argparse
import json
import os
from pprint import pprint


def main():
    questions_and_answers = {}

    parser = argparse.ArgumentParser(description='Указываем папку, откуда брать файлы для словаря викторины')
    parser.add_argument('-p', '--path_to_dir', default='questions')
    args = parser.parse_args()

    counter = 0
    for dir, path, files in os.walk(args.path_to_dir):
        for file in files:
            file_path = os.path.join(dir, file)
            with open(file_path, 'r', encoding='KOI8-R') as file_for_read:
                read_file = file_for_read.readlines()
                question = ''
                answer = ''
                question_flag = False
                answer_flag = False
                for read_string in read_file:
                    if read_string.startswith('Вопрос'):
                        question_flag = True
                        continue
                    if read_string.startswith('Ответ'):
                        answer_flag = True
                        continue
                    if read_string == '\n':
                        question_flag = False
                        answer_flag = False
                        if question and answer:
                            counter += 1
                            questions_and_answers[counter] = {'question': question, 'answer': answer}
                            question = ''
                            answer = ''

                    if question_flag:
                        question += read_string.replace('\n', ' ')
                    if answer_flag:
                        answer += read_string.replace('\n', ' ')
    with open('questions_and_answers.json', 'w') as write_file:
        json.dump(questions_and_answers, write_file, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
