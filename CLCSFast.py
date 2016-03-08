#Lea Coligado, 05785578, coligado
#Vicki Lau, 05789700, vickilau
#Stephany Yong, 05786562, syong

import sys
import numpy

def main (): 
  if len(sys.argv) != 1:
    sys.exit('Usage: `python CLCSFast.py < input`')
  for l in sys.stdin:
     A,B = l.split()
     print CLCS(A,B)
  return

def CLCS(A,B):
  global preallocated_table
  global subsequence_lengths
  global double_A
  global original_B
  global m
  global n
  m = len(A)
  n = len(B)
  double_A = A + A
  double_m = len(double_A)
  original_B = B
  
  # initialize the table of paths
  preallocated_table = numpy.chararray((double_m+1, n+1))
  preallocated_table[:] = '0'
  for x in range(n):
    preallocated_table[0,x+1] = B[x]
  for y in range(double_m):
    preallocated_table[y+1,0] = A[y%m]

  # initialize the list of paths p_i
  p = [[] for i in range(m)]
  subsequence_lengths = [0 for i in range(m)]
  p[0] = single_shortest_path(p, 0, -1, -1)
  p[m-1] = single_shortest_path(p, m-1, -1, -1)
  find_shortest_paths(p, 0, m-1)
  return max(subsequence_lengths)

def find_shortest_paths(p, upper_bound, lower_bound):
  if lower_bound - upper_bound <= 1:
    return
  mid = (upper_bound+lower_bound)/2
  p[mid] = single_shortest_path(p, mid, upper_bound, lower_bound)
  find_shortest_paths(p, mid, lower_bound)
  find_shortest_paths(p, upper_bound,mid)

def single_shortest_path(p, mid, upper_bound, lower_bound):
  global preallocated_table
  global double_A
  global original_B
  global m
  global n
  A = double_A[mid:mid+m]
  length_table = numpy.zeros(shape=(m+1,n+1))
  direction_table = numpy.chararray((m+1, n+1))
  direction_table[:] = '0'

  x = 0
  y = 0
  skipY = float('-inf')
  while x < m+1:
    while y < n+1:
      if x >= 1 and y >= 1:
        if y > skipY:
            if passed_upper_bound((x+mid, y), p[upper_bound]):
              length_table[x,y] = float('-inf')
              break
            elif passed_lower_bound((x+mid, y), p[lower_bound]):
              length_table[x,y] = float('-inf')
              skipY = y
            else:
              if A[x-1] == original_B[y-1]:
                length_table[x,y] = length_table[x-1,y-1] + 1
                direction_table[x,y] = '\\'
              elif length_table[x-1,y] >= length_table[x,y-1]:
                length_table[x,y] = length_table[x-1,y]
                direction_table[x,y] = '^'
              else:
                length_table[x,y] = length_table[x,y-1]
                direction_table[x,y] = '<'
      y = y + 1
    y = 0
    x = x + 1
  return print_LCS(direction_table, A, m, n, mid)

def passed_upper_bound(point, upper_bound):
  if not upper_bound:
    return False
  if point[0] < upper_bound[point[1]][-1]: 
    return True
  else:
    return False

def passed_lower_bound(point, lower_bound):
  if not lower_bound:
    return False;
  if point[0] > lower_bound[point[1]][0]:  
    return True 
  else:
    return False

def print_LCS(direction_table, A, x, y, mid):
  global subsequence_lengths
  path_i = [[] for i in range(x+y)]
  count = 0
  while x != 0 and y != 0:
    path_i[y].append(x+mid)
    if x == 1:
        break
    if direction_table[x,y] == '\\':
      count = count + 1
      x = x - 1
      y = y - 1
    elif direction_table[x,y] == '^':
      x = x - 1
    else:
      y = y - 1
  intersection_found = False
  while x == 1 and y >= 1:
    if direction_table[x,y] == '\\' and intersection_found == False:
      count = count + 1
      intersection_found = True
    path_i[y].append(x+mid)
    y = y - 1
  subsequence_lengths[mid] = count
  return path_i

if __name__ == '__main__':
  main()
