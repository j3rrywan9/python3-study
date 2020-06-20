# LC 394


class Solution(object):
    def decode_string(self, s):
        stack = []
        curr_num = 0
        curr_string = ""

        for char in s:
            if char == '[':
                stack.append(curr_string)
                stack.append(curr_num)
                curr_string = ""
                curr_num = 0
            elif char == ']':
                num = stack.pop()
                prev_string = stack.pop()
                curr_string = prev_string + num * curr_string
            elif char.isdigit():
                curr_num = curr_num * 10 + int(char)
            else:
                curr_string += char

        return curr_string
