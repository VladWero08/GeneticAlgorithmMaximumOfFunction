import math

class Codification:
    def __init__(self, a, b, p):
        self.left_closure = a
        self.right_closure = b
        self.precision = p

        # when we know the closures and the precision,
        # calculate the other attributes
        self.generate_num_of_characteristic()
        self.generate_discretization()

    def generate_num_of_characteristic(self):
        self.num_of_characteristics = math.ceil(math.log2((self.right_closure - self.left_closure) * (10 ** self.precision)))

    def generate_discretization(self):
        self.discretization = (self.right_closure - self.left_closure) / 2 ** self.num_of_characteristics

    def find_interval_for_bits_num(self, bits_num):
        # return the discretization interval in which
        # the binary number integrates
        num = 0

        for bit in range(self.num_of_characteristics - 1, -1, -1):
            num += bits_num[bit] * (2 ** (self.num_of_characteristics - bit - 1))

        return [self.left_closure + num * self.discretization, self.left_closure + (num + 1) * self.discretization]

    def find_interval_for_decimal_num(self, num):
        # return the binary number that represents
        # in which discretization interval is the number placed
        desired_interval = 0
        num_of_intervals = 2 ** self.num_of_characteristics

        # perform the binary search to find the corresponding interval
        left, right = 0, num_of_intervals
        while left <= right:
            mid = (left + right) // 2
            mid_left_closure = self.left_closure + self.discretization * mid
            mid_right_closure = self.left_closure + self.discretization * (mid + 1)

            if mid_left_closure <= num < mid_right_closure:
                desired_interval = mid
                break
            elif num >= mid_left_closure:
                left = mid + 1
            else:
                right = mid - 1

        bits_string = bin(desired_interval).replace("0b", "").zfill(self.num_of_characteristics)
        return [int(bit) for bit in bits_string]
