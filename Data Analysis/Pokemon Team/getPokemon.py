# Trial Script to get Pokemon in Table from Bulbapedia
# using Pandas

# Link: https://bulbapedia.bulbagarden.net/wiki/
#				List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
import os
from tkinter import *


print('Reading National Pokedex')

def getHTMLpage():
	'''Uses Request client to obtain the Bulbapedia page.'''
	url = 'https://bulbapedia.bulbagarden.net/wiki/' + \
 		'List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'

 	# Act like a browser to access the website
	header = {
	  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" +
	  					" AppleWebKit/537.36 (KHTML, like Gecko)" + 
	  					" Chrome/50.0.2661.75 Safari/537.36",
	  "X-Requested-With": "XMLHttpRequest"
	}

	r = requests.get(url, headers=header)

	return r.text

def getPokemonFromBulba():
	'''Convert HTML page into a data frame for pandas.'''
	dfs = pd.read_html(getHTMLpage())

	return dfs

def getPokemonImageBulba(pokemonName):
	'''Gets specific pokemon image from webpage.'''
	soup = BS(getHTMLpage(), features = "lxml")

	# Ex: 'img alt="Umbreon"'
	for imgtag in soup.find_all("img", {"alt": pokemonName}): 
		filename = imgtag['src']
		print(filename)
		print(imgtag)

	return imgtag

def getListFromCSV(filename):
	pokeList = pd.read_csv(filename,index_col = 'Number')
	return pokeList

def changeValToInt(dexFrame, col):
	'''Ex: Changes #001 to 1'''
	numRows = len(dexFrame.index)

	for row in range(numRows):
		if isinstance(dexFrame.at[row, col], str):
			if dexFrame.at[row, col][0] == '#':
				# Cell needs to be changed
				dexFrame.at[row, col] = int(dexFrame.at[row, col][1:])



def formatRegionalDex(dexFrame, verbose = False):
	'''Takes the HTML version and makes a useable form of the regional
	pokedex.'''
	

	# Change the format of the dex numbering
	changeValToInt(dexFrame, 1) # National pokedex (Ndex)
	changeValToInt(dexFrame, 0) # Regional pokedex (e.g. Kdex for kanto)

	# Remove inrelevant or incorrect rows
	dexFrame = dexFrame.dropna(subset = [0])

	if verbose:
		print('New Head is ', dexFrame.head(25))

	# Set the column labels to the first row, namely:
	regionDex = dexFrame.at[0, 0]
	col_names = [regionDex, 'Ndex', 'MS', 'Pokemon', 'Type', 'Type 2']
	dexFrame.columns = col_names
	# dexFrame.columns = dexFrame.loc[0]

	# Now that the columns are relabelled, drop the duplicate row
	dexFrame = dexFrame.drop(0)

	# No need to include the 'MS' Column (saved for pictures)
	dexFrame = dexFrame.drop('MS', axis = 1)

	# Set the frame to beindexed by the national index
	dexFrame.set_index('Ndex', inplace = True)

	if verbose:
		# Print the head
		print(dexFrame.head())

	return dexFrame

def printMergeInfo(filename, nationalDex):
	'''Reads a csv and prints info from national pokedex.'''
	infoFrame = getListFromCSV(filename)
	if 'Pokemon' in infoFrame.columns.values and \
				'Pokemon' in nationalDex.columns.values:
		info = pd.merge(nationalDex.reset_index(), infoFrame, \
			on = 'Pokemon', how = 'inner')
		print(info)
		print()

def main():
	'''Gets the national pokedex, formats each regional dex, and appends them
	into a single pokedex.'''

	# If the saved file does not exist,
	# get data from website, make data frame, and save data frame
	# Else, load from saved data frame
	if not os.path.isfile('./nationalDex.pickle'):
		print("Loading data from website")
		dfs = getPokemonFromBulba()

		# Create the regional pokedex
		kanto = formatRegionalDex(dfs[1])
		johto = formatRegionalDex(dfs[2])
		hoenn = formatRegionalDex(dfs[3])
		sinnoh = formatRegionalDex(dfs[4])
		unova = formatRegionalDex(dfs[5])
		print(dfs[6])

		# Concatinate the regional pokedex together to make the national pokedex
		national = pd.concat([kanto, johto, hoenn, sinnoh, unova], sort = 'False')
		natCols = ['Kdex', 'Jdex', 'Hdex', 'Sdex', 'Pokemon', 'Type', 'Type 2']
		national = national[natCols]

		# Save data to a more easily read format (i.e. a pickle)
		national.to_pickle('nationalDex.pickle')
	else:
		print("Loading data from file")
		# Read data from saved pickle
		national = pd.read_pickle('nationalDex.pickle')

	print(national.head(12))
	print()

	# printMergeInfo('RidePokemon.csv', national)
	# printMergeInfo('ShoulderPokemon.csv', national)
	printMergeInfo('danielTeam.csv', national)
	printMergeInfo('josephTeam.csv', national)

	getPokemonImageBulba('Swampert')

if __name__ == '__main__':
	main()