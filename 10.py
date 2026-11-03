from collections import Counter
from huffman import build_huffman, encode, decode, calc, check_prefix

f = open("sample.txt", encoding="utf-8")
text = f.read().strip()
f.close()

freq = Counter(text)
tree, codes = build_huffman(freq)

print("Длина текста:", len(text))
print("Разных символов:", len(freq))
print("Префиксный:", check_prefix(codes))
for s, n in freq.most_common():
    print(repr(s), n, round(n / len(text), 4), codes[s], len(codes[s]))

H, L, eta, R = calc(freq, codes)
print("H =", round(H, 4))
print("L =", round(L, 4))
print("eta =", round(eta, 2), "%")
print("R =", round(R, 2), "%")

utf8 = len(text.encode("utf-8"))
print("UTF-8:", utf8, "байт")

bits = encode(text, codes)
pad = 0
while len(bits) % 8 != 0:
    bits = bits + "0"
    pad = pad + 1
data = []
for i in range(0, len(bits), 8):
    data.append(int(bits[i:i + 8], 2))
data = bytes(data)
print("Битов Хаффмана:", len(bits) - pad)
print("Добавлено нулей в конце:", pad)
print("Сжатые данные:", len(data), "байт")

table = ""
for s in codes:
    table = table + s + codes[s] + "\n"
table = table.encode("utf-8")
print("Таблица кодов:", len(table), "байт")
total = len(data) + len(table) + 1
print("Всего с таблицей:", total, "байт")

print("Kc без таблицы =", round(utf8 / len(data), 4), "S =", round((1 - len(data) / utf8) * 100, 2), "%")
print("Kc с таблицей =", round(utf8 / total, 4), "S =", round((1 - total / utf8) * 100, 2), "%")

bits2 = ""
for b in data:
    bits2 = bits2 + format(b, "08b")
bits2 = bits2[:len(bits2) - pad]
print("Распаковано правильно:", decode(bits2, tree) == text)
