# -*- coding: utf-8 -*-
import brailleDB as db
import hangul
import numpy as np
import sys

from translate import translate

#   점자의 번호:
#   (1) (4)
#   (2) (5)
#   (3) (6)

#   점자 유니코드는 U+2800 부터 시작한다.
#   점자 코드는 기계적으로 계산이 가능하게 배치되어있다.
#   점자 번호를 역순으로 나열해서 2진수로 계산하면 해당 점자 코드가 나온다.
#
#    예) ⠓ (1-2-5)일 경우, 점자 유무로 표기하면 "1 1 0 0 1 0 0 0"가 되고, 이를 역순 이진법으로 취하면 "00010011(19, 0x13)"이 된다.
#   그러므로 0x2800 + 0x13 = 0x2813, 즉 U+2813이 해당 점자의 유니코드가 된다.

def transfrom_to_braille(braille_text, horizontal = 32):
    """
    점자 문자열을 가로칸에 맞춰 줄바꿈하고, 여백을 점자 공백으로 채우는 함수
        :param braille_text: 점자 문자열
        :param horizontal: 최대 가로칸
        :return: 최대 가로칸으로 줄바꿈(\n)한 점자 문자열
    """
    # 문자열처리를 위해 점자 공백을 일반 공백으로 변경
    braille_text = braille_text.replace("⠀", " ")

    words = braille_text.split(" ")  # 공백으로 단어로 나눔
    words_list = []  # 결과를 저장할 리스트

    # 가로길이에 맞게 단어 분할
    for word in words:
        while len(word) > horizontal:  # 단어가 horizontal글자보다 길 경우
            words_list.append(word[:horizontal])  # horizontal글자까지 자른 후 추가
            word = word[horizontal:]  # 나머지 단어로 다시 반복

        words_list.append(word)  # horizontal글자 이하인 단어는 그대로 추가

    # 최대 길이 horizontal으로 나누기
    lines = []
    line = ''
    # 단어 목록을 순회하면서 줄바꿈
    for word in words_list:
        # 단어를 추가했을 때 가로보다 길면 라인을 추가하고, 새로운 라인 생성
        if len(line) + len(word) + 1 > horizontal:
            lines.append(line)
            line = ""
        # 단어 중간에 줄바꿈 표가 있을 경우 줄바꿈을 우선으로 라인 생성
        if "\n" in word:
            split_words = word.split("\n")
            for i, split_word in enumerate(split_words):
                if len(line) + len(split_word) + 1 > horizontal:
                    lines.append(line)
                    line = ""
                else:
                    if line:
                        line += " "
                    line += split_word
        # 그렇지 않으면 공백으로 단어 추가
        else:
            if line:
                line += " "
            line += word

    # 마지막 라인이 있으면 추가
    if line:
        lines.append(line)

    # 모든 줄을 넘파이 배열로 변환
    chunks = np.array(lines)

    # 패딩할 점자 공백("⠀")
    pad_char = "⠀"

    # 각 문자열에 대해 패딩을 적용하여 가로칸을 맞춤
    padded_array = []
    for s in chunks:
        if len(s) < horizontal:
            pad_length = horizontal - len(s)
            padded_string = s + pad_char * pad_length
        else:
            padded_string = s
        # 문자열에서 공백을 데이터화 가능한 점자 공백("⠀")으로 변경
        padded_array.append(padded_string.replace(" ", "⠀"))

    return "\n".join(padded_array)


# 출력할 문자열을 utf-8로 인코딩
braille_text = transfrom_to_braille(translate(sys.argv[1]))
braille_text_utf8 = braille_text.encode('utf-8')

# utf-8로 인코딩한 문자열을 표준 출력으로 출력
sys.stdout.buffer.write(braille_text_utf8)
