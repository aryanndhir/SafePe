def getKey(str):
    '''
    Input string containing bytestring of hexadecimal values to convert into a Integer Array
    :param str: name of string containing bytestring
    :return: Integer Array
    '''
    intArray = []
    for i in range(0, (len(str)), 2):
        intArray.append(int(str[i:i+2], 16))
    return intArray
