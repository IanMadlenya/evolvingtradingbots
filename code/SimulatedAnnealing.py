
from MRSingleDay import MRSingleDay

import numpy as np

import seaborn as sns
sns.set_style("white")

import time
import timeit

import scipy.stats 
import pandas as pd
import pymc as pm

import re
import numpy as np
from datetime import datetime
from datetime import timedelta as td

if __name__ == '__main__':

	def getFileDate(fileName):
		rDate = fileName.replace('.', '_').split('_')[1]
		return datetime.strptime(rDate, "%Y%m%d")
	v_getFileDate = np.vectorize(getFileDate)
	
	def modifyParameters(scalingParameter, meanDays):
		return (np.max((scalingParameter + np.random.normal()), 0.1), meanDays + np.random.randint(-1, 2))

	def getFileFromDate(d):
		r = datetime(2014,4,1)
		return "ZS201605_{0:04d}{1:02d}{2:02d}.csv".format(d.year, d.month, d.day)
	v_getFileFromDate = np.vectorize(getFileFromDate)

	def getFilesForPeriod(minuteFiles, start, end):
		#print "start: ", start, " end: ", end
		fileDates = v_getFileDate(minuteFiles)
		filesForPeriod = fileDates[(fileDates >= start) & (fileDates <= end)]
		#print "Files For Period: ", v_getFileFromDate(filesForPeriod)
		return v_getFileFromDate(filesForPeriod)
		
	def simulatedAnnealing(evalDate, initialMeanDays, initialScalingParameter, profitTarget, stopLoss, initTemp, thermostat, maxIter, reannealing):
		scores = []
		maxScores = []
		temperature = initTemp
		it = 0
		currentFileName = getFileFromDate(evalDate)
		print "Current File Name: ", currentFileName
		
		scalingParameter = initialScalingParameter
		meanDays = initialMeanDays
		
		d = MRSingleDay(currentFileName, scalingParameter, meanDays, profitTarget, stopLoss)

		ro = d.calc_returns()
		prevE = ro.cum_ret
		maxScore = prevE
		maxParams = (initialScalingParameter, meanDays)
		
		numBaseSteps = 2
		numIterations = 0
		while(it >= 0):
			L = np.max((np.floor(temperature * numBaseSteps).astype(int),1))
			proposedScaling, proposedMean = modifyParameters(scalingParameter, meanDays)
			d = MRSingleDay(currentFileName, proposedScaling, proposedMean, profitTarget, stopLoss)
			ro = d.calc_returns()
			newE = ro.cum_ret
			deltaE = newE - prevE
			u = np.random.uniform()
			prob = np.exp( -deltaE/temperature)

			# If we're heading up (in this case higher score better), keep
			if(newE > prevE):
				scalingParameter = proposedScaling
				meanDays = proposedMean
				prevE = newE
				it += 1
			elif u < prob:
				scalingParameter = proposedScaling
				meanDays = proposedMean
				prevE = newE
				it += 1
				
			if(prevE > maxScore):
				maxScore = prevE
				maxParams = (scalingParameter, meanDays)
				maxScores.append(prevE)
				print "Max Score Increase ", numIterations, " max score: ", maxScore, " parameters: ", maxParams
			
			numIterations += 1
			
			if(it % reannealing) == 0:
				temperature = thermostat * temperature
				
				# reheat
				if(temperature < 0.01):
					temperature = 1
					scalingParameter, meanDays = maxParams
					prevE = maxScore
					
			if numIterations > maxIter:
				print "Ending @ ", numIterations, " with max parameters: ", maxParams
				break
				
		return maxScore, maxScores, maxParams
		
		
	d = MRSingleDay("ZS201605_20160314.csv", 0.8, 4, 2, -5)
	ro = d.calc_returns()
	print "winning: {}, loosing: {}, profit: {}".format(ro.num_win, ro.num_loose, ro.cum_ret)
	
	evalDate = datetime(2016,3,14)
#ZS201605_20160314.csv
	initialMeanDays = 4
	initialScalingParameter = 0.8
	profitTarget = 2
	stopLoss = -5
	initTemp = 2
	thermostat = 0.95
	maxIter = 30
	reannealing = 10
	simulatedAnnealing(evalDate, initialMeanDays, initialScalingParameter, profitTarget, stopLoss, initTemp, thermostat, maxIter, reannealing)


	print "all done boss"