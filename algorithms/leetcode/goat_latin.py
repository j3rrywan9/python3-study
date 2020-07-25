# LC 824


class Solution:
    def to_goat_latin(self, S):
        def proc(index, word):
            if word[0] not in 'aeiouAEIOU':
                word = word[1:] + word[0]

            return word + 'ma' + ('a' * index)

        return ' '.join([proc(i, w) for i, w in enumerate(S.split(), 1)])
