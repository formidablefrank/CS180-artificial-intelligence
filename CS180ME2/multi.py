from threading import Thread

x = 100


def function(i):
	return i**64


def notThreaded():
	var = map(function, range(x))
	print var


def Threaded():
	for i in range(x):
		thread = Thread(target = function(i))
		thread.start()

if __name__ == '__main__':
	notThreaded()
	#Threaded()