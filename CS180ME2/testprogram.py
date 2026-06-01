# CS 180 ME2: Naive Bayes Classifier for Spam Filtering
# Date started: January 25, 2014

import glob
from multiprocessing import Pool, cpu_count
from decimal import Decimal
import sys


class SpamFilter:
	"""ADT for spam filter"""

	def __init__(self, cHam, cSpam, tot, frHam, frSpam):
		self.total = Decimal(tot)
		self.cHam = Decimal(cHam)
		self.cSpam = Decimal(cSpam)
		self.frHam = frHam
		self.frSpam = frSpam
		self.alphaDic = sorted(list(set(frHam.keys() + frSpam.keys())))
		self.tHam = 0
		self.tSpam = 0
		#print 'SPAM FILTER BEGIN:\ncHam -> %s, cSpam -> %s\nfrHam -> %s\nfrSpam -> %s\nDic -> %s\n' % (self.cHam, self.cSpam, self.frHam, self.frSpam, self.alphaDic)

	def filterIfHam(self, fname, wlist):
		#print 'ANALYZING %s...' % filename
		vector = []
		#print wlist
		for word in self.alphaDic:
			if word in wlist:
				vector.append(1)
			else:
				vector.append(0)
		#print vector
		prob = self.prob('ham', vector)
		if prob >= Decimal(.5):
			self.tHam += 1
			return '%-7s - ham' % fname
		else:
			self.tSpam += 1
			return '%-7s - spam' % fname

	def prob(self, typed, vector):
		pWiHam, pWiSpam, P = Decimal(1.), Decimal(1.), Decimal(1.)
		for ctr in range(len(vector)):
			if vector[ctr] == 1:
				#print '%s - %f - %f' % (self.alphaDic[ctr], self.frHam.get(self.alphaDic[ctr], 0)/self.cHam, self.frSpam.get(self.alphaDic[ctr], 0)/self.cSpam)
				pWiHam *= Decimal(self.frHam.get(self.alphaDic[ctr], Decimal(0))/self.cHam)
				pWiSpam *= Decimal(self.frSpam.get(self.alphaDic[ctr], Decimal(0))/self.cSpam)
		if pWiSpam == 0 and pWiHam == 0:
			#print '\nUSE LAMBDA SMOOTHING'
			pWiHam, pWiSpam = Decimal(1.), Decimal(1.)
			for ctr in range(len(vector)):
				if vector[ctr] == 1:
					#print '%s - %f - %f' % (self.alphaDic[ctr], self.frHam.get(self.alphaDic[ctr], 1.0) / (self.cHam + 2.0), self.frSpam.get(self.alphaDic[ctr], 1.0) / (self.cSpam + 2.0))
					pWiHam *= Decimal(self.frHam.get(self.alphaDic[ctr], Decimal(1.0)) / (self.cHam + Decimal(2.0)))
					pWiSpam *= Decimal(self.frSpam.get(self.alphaDic[ctr], Decimal(1.0)) / (self.cSpam + Decimal(2.0)))
		#print 'pWiHam = %s\npWiSpam = %s' % (pWiHam, pWiSpam)
		if typed == 'ham':
			P = (self.cHam / self.total * pWiHam) / (self.cHam / self.total * pWiHam + self.cSpam / self.total * pWiSpam)
			return P
		elif typed == 'spam':
			P = (self.cSpam / self.total * pWiSpam) / (self.cHam / self.total * pWiHam + self.cSpam / self.total * pWiSpam)
			return P
		else:
			print 'ERROR IN TYPE'


def processFiles(args):
	files, totals = args
	dicti = {}
	count = 0
	bound = totals
	for myfile in files:
		string = list(set(open(myfile, 'r').read().split()))
		for word in string:
			if word in dicti.keys():
				dicti[word] += 1
			else:
				dicti.update({word: 1})
		if count >= bound:
			break
		else:
			count += 1
	return dicti

if __name__ == '__main__':
	print 'START PROGRAM'
	HamFiles = glob.glob('dataset/training/ham/*')
	SpamFiles = glob.glob('dataset/training/spam/*')
	totalHam, totalSpam = float(len(HamFiles)), float(len(SpamFiles))
	total = totalHam + totalSpam
	#print 'Training data: ham -> %d, ham -> %d' % (totalHam, totalSpam)

	print 'READING TRAINING DATA...',
	hamDict, spamDict = Pool(cpu_count()).map(processFiles, [(HamFiles, totalHam), (SpamFiles, totalSpam)])
	print 'COMPLETE'

	MailFilter = SpamFilter(totalHam, totalSpam, total, hamDict, spamDict)
	print 'FILTERING TEST FILES'
	try:
		outputFile = open('output', 'w')
	except IOError:
		print 'Error creating output file'
		sys.exit(-1)
	TestFiles = glob.glob('dataset/test/*')
	for i in range(1, len(TestFiles) + 1):
		filename = str(i) + '.txt'
		testfile = 'dataset/test\\' + filename
		TestFiles.remove(testfile)
		print >> outputFile, MailFilter.filterIfHam(filename, list(set(open(testfile, 'r').read().split())))
	for testFile in TestFiles:
		print >> outputFile, MailFilter.filterIfHam(filename, list(set(open(testfile, 'r').read().split())))
	print >> outputFile, 'Total number of ham messages: %d' % MailFilter.tHam
	print >> outputFile, 'Total number of spam messages: %d' % MailFilter.tSpam
	outputFile.close()
	print 'END OF PROGRAM. see output file'