import heapq

INF = float("inf")


def copy_matrix(matrix):
    return [row[:] for row in matrix]


def print_matrix(matrix, title="Матрица"):
    print(f"\n{title}")

    for row in matrix:
        print(" ".join("INF" if x == INF else f"{int(x):3}" for x in row))


def reduce_matrix(matrix):
    n = len(matrix)
    reduction_cost = 0

    for i in range(n):
        row_min = min(matrix[i])

        if row_min != INF and row_min > 0:
            reduction_cost += row_min

            for j in range(n):
                if matrix[i][j] != INF:
                    matrix[i][j] -= row_min

    for j in range(n):
        col_min = min(matrix[i][j] for i in range(n))

        if col_min != INF and col_min > 0:
            reduction_cost += col_min

            for i in range(n):
                if matrix[i][j] != INF:
                    matrix[i][j] -= col_min

    return reduction_cost


def find_best_zero(matrix):
    n = len(matrix)

    best_penalty = -1
    best_i = -1
    best_j = -1

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

            if penalty > best_penalty:
                best_penalty = penalty
                best_i = i
                best_j = j

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

    lower_bound = reduce_matrix(root_matrix)

    heap = []
    counter = 0

    heapq.heappush(
        heap,
        (
            lower_bound,
            counter,
            root_matrix,
            [],
            0,
        ),
    )

    counter += 1

    best_cost = INF
    best_edges = []

    step = 1

    while heap:
        print(f"\n========== ШАГ {step} ==========")
        step += 1

        bound, _, matrix_now, edges, real_cost = heapq.heappop(heap)

        print(f"Текущая граница: {bound}")
        print(f"Текущая стоимость: {real_cost}")
        print(f"Текущие ребра: {edges}")

        if bound >= best_cost:
            print("Ветка отсечена")
            continue

        if len(edges) == n:
            if real_cost < best_cost:
                best_cost = real_cost
                best_edges = edges

            continue

        i, j = find_best_zero(matrix_now)

        if not creates_cycle(edges, i, j, n):
            include_matrix = copy_matrix(matrix_now)

            for k in range(n):
                include_matrix[i][k] = INF

            for k in range(n):
                include_matrix[k][j] = INF

            include_matrix[j][i] = INF

            reduction = reduce_matrix(include_matrix)

            new_real_cost = real_cost + original[i][j]

            new_bound = bound + reduction

            heapq.heappush(
                heap,
                (
                    new_bound,
                    counter,
                    include_matrix,
                    edges + [(i, j)],
                    new_real_cost,
                ),
            )

            counter += 1

        exclude_matrix = copy_matrix(matrix_now)
        exclude_matrix[i][j] = INF
        reduction = reduce_matrix(exclude_matrix)

        exclude_bound = bound + reduction

        heapq.heappush(
            heap,
            (
                exclude_bound,
                counter,
                exclude_matrix,
                edges,
                real_cost,
            ),
        )

        counter += 1

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

matrix = []

for _ in range(n):
    row = list(map(float, input().split()))

    matrix.append([INF if x == -1 else x for x in row])

cost, edges = little(matrix)

path = build_path(edges)

print("\n========== РЕЗУЛЬТАТ ==========")
print("Минимальная стоимость:", cost)
print("Маршрут:", *path)
