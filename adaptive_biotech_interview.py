def generate_all_permutations(s: str):
    permutations = set()

    def _generate_all_permutations(s: str, start: int):
        fixed = s[:start]
        for i in range(start, len(s)):
            before = s[start:i]
            after = s[i+1:]
            t = fixed + s[i] + before + after
            if start == len(s) - 1:
                permutations.add(t)
            else:
                _generate_all_permutations(t, start+1)

    _generate_all_permutations(s, 0)

    return permutations


if __name__ == "__main__":
    x = generate_all_permutations("aacg")
    print(sorted(list(x)))
