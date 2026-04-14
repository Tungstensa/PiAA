import time
import matplotlib.pyplot as plt
import numpy as np


def solve(n_input, silent=True):
    def get_scale(val):
        for i in range(2, val + 1):
            if val % i == 0:
                return i, val // i
        return val, 1

    n_local, scale = get_scale(n_input)
    board = [0] * n_local
    full = (1 << n_local) - 1
    state = {"best_k": 10**9, "best_res": []}
    current_res = []

    if not silent:
        print(f"Начало поиска для N={n_input}, Масштаб x{scale}")

    def place(x, y, size, add=True):
        mask = ((1 << size) - 1) << x
        for i in range(size):
            if add:
                board[y + i] |= mask
            else:
                board[y + i] &= ~mask

    def max_sq(x, y):
        size = 1
        while x + size < n_local and y + size < n_local:
            mask = ((1 << (size + 1)) - 1) << x
            if any(board[y + i] & mask for i in range(size + 1)):
                break
            size += 1
        return size

    def find_first():
        for y in range(n_local):
            if board[y] != full:
                free = ~board[y] & full
                x = (free & -free).bit_length() - 1
                if not silent:
                    print(
                        f"Первая пустая клетка найдена в ({x+1}, {y+1}). "
                        f"Макс. размер там: {max_sq(x, y)}"
                    )
                return x, y
        return None

    def backtrack(count):
        if count >= state["best_k"]:
            return

        pos = find_first()

        if pos is None:
            if not silent:
                print(f"Найдено решение: {count} квадратов")

            state["best_k"] = count
            state["best_res"] = current_res[:]

            if not silent:
                print(f"Новое лучшее решение - {count}")
                print(f"Состояний стека - ", len(current_res))

            return

        x, y = pos
        m = max_sq(x, y)

        for size in range(m, 0, -1):

            if not silent and size != m:
                print(f"Уменьшаем квадрат, теперь {size} в ({x+1}, {y+1})")

            if not silent:
                print(f"Ставим квадрат {size} в ({x+1}, {y+1})")

            place(x, y, size, True)
            current_res.append((x, y, size))

            backtrack(count + 1)

            current_res.pop()
            place(x, y, size, False)

            if not silent:
                print(f"Убираем квадрат {size} в ({x+1}, {y+1})")
                print(f"Состояний стека - ", len(current_res))

            if not silent and size == 1:
                print(f"Все варианты для ({x+1}, {y+1}) исчерпаны, идем выше по стеку")

    def prefill():
        mid, small = (n_local + 1) // 2, n_local // 2

        place(0, 0, mid)
        current_res.append((0, 0, mid))

        place(mid, 0, small)
        current_res.append((mid, 0, small))

        place(0, mid, small)
        current_res.append((0, mid, small))

    prefill()
    backtrack(3)

    if not silent:
        print(state["best_k"])
        for x, y, size in state["best_res"]:
            print(f"({x * scale + 1}, {y * scale + 1}) {size * scale}")

    return state["best_k"]


def run_benchmarks():

    even_ns = np.array([n for n in range(6, 41, 2)])
    comp_ns = np.array(
        [
            n
            for n in range(6, 41)
            if any(n % i == 0 for i in range(2, int(n**0.5) + 1)) and n % 2 != 0
        ]
    )
    prime_ns = np.array([5, 7, 11, 13, 17, 19, 23, 29, 31, 37])

    def measure_times(ns, repeats=5):
        times = []
        for n in ns:
            run_times = []
            for _ in range(repeats):
                start = time.perf_counter()
                solve(n, silent=True)
                run_times.append(time.perf_counter() - start)
            times.append(np.median(run_times))
        return np.array(times)

    even_times = measure_times(even_ns)
    comp_times = measure_times(comp_ns)
    prime_times = measure_times(prime_ns)

    coef_even = np.mean(even_times)
    theor_even = np.full_like(even_ns, coef_even, dtype=float)

    log_c_times = np.log(comp_times)
    alpha_c, beta_c = np.polyfit(comp_ns, log_c_times, 1)
    x_comp_smooth = np.linspace(min(comp_ns), max(comp_ns), 200)
    theor_comp = np.exp(alpha_c * x_comp_smooth + beta_c)

    log_p_times = np.log(prime_times)
    alpha_p, beta_p = np.polyfit(prime_ns, log_p_times, 1)
    x_prime_smooth = np.linspace(min(prime_ns), max(prime_ns), 200)
    theor_prime = np.exp(alpha_p * x_prime_smooth + beta_p)

    plt.figure(figsize=(14, 10))

    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(even_ns, even_times, "g-o", label="Четное-практика")
    ax1.plot(even_ns, theor_even, "g--", label="Четное-теория (O(1))")

    ax1.plot(comp_ns, comp_times, "b-o", label="Составное-практика")
    ax1.plot(x_comp_smooth, theor_comp, "b--", label="Составное-теория")

    ax1.set_xlabel("N")
    ax1.set_ylabel("Время (сек)")
    ax1.grid(True)
    ax1.legend()

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(prime_ns, prime_times, "r-o", label="Простое-практика")
    ax2.plot(x_prime_smooth, theor_prime, "r--", label="Простое-теория")

    ax2.set_xlabel("N")
    ax2.set_ylabel("Время (сек)")
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    user_input = int(input())

    if user_input == 0:
        run_benchmarks()
    else:
        start = time.perf_counter()

        solve(user_input, silent=False)

        end = time.perf_counter()
        print(f"\n{end - start} секунд")
