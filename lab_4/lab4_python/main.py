import argparse
import multiprocessing as mp
import hashlib
import funcs
import file_operations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings', help="Путь к json файлу с данными.", required=True)
    parser.add_argument('-i', '--plot_image', help="Сохранять ли изображения графики зависимостей.")
    parser.add_argument('-p', '--num_of_processes', help='Максимальное количество процессов')
    args = parser.parse_args()
    res = file_operations.read_json(args.settings)
    funcs.get_plot(res['hash'], res['bins_list'], res['last_symbols'], args.num_of_processes, args.plot_image)


if __name__ == '__main__':
    main()
