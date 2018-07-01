

import heapq

# load contents of text file into a list numList
NUMLIST_FILENAME = "median.txt" # requested interval: [-10000, 10000] / answer: 1213
# NUMLIST_FILENAME = "tests/median-0.txt" # medians: [9, 9, 9, 7, 7, 3, 4, 4, 5, 5, 6, 6]
# NUMLIST_FILENAME = "tests/median-1.txt" # medians: [2, 2, 8, 7, 7, 3, 4]

inFile = open(NUMLIST_FILENAME, 'r')

heapLo = [] # holds the lower numbers in negative value to be able to extract the highest
heapHi = [] # holds the highest numbers
heapq.heapify(heapHi)
heapq.heapify(heapLo)

# holds the medians for each interaction
medians = [] 

# initializing the heaps 
with inFile as f:
    for integers in f.readlines():
        num = int(integers.strip())     

        # pushing the numbers into one of the heaps heapLo, heapHi
        if not heapLo:
            heapq.heappush(heapLo, num * -1)
        else:
            lenHeapLo = len(heapLo)
            lenHeapHi = len(heapHi)
            hiLo = heapq.heappop(heapLo) * -1

            # push last median
            medians.append(hiLo)

            if num <= hiLo:
                if lenHeapLo <= lenHeapHi:
                    heapq.heappush(heapLo, num * -1)
                    heapq.heappush(heapLo, hiLo * -1)
                else:
                    heapq.heappush(heapLo, num * -1)
                    heapq.heappush(heapHi, hiLo)
            else: 
                if lenHeapHi < lenHeapLo:
                    heapq.heappush(heapHi, num)
                    heapq.heappush(heapLo, hiLo * -1)
                else:
                    loHi = heapq.heappop(heapHi)
                    if loHi < num:
                        heapq.heappush(heapHi, num)
                        heapq.heappush(heapLo, loHi * -1)
                        heapq.heappush(heapLo, hiLo * -1)
                    else:
                        heapq.heappush(heapLo, num * -1)
                        heapq.heappush(heapHi, loHi)
                        heapq.heappush(heapLo, hiLo * -1)

# push last median
medians.append(heapq.heappop(heapLo) * -1)

print('medians', medians)
print('result', sum(medians)%10000)
