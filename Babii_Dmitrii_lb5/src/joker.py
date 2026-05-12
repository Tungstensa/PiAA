from collections import deque


class Node:
    def __init__(self, node_id: int):
        self.node_id: int = node_id
        self.next: dict[str, int] = {}
        self.link: int = 0
        self.term_link: int = 0
        self.output = []


class AhoCorasick:
    def __init__(self):
        self.nodes: list[Node] = [Node(0)]

    def add_pattern(self, pattern: str, block_info: tuple[int, int]):
        v = 0
        print(f"Добавление блока '{pattern}' (смещение {block_info[1]}):")
        for ch in pattern:
            if ch not in self.nodes[v].next:
                new_id = len(self.nodes)
                self.nodes[v].next[ch] = new_id
                self.nodes.append(Node(new_id))

                print(f"  Из узла {v} по символу '{ch}' -> новый узел {new_id}")
            else:
                print(
                    f"  Из узла {v} по символу '{ch}' -> уже есть переход в {self.nodes[v].next[ch]}"
                )

            v = self.nodes[v].next[ch]

        self.nodes[v].output.append(block_info)
        print(
            f"  Узел {v} помечен как терминальный для блока со смещением {block_info[1]}\n"
        )

    def build_links(self, ch: str, u: int, v: int):
        j = self.nodes[v].link

        while j > 0 and ch not in self.nodes[j].next:
            j = self.nodes[j].link

        if ch in self.nodes[j].next:
            self.nodes[u].link = self.nodes[j].next[ch]
        else:
            self.nodes[u].link = 0

    def build_term_links(self, u: int):
        link_u = self.nodes[u].link

        if self.nodes[link_u].output:
            self.nodes[u].term_link = link_u
        else:
            self.nodes[u].term_link = self.nodes[link_u].term_link

    def build(self):
        print("--- Построение ссылок автомата ---")
        q = deque()

        for ch, nxt in self.nodes[0].next.items():
            self.nodes[nxt].link = 0
            q.append(nxt)
            print(f"Узел {nxt}={ch} (первый уровень): link -> 0")

        while q:
            v = q.popleft()

            for ch, u in self.nodes[v].next.items():
                self.build_links(ch, u, v)
                self.build_term_links(u)

                print(
                    f"Узел {u}={ch}: link -> {self.nodes[u].link}, "
                    f"term_link -> {self.nodes[u].term_link}"
                )

                q.append(u)

        print("------------------------------------------\n")

    def search(self, text: str, t_len: int, p_len: int):
        counts = [0] * t_len
        print(f"--- Процесс поиска блоков в тексте '{text}' ---")

        v = 0
        for i, ch in enumerate(text):
            while v > 0 and ch not in self.nodes[v].next:
                v = self.nodes[v].link

            if ch in self.nodes[v].next:
                v = self.nodes[v].next[ch]

            cur = v
            while cur > 0:
                if self.nodes[cur].output:
                    for block_len, block_offset in self.nodes[cur].output:
                        start_of_match = (i - block_len + 1) - block_offset
                        if 0 <= start_of_match <= t_len - p_len:
                            counts[start_of_match] += 1
                            print(
                                f"  Блок найден! "
                                f"Конец в {i}, "
                                f"начало шаблона может быть в {start_of_match + 1}"
                            )

                cur = self.nodes[cur].term_link
        print("----------------------------------------------\n")

        return counts


if __name__ == "__main__":
    text = input()
    p_full = input()
    wildcard = input()

    t_len = len(text)
    p_len = len(p_full)

    blocks = []

    start = -1
    for i, char in enumerate(p_full):
        if char != wildcard:
            if start == -1:
                start = i

        else:
            if start != -1:
                blocks.append((p_full[start:i], start))
                start = -1

    if start != -1:
        blocks.append((p_full[start:], start))

    ac = AhoCorasick()

    for b_text, b_offset in blocks:
        ac.add_pattern(b_text, (len(b_text), b_offset))

    ac.build()

    counts = ac.search(text, t_len, p_len)

    print("ИТОГОВЫЙ ВЫХОД:")
    print(f"Количество вершин в автомате: {len(ac.nodes)}")

    k = len(blocks)

    for i in range(t_len - p_len + 1):
        if counts[i] == k:
            print(i + 1)
