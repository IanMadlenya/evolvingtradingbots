from MRSingleDay import MRSingleDay
from FileIndexer import FileIndexer

import numpy as np
from datetime import datetime


def modifyParameters(scalingParameter, meanDays):
    modScalingParameter = np.max((scalingParameter + np.random.normal()), 0.1)
    modMeanDays = np.maximum((meanDays + np.random.randint(-1, 2)), 1)
    return (modScalingParameter, modMeanDays)

def cum_ret_fitness(ro_in):
    """Cumulative Returns Fitness function"""
    return ro_in.cum_ret

def win_ratio_fitness(ro_in):
    """Win Ratio Fitness function"""
    denom = ro_in.num_loose + ro_in.num_win
    if denom == 0: return 0.0
    return 20.0 * ro_in.num_win/denom

def avg_profit_fitness(ro_in):
    """Average Profit Per Trade Fitness function"""
    denom = ro_in.num_loose + ro_in.num_win
    if denom == 0: return 0.0
    return 5.0 * ro_in.cum_ret/denom

def simulatedAnnealing(currentFileName, initialMeanDays, initialScalingParameter, profitTarget, stopLoss, initTemp,
                           thermostat, maxIter, reannealing, fitness_ftn):
    scores = []
    maxScores = []
    temperature = initTemp
    it = 0

    print "Current File Name: ", currentFileName

    scalingParameter = initialScalingParameter
    meanDays = initialMeanDays

    d = MRSingleDay(currentFileName, scalingParameter, meanDays, profitTarget, stopLoss)

    ro = d.calc_returns()
    prevE = fitness_ftn(ro)
    maxScore = prevE
    maxParams = (initialScalingParameter, meanDays)

    numBaseSteps = 2
    numIterations = 0
    while (it >= 0):
        L = np.max((np.floor(temperature * numBaseSteps).astype(int), 1))
        proposedScaling, proposedMean = modifyParameters(scalingParameter, meanDays)
        d = MRSingleDay(currentFileName, proposedScaling, proposedMean, profitTarget, stopLoss)
        ro = d.calc_returns()
        newE = fitness_ftn(ro)
        deltaE = newE - prevE
        u = np.random.uniform()
        prob = np.exp(-deltaE / temperature)

        # If we're heading up (in this case higher score better), keep
        if (newE > prevE):
            scalingParameter = proposedScaling
            meanDays = proposedMean
            prevE = newE
            it += 1
        elif u < prob:
            scalingParameter = proposedScaling
            meanDays = proposedMean
            prevE = newE
            it += 1

        if (prevE > maxScore):
            maxScore = prevE
            maxParams = (scalingParameter, meanDays)
            maxScores.append(prevE)
            print "Max Score Increase ", numIterations, " max score: ", maxScore, " parameters: ", maxParams

        numIterations += 1

        if (it % reannealing) == 0:
            temperature = thermostat * temperature

            # reheat
            if (temperature < 0.01):
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
    fitness_ftn = avg_profit_fitness
    maxScore, maxScores, maxParams = simulatedAnnealing(fileName, initialMeanDays, initialScalingParameter,
                                                        profitTarget, stopLoss, initTemp, thermostat, maxIter,
                                                        reannealing, fitness_ftn)
    return maxScore, maxParams[0], maxParams[1]


if __name__ == '__main__':

    fIndexer = FileIndexer("../data/min/")
    startDate = datetime(2014, 4, 1)
    endDate = datetime(2016, 1, 1)
    fileList = fIndexer.getFilesForPeriod(startDate, endDate)

    results = np.empty((fileList.shape[0], 3))
    fw = open("SA_avgprofit_results.txt", 'w', 0)

    for i in np.arange(fileList.shape[0] - 1):
        maxScore, scalingParameter, meanObs = runSimulatedAnnealing(fileList[i])
        results[i][0] = scalingParameter
        results[i][1] = meanObs
        results[i][2] = maxScore
        print "Computed Result for ", fileList[i], " -- ", results[i][0], ", ", results[i][1], " -- max score: ", \
            results[i][2]

        # get next day's performance with these parms
        d = MRSingleDay(fileList[i+1], scalingParameter, meanObs, 2.0, -5.0)
        ro = d.calc_returns()
        fw.write("{}\t{}\t{}\t{}\t{}\n".format(fileList[i], maxScore, scalingParameter, meanObs, ro.cum_ret))

    print "Results: ", results

    print "all done boss"
