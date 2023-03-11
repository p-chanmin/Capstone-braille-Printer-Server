import brailleDB
import number
from hangul import isHangul
from checkText import getChar


def isMark(letter):
    """
    입력된 문자 1개가 숫자인지 판별
        :param letter: 문자 1개
        :return: 숫자이면 true, 아니면 false
    """
    if (letter is None): return False
    return True if (letter in brailleDB.mark_dict) else False

def isSpace(letter):
    """
    입력된 문자가 공백인지 판별
        :param letter: 입력된 문자
        :return: 공백이면 true, 아니면 false
    """
    return True if letter == ' ' else False

def MarkToBraille(letter, index, text):
    """
    특수문자를 점자로 점역하는 함수
    :param letter: 입력된 특수 문자 1개
    :param index: 특수 문자의 해당 인덱스
    :param text: 전체 문장
    :return: 입력된 특수 문자 1개에 매칭되는 점자
    """

    prev = getChar(text, index-1)
    next = getChar(text, index+1)

    ## 한글자 이상 입력이 들어올 경우
    if len(letter) > 1:
        print("ERR: MarkToBraille()은 한글자만 입력 받음")
        return ""

    if (not (isMark(letter) or isSpace(letter))):
        # print(f"ERR: <{letter}>은 한글 문자가 아님")
        # 숫자 문자가 아니면 일단 그대로 반환
        return f"{letter}"

    tran = []  # 점역된 점자가 들어갈 리스트

    # 제 47항 예외, 수의 자릿점을 표현하는 (,)의 경우 (⠂)으로 표현
    if(letter == ',' and
            number.isNumber(prev) and
            (number.isNumber(getChar(text, index+1)) and
             number.isNumber(getChar(text, index+2)) and
             number.isNumber(getChar(text, index+3)))):
        tran.append('⠂')
    # 제 47항 예외, 줄임표(…)는 1~2개까지 표현
    elif(letter == '…' and prev == '…'):
        pass
    # 제 73항 예외, 연산기호(+−×÷=±%)가 한글 사이에 오면 앞뒤 한 칸씩 띄어 표현
    elif (letter in "+−×÷=±"):
        if(isHangul(prev)):
            tran.append(" ")
        tran.append(brailleDB.mark_dict[letter])
        if (isHangul(next)):
            tran.append(" ")
    elif (letter in "%‰°′″Å"):
        if(letter == "%"):
            if (isHangul(prev)):
                tran.append(" ")
        if (letter == "°" and next is not None and next in "CF") or (letter == "%" and next is not None and next in "p"):
            tran.append(brailleDB.mark_dict[letter])
        else:
            tran.append(brailleDB.mark_dict[letter])
            if(next != ' '):
                tran.append(" ")
    elif(letter == 'ʼ' and number.isNumber(getChar(text, index+1))):
        tran.append(brailleDB.num_start)
        tran.append(brailleDB.mark_dict[letter])
    else:
        # 특수문자를 점자로 점역
        tran.append(brailleDB.mark_dict[letter])



    return "".join(tran)