import itertools
import sys
from bitarray import bitarray


class Tcmine():
    def __init__(self, min_rf, min_cs, max_or, input_file, output_file):
        self.Min_rf = float(min_rf)
        self.Min_cs = float(min_cs)
        self.Max_or = float(max_or)
        self.Input_file = input_file
        self.Output_file = output_file
        self.number_of_transactions = self.get_num_transactions()
        self.data = self.get_data()
        self.data_count = self.get_data_count()
        self.coverage_patterns = self.mine_data()
        # print('coverage patterns are')
        # print(self.coverage_patterns)
        # print(self.data)
        # print(self.number_of_transactions)
        # print(self.data['c'] & self.data['a']) bitwise operations
        # print(self.data['d'].count()) used for counting number of 1 bits
    def get_data(self):
        t_list = {}
        with open(self.Input_file, 'r') as f:
            lines = f.readlines()
            for itr, line in enumerate(lines):
                trans_list = line.strip().split(',')
                for item in trans_list:
                    if item in t_list:
                        t_list[item][itr] = 1
                    else:
                        t_list[item] = bitarray(self.number_of_transactions)
                        t_list[item].setall(0)
                        t_list[item][itr] = 1

        f.close()
        if '' in t_list:
            t_list.pop('')
        return t_list

    def get_data_count(self):
        c1 = {}
        for keys in self.data:
            c1[keys] = self.data[keys].count()
        return c1

    def check_overlap_ratio(self, pattern):
        pass

    def get_num_transactions(self):
        with open(self.Input_file, 'r') as f:
            lines = f.readlines()
            num_transactions = len(lines)
        f.close()
        return num_transactions

    def mine_data(self):
        min_rf = self.Min_rf * self.number_of_transactions
        min_cs = self.Min_cs * self.number_of_transactions
        max_or = self.Max_or
        coverage_patterns = []
        # sorted_patterns_1 = sorted(c1.items(), key=lambda l: l[1], reverse=True)
        non_overlap_patterns_1 = dict((key, value) for (key, value) in self.data_count.items() if value >= min_rf)
        coverage_list = [key for (key, value) in non_overlap_patterns_1.items() if value >= min_cs]
        coverage_patterns.extend(coverage_list)
        non_overlap_patterns_list = [[key] for (key, value) in non_overlap_patterns_1.items()]
        # print(non_overlap_patterns_list)
        candidate_pattern = self.candidate_generation(non_overlap_patterns_list, len(non_overlap_patterns_list))
        while len(candidate_pattern) != 0:
            non_overlap_patterns_list = [pattern for pattern in candidate_pattern if self.get_overlap_ratio(pattern) <= max_or]
            coverage_list = [pattern for pattern in non_overlap_patterns_list if self.get_coverage_support(pattern).count() >= min_cs]
            candidate_pattern = self.candidate_generation(non_overlap_patterns_list, len(non_overlap_patterns_list))
            candidate_pattern = self.prune(candidate_pattern, non_overlap_patterns_list)
            coverage_patterns.extend(coverage_list)
        return coverage_patterns

    def prune(self, candidate_pattern, non_overlap_patterns_list):
        # this method prunes the candidate patterns generated
        # any k -1 subset of k-set pattern is not in k-1 non overlap patterns then
        # it is also not present k-set non overlap pattern so can be removed
        for pattern in candidate_pattern:
            k_subset_list = list(itertools.combinations(pattern, len(pattern)-1))
            k_subset_list = [list(k) for k in k_subset_list]
            for kitem in k_subset_list:
                if kitem in non_overlap_patterns_list:
                    continue
                else:
                    candidate_pattern.remove(pattern)
                    break
        return candidate_pattern

    def get_pattern_count(self, pattern):
        # returns the frequency of a particular set of items in database
        b = self.data[pattern[0]]
        for i in range(1, len(pattern)):
            b = b & self.data[pattern[i]]
        return b.count()

    def get_coverage_support(self, pattern):
        # this function returns the coverage support of the given pattern and its count
        b = self.data[pattern[0]]
        for i in range(1, len(pattern)):
            b = b | self.data[pattern[i]]
        return b

    def get_overlap_ratio(self, pattern):
        length = len(pattern)
        first_pattern = pattern[0:length-1]
        last_item = pattern[length-1]
        first_bit_array = self.get_coverage_support(first_pattern)
        intersection_array = first_bit_array & self.data[last_item]
        overlap_ratio = intersection_array.count() / self.data_count[last_item]
        return overlap_ratio

    def sort_non_overlap_pattern(self, pattern):
        # takes a pattern and sort them according to their frequency in database
        sorted_pattern = sorted(pattern, key=lambda x: self.data_count[x], reverse=True)
        return sorted_pattern

    def candidate_generation(self, pattern, length):
        # this function takes a k-pattern and joins with itself to give k+1 pattern
        candidate = []
        for i in range(0, length):
            element1 = pattern[i]
            for j in range(i+1, length):
                element2 = pattern[j]
                len_each_pattern = len(element1)
                if len_each_pattern == 1:
                    next_list = element1 + element2
                    candidate.append(self.sort_non_overlap_pattern(next_list))
                else:
                    if element1[0:len_each_pattern-1] == element2[0:len_each_pattern-1]:
                        next_list = element1[0:len_each_pattern-1]
                        next_list.append(element1[len_each_pattern-1])
                        next_list.append(element2[len_each_pattern-1])
                        candidate.append(self.sort_non_overlap_pattern(next_list))
        return candidate


if __name__ == '__main__':
    min_rf = sys.argv[1]
    min_cs = sys.argv[2]
    max_or = sys.argv[3]
    input_file = sys.argv[4]
    output_file = 'out.txt'
    Tcmine(min_rf, min_cs, max_or, input_file, output_file)
