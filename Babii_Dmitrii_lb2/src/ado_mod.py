def print_matrix(matrix, title="Матрица"):
    print(f"\n{title}")

    for row in matrix:
        print(" ".join("INF" if x == INF else f"{int(x):3}" for x in row))


def print_tree(tree):
    print("\nТекущее MST:")

    for i in range(len(tree)):
        print(f"{i}: {tree[i]}")


def build_mst(n, matrix):
    visited = [False] * n
    min_bound = [INF] * n
    parent = [-1] * n

    min_bound[start] = 0

    print("\n========== ПОСТРОЕНИЕ MST ==========")

    for step in range(n):
        print(f"\n--- ШАГ {step + 1} ---")

        v = -1
        best = INF

        # Поиск вершины с минимальной границей
        for i in range(n):
            if not visited[i] and min_bound[i] < best:
                best = min_bound[i]
                v = i

        print(f"Выбрана вершина: {v}")
        print(f"Минимальная стоимость подключения: {best}")

        visited[v] = True

        print(f"Посещенные вершины: {visited}")

        # Обновление границ
        for to in range(n):
            if not visited[to] and matrix[v][to] < min_bound[to]:

                old = min_bound[to]

                min_bound[to] = matrix[v][to]
                parent[to] = v

                print(
                    f"Обновление вершины {to}: "
                    f"{old} -> {min_bound[to]} "
                    f"(родитель {v})"
                )

        print(f"min_bound: {min_bound}")
        print(f"parent:    {parent}")

    # Построение дерева
    tree = [[] for _ in range(n)]

    print("\n========== ПОСТРОЕНИЕ ДЕРЕВА ==========")

    for i in range(n):
        if parent[i] != -1:
            p = parent[i]

            tree[p].append(i)
            tree[i].append(p)

            print(f"Ребро MST: {p} <-> {i}")

    for i in range(n):
        tree[i].sort(key=lambda x: matrix[i][x])

    print_tree(tree)

    return tree


def dfs(tree):
    visited = [False] * n
    path = []

    print("\n========== DFS ОБХОД ==========")

    def walk(v):
        print(f"\nПереход в вершину {v}")

        visited[v] = True
        path.append(v)

        print(f"Текущий путь: {path}")

        for to in tree[v]:
            if not visited[to]:
                print(f"Из {v} идем в {to}")
                walk(to)

    walk(start)

    path.append(start)

    print(f"\nВозврат в стартовую вершину {start}")
    print(f"Итоговый путь: {path}")

    cost = 0.0

    print("\n========== ПОДСЧЕТ СТОИМОСТИ ==========")

    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]

        edge_cost = matrix[a][b]

        print(f"{a} -> {b} = {edge_cost}")

        cost += edge_cost

    print(f"\nПолная стоимость: {cost}")

    return path, cost


start = int(input())

matrix = []

while True:
    try:
        line = input()

        if not line:
            break

        matrix.append(list(map(float, line.split())))

    except:
        break

n = len(matrix)
INF = float("inf")

for i in range(n):
    for j in range(n):
        if matrix[i][j] == -1:
            matrix[i][j] = INF

for i in range(n):
    matrix[i][i] = INF

print_matrix(matrix, "Исходная матрица")

tree = build_mst(n, matrix)

path, cost = dfs(tree)

print("\n========== РЕЗУЛЬТАТ ==========")
print(f"Стоимость: {cost:.2f}")
print("Маршрут:", *path)
