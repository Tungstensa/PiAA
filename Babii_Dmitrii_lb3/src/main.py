def levenstein_4_ops(str_1, str_2, cost):
    n, m = len(str_1), len(str_2)

    current_row = [0] * (n + 1)

    print("Таблица:")
    print("   ", *["#"] + list(str_1))

    for j in range(1, n + 1):
        current_row[j] = current_row[j - 1] + 1
        print(f"first_row[{j}] -> удаление '{str_1[j-1]}': {current_row[j]}")

        if j >= 2 and str_1[j - 1] != str_1[j - 2]:
            new_val = current_row[j - 2] + cost
            if new_val < current_row[j]:
                print(
                    f"first_row[{j}] -> удаление пары "
                    f"'{str_1[j-2]}{str_1[j-1]}' за {cost}: {new_val}"
                )
            current_row[j] = min(current_row[j], new_val)

    print("# ", *current_row)
    print()

    for i in range(1, m + 1):
        previous_row = current_row
        current_row = [i] + [0] * n

        print(f"Обрабатываем символ '{str_2[i-1]}'")

        for j in range(1, n + 1):
            cost_change = 0 if str_1[j - 1] == str_2[i - 1] else 1

            delete_cost = previous_row[j] + 1
            insert_cost = current_row[j - 1] + 1
            replace_cost = previous_row[j - 1] + cost_change

            res = min(delete_cost, insert_cost, replace_cost)

            print(
                f"cell[{i}][{j}] ({str_1[j-1]} -> {str_2[i-1]}): "
                f"del={delete_cost}, ins={insert_cost}, rep={replace_cost}"
            )

            if j >= 2 and str_1[j - 1] != str_1[j - 2]:
                pair_delete = current_row[j - 2] + cost
                print(
                    f"cell[{i}][{j}] pair_del "
                    f"'{str_1[j-2]}{str_1[j-1]}' = {pair_delete}"
                )
                res = min(res, pair_delete)

            current_row[j] = res
            print(f" -> min = {res}")

        print(str_2[i - 1], *current_row)
        print()

    return current_row[n]


s1 = input()
s2 = input()
print("Ответ:", levenstein_4_ops(s1, s2, 1))
