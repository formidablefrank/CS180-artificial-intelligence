from testprogram import SpamFilter

if __name__ == '__main__':
	frHam = {'replica': 2, 'email': 1, 'weight': 2, 'paper': 1, 'brazil': 1}
	frSpam = {'replica': 1, 'email': 1, 'weight': 2, 'paper': 2, 'brazil': 1}
	testMail = ['replica', 'paper', 'weight', 'hi']
	print SpamFilter(3, 3, 6, frHam, frSpam).filterIfHam('test', testMail)