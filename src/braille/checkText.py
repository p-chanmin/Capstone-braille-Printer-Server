

text = "01234567"

def getChar(text: str, index: int):
    """
    문자열 text에서 index 값에 해당하는 문자를 반환
    인덱스에 없는 값이 호출되면 None을 반환
        :param text: 문자열
        :param index: 호출할 인덱스
        :return: 문자열 혹은 None
    """
    try:
        if(index in range(len(text))):
            return text[index]
        else: return None
    except:
        return None

