class BaseAscii:
    def __init__(self, string):
        self.string = string
        self.base26_list = self._to_base_26_list()
        self.number = self._base_26_to_10()
    
    def _to_base_26_list(self):
        return list(map(lambda c: ord(c) - 97, self.string))

    def _base_26_to_10(self):
        base10 = 0
        n = len(self.base26_list) - 1

        for i in self.base26_list:
            base10 += i * 26**n
            n -= 1

        return base10

    def _to_ascii(number):
        string = ''
        result = number
        remainder = number % 26
        n = 0

        while result != 0:
            string = chr(remainder + 97) + string
            result //= 26 
            remainder = result % 26
            n += 1

        return string

    def __add__(self, x):
        string = BaseAscii._to_ascii(self.number + x)
        string = string.rjust(len(self.string), 'a')
        return string

    def __sub__(self, x):
        if self.number > x.number:
            return self.number - x.number + 1
        else:
            return x.number - self.number + 1

    def __gt__(self, x):
        return self.number > x.number

    def __lt__(self, x):
        return self.number < x.number

def main():
    start = BaseAscii("aaa")
    stop = BaseAscii("aaz")

    count = stop - start
    print(count)

    half = BaseAscii(start+count//2)

    print(stop - half)

if __name__ == "__main__":
    main()
