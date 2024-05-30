import hashlib
import multiprocessing as mp
from matplotlib import pyplot as plt
import tqdm
import time


def luna_alg_check_card_number(card_num: str):
    card_num_arr = [int(a) for a in card_num]
    for i in range(len(card_num_arr) - 2, -1, -2):
        card_num_arr[i] *= 2
        if card_num_arr[i] > 9:
            card_num_arr[i] -= 9
    return sum(card_num_arr) % 10 == 0


def get_right_symbols(cur_hash, begins, end, range_b, range_e, q):
    res = []
    for i in range(range_b, range_e):
        i = str(i).rjust(6, '0')
        for b in begins:
            b = b + i + end
            hash_ = hashlib.sha256(b.encode()).hexdigest()
            if hash_ == cur_hash:
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

    for i in tqdm.trange(1, int(max_n_o_p) + 1, ncols=80, desc='Total'):
        # for i in range(1, int(max_n_o_p)+1):
        time_start = time.perf_counter()
        if i == 1:
            res2 = find_right_numbers(cur_hash, begins, end, i)
        else:
            res_ = find_right_numbers(cur_hash, begins, end, i)
        time_arr.append(time.perf_counter() - time_start)
    return time_arr, res2


def get_plot(cur_hash, begins, end, max_n_o_p=None, save_img=True):
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
