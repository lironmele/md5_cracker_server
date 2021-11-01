import BaseAscii

class Range:
    def __init__(self, md5="", start='aaaaaaaa', stop='zzzzzzzz', range_count=10):
        self.start = BaseAscii.BaseAscii(start)
        self.stop = BaseAscii.BaseAscii(stop)
        self.range_count = range_count
        self.md5 = md5
        self.ranges = []
        if self.range_count != 1:
            self.ranges = self // self.range_count
        self.taken = False

    def to_list(self):
        lst = []
        
        for r in self.ranges:
            lst.append([r.start.string, r.stop.string])
        
        return lst

    def __bool__(self):
        return self.taken

    def __str__(self) -> str:
        string = f"start: {self.start.string}, stop: {self.stop.string}, count: {self.range_count}"
        
        for r in self.ranges:
            string += f"\r\n\t{r}"

        return string

    def __floordiv__(self, x):
        ranges = []
        r = None
        start_part = None
        end_part = None
        count_per_part = (self.stop - self.start) // x

        for i in range(x-1):
            start_part = BaseAscii.BaseAscii(self.start+(i*count_per_part))
            stop_part = BaseAscii.BaseAscii(self.start+((i+1)*count_per_part))

            ranges.append(Range(self.md5, start_part.string, stop_part.string, 1))

        start_part = BaseAscii.BaseAscii(self.start+((x-1)*count_per_part))
        stop_part = BaseAscii.BaseAscii(self.stop.string)

        ranges.append(Range(self.md5, start_part.string, stop_part.string, 1))

        return ranges

def main():
    default = Range()
    
    print(default)

if __name__ == '__main__':
    main()