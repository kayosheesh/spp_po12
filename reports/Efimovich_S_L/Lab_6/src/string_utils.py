def index_of_difference(str1, str2):
    if str1 is None and str2 is None:
        raise TypeError

    if str1 is None or str2 is None:
        return 0

    if str1 == "" and str2 == "":
        return -1

    min_len = min(len(str1), len(str2))

    for i in range(min_len):
        if str1[i] != str2[i]:
            return i

    if len(str1) != len(str2):
        return min_len

    return -1
