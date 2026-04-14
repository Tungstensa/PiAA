def levenstein_4_ops(str_1, str_2, cost):
    n, m = len(str_1), len(str_2)

    current_row = [0] * (n + 1)

    print("  ", *["#"] + list(str_1))

    for j in range(1, n + 1):
        current_row[j] = current_row[j - 1] + 1
        if j >= 2 and str_1[j - 1] != str_1[j - 2]:
            current_row[j] = min(current_row[j], current_row[j - 2] + cost)

    print("# ", *current_row)

    for i in range(1, m + 1):
        previous_row = current_row
        current_row = [i] + [0] * n

        for j in range(1, n + 1):
            cost_change = 0 if str_1[j - 1] == str_2[i - 1] else 1

            res = min(
                previous_row[j] + 1,
                current_row[j - 1] + 1,
                previous_row[j - 1] + cost_change,
            )

            if j >= 2 and str_1[j - 1] != str_1[j - 2]:
                res = min(res, current_row[j - 2] + cost)

            current_row[j] = res

        print(str_2[i - 1], "", *current_row)

    return current_row[n]


s1 = input()
s2 = input()
print(levenstein_4_ops(s1, s2, 1))
