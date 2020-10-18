import jieba
import re
import os


def clean(path):
    try:
        file = open(path, 'r', encoding='utf-8')
        txt = file.read()
        words = jieba.lcut(txt)  # cut words
        count = {}
        for word in words:
            if len(word) < 2:  # exclude the single word
                continue
            elif word.isdigit():  # exclude the number
                continue
            else:
                count[word] = count.get(word, 0) + 1
        exclude = ['patient', 'doctor']
        for key in list(count.keys()):
            if key in exclude:
                del count[key]
        m_list = list(count.items())
        m_list.sort(key=lambda x: x[1], reverse=True)
        print('Total number of key word : {}'.format(len(m_list)))
        return count
    except IOError as e:
        print('{} not exists'.format(path))
        print('e:' + e)
        return None


def get_key_single_sentence(path, sorted_dict):
    try:
        file = open(path, 'r', encoding='utf-8')
        lines = file.readlines()
        if os.path.exists('results.txt'):
            os.remove('result.txt')
        result = open('result.txt', 'a', encoding='utf-8')
        for index, line in enumerate(lines):
            print(index)
            patient, doctor = re.findall('\[(.*?)\]', line)
            string = 'Q&A : {}, patient: {}, doctor: {}'.format(index+1,
                                                                str(compare(patient, sorted_dict)),
                                                                str(compare(doctor, sorted_dict)))
            result.write(string+'\n')
    except IOError as e:
        print('{} not exists'.format(path))
        print('e:' + e)
        return None


def compare(txt, m_dict):
    result = {}
    words = jieba.lcut(txt)
    for word in words:
        if word in m_dict.keys():
            if m_dict[word] >= 50:
                result[word] = result.get(word, 0) + 1
    return result


if __name__ == '__main__':
    cleaned_dict = clean('neifenmi.txt')
    if cleaned_dict is not None:
        get_key_single_sentence('neifenmi.txt', cleaned_dict)
