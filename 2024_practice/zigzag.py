#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'minOperations' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY arr as parameter.
#

# ahhhhhhhhhhhh the 0th item is the length of the array? this is criminal! :D

## eh, never mind, I give up


# we need to calc both, no matter what
from copy import deepcopy


def minOperations(arr):
    lh_no_of_replace = 0
    hl_no_of_replace = 0
    number_pos = 1
    prev_modified = False
    for i in range(0, len(arr)):
        if number_pos == len(arr):
            break

        if number_pos % 2 != 0:
            if arr[i + 1] <= arr[i] and not prev_modified:
                lh_no_of_replace += 1
                prev_modified = True
            elif arr[i + 1] >= arr[i] and not prev_modified:
                hl_no_of_replace += 1
                prev_modified = True
            else:
                prev_modified = False
        else:
            if arr[i + 1] >= arr[i] and not prev_modified:
                lh_no_of_replace += 1
                prev_modified = True
            elif arr[i + 1] <= arr[i] and not prev_modified:
                hl_no_of_replace += 1
                prev_modified = True
            else:
                prev_modified = False

        number_pos += 1

    print(arr, lh_no_of_replace, hl_no_of_replace)

    # can you join again?
    # yes, but try solving it here, I can still see your code, my zoom conf ends the calls at 40 mins exactly


# [8,2,1 ,2,3,4 ,5,2,9]
# [8,2,1+,2,3,4-,5,2,9]


if __name__ == '__main__':

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr_count = int(input().strip())

    arr = []

    for _ in range(arr_count):
        arr_item = int(input().strip())
        arr.append(arr_item)

    result = minOperations(arr)

    fptr.write(str(result) + '\n')

    fptr.close()
