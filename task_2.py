from trie import Trie, TrieNode


class SuffixTrie:
    def __init__(self):
        self.root = TrieNode()

    def put(self, key: str, value=None) -> None:
        current = self.root
        for char in reversed(key):
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.value = value

    def count_words_with_suffix(self, suffix: str) -> int:
        if not isinstance(suffix, str):
            raise TypeError("Suffix must be a string")

        current = self.root
        for char in reversed(suffix):
            if char not in current.children:
                return 0
            current = current.children[char]
        return self._count_words(current)

    def _count_words(self, node):
        count = 1 if node.value is not None else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count


class Homework(Trie):
    def count_words_with_suffix(self, pattern: str) -> int:
        if not isinstance(pattern, str):
            raise TypeError(
                f"Illegal argument for countWordsWithSuffix: pattern = {pattern} must be a string"
            )

        all_words = self._collect_all_words(self.root, "")
        return sum(1 for word in all_words if word.endswith(pattern))

    def _collect_all_words(self, node, prefix):
        words = []
        if node.value is not None:
            words.append(prefix)
        for char, child in node.children.items():
            words.extend(self._collect_all_words(child, prefix + char))
        return words

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError(
                f"Illegal argument for countWordsWithPrefix: prefix = {prefix} must be a string"
            )

        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]

        return True


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat

    suffix_trie = SuffixTrie()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        suffix_trie.put(word, i)

    assert suffix_trie.count_words_with_suffix("e") == 1  # apple
    assert suffix_trie.count_words_with_suffix("ion") == 1  # application
    assert suffix_trie.count_words_with_suffix("a") == 1  # banana
    assert suffix_trie.count_words_with_suffix("at") == 1  # cat
