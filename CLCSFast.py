import LCS
import sys
import numpy

def main (): 
  if len(sys.argv) != 2:
    sys.exit('Usage: `python LCS.py < input`')

  with open(sys.argv[1]) as f: 
    for line in f: 
      A,B = line.split()
      print '\nPaths for ' + A + ' x ' + B
      print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
      preallocate_table(A,B)
      return


def preallocate_table(A,B):
  global preallocated_table
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
  p[0] = single_shortest_path(p,0,-1,-1)
  p[m-1] = single_shortest_path(p,m-1,-1,-1)
  find_shortest_paths(p,0,m-1)
  print '\nHere are all paths:'
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
  for i in p:
    print i


def find_shortest_paths(p,upper_bound,lower_bound):
  print 'find_shortest_paths with u: ' + str(upper_bound) + ' and l: ' + str(lower_bound)
  if lower_bound - upper_bound <= 1:
    return
  mid = (upper_bound+lower_bound)/2
  p[mid] = single_shortest_path(p,mid,upper_bound,lower_bound)
  find_shortest_paths(p,mid,lower_bound)
  find_shortest_paths(p,upper_bound,mid)


def single_shortest_path(p,mid,upper_bound,lower_bound):
  global preallocated_table
  global double_A
  global original_B
  global m
  global n
  A = double_A[mid:mid+m]

  if (upper_bound >= 0):
    print 'This is the upper_bound:'
    print p[upper_bound]
  if (lower_bound >= 0):
    print 'This is the lower_bound:'
    print p[lower_bound]

  length_table = numpy.zeros(shape=(m+1,n+1))
  direction_table = numpy.chararray((m+1, n+1))
  direction_table[:] = '0'

  for (x,y), value in numpy.ndenumerate(direction_table):
    if x >= 1 and y >= 1:
      if A[x-1] == original_B[y-1]:
        length_table[x,y] = length_table[x-1,y-1] + 1
        direction_table[x,y] = '\\'
      elif length_table[x-1,y] >= length_table[x,y-1]:
        length_table[x,y] = length_table[x-1,y]
        direction_table[x,y] = '^'
      else:
        length_table[x,y] = length_table[x,y-1]
        direction_table[x,y] = '<'

  p_mid = print_LCS_nonrecursively(direction_table,A,m,n,mid)
  for value in p_mid:
    preallocated_table[value[0],value[1]] = str(mid+1)
  for x in range(n):
    direction_table[0,x+1] = original_B[x]
  for y in range(m):
    direction_table[y+1,0] = A[y%m]
  print '\n\np_mid[' + str(mid) + ']:'
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print p_mid
  print '\ndirection_table for ' + A + ' x ' + original_B + ':'
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print direction_table
  print '\npreallocated_table:'
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print preallocated_table
  return p_mid


def print_LCS_nonrecursively(direction_table,A,x,y,mid):
  path_i = []
  while x != 0 and y != 0:
    path_i.append((x+mid,y))
    if x == 1:
      break
    if direction_table[x,y] == '\\':
      x = x - 1
      y = y - 1
    elif direction_table[x,y] == '^':
      x = x - 1
    else:
      y = y - 1
  while x == 1 and y > 1:
    y = y - 1
    path_i.append((x+mid,y))
  return path_i


if __name__ == '__main__':
  main()