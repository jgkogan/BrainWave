import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import getData
import os

def listdir_nohidden(path):
	for f in os.listdir(path):
         if not f.startswith('.'):
			if not f.endswith('p'):
				yield f

#get name of dataset to work with
dataset = getData.getCurrentDataset()

#gets directory of raw data and where output should go
rawDataDirectory = '../datasets/' + dataset + '/'
outputDirectory = '../analyzedDatasets/' + dataset + '/'



originalFiles = map(lambda x: x.rpartition('.')[0], listdir_nohidden(outputDirectory + 'neuronSimilarityAnalysis'))

def getSimilarities(location):
	f = open(location+'.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)
	data=data[1:]
	data=map(lambda x: 
			map(lambda y: 
				y.strip()
			,x.strip().split(','))[:5]
		,data)

	return data

def getLocations():
	f = open(rawDataDirectory + 'centers.txt', 'r')
	data=[]
	for line in f:
	    data.append(line)
	data=map(lambda x: 
			map(lambda y: 
				float(y.strip())
			,x.strip().split('\t'))
		,data)

	return data

def euclidDistance(pt1,pt2):
	return np.linalg.norm(np.array(pt1)-np.array(pt2))



neuronLocations=getLocations()

def createPlot(name):	
	similarities = getSimilarities(outputDirectory + 'neuronSimilarityAnalysis/'+name)

	for x in range(len(similarities)):
		similarities[x][0]=int(similarities[x][0])
		similarities[x][1]=int(similarities[x][1])
		similarities[x][2]=int(similarities[x][2])
		similarities[x][3]=float(similarities[x][3])
		similarities[x][4]=float(similarities[x][4])

	distanceToSimilarities={}
	for simil in similarities:
		neuron1=simil[0]
		neuron2=simil[1]
		shift=simil[2]
		similarity=simil[3]
		distance=euclidDistance(neuronLocations[neuron1-1], neuronLocations[neuron2-1])
		percentile=simil[4]
		

	
		try:
			distanceToSimilarities[shift]=distanceToSimilarities[shift]+[[distance,similarity]]

		except (KeyError, AttributeError) as e:
			distanceToSimilarities[shift]=[]
			distanceToSimilarities[shift]=distanceToSimilarities[shift]+[[distance,similarity]]


	for shift in distanceToSimilarities:

		toPlot=np.array(distanceToSimilarities[shift]).transpose().tolist()

		cor=scipy.stats.pearsonr(toPlot[0],toPlot[1])[0]


		plt.scatter(toPlot[0], toPlot[1])
		plt.xlabel('distance')
		plt.ylabel('similarity')
		plt.title(name +' Shift: ' + str(shift))
		plt.text(0, -.1, 'correlation: ' + str(cor))
		plt.savefig(outputDirectory + 'similarityToDistance/' + name + 'Shift' + str(shift) + '.pdf')
		plt.ylim((-.2,1.2))
		plt.close()



for name in originalFiles:
	createPlot(name)


