def build_lps(pattern: str, m: int):
    length = 0
    i = 1
    lps = [0] * m

    print("Шаблон:", pattern)

    while i < m:
        print(f"i={i}, length={length}")

        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            print(f"Совпадение → lps[{i}] = {length}")
            i += 1
        else:
            if length != 0:
                print(
                    f"Несовпадение → откат length = lps[{length - 1}] = {lps[length - 1]}"
                )
                length = lps[length - 1]
            else:
                lps[i] = 0
                print(f"Несовпадение → lps[{i}] = 0")
                i += 1

    print("Итоговый LPS:", lps)
    print()
    return lps
