import hashlib
import multiprocessing as mp
from matplotlib import pyplot as plt
import time


def get_right_symbols(cur_hash, begins, end, range_b, range_e, q):
    # begins - массив, состоящий из всех подхоядих
    # первых 6 символов-цифр (правильные БИНы)
    # end - последние четыре символа-цифр
    res = []
    for i in range(range_b, range_e):
        i = str(i).rjust(6, '0')
        for b in begins:
            b = b + i + end
            hash_ = hashlib.sha256(b.encode()).hexdigest()
            if hash_ == cur_hash:
                print(b)
                res.append(b)
    q.put(res)


def find_right_numbers(cur_hash, begins, end, n_o_p):
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


def get_dependency(cur_hash, begins, end, max_n_o_p=None):
    time_arr = []
    if max_n_o_p is None:
        max_n_o_p = int(mp.cpu_count() * 1.5)
    for i in range(1, int(max_n_o_p)):
        time_start = time.perf_counter()
        res = find_right_numbers(cur_hash, begins, end, i)
        time_arr.append(time.perf_counter() - time_start)
    return time_arr


def get_plot(cur_hash, begins, end, max_n_o_p=None, save_img=True):
    if max_n_o_p is None:
        max_n_o_p = int(mp.cpu_count() * 1.5)
    time_arr = get_dependency(cur_hash, begins, end, max_n_o_p)
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('Время поиска коллизии, с')
    plt.xlabel('Количество процессов')
    plt.plot(list(range(1, int(max_n_o_p))), time_arr, color='green', linestyle='--', marker='x', linewidth=1,
             markersize=4)
    if save_img:
        plt.savefig("res.png")
    plt.show()
