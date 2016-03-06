import LCS
import sys
import numpy

def main (): 
  if len(sys.argv) != 2:
    sys.exit('Usage: `python LCS.py < input`')

  with open(sys.argv[1]) as f: 
    for line in f: 
      print line
      A,B = line.split()
      single_shortest_path(A,B)
      return


def set_up(A,B):
  double_A = A + A
  m = len(double_A)
  n = len(B)
  p = []


def find_shortest_paths(A,B,p,l,u):
  if u - l <= 1:
    return
  mid = (u+l)/2
  p[mid] = single_shortest_path(A,B,mid,p[l],p[u])
  find_shortest_paths(A,B,p,l,mid)
  find_shortest_paths(A,B,p,mid,u)


def single_shortest_path(A,B):
  A = 'ABCBDAB' # test string, later change the string to be that bounded by the table
  B = 'BDCABA' # test string

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

  print direction_table
  print length_table
  print_LCS(direction_table,A,len(A),len(B))

  # create something that represents the path?
  # allocate storage for the paths p_i
  # compute p_0 using the whole table
  return


def print_LCS(direction_table,A,x,y):
  if x == 0 or y == 0:
    return
  if direction_table[x,y] == '\\':
    print_LCS(direction_table,A,x-1,y-1)
    print A[x-1]
  elif direction_table[x,y] == '^':
    print_LCS(direction_table,A,x-1,y)
  else:
    print_LCS(direction_table,A,x,y-1)


if __name__ == '__main__':
  main()