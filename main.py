import numpy as np 
import matplotlib.pyplot as plt 
from variables import *
from data_process import Data 

if __name__ == "__main__":

	# data collected from https://openpsychometrics.org/_rawdata/
	# dataset: IPIP-FFM-data-8Nov2018.zip, containig 1,015,342 data
	# data created from http://openpsychometrics.org/tests/IPIP-BFFM/
	# in my opinion, this is a largely insufficient test battery, containing
	# only 50 items, whilst the IPIP-NEO contains up to 300 items.
	data_file_name = "data/bigfive_data.csv"

	pipeline = ["load", 
				"parse", 
				"correlate",
				"plot"]
	args = ("correlation", "EXT", "EST")

	data = Data(data_file_name)
	data.process(pipeline, *args)
	print(data.corr_matrix)
	plt.show()
	