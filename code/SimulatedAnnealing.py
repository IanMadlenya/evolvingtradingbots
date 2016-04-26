
from MRSingleDay import MRSingleDay
from FileIndexer import FileIndexer

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
	def modifyParameters(scalingParameter, meanDays):
		modScalingParameter = np.max((scalingParameter + np.random.normal()), 0.1)
		modMeanDays = np.maximum((meanDays + np.random.randint(-1, 2)), 1)
		return (modScalingParameter, modMeanDays)

	def simulatedAnnealing(currentFileName, initialMeanDays, initialScalingParameter, profitTarget, stopLoss, initTemp, thermostat, maxIter, reannealing):
		scores = []
		maxScores = []
		temperature = initTemp
		it = 0
		
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
	

	
	def runSimulatedAnnealing(fileName):
		initialMeanDays = 4
		initialScalingParameter = 0.8
		profitTarget = 2
		stopLoss = -5
		initTemp = 2
		thermostat = 0.95
		maxIter = 30
		reannealing = 10
		maxScore, maxScores, maxParams = simulatedAnnealing(fileName, initialMeanDays, initialScalingParameter, profitTarget, stopLoss, initTemp, thermostat, maxIter, reannealing)		
		return maxScore, maxParams[0], maxParams[1]
	
	fIndexer = FileIndexer("../data/unzipped/")
	startDate = datetime(2014,4,1)
	endDate = datetime(2016,1,1)
	fileList = fIndexer.getFilesForPeriod(startDate, endDate)
	#print "File List: ", fileList
	
	results = np.empty((fileList.shape[0], 3))
	#for i in np.array(fIndexer.shape[0]):
	for i in np.arange(fileList.shape[0]):
		maxScore, scalingParameter, meanObs = runSimulatedAnnealing(fileList[i])
		results[i][0] = scalingParameter
		results[i][1] = meanObs
		results[i][2] = maxScore
		print "Computed Result for ", fileList[i], " -- ", results[i][0], ", ", results[i][1], " -- max score: ", results[i][2]
	
	print "Results: ", results
	#runSimulatedAnnealing(fileList[0])
	#d = MRSingleDay("ZS201605_20160314.csv", 0.8, 4, 2, -5)
	#ro = d.calc_returns()
	#print "winning: {}, loosing: {}, profit: {}".format(ro.num_win, ro.num_loose, ro.cum_ret)
	



	print "all done boss"