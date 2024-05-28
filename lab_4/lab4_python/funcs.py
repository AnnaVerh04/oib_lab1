import hashlib


AL_HASH = '4006234246b4fd2b2833d740927ab20465afad862c74b1a88ec0869bde5c836c'


def get_right_symbols(begins, end, range_b, range_e, q):
    # begins - массив, состоящий из всех подхоядих
    # первых 6 символов-цифр (правильные БИНы)
    # end - последние четыре символа-цифр
    res = []
    for i in range(range_b, range_e):
        i = str(i).rjust(6, '0')
        for b in begins:
            b = b + i + end
            hash_ = hashlib.sha256(i.encode()).hexdigest()
            if hash_ == AL_HASH:
                res.append(b)
    q.put(res)
