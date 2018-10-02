def get_round50(str_num):
    try:
        num = int(str_num)
    except ValueError:
        num = int(float(str_num))
    while num % 50 != 0:
        num += 1
    return num
