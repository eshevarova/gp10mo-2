def get_round50(str_num):
    try:
        num = int(str_num)
    except ValueError:
        num = int(float(str_num))
    round_to_ceil = 50
    div, mod = divmod(num, round_to_ceil)
    if mod == 0:
        return num
    else:
        return (div + 1) * round_to_ceil


if __name__ == "__main__":
    print(get_round50('144.5'))