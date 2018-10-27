# should always be 1 try per movement.
# Otherwise there may be an issue with mouse acceleration
# Which will cause movements that happen within 0.3 secs of each other
# to be greater than intended.
import uinput
import time
import random
from PyQt4.QtGui import QPixmap, QApplication, QImage, QCursor

app = QApplication([])
device = uinput.Device((uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT))


# pos = QCursor.pos()
# x,y = pos.x(), pos.y()
# print x
# print y

time.sleep(2)

# dest = {"x": 1500, "y": 200}
# device.emit(uinput.REL_X, dest[0]-x, syn = False)
# device.emit(uinput.REL_Y, dest[1]-y)
# print QCursor.pos()

def move_or_print(target, tries=0):
	pos = QCursor.pos()
	device.emit(uinput.REL_X, target['x']-pos.x(), syn = False)
	device.emit(uinput.REL_Y, target['y']-pos.y())
	newpos = QCursor.pos()
	if newpos.x() != target['x'] or newpos.y() != target['y']:
		if tries<10:
			return 1+move_or_print(target, tries+1)
		else:
			if newpos.x() == 0:
				time.sleep(1)
				device.emit(uinput.REL_X, target['x']-newpos.x(), syn = False)
				device.emit(uinput.REL_Y, target['y']-newpos.y())
			newpos2 = QCursor.pos()
			print "maximum depth exceeded"
			print 'x:', target['x'], 'y:', target['y']
			print pos, newpos, newpos2
	return 0

def move_or_print_static(target):
	tries = 0
	max_tries = 8
	oldpos = []
	pos = QCursor.pos()
	while tries < max_tries and (pos.x(), pos.y()) != (target['x'], target['y']):
		# if (pos.x(), pos.y()) == (0,0):
			# tries += 0.1
		device.emit(uinput.REL_X, target['x']-pos.x(), syn = False)
		device.emit(uinput.REL_Y, target['y']-pos.y())
		tries += 1
		oldpos.append(pos)
		pos = QCursor.pos()
	# if tries == 2:
	# 	print "maximum depth exceeded"
	# 	print 'x:', target['x'], 'y:', target['y']
	# 	print oldpos
	# 	print pos
	return tries

dests = []
for i in range(100):
	dests.append({"x": int(random.random()*900+100), "y": int(random.random()*900+100)})
a = time.time()
s = 0
reslist = []
for i in range(100):
	res = move_or_print_static(dests[i])
	# time.sleep(0.275)
	s += res
	reslist.append(res)
print time.time() - a
print s/100.0, "tries per iteration"
print QCursor.pos(), dests[-1]['x'], dests[-1]['y']
print reslist


