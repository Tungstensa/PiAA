from collections import deque


class Node:
    def __init__(self, node_id):
        self.node_id: int = node_id
        self.next: dict[str, int] = {}
        self.link: int = 0
        self.term_link: int = 0
        self.output = []


class AhoCorasick:
    def __init__(self):
        self.nodes: list[Node] = [Node(0)]

    def add_pattern(self, pattern: str, pattern_id: int):
        v = 0
        print(f"Добавление шаблона '{pattern}' (ID: {pattern_id}):")
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
        self.nodes[v].output.append(pattern_id)
        print(f"  Узел {v} помечен как терминальный для шаблона {pattern_id}\n")

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
            v: int = q.popleft()

            for ch, u in self.nodes[v].next.items():
                self.build_links(ch, u, v)
                self.build_term_links(u)

                print(
                    f"Узел {u}={ch}: link -> {self.nodes[u].link}, term_link -> {self.nodes[u].term_link}"
                )
                q.append(u)

    def search(self, text: str, patterns: list[str]):
        print(f"--- Процесс поиска в тексте '{text}' ---")
        result = []
        v = 0
        for i, ch in enumerate(text):
            while v > 0 and ch not in self.nodes[v].next:
                v = self.nodes[v].link

            if ch in self.nodes[v].next:
                v = self.nodes[v].next[ch]

            cur = v
            while cur > 0:
                if self.nodes[cur].output:
                    for pattern_id in self.nodes[cur].output:
                        p_len = len(patterns[pattern_id - 1])
                        start = i - p_len + 2
                        end = i + 1
                        result.append((start, end, pattern_id))
                        print(
                            f"  Найдено: '{patterns[pattern_id-1]}' в позиции {start}-{end}"
                        )
                cur = self.nodes[cur].term_link
        return result


if __name__ == "__main__":
    text = input().strip()
    n = int(input().strip())

    patterns = []
    for _ in range(n):
        patterns.append(input().strip())

    ac = AhoCorasick()

    for i, pattern in enumerate(patterns, 1):
        ac.add_pattern(pattern, i)

    ac.build()

    matches = ac.search(text, patterns)

    matches.sort()
    intersected_ids = set()
    k = len(matches)

    for i in range(k):
        l1, r1, id1 = matches[i]
        is_hit = False

        for j in range(k):
            if i == j:
                continue
            l2, r2, id2 = matches[j]
            if max(l1, l2) <= min(r1, r2):
                is_hit = True
                break

        if is_hit:
            intersected_ids.add((l1, id1))

    print("ИТОГОВЫЙ ВЫХОД:")
    print(f"Количество вершин в автомате: {len(ac.nodes)}")

    final_output = sorted(list(intersected_ids))
    for pos, p_id in final_output:
        print(f"{pos} {p_id}")
