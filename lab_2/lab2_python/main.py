import math
import mpmath
import file_operations

PI_i = [0.2148, 0.3672, 0.2305, 0.1875]


def freq_bit_test(s: str) -> float:
    """
    Выполняет тест на частоту битов для строки s.
    Параметры:
    s (str): Строка, содержащая битовую последовательность.
    Возвращает:
    P(float): Результат теста на частоту битов.
    """
    try:
        count_ones = s.count("1")
        count_zeros = s.count("0")

        x = count_ones - count_zeros

        N = len(s)
        SN = x / math.sqrt(N)

        P = math.erfc(SN / math.sqrt(2))
        return P
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def same_bits_test(s: str) -> float:
    """
        Выполняет тест на одинаковые подряд идущие биты для строки s.
        Параметры:
        s (str): Строка, содержащая битовую последовательность.
        Возвращает:
        P(float): Результат теста на одинаковые подряд идущие биты.
        """
    try:
        N = len(s)
        zeta = 0
        zeta = sum(int(a) for a in s)
        zeta /= N
        if abs(zeta - 0.5) >= 2 / math.sqrt(N):
            return 0
        VN = 0
        for i in range(N - 1):
            if s[i] != s[i + 1]:
                VN += 1
        P = math.erfc(abs(VN - 2 * N * zeta * (1 - zeta)) / (2 * math.sqrt(2 * N) * zeta * (1 - zeta)))
        return P
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def get_len_seq(block: str) -> int:
    """
       Находит максимальное расстояние между нулями в блоке.
       Параметры:
       block (str): Строка, представляющая блок битов.
       Возвращает:
       max_dist(int): Максимальное расстояние между нулями в блоке.
       """
    try:
        zero_indices = [-1]
        for i in range(len(block)):
            if block[i] == '0':
                zero_indices.append(i)
        zero_indices.append(len(block))
        max_dist = -1
        for i in range(len(zero_indices) - 1):
            if zero_indices[i + 1] - zero_indices[i] - 1 > max_dist:
                max_dist = zero_indices[i + 1] - zero_indices[i] - 1
        return max_dist
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def longest_ones_sequence_test(s: str) -> float:
    """
       Выполняет тест на самую длинную последовательность единиц в блоке.
       Параметры:
       s (str): Строка, содержащая битовую последовательность.
       Возвращает:
       P(float): Результат теста на самую длинную последовательность единиц в блоке.
       """
    try:
        block_length = 8
        # Разбиваем строку на блоки
        blocks = []
        for i in range(0, len(s), block_length):
            blocks.append(s[i: i + block_length])
        blocks_ones_length = []
        for b in blocks:
            blocks_ones_length.append(get_len_seq(b))
        v_i = [0, 0, 0, 0]
        for b in blocks_ones_length:
            match b:
                case 0 | 1:
                    v_i[0] += 1
                case 2:
                    v_i[1] += 1
                case 3:
                    v_i[2] += 1
                case _:
                    v_i[3] += 1
        hi_sq = 0
        for i in range(len(v_i)):
            hi_sq += pow(v_i[i] - 16 * PI_i[i], 2) / (16 * PI_i[i])
        P = mpmath.gammainc(3 / 2, hi_sq / 2)
        return P
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


if __name__ == '__main__':
    s = file_operations.read_json('sequences.json')
    cpp_num = s['cpp']
    res1 = freq_bit_test(cpp_num)
    res2 = same_bits_test(cpp_num)
    res3 = longest_ones_sequence_test(cpp_num)
    cpp_str = 'Генерация на C++\n'
    cpp_str += 'Частнотный побитовый тест: ' + str(res1) + '\n'
    cpp_str += 'Тест на одинаковые подряд идущие биты: ' + str(res2) + '\n'
    cpp_str += 'Тест на самую длинную послед-ть единиц в блоке: ' + str(res3) + '\n'
    file_operations.write_file('cpp_res1.txt', cpp_str)

    java_num = s['java']
    result1 = freq_bit_test(java_num)
    result2 = same_bits_test(java_num)
    result3 = longest_ones_sequence_test(java_num)
    java_str = 'Генерация на Java\n'
    java_str += 'Частнотный побитовый тест: ' + str(result1) + '\n'
    java_str += 'Тест на одинаковые подряд идущие биты: ' + str(result2) + '\n'
    java_str += 'Тест на самую длинную послед-ть единиц в блоке: ' + str(result3) + '\n'
    file_operations.write_file('java_res1.txt', java_str)
