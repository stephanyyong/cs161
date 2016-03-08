#Lea Coligado, 05785578, coligado
#Vicki Lau, 05789700, vickilau
#Stephany Yong, 05786562, syong

import sys
import numpy as np

arr = np.zeros((2048, 2048), dtype=int)

def main():
  if len(sys.argv) != 1:
    sys.exit('Usage: `python CLCSSlow.py < input`')

  for l in sys.stdin:
    A,B = l.split()
    print CLCS(A,B)
  return

def LCS(A,B):
  m = len(A)
  n = len(B)

  for i in range(1,m+1):
    for j in range(1,n+1):
      if A[i-1] == B[j-1]:
        arr[i][j] = arr[i-1][j-1]+1
      else:
        arr[i][j] = max(arr[i-1][j], arr[i][j-1])

  return arr[m][n]

def CLCS(A,B):
  len_A = len(A)
  len_B = len(B)
  if len_A > len_B:
	  shorter = B
	  longer = A
  else:
		shorter = A
		longer = B

  max_seq_len = 0 

  for i in range (0, len(shorter)):
	  curr_lcs_len = LCS(cut(shorter, i), longer)
	  if curr_lcs_len > max_seq_len:
		  max_seq_len = curr_lcs_len

  return max_seq_len

def cut (shorter, i):
	new_str = shorter[i:] + shorter[:i]
	return new_str

if __name__ == '__main__':
	main()
