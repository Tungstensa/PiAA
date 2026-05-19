def copy_matrix(matrix):
    return [row[:] for row in matrix]


def print_matrix(matrix, title="Матрица"):
    print(f"\n{title}")

    for row in matrix:
        print(" ".join("INF" if x == INF else f"{int(x):3}" for x in row))


def reduce_matrix(matrix):
    n = len(matrix)
    reduction_cost = 0

    print_matrix(matrix, "До редукции")

    # Редукция строк
    for i in range(n):
        row_min = min(matrix[i])

        if row_min != INF and row_min > 0:
            print(f"Минимум строки {i}: {row_min}")

            reduction_cost += row_min

            for j in range(n):
                if matrix[i][j] != INF:
                    matrix[i][j] -= row_min

    print_matrix(matrix, "После редукции строк")

    # Редукция столбцов
    for j in range(n):
        col_min = min(matrix[i][j] for i in range(n))

        if col_min != INF and col_min > 0:
            print(f"Минимум столбца {j}: {col_min}")

            reduction_cost += col_min

            for i in range(n):
                if matrix[i][j] != INF:
                    matrix[i][j] -= col_min

    print_matrix(matrix, "После редукции столбцов")

    print(f"Стоимость редукции: {reduction_cost}\n")

    return reduction_cost


def find_best_zero(matrix):
    n = len(matrix)

    best_penalty = -1
    best_i = -1
    best_j = -1

    print("\nОценки нулевых элементов:")

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                continue

            row_values = [
                matrix[i][k] for k in range(n) if k != j and matrix[i][k] != INF
            ]

            col_values = [
                matrix[k][j] for k in range(n) if k != i and matrix[k][j] != INF
            ]

            row_min = min(row_values) if row_values else 0
            col_min = min(col_values) if col_values else 0

            penalty = row_min + col_min

            print(
                f"Ноль ({i}, {j}) -> "
                f"min_row={row_min}, "
                f"min_col={col_min}, "
                f"штраф={penalty}"
            )

            if penalty > best_penalty:
                best_penalty = penalty
                best_i = i
                best_j = j

    print(f"\nВыбран ноль: ({best_i}, {best_j}) " f"со штрафом {best_penalty}")

    return best_i, best_j


def creates_cycle(edges, start, end, n):
    graph = {}

    for a, b in edges:
        graph[a] = b

    graph[start] = end

    current = end
    length = 1

    while current in graph:
        current = graph[current]
        length += 1

        if current == start:
            return length < n

    return False


def little(matrix):
    n = len(matrix)

    original = copy_matrix(matrix)

    root_matrix = copy_matrix(matrix)

    print("\n========== НАЧАЛО АЛГОРИТМА ЛИТТЛА ==========")

    lower_bound = reduce_matrix(root_matrix)

    print(f"Начальная нижняя граница: {lower_bound}")

    stack = [(root_matrix, lower_bound, [], 0)]

    best_cost = INF
    best_edges = []

    step = 1

    while stack:
        print(f"\n\n========== ШАГ {step} ==========")
        step += 1

        matrix_now, bound, edges, real_cost = stack.pop()

        print(f"Текущая граница: {bound}")
        print(f"Текущая стоимость: {real_cost}")
        print(f"Текущие ребра: {edges}")

        print_matrix(matrix_now, "Текущая матрица")

        if bound >= best_cost:
            print("Ветка отсечена")
            continue

        if len(edges) == n:
            print("Найден полный маршрут")

            if real_cost < best_cost:
                best_cost = real_cost
                best_edges = edges

                print(f"Новый лучший маршрут: {best_edges}")
                print(f"Новая лучшая стоимость: {best_cost}")

            continue

        i, j = find_best_zero(matrix_now)

        if i == -1:
            print("Нулей не найдено")

            used_from = {a for a, b in edges}
            used_to = {b for a, b in edges}

            remaining_from = [v for v in range(n) if v not in used_from]
            remaining_to = [v for v in range(n) if v not in used_to]

            if len(remaining_from) == 1 and len(remaining_to) == 1:
                a = remaining_from[0]
                b = remaining_to[0]

                if not creates_cycle(edges, a, b, n) or len(edges) == n - 1:
                    final_edges = edges + [(a, b)]

                    final_cost = real_cost + original[a][b]

                    print(f"Автодобавление последнего ребра ({a}, {b})")

                    if final_cost < best_cost:
                        best_cost = final_cost
                        best_edges = final_edges

                        print(f"Новый лучший маршрут: {best_edges}")
                        print(f"Новая лучшая стоимость: {best_cost}")

            continue

        if not creates_cycle(edges, i, j, n):
            print(f"\n--- ВКЛЮЧАЕМ ребро ({i}, {j}) ---")

            include_matrix = copy_matrix(matrix_now)

            for k in range(n):
                include_matrix[i][k] = INF

            for k in range(n):
                include_matrix[k][j] = INF

            include_matrix[j][i] = INF

            reduction = reduce_matrix(include_matrix)

            new_real_cost = real_cost + original[i][j]
            new_bound = bound + original[i][j] + reduction

            print(f"Новая стоимость: {new_real_cost}")
            print(f"Новая граница: {new_bound}")

            stack.append(
                (
                    include_matrix,
                    new_bound,
                    edges + [(i, j)],
                    new_real_cost,
                )
            )

        else:
            print(f"Ребро ({i}, {j}) создает цикл")

        # Исключение ребра
        print(f"\n--- ИСКЛЮЧАЕМ ребро ({i}, {j}) ---")

        exclude_matrix = copy_matrix(matrix_now)

        exclude_matrix[i][j] = INF

        reduction = reduce_matrix(exclude_matrix)

        exclude_bound = real_cost + reduction

        print(f"Граница после исключения: {exclude_bound}")

        stack.append(
            (
                exclude_matrix,
                exclude_bound,
                edges,
                real_cost,
            )
        )

    return best_cost, best_edges


def build_path(edges):
    graph = {}

    for a, b in edges:
        graph[a] = b

    path = [0]

    current = 0

    while True:
        current = graph[current]

        path.append(current)

        if current == 0:
            break

    return path


n = int(input())
INF = float("inf")
matrix = []

for _ in range(n):
    row = list(map(float, input().split()))

    matrix.append([INF if x == -1 else x for x in row])

cost, edges = little(matrix)

path = build_path(edges)

print("\n========== РЕЗУЛЬТАТ ==========")
print("Минимальная стоимость:", cost)
print("Маршрут:", *path)
