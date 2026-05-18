def copy_matrix(matrix):
    return [row[:] for row in matrix]


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
    stack = [(root_matrix, lower_bound, [], 0)]

    best_cost = INF
    best_edges = []

    while stack:
        matrix_now, bound, edges, real_cost = stack.pop()

        if bound >= best_cost:
            continue

        if len(edges) == n:
            if real_cost < best_cost:
                best_cost = real_cost
                best_edges = edges

            continue

        i, j = find_best_zero(matrix_now)

        if i == -1:
            continue

        if not creates_cycle(edges, i, j, n):
            include_matrix = copy_matrix(matrix_now)

            for k in range(n):
                include_matrix[i][k] = INF

            for k in range(n):
                include_matrix[k][j] = INF

            include_matrix[j][i] = INF

            reduction = reduce_matrix(include_matrix)
            new_real_cost = real_cost + original[i][j]
            new_bound = new_real_cost + reduction
            stack.append((include_matrix, new_bound, edges + [(i, j)], new_real_cost))

        exclude_matrix = copy_matrix(matrix_now)

        exclude_matrix[i][j] = INF
        reduction = reduce_matrix(exclude_matrix)

        stack.append((exclude_matrix, real_cost + reduction, edges, real_cost))

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

print(cost)
print(*path)
