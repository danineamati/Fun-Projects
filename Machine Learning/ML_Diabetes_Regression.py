# Practice  with SKLearn
# Daniel Neamati

from math import ceil
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import random


class diabetesModel():
	"""Linear Regression for Diabetes Data"""
	def __init__(self):
		self.diabetes = datasets.load_diabetes()
		self.random_state = random.randrange(30, 80)
		# Features are:
		self.features = ["Age", "Sex", "BMI", "Avg Blood Pressure", "S1", "S2",\
				 "S3", "S4", "S5", "S6"]

	def printDescriptor(self):
		print(self.diabetes.DESCR)

	def assessColumn(self, col, rand_state, verbose = False):
		'''Perform a linear regression on a single column.'''
		data = self.diabetes.data[:, np.newaxis, col]
		# Split the data into training and test sets
		# Since we are doing a linear regression, we choose one c olumn
		data_train, data_test, target_train, target_test = train_test_split(
			data, self.diabetes.target, 
			test_size = 0.2, 
			random_state = rand_state)

		assert len(data_train) + len(data_test) == len(self.diabetes.data), (
			str(len(data_train)) + ' + ' + str(len(data_test)) + ' != ' + 
			str(len(self.diabetes.data)))

		# Make the model
		model = linear_model.LinearRegression()
		model.fit(data_train, target_train)

		# Predict diabetes of test set
		data_pred = model.predict(data_test)

		if verbose:
			# The coefficients
			print('Coefficients: \n', model.coef_)
			# The mean squared error
			print("Mean squared error: %.2f"
			      % mean_squared_error(data_test, data_pred))
			# Explained variance score: 1 is perfect prediction
			print('Variance score: %.2f' % r2_score(target_test, data_pred))

		return (r2_score(target_test, data_pred), 
			data_train, data_test, target_train, target_test,  data_pred)

	def findBestPredictor(self):
		'''Of the available columns, find the one with the best correllation.'''
		bestCol = 0
		bestR2 = 0
		scoreDict = {}

		for i in range(len(self.features)):
			# Since we are doing a linear regression, we choose one column at 
			# a time. 
			# Repeat the test a few times
			scores = []
			for j in range(40, 60):
				score = self.assessColumn(i, j)
				scores.append(score[0])

			avg_score = (sum(scores) / len(scores))
			if avg_score > bestR2:
				bestCol = i
				bestR2  = avg_score

			# Record score
			scoreDict[self.features[i]] = avg_score

		self.printDict(scoreDict)
		return bestCol

	def printDict(self, dictionary):
		'''Prints the Dictionary more clearly.'''
		for s in dictionary:
			space = ' ' * ceil((24 - len(s)) / 2)
			print (space, s, space, dictionary[s])

	def visualizeBestPredictor(self):
		'''Graph of predictor.'''
		bestCol = self.findBestPredictor()

		all_data_train = []
		all_data_test = []
		all_target_train = []
		all_target_test = []
		all_data_pred = []

		for j in range(50, 60):
			score, data_train, data_test, \
			target_train, target_test, data_pred = \
				self.assessColumn(bestCol, j)
			all_data_train.append(data_train)
			all_data_test.append(data_test)
			all_target_train.append(target_train)
			all_target_test.append(target_test)
			all_data_pred.append(data_pred)

		fig = plt.figure(figsize = (15, 5))
		fig.suptitle("Diabetes Correletion for " + self.features[bestCol], \
						 fontsize=14, fontweight='bold')

		# Use a big subplot to have common labels.
		# Remove axis lines and ticks on the larger subplot
		ax = fig.add_subplot(111)
		ax.spines['top'].set_color('none')
		ax.spines['bottom'].set_color('none')
		ax.spines['left'].set_color('none')
		ax.spines['right'].set_color('none')
		ax.tick_params(labelcolor='w', top='off', bottom='off',\
						 left='off', right='off')

		for i in range(len(all_data_train)):
			# Initialize subplots in a grid of 2X5, at i+1th position
			ax1 = fig.add_subplot(2, 5, 1 + i)
			ax1.scatter(all_data_test[i], all_target_test[i], \
				color = 'red')
			ax1.scatter(all_data_train[i], all_target_train[i], \
				color = 'black')
			ax1.plot(all_data_test[i], all_data_pred[i], color = 'blue', \
				linewidth = 1)

		ax.set_xlabel(self.features[bestCol] + " (Normalized)")
		ax.set_ylabel("Diabetes Measure 1 yr Later")

		plt.show()

model = diabetesModel()
model.printDescriptor()
model.visualizeBestPredictor()
