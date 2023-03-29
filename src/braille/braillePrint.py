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
    # 문자열처리를 위해 양쪽 끝의 줄바꿈 표를 없애고, 점자 공백을 일반 공백으로 변경
    braille_text = braille_text.strip('\n').replace("⠀", " ")

    form = ""  # 결과를 저장할 리스트

    cnt = 0
    for c in braille_text:
        if cnt == horizontal:
            form += '\n'
            cnt = 0
        form += c
        if c == '\n':
            cnt = 0
        else:
            cnt += 1

    return form.strip('\n').replace(" ", "⠀")


# 출력할 문자열을 utf-8로 인코딩
braille_text = transfrom_to_braille(translate(sys.argv[1]))
braille_text_utf8 = braille_text.encode('utf-8')

# utf-8로 인코딩한 문자열을 표준 출력으로 출력
sys.stdout.buffer.write(braille_text_utf8)
