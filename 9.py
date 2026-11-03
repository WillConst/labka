import heapq
import math
from itertools import count
from collections import Counter


def build_huffman(freq):
    if not freq:
        raise ValueError("Пустой алфавит")
    order = count()
    heap = [(w, next(order), s) for s, w in freq.items() if w > 0]
    heapq.heapify(heap)
    if not heap:
        raise ValueError("Все частоты нулевые")
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(order), (left, right)))
    tree = heap[0][2]
    codes = {}

    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")

    walk(tree)
    return tree, codes


def encode(text, codes):
    return "".join(codes[s] for s in text)


def decode(bits, tree):
    if isinstance(tree, str):
        if any(b != "0" for b in bits):
            raise ValueError("Некорректный битовый поток")
        return tree * len(bits)
    result, node = [], tree
    for b in bits:
        if b not in "01":
            raise ValueError("Недопустимый бит")
        node = node[int(b)]
        if isinstance(node, str):
            result.append(node)
            node = tree
    if node is not tree:
        raise ValueError("Неполное кодовое слово")
    return "".join(result)


def calc(freq, codes):
    total = sum(freq.values())
    H = 0
    L = 0
    for s in freq:
        p = freq[s] / total
        H = H - p * math.log2(p)
        L = L + p * len(codes[s])
    eta = H / L * 100
    R = 100 - eta
    return H, L, eta, R


def check_prefix(codes):
    for a in codes.values():
        for b in codes.values():
            if a != b and b.startswith(a):
                return False
    return True


if __name__ == "__main__":
    text = "ABCADE"
    freq = Counter(text)
    tree, codes = build_huffman(freq)
    print("Частоты:", dict(freq))
    print("Коды:", codes)
    print("Префиксный:", check_prefix(codes))

    H, L, eta, R = calc(freq, codes)
    print("H =", round(H, 4))
    print("L =", round(L, 4))
    print("eta =", round(eta, 2), "%")
    print("R =", round(R, 2), "%")

    bits = encode(text, codes)
    print("Биты:", bits, len(bits), "бит")
    res = decode(bits, tree)
    print("Декодировано:", res)
    print("Совпадает:", res == text)

    print()
    text2 = "AAAA"
    tree2, codes2 = build_huffman(Counter(text2))
    bits2 = encode(text2, codes2)
    print("Один символ:", codes2, bits2, decode(bits2, tree2))
