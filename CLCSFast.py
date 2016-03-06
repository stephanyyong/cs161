import LCS
import sys
import numpy

def main (): 
  if len(sys.argv) != 2:
    sys.exit('Usage: `python LCS.py < input`')

  with open(sys.argv[1]) as f: 
    for line in f: 
      A,B = line.split()
      # print 'SINGLE SHORTEST PATH: ' + single_shortest_path(A,B)
      print "Paths for " + line + ":"
      set_up(A,B)


def set_up(A,B):
  double_A = A + A
  double_m = len(double_A)
  m = len(A)
  n = len(B)
  p = ['' for x in range(m)]
  # p[0] = single_shortest_path(double_A,B,0,m)
  # p[m-1] = single_shortest_path(double_A,B,m-1,double_m)
  for r in range(m):
    p[r] = single_shortest_path(A,B,r,r+m)
  # find_shortest_paths(double_A,B,p,0,m)
  print p
  print '\n'


def find_shortest_paths(A,B,p,l,u):
  if u - l <= 1:
    return
  mid = (u+l)/2
  p[mid] = single_shortest_path(A,B,l,u)
  find_shortest_paths(A,B,p,l,mid)
  find_shortest_paths(A,B,p,mid,u)


def single_shortest_path(A,B,lower_bound,upper_bound):
  A = A[lower_bound:upper_bound] # should have the same length as original A
  m = len(A) + 1
  n = len(B) + 1

  length_table = numpy.zeros(shape=(m,n)) #c
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
  # LCS = []
  # print_LCS(direction_table,A,len(A),len(B),LCS)
  LCS = print_LCS_nonrecursively(direction_table,A,x,y)
  return LCS


def print_LCS_nonrecursively(direction_table,A,x,y):
  subsequence = ''
  while x != 0 and y != 0:
    if direction_table[x,y] == '\\':
      subsequence += A[x-1]
      x = x - 1
      y = y - 1
    elif direction_table[x,y] == '^':
      x = x - 1
    else:
      y = y - 1
  return subsequence


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