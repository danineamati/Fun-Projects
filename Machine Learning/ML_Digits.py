# First Machine Learning Practice File
# Daniel Neamati
# 10 September 2018

import numpy as np
from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class digitsML_model():
	""" This serves a wrapper for the sklearn KMeans model for 
	unsupervised learning."""
	def __init__(self, k):
		self.k = k
		self.model = KMeans(n_clusters = k)

		# Get the handwritting data set from SKLearn
		digits = datasets.load_digits()
		self.data = digits.data

		# Make the model
		self.makeModel()

		# Image to number mapping
		self.mapping = []

	def makeModel(self):
		self.model.fit(self.data)
		print("Created the model")
	
	def showModelImages(self):
		print("Showing image")

		fig = plt.figure(figsize=(8, 3))
		fig.suptitle('Cluser Center Images', fontsize=14, fontweight='bold')
		for i in range(k):
			# Initialize subplots in a grid of 2X5, at i+1th position
			ax = fig.add_subplot(2, 5, 1 + i)
			# Display images
			ax.imshow(self.model.cluster_centers_[i].reshape((8, 8)), 
				cmap=plt.cm.binary)
		plt.show()

	def getImageNumberMapping(self):
		for plot in range(self.k):
			self.showModelImages()
			num = input("What is number in plot " + str(plot + 1) + 
							"?     Enter: ")
			self.mapping.append(int(num))

		print("You selected: ", self.mapping)



k = 10
my_model = digitsML_model(k)
my_model.getImageNumberMapping()


