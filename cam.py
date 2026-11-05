import cv2

class Cam():
	def __init__(self, index = 0):
		self.cap = cv2.VideoCapture(index)
		ret, self.frame = self.cap.read()

	def make_frame(self):
		ret, self.frame = self.cap.read()
		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
		self.hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2HSV)

	def show(self):
		cv2.imshow('frame', self.frame)
		cv2.waitKey(1)
	
	def res(self):
		return self.frame.shape

	def read_color(self, x, y):
		w,h = self.frame.shape[:2]
		if x >= 0 and x < w and y >= 0 and y < h:
			return self.frame[y][x]
		else:
			return [0,0,0]
	
	def read_color_hsv(self, x, y):
		w,h = self.frame.shape[:2]
		if x >= 0 and x < w and y >= 0 and y < h:
			return self.hsv_frame[y][x]
		else:
			return [0,0,0]

