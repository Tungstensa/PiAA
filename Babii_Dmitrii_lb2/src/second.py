def build_mst(n, matrix):
    visited = [False] * n
    min_bound = [INF] * n
    parent = [-1] * n

    min_bound[start] = 0

    for _ in range(n):
        v = -1
        best = INF
        for i in range(n):
            if not visited[i] and min_bound[i] < best:
                best = min_bound[i]
                v = i

        visited[v] = True

        for to in range(n):
            if not visited[to] and matrix[v][to] < min_bound[to]:
                min_bound[to] = matrix[v][to]
                parent[to] = v

    tree = [[] for _ in range(n)]
    for i in range(n):
        if parent[i] != -1:
            p = parent[i]
            tree[p].append(i)
            tree[i].append(p)

    for i in range(n):
        tree[i].sort(key=lambda x: matrix[i][x])

    return tree


def dfs(tree):
    visited = [False] * n
    path = []

    def dfs(v):
        visited[v] = True
        path.append(v)
        for to in tree[v]:
            if not visited[to]:
                dfs(to)

    dfs(start)
    path.append(start)

    cost = 0.0
    for i in range(len(path) - 1):
        cost += matrix[path[i]][path[i + 1]]

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

tree = build_mst(n, matrix)
path, cost = dfs(tree)
print(f"{cost:.2f}")
print(*path)
