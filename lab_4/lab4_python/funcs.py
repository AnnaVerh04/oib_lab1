import hashlib
import multiprocessing as mp
import queue

from matplotlib import pyplot as plt
import tqdm
import time


def luna_alg_check_card_number(card_num: str) -> bool:
    """
    Проверяет валидность номера банковской карты с помощью алгоритма Луна.
        card_num (str): Номер банковской карты для проверки.
        bool: True, если номер карты валиден, иначе False.
    """
    if not card_num.isdigit():
        raise ValueError("Номер карты должен содержать только цифры.")
    card_num_arr = [int(a) for a in card_num]
    for i in range(len(card_num_arr) - 2, -1, -2):
        card_num_arr[i] *= 2
        if card_num_arr[i] > 9:
            card_num_arr[i] -= 9
    return sum(card_num_arr) % 10 == 0


def get_right_symbols(cur_hash: str, begins: list, end: str, range_b: int, range_e: int, q: queue) -> None:
    """
        Находит правильные символы для заданного хэша.
            cur_hash (str): Хэш, который необходимо сопоставить.
            begins (list): Список начальных символов.
            end (str): Конечный символ.
            range_b (int): Начало диапазона чисел.
            range_e (int): Конец диапазона чисел.
            q (Queue): Очередь для сохранения результатов.
    """
    res = []
    for i in range(range_b, range_e):
        i = str(i).rjust(6, '0')
        for b in begins:
            b = b + i + end
            hash_ = hashlib.sha256(b.encode()).hexdigest()
            if hash_ == cur_hash:
                res.append(b)
    q.put(res)


def find_right_numbers(cur_hash: str, begins: list, end: str, n_o_p: int) -> list:
    """
        Находит правильные числа для заданного хэша, используя несколько процессов.
            cur_hash (str): Хэш, который необходимо сопоставить.
            begins (list): Список начальных символов.
            end (str): Конечный символ.
            n_o_p (int): Количество процессов для параллельного выполнения.
            list: Список правильных чисел для заданного хэша.
    """
    process_arr = []
    queue_arr = []
    for i in range(n_o_p):
        queue_arr.append(mp.Queue())
        process_arr.append(mp.Process(target=get_right_symbols,
                                      args=[cur_hash, begins, end, i * 1000000 // n_o_p, (i + 1) * 1000000 // n_o_p,
                                            queue_arr[-1]]))
        process_arr[-1].start()
    for p in process_arr:
        p.join()
    res_total = []
    for q in queue_arr:
        for a in q.get():
            res_total.append(a)
    return res_total


def get_dependency(cur_hash: str, begins: list, end: str, max_n_o_p: int = None) -> tuple:
    """
       Получает зависимость времени выполнения от количества процессов.
           cur_hash (str): Хэш, который необходимо сопоставить.
           begins (list): Список начальных символов.
           end (str): Конечный символ.
           max_n_o_p (int): Максимальное количество процессов. Если не указано, используется 1.5 * количество ядер.
           tuple: Время выполнения для каждого количества процессов, результат для последнего количества процессов.
    """
    time_arr = []
    if max_n_o_p is None:
        max_n_o_p = int(mp.cpu_count() * 1.5)

    for i in tqdm.trange(1, int(max_n_o_p) + 1, ncols=80, desc='Total'):
        # for i in range(1, int(max_n_o_p)+1):
        time_start = time.perf_counter()
        if i == 1:
            res2 = find_right_numbers(cur_hash, begins, end, i)
        else:
            res_ = find_right_numbers(cur_hash, begins, end, i)
        time_arr.append(time.perf_counter() - time_start)
    return time_arr, res2


def get_plot(cur_hash: str, begins: list, end: str, max_n_o_p: int = None, save_img: bool = True) -> list:
    """
        Получает график зависимости времени выполнения от количества процессов.
            cur_hash (str): Хэш, который необходимо сопоставить.
            begins (list): Список начальных символов.
            end (str): Конечный символ.
            max_n_o_p (int): Максимальное количество процессов. Если не указано, используется 1.5 * количество ядер.
            save_img (bool): Флаг для сохранения изображения графика.
            list: Результат выполнения функции get_dependency.
    """
    if max_n_o_p is None:
        max_n_o_p = int(mp.cpu_count() * 1.5)
    time_arr, card_codes = get_dependency(cur_hash, begins, end, max_n_o_p)
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('Время поиска коллизии, с')
    plt.xlabel('Количество процессов')
    plt.plot(list(range(1, int(max_n_o_p) + 1)), time_arr, color='red', linestyle='-', marker='o', linewidth=1,
             markersize=4)
    if save_img:
        plt.savefig("res.png")
    plt.show()
    return card_codes
