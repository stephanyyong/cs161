import LCS
import sys

def main (): 
	if len(sys.argv) != 2:
		sys.exit('Usage: `python LCS.py < input`')

	with open(sys.argv[1]) as f: 
		for line in f: 
			print line
			A,B = line.split()

			CLCS_slow (A, B)
			
		



def CLCS_slow (A,B):
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
		curr_lcs_len = LCS.LCS(cut(shorter, i), longer)
		if curr_lcs_len > max_seq_len:
			max_seq_len = curr_lcs_len

	print max_seq_len


def cut (shorter, i):
	new_str = shorter[i:] + shorter[:i]
	return new_str


if __name__ == '__main__':
	main()