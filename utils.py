from threading import Thread, Event

class StoppableThread(Thread):
	def __init__(self):
		super(StoppableThread, self).__init__()
		self._stop = Event()
	
	def stop(self):
		self._stop.set()

	def sleep(self, time):
		self._stop.wait(time)

	def isRunning(self):
		return not self._stop.isSet()

			

