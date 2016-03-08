import LCS
import sys
import numpy

def main (): 
  if len(sys.argv) != 2:
    sys.exit('Usage: `python LCS.py < input`')

  with open(sys.argv[1]) as f: 
    for line in f: 
      A,B = line.split()
      preallocate_table(A,B)


def preallocate_table(A,B):
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

  # initialzie the list of paths p_i
  p = [[] for i in range(m)]
  subsequence_lengths = [0 for i in range(m)]
  p[0] = single_shortest_path(p, 0, -1, -1)
  p[m-1] = single_shortest_path(p, m-1, -1, -1)
  find_shortest_paths(p, 0, m-1)
  # print '\nHere are all paths:'
  # print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
  # for i in p:
  #   print i
  # print '\nHere are all subsequence_lengths:'
  # print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
  # for i in subsequence_lengths:
  #   print i
  print max(subsequence_lengths)

def find_shortest_paths(p, upper_bound, lower_bound):
  # print 'find_shortest_paths with upper_bound: ' + str(upper_bound) + ' and l: ' + str(lower_bound)
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

  # for every row in the direction_table 
  #   for every column in the direction_table:
  #     check if the current cell is within the bounds of the lower and upper bound
  #     if it is, then assign costs as normal
  #     if it is not because it has exceeded an upper_bound path going right, then go to next row
  #     if it is not because it has exceeded a lower_bound path going down, then go to next column

  x = 0
  y = 0
  skipY = float('-inf')
  while x < m+1:
    while y < n+1:
      if y <= skipY:
        y = y + 1
      elif x >= 1 and y >= 1:
        if passed_upper_bound((x+mid, y), p[upper_bound]):
          #print 'upper_bound passed at (' + str(x+mid) + ', ' + str(y) + ')!'
          length_table[x,y] = float('-inf')
          break
        elif passed_lower_bound((x+mid, y), p[lower_bound]):
          #print 'lower_bound passed at (' + str(x+mid) + ', ' + str(y) + ')!'
          length_table[x,y] = float('-inf')
          skipY = y
        else:
          #print '(' + str(x+mid) + ', ' + str(y) + ')'
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
  p_mid = list(reversed(print_LCS_nonrecursively(direction_table, A, m, n, mid)))
  for value in p_mid:
    preallocated_table[value[0],value[1]] = str(mid+1)
  for x in range(n):
    direction_table[0,x+1] = original_B[x]
  for y in range(m):
    direction_table[y+1,0] = A[y%m]
  return p_mid


def passed_upper_bound(point, upper_bound):
  if not upper_bound:
    return False
  highest_point_on_column = float('inf')
  for p in upper_bound:
    if p[1] == point[1]:
      if p[0] < highest_point_on_column:
        highest_point_on_column = p[0]
  if (point[0] < highest_point_on_column):
    return True
  else:
    return False


def passed_lower_bound(point, lower_bound):
  if not lower_bound:
    return False;
  lowest_point_on_column = float('-inf')
  for p in lower_bound:
    if p[1] == point[1]:
      if p[0] > lowest_point_on_column:
        lowest_point_on_column = p[0]
  if (point[0] > lowest_point_on_column):
    return True 
  else:
    return False


def print_LCS_nonrecursively(direction_table, A, x, y, mid):
  global subsequence_lengths
  path_i = []
  count = 0
  while x != 0 and y != 0:
    path_i.append((x+mid,y))
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
    path_i.append((x+mid,y))
    y = y - 1
  subsequence_lengths[mid] = count
  return path_i


if __name__ == '__main__':
  main()