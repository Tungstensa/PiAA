from lsp import build_lps


def kmp(pattern: str, text: str):
    m = len(pattern)
    n = len(text)

    print("=== KMP ПОИСК ===")
    lps = build_lps(pattern, m)

    i = 0
    j = 0
    result = []

    while i < n:
        print(f"i={i}, j={j}, text[i]={text[i]}, pattern[j]={pattern[j]}")

        if text[i] == pattern[j]:
            print("Совпадение → двигаем i и j")
            i += 1
            j += 1

            if j == m:
                print(f"НАЙДЕНО в позиции {i - j}")
                result.append(i - j)
                print(f"Переход j = lps[{j - 1}] = {lps[j - 1]}")
                j = lps[j - 1]

        else:
            print("Несовпадение")
            if j != 0:
                print(f"Откат j = lps[{j - 1}] = {lps[j - 1]}")
                j = lps[j - 1]
            else:
                print("Сдвигаем i")
                i += 1

    print()
    if result:
        print("Все вхождения:", result)
        print(",".join(map(str, result)))
    else:
        print("Совпадений нет")
        print(-1)


kmp(input("pattern: "), input("text: "))
