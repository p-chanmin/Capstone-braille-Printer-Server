import brailleDB
from checkText import getChar

# 초성에 올 수 있는 자음
cho = [
    'ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]
# 중성에 올 수 있는 모음
jung = [
    'ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ'
]
# 종성에 올 수 있는 자음
jong = [
    None, 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]

def isHangul(letter):
    """
    입력된 문자 1개가 한글인지 판별
        :param letter: 문자 1개
        :return: 한글이면 true, 아니면 false
    """
    if (letter is None): return False
    return True if ((ord('가') <= ord(letter) and ord(letter) <= ord('힣')) or letter in cho or letter in jung) else False

def isSpace(letter):
    """
    입력된 문자가 공백인지 판별
        :param letter: 입력된 문자
        :return: 공백이면 true, 아니면 false
    """
    return True if letter == ' ' else False

# 한글 음절 분리
def Syllabification(letter):
    """
    한글 문자 1개를 초성, 중성, 종성으로 분리하는 함수
        :param letter: 입력된 한글 문자 1개
        :return: 초성, 중성, 종성 순서로 반환,(한글이 아닌 문자나 None이 입력되면 None을 반환)
    """
    if(letter == None or not isHangul(letter) or letter in cho or letter in jung): return None, None, None
    offset = ord(letter) - ord('가') # index 계산을 위한 offset 설정
    # 음절 분리
    ## 초성
    chosung = cho[offset // (len(jung) * len(jong))]
    ## 중성
    jungsung = jung[(offset // len(jong)) % len(jung)]
    ## 종성
    jongsung = jong[offset % len(jong)] # 종성이 있는지 없는지 확인
    
    return chosung, jungsung, jongsung

def HangleToBraille(letter, index, text):
    """
    한글 문자 1개를 점자로 점역하는 함수
        :param letter: 입력된 한글 문자 1개
        :param index: 한글 문자의 해당 인덱스
        :param text: 전체 문장
        :return: 입력된 한글 문자 1개에 매칭되는 점자
    """
    ## 한글자 이상 입력이 들어올 경우
    if len(letter) > 1:
        print("ERR: Syllabification()은 한글자만 입력 받음")
        return ""

    # 제 9항 단독으로 쓰인 자모일 경우 온표(⠿)를 적어 나타냄
    if (letter in brailleDB.han_cho_dict):
        return "⠿" + brailleDB.han_cho_dict[letter] + " "
    elif (letter in brailleDB.han_jung_dict):
        return "⠿" + brailleDB.han_jung_dict[letter] + " "

    if (not (isHangul(letter) or isSpace(letter))):
        # print(f"ERR: <{letter}>은 한글 문자가 아님")
        # 한글 문자가 아니면 일단 그대로 반환
        return f"{letter}"

    syllables = []  # 분리된 음절이 들어갈 리스트
    tran = [] # 점역된 점자가 들어갈 리스트

    if letter == ' ':   # 공백일 경우
        return ' '

    # 이전, 다음 문자 가져오기
    prev = getChar(text, index - 1)
    next = getChar(text, index + 1)
    # 초성, 중성, 종성으로 음절 분리
    chosung , jungsung, jongsung = Syllabification(letter)
    prev_cho, prev_jung, prev_jong = Syllabification(prev)
    next_cho, next_jung, next_jong = Syllabification(next)

    syllables.append(chosung)
    syllables.append(jungsung)
    # 종성의 분리
    if jongsung is not None:
        if jongsung in brailleDB.han_jong_double:
            syllables += brailleDB.han_jong_separate[jongsung]
        else:
            syllables.append(jongsung)

    # 초성,중성,종성으로 하는 약자인지 확인 (것)
    if(chosung in "ㄱㄲ" and jungsung == 'ㅓ' and jongsung == "ㅅ"):
        if (chosung == 'ㄱ'): tran.append(brailleDB.abb_char_dict['것'])
        else: tran.append(brailleDB.abb_char_dict['껏'])
        syllables = syllables[3:] # 초성, 중성, 종성 제거, 나머지 있을 수 없음, 빈 리스트
    # 제16항 "성, 썽, 정, 쩡, 청" 은 "영"의 약자를 적어 나타낸다
    elif(letter in "성썽정쩡청"):
        tran.append(brailleDB.han_cho_dict[chosung])
        tran.append(brailleDB.abb_char_dict['영'])
    # 초성과 중성으로 하는 약자인지 확인 (가까나다따마바빠사싸아자짜카타파하) // 제 17항 붙임 '팠'은 예외
    elif(jungsung == 'ㅏ' and chosung in "ㄱㄲㄴㄷㄸㅁㅂㅃㅅㅆㅇㅈㅉㅋㅌㅍㅎ" and letter != '팠'):
        # 제 17항 (나다따마바빠자짜카타파하) 뒤에 모음이 이어나올 경우 생략x
        # 제 10항 다음 글자로 (ㅖ)가 올 경우에는 약자 반영
        if (letter in "나다따마바빠자짜카타파하" and next_cho is not None and next_cho == "ㅇ" and next_jung != "ㅖ"):
            if (chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung])
            tran.append(brailleDB.han_jung_dict[jungsung])
        # 제 17항 예외가 아닐 경우
        else:
            tran.append(brailleDB.abb_char_dict[chosung])
            syllables = syllables[2:]  # 초성, 중성 제거, 나머지 있을 수 있음, 나머지 모두 종성
            if jongsung is not None: tran.append(brailleDB.han_jong_dict[jongsung])
    # 중성과 종성으로 하는 약자인지 확인
    # 억,언,얼
    elif(jungsung == 'ㅓ' and (jongsung is not None) and syllables[2] in "ㄱㄴㄹ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if(syllables[2] == 'ㄱ'): tran.append(brailleDB.abb_char_dict['억'])
        elif (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['언'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['얼'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 연,열,영
    elif(jungsung == 'ㅕ' and (jongsung is not None) and syllables[2] in "ㄴㄹㅇ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['연'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['열'])
        elif (syllables[2] == 'ㅇ'): tran.append(brailleDB.abb_char_dict['영'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 옥,온,옹
    elif(jungsung == 'ㅗ' and (jongsung is not None) and syllables[2] in "ㄱㄴㅇ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄱ'): tran.append(brailleDB.abb_char_dict['옥'])
        elif (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['온'])
        elif (syllables[2] == 'ㅇ'): tran.append(brailleDB.abb_char_dict['옹'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 운,울
    elif(jungsung == 'ㅜ' and (jongsung is not None) and syllables[2] in "ㄴㄹ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['운'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['울'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 은,을
    elif(jungsung == 'ㅡ' and (jongsung is not None) and syllables[2] in "ㄴㄹ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['은'])
        elif (syllables[2] == 'ㄹ'): tran.append(brailleDB.abb_char_dict['을'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])
    # 인
    elif(jungsung == 'ㅣ' and (jongsung is not None) and syllables[2] in "ㄴ"):
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung]) # 초성이 ㅇ이 아니면 먼저 삽입
        if (syllables[2] == 'ㄴ'): tran.append(brailleDB.abb_char_dict['인'])
        syllables = syllables[3:]  # 초성, 중성, 종성 제거, 나머지 있을 수 있음, 나머지 모두 종성
        for s in syllables:
            tran.append(brailleDB.han_jong_dict[s])

    # 제 10항 모음자에 (ㅖ)가 이어 나올 때 그 사이에 붙임표(⠤)를 적어 나타낸다
    elif(chosung == "ㅇ" and jungsung == 'ㅖ' and not isSpace(prev) and prev != None and prev_jong is None):
        tran.append("⠤")    # 붙임표
        tran.append(brailleDB.han_jung_dict[jungsung])
        if jongsung is not None: tran.append(brailleDB.han_jong_dict[jongsung])
    # 제 11항 (ㅑ,ㅘ,ㅜ,ㅝ)에 (ㅐ)가 이어 나올 때 그 사이에 붙임표를 적어 나타낸다
    elif (chosung == "ㅇ" and jungsung == 'ㅐ' and prev_jong is None and prev_jung in ['ㅑ','ㅘ','ㅜ','ㅝ']):
        tran.append("⠤")  # 붙임표
        tran.append(brailleDB.han_jung_dict[jungsung])
        if jongsung is not None: tran.append(brailleDB.han_jong_dict[jongsung])
    # 약자가 반영이 없는 경우
    else:
        # 초성의 ㅇ은 생략
        if(chosung != 'ㅇ'): tran.append(brailleDB.han_cho_dict[chosung])
        tran.append(brailleDB.han_jung_dict[jungsung])
        # 종성이 있는지 확인
        if jongsung is not None: tran.append(brailleDB.han_jong_dict[jongsung])

    return "".join(tran)

def HangleApplyAbbreviationWords(text: str):
    """
    문장에서 약어를 반영하여 약어를 점자로 바꾼 문자열을 반환
        :param text: 점역할 문장
        :return: 문장에서 약어를 점자로 바꾼 문자열
    """
    # 제 18항 약어 적용
    for abbWord in brailleDB.abb_word_dict:
        text = text.replace(abbWord, brailleDB.abb_word_dict[abbWord])
        # 제 18항 예외 조항 ("쭈그리고, 우그리고, 오그리고, 찡그리고"의 경우 약어 반영x)
        if(abbWord == '그리고'):
            # 다시 원본 문자열로 변환
            text = text.replace("쭈"+brailleDB.abb_word_dict[abbWord], "쭈그리고")
            text = text.replace("우" + brailleDB.abb_word_dict[abbWord], "우그리고")
            text = text.replace("오" + brailleDB.abb_word_dict[abbWord], "오그리고")
            text = text.replace("찡" + brailleDB.abb_word_dict[abbWord], "찡그리고")

    return text
