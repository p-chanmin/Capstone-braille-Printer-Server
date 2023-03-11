import brailleDB, mark, number
from checkText import getChar
import re


def isEnglish(letter):
    """
    입력된 문자 1개가 영어인지 판별
        :param letter: 문자 1개
        :return: 영어면 true, 아니면 false
    """
    if(letter is None): return False
    # (@#^&)는 한글 점자 규정이 없어 영어 점자 규정을 따라간다. 따라서 영어로 해석되어야 함
    return True if (letter in brailleDB.eng_dict) else False

def isSpace(letter):
    """
    입력된 문자가 공백인지 판별
        :param letter: 입력된 문자
        :return: 공백이면 true, 아니면 false
    """
    return True if letter == ' ' else False

def UpperDFS(i, d, eng_text, end = False, now_cnt = 1, prev_cnt = 1):
    """
    대문자 범위를 판별하기 위한 DFS 함수
    :param i: 시작 인덱스
    :param d: 깊이
    :param eng_text: 영어 문장
    :param end: 종료표의 필요 여부
    :param now_cnt: 현재 단어의 대문자 cnt
    :param prev_cnt: 이전 단어의 대문자 cnt
    :return: (대문자 시작 인덱스, 대문자 마지막 인덱스, 종료표 여부)
    """
    next = getChar(eng_text, d+1)
    if(next is None):
        return (i, d, False)
    elif(now_cnt >= 1 and eng_text[d].isupper() and next.isupper()): # 대문자 1개인 상태에서 다음 대문자로 넘어갈 경우
        (ti, td, te) = UpperDFS(i, d+1, eng_text, end, now_cnt+1, prev_cnt+1)
        return (i, td, te)
    elif (prev_cnt != 1 and now_cnt == 0 and next.isupper() and getChar(eng_text, d+2) is not None and getChar(eng_text, d+2).isupper()):  # 현재 카운트 0인 상태에서 다음 대문자 단어로 넘어가는 경우
        (ti, td, te) = UpperDFS(i, d + 1, eng_text, end, now_cnt + 1, 1)
        return (i, td, te)
    elif((isSpace(next) or next in ",")):
        (ti, td, te) = UpperDFS(i, d+1, eng_text, end, 0, prev_cnt)
        return (i, td, te)
    else: # 대문자 종료 구문
        if(next.islower() or number.isNumber(next) or (mark.isMark(next) and next not in ",")):
            return (i, d, True)
        else:
            return (i, d, end)


def findUpper(eng_text):
    """
    영어 문장에서 대문자의 범위를 판별하여, 대문자표를 삽입할 인덱스를 반환하는 함수
        :param eng_text: 영어 문장
        :return: [대문자 기호표 인덱스], [대문자 단어표 인덱스], [대문자 구절표 인덱스], [대문자 종료표 인덱스]
    """
    max_idx = -1
    one_upper = []
    word_upper = []
    str_upper = []
    end_upper = []

    for i in range(len(eng_text)):
        if(i <= max_idx):
            continue
        if(eng_text[i].isupper()):  # 대문자 범위 탐색
            start_idx, end_idx, end  = UpperDFS(i, i, eng_text)   # 대문자 범위 탐색
            max_idx = end_idx   # 최대 idx 갱신, 범위 안의 문자는 다시 탐색x

            sub_text = re.sub(r"\s+$", "", eng_text[start_idx:end_idx+1])   # 문자열의 마지막 공백을 제거한 대문자 범위 문자열

            if(len(sub_text) == 1): # 대문자 1개일 경우, 대문자 기호표
                one_upper.append(i)
            else:   # 대문자 1개 이상일 경우
                sub_text_list = sub_text.split(" ") # 공백으로 단어 분리
                if(len(sub_text_list) >= 3):    # 단어가 3개 이상일 경우, 대문자 구절표
                    str_upper.append(i)
                    if(end):    # 대문자 종료표를 적어야 할 경우
                        end_upper.append(i+len(sub_text))
                else: # 단어가 2개 이하일 경우, 대문자 단어표
                    for ti in range(len(sub_text_list)):
                        if(ti == 0): word_upper.append(i)
                        else:
                            word_upper.append(i + len(sub_text_list[ti-1]) + 1)
                    if (end):  # 대문자 종료표를 적어야 할 경우
                        end_upper.append(i + len(sub_text))


    return one_upper, word_upper, str_upper, end_upper


def EnglishToBraille(start, end, text):
    """
    영어문장을 점자로 점역하는 함수
        :param start: 전체 문장에서 영어 부분의 시작 인덱스
        :param end: 전체 문장에서 영어 부분의 끝 인덱스
        :param text: 전체 문장
        :return: 영어 문장을 영어로 점역된 문장
    """

    # 전체 text에서 영어 부분만 추출
    eng_text = text[start:end+1]

    # 대문자표 삽입 위치 탐색
    one_upper, word_upper, str_upper, end_upper = findUpper(eng_text)

    eng_text = list(text[start:end + 1])
    # 대문자 표 작성
    for i in range(len(eng_text)):
        if (i in one_upper):
            eng_text[i] = brailleDB.eng_upper + eng_text[i]
        elif (i in word_upper):
            eng_text[i] = brailleDB.eng_word_upper + eng_text[i]
        elif (i in str_upper):
            eng_text[i] = brailleDB.eng_str_upper + eng_text[i]
        if (i in end_upper):
            eng_text[i] = brailleDB.eng_end_upper + eng_text[i]

    eng_text = "".join(eng_text)
    # 로마자 시작 표시 추가
    eng_text = brailleDB.eng_start + eng_text

    # 영어 끝나면 로마자 종료 표시
    # 영어 다음에 (.)이 나오면 종료 표시 대신 마침표(.)의 점자를 찍음
    if (eng_text[-1] != '.'):
        # 제 31항 단위 부호로 끝날 경우 공백을 추가
        #   °C, °F
        #   %p
        if(eng_text[-1] in "%‰°′″Å"
                or (eng_text[-1] in "CF" and eng_text[-2] == "°")
                or (eng_text[-1] in "p" and eng_text[-2] == "%")):
            # 단위로 끝날 경우 특수문자에서 처리
            pass
        elif(getChar(text, end+1) is not None and (getChar(text, end+1).isnumeric() or getChar(text, end+1) == '.')):
            pass
        else:   # 일반적인 경우 로마자 종료 표시
            eng_text = eng_text + brailleDB.eng_end

    # 대문자표, 로마자 시작, 종료표 반영 완료 후 text를 모두 소문자로 변환
    eng_text = eng_text.lower()

    # 점역된 문자 저장될 리스트 (얕은 복사)
    translated_text = list(eng_text)[:]

    # 한글자 씩 점역
    for i in range(len(eng_text)):
        if isEnglish(eng_text[i]):  # 영어 점역
            translated_text[i] = brailleDB.eng_dict[eng_text[i]]
        elif number.isNumber(eng_text[i]):  # 숫자 점역
            translated_text[i] = number.NumberToBraille(eng_text[i], i, eng_text)
        elif mark.isMark(eng_text[i]):  # 특수 문자 점역
            if(eng_text[i] in brailleDB.eng_mark_dict): # 영문 특수문자가 존재하면 영문 특수문자로 점역
                translated_text[i] = brailleDB.eng_mark_dict[eng_text[i]]
            else:   # 영문 특수문자가 없으면 기본 한글 특수문자로 점역
                translated_text[i] = mark.MarkToBraille(eng_text[i], start+i-1, text)

    return "".join(translated_text)
