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
      CLCS_fast(A,B)
      return


def CLCS_fast(A,B):
  A = 'ABCBDAB' # test string
  B = 'BDCABA' # test string

  double_A = A + A
  m = len(double_A)
  n = len(B)

  length_table = numpy.zeros(shape=(m,n)) #c
  direction_table = numpy.chararray((m, n))
  direction_table[:] = '0'

  for (x,y), value in numpy.ndenumerate(direction_table):
    if x >= 1 and y >= 1:
      if double_A[x] == B[y]:
        length_table[x,y] = length_table[x-1,y-1] + 1
        direction_table[x,y] = '\\'
      elif length_table[x-1,y] >= length_table[x,y-1]:
        length_table[x,y] = length_table[x-1,y]
        direction_table[x,y] = '^'
      else:
        direction_table[x,y] = '<'

  # create something that represents the path?
  # allocate storage for the paths p_i
  # compute p_0 using the whole table
  return

def find_shortest_paths(A,B,p,l,u):
  if u - l <= 1:
    return
  mid = (u+l)/2
  p[mid] = single_shortest_path(A,B,mid,p[l],p[u])
  find_shortest_paths(A,B,p,l,mid)
  find_shortest_paths(A,B,p,mid,u)


def cut (shorter, i):
  new_str = shorter[i:] + shorter[:i]
  return new_str


if __name__ == '__main__':
  main()