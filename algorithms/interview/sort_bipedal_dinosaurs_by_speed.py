#!/usr/bin/env python3
import math
import heapq


class Solution:
    def sort_bipedal_dinosaurs_by_speed(self, filePathDinoInfo, filePathAddInfo):
        bipedal_dinosaurs = {}
        g = 9.8

        with open(filePathAddInfo, 'r') as f:
            line = f.readline()
            while line:
                line = f.readline().strip()
                if line:
                    NAME, STRIDE_LENGTH, STANCE = line.split(',')
                    if STANCE == "bipedal":
                        bipedal_dinosaurs[NAME] = float(STRIDE_LENGTH)

        with open(filePathDinoInfo, 'r') as f:
            line = f.readline()
            while line:
                line = f.readline().strip()
                if line:
                    NAME, LEG_LENGTH, DIET = line.split(',')
                    if NAME in bipedal_dinosaurs:
                        STRIDE_LENGTH, LEG_LENGTH = bipedal_dinosaurs[NAME], float(LEG_LENGTH)
                        bipedal_dinosaurs[NAME] = ((STRIDE_LENGTH / LEG_LENGTH) - 1) * math.sqrt(LEG_LENGTH * g)

        heap = [(value, key) for key, value in bipedal_dinosaurs.items()]
        fastest = heapq.nlargest(len(heap), heap)  # O(n + mlogn)
        print(*[name for speed, name in fastest], sep='\n')


if __name__ == '__main__':
    Solution().sort_bipedal_dinosaurs_by_speed('dataset1.csv', 'dataset2.csv')
