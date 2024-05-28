import multiprocessing as mp
import funcs

if __name__ == '__main__':
    n_o_p = 10
    begins = ['555949']
    end = '4301'

    process_arr = []
    queue_arr = []
    for i in range(n_o_p):
        queue_arr.append(mp.Queue())
        process_arr.append(mp.Process(target=funcs.get_right_symbols, args=[begins, end, i*1000000//n_o_p, (i+1)*1000000//n_o_p, queue_arr[-1]]))
        process_arr[-1].start()
    for p in process_arr:
        p.join()
    res_total = []
    for q in queue_arr:
        for a in q.get():
            res_total.append(a)
    print(res_total)
