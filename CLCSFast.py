import LCS
import sys
import numpy

def main (): 
  if len(sys.argv) != 2:
    sys.exit('Usage: `python LCS.py < input`')

  with open(sys.argv[1]) as f: 
    for line in f: 
      A,B = line.split()
      print '\n~~~~~~~~~~~~~~~~~~~~~~~~~~'
      print '\nPaths for ' + A + ' x ' + B
      preallocate_table(A,B)
      return


def preallocate_table(A,B):
  global preallocated_table
  m = len(A)
  n = len(B)
  double_A = A + A
  double_m = len(double_A)
  
  # initialize the table of paths
  preallocated_table = numpy.chararray((double_m+1, n+1))
  preallocated_table[:] = '0'
  for x in range(n):
    preallocated_table[0,x+1] = B[x]
  for y in range(double_m):
    preallocated_table[y+1,0] = A[y%m]

  # initialzie the list of paths p_i
  p = [[] for i in range(m)]
  p[0] = single_shortest_path(p,0,double_A,B,m,-1,-1)
  p[m-1] = single_shortest_path(p,m-1,double_A,B,m,-1,-1)
  find_shortest_paths
  print '\n~~~~~~~~~~~~~~~~~~~~~~~~~~'
  for i in p:
    print i


def find_shortest_paths(A,B,p,u,l):
  if u - l <= 1:
    return
  mid = (u+l)/2
  p[mid] = single_shortest_path(A,B,l,u)
  find_shortest_paths(A,B,p,l,mid)
  find_shortest_paths(A,B,p,mid,u)


def single_shortest_path(p,mid,double_A,B,original_height,upper_bound,lower_bound):
  global preallocated_table
  A = double_A[mid:mid+original_height]
  m = len(A) + 1
  n = len(B) + 1

  length_table = numpy.zeros(shape=(m,n))
  direction_table = numpy.chararray((m, n))
  direction_table[:] = '0'

  for (x,y), value in numpy.ndenumerate(direction_table):
    if x >= 1 and y >= 1:
      if A[x-1] == B[y-1]:
        length_table[x,y] = length_table[x-1,y-1] + 1
        direction_table[x,y] = '\\'
      elif length_table[x-1,y] >= length_table[x,y-1]:
        length_table[x,y] = length_table[x-1,y]
        direction_table[x,y] = '^'
      else:
        length_table[x,y] = length_table[x,y-1]
        direction_table[x,y] = '<'

  p_mid = print_LCS_nonrecursively(direction_table,A,m-1,n-1,mid)
  for value in p_mid:
    preallocated_table[value[0],value[1]] = str(mid+1)
  for x in range(n-1):
    direction_table[0,x+1] = B[x]
  for y in range(m-1):
    direction_table[y+1,0] = A[y%m]
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'p_mid:'
  print p_mid
  print '\n~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'direction_table:'
  print direction_table
  print '\n~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'preallocated_table:'
  print preallocated_table
  return p_mid


def print_LCS_nonrecursively(direction_table,A,x,y,mid):
  path_i = []
  subsequence = ''
  while x != 0 and y != 0:
    path_i.append((x+mid,y))
    if direction_table[x,y] == '\\':
      subsequence += A[x-1]
      x = x - 1
      y = y - 1
    elif direction_table[x,y] == '^':
      x = x - 1
    else:
      y = y - 1
  return path_i


def print_LCS(direction_table,A,x,y,LCS):
  if x == 0 or y == 0:
    return
  if direction_table[x,y] == '\\':
    print_LCS(direction_table,A,x-1,y-1,LCS)
    LCS.append(A[x-1])
  elif direction_table[x,y] == '^':
    print_LCS(direction_table,A,x-1,y,LCS)
  else:
    print_LCS(direction_table,A,x,y-1,LCS)


if __name__ == '__main__':
  main()