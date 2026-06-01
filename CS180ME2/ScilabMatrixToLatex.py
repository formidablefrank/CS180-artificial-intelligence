import sys
import math

if __name__ == '__main__':
	try:
		input = open('inputmatrix', 'r')
		output = open('outputmatrix', 'w')
	except IOError:
		print 'Error creating output file'
		sys.exit(-1)

	string = input.read()
	input.close()

	string2 = string.replace(' ', '').replace('\n', '').replace('\t', '').split('')
	try:
		string2.remove('')
	except Exception:
		pass
	else:
		pass
	L = len(string2)
	print string2, L

	for i in range(1, L + 1):
		if i % int(math.sqrt(L)) == 0:
			output.write(string2[i - 1] + ' \\\\\n')
		else:
			output.write(string2[i - 1] + ' & ')
