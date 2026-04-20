from lsp import build_lps


def kmp_cycle(pattern: str, text: str):
    m = len(pattern)
    if len(text) != m:
        print(-1)
        return
    print("=== KMP_CYCLE ПОИСК ===")
    text = text + text
    lps = build_lps(pattern, m)

    i = 0
    j = 0

    while i < 2 * m - 1:
        print(f"i={i}, j={j}, text[i]={text[i]}, pattern[j]={pattern[j]}")

        if text[i] == pattern[j]:
            print("Совпадение → двигаем i и j")
            i += 1
            j += 1

            if j == m:
                print(f"НАЙДЕНО! Начало в позиции {i - j}")
                print(i - j)
                return

        else:
            print("Несовпадение")
            if j != 0:
                print(f" Откат j = lps[{j - 1}] = {lps[j - 1]}")
                j = lps[j - 1]
            else:
                print("Сдвигаем i")
                i += 1

    print("Совпадений нет")
    print(-1)


kmp_cycle(input("A: "), input("B: "))
