import os
import numpy as np
from datetime import datetime
from datetime import timedelta as td

class FileIndexer:

	def __init__(self, fileDirectory):
		self.fileDirectory = fileDirectory
		
		self.minuteFiles = np.array(os.listdir(fileDirectory))
		self.dateconv = lambda x: datetime.strptime(x, "%Y%m%d %H:%M:%S")		
	
	def getFileDate(fileName):
		rDate = fileName.replace('.', '_').split('_')[1]
		return datetime.strptime(rDate, "%Y%m%d")
	v_getFileDate = np.vectorize(getFileDate)
	
	def readMinuteFile(fullFileName):
		names=("date","open","high","low","close","volume"	,"adjclose")
		types=("|S18", float, float, float, float, int, float)
		data = np.genfromtxt(fullFileName, delimiter=",", skip_header=1, names=names, dtype=None, converters={'date': self.dateconv})
		return data
		
	def getFullFileName(self, minuteFileName):
		return self.minuteDirectory + "/" + minuteFileName
	v_getFullFileName = np.vectorize(getFullFileName)
	
	def getFilesForPeriod(self, startDate, endDate):
		minuteDates = self.v_getFileDate(self.minuteFiles)
		minuteDatesAndFiles = np.vstack((self.minuteFiles, minuteDates)).T
				
		return minuteDatesAndFiles[(minuteDatesAndFiles[:,1] >= startDate) & (minuteDatesAndFiles[:,1] <= endDate)][:,0]