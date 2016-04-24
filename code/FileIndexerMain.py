from FileIndexer import FileIndexer
from datetime import datetime
from datetime import timedelta as td

if __name__ == '__main__':
	fileIndexer = FileIndexer("..\data\unzipped")
	startDate = datetime(2016,4,14)
	endDate = datetime(2016,4,18)
	filesToUse = fileIndexer.getFilesForPeriod(startDate, endDate)
	print "Files To Use: ", filesToUse
