myOutput = open('output', 'r').read().split()
sirOutput = open('testoutput.txt', 'r').read().split()
errors = 0
a = min([len(myOutput), len(sirOutput)])

for i in range(a):
	if myOutput[i] == sirOutput[i]:
		print i
		continue
	else:
		print 'error in', i, myOutput[i], sirOutput[i]
		errors += 1

print 'total errors:', errors