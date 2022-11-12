import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from variables import *

"""Class for analysing the Big Five data. Specifically designed to
   analyze this type of data, plotting, correlations, etc.
"""
class Data:
	def __init__(self, filename, n_bins=N_BINS):
		self.filename = filename
		self.n_data = 0
		self.full_data = None
		self.processed_data = {"EXT": None, "EST": None, "AGR": None, "CSN": None, "OPN": None}
		self.bins_data = {"EXT": None, "EST": None, "AGR": None, "CSN": None, "OPN": None}
		self.n_bins = n_bins

	""" Loading the data in the form of a csv file. """
	def load(self, sep=";") -> None:
		print("Loading data..")
		data = pd.read_csv(self.filename, sep=sep)
		self.full_data = data

	""" Method to normalize the scores. Reversing when necesary. """
	def score_eq(self, cat, label, score) -> np.ndarray:
		if cat == "EXT":
			s_eq = (1 - ext_map[label]) * (MAX_SCORE - score + MIN_SCORE) + ext_map[label] * score
		elif cat == "EST":
			s_eq = (1 - est_map[label]) * (MAX_SCORE - score + MIN_SCORE) + est_map[label] * score
		elif cat == "AGR":
			s_eq = (1 - agr_map[label]) * (MAX_SCORE - score + MIN_SCORE) + agr_map[label] * score
		elif cat == "CSN":
			s_eq = (1 - csn_map[label]) * (MAX_SCORE - score + MIN_SCORE) + csn_map[label] * score
		elif cat == "OPN":
			s_eq = (1 - opn_map[label]) * (MAX_SCORE - score + MIN_SCORE) + opn_map[label] * score
		else:
			raise "Wrong category"

		return s_eq

	""" Parsing the data. Kicking NaN data and bad data. """
	def parse(self) -> None:
		# separate by category
		print("Parsing...")
		ext_data = self.full_data[list(ext_map.keys())].dropna().loc[~(self.full_data==0).any(axis=1)]
		est_data = self.full_data[list(est_map.keys())].dropna().loc[~(self.full_data==0).any(axis=1)]
		agr_data = self.full_data[list(agr_map.keys())].dropna().loc[~(self.full_data==0).any(axis=1)]
		csn_data = self.full_data[list(csn_map.keys())].dropna().loc[~(self.full_data==0).any(axis=1)]
		opn_data = self.full_data[list(opn_map.keys())].dropna().loc[~(self.full_data==0).any(axis=1)]

		self.n_data = len(ext_data)

		# crunch numbers by category
		s_eq_ext = np.sum([self.score_eq("EXT", label, ext_data[label].to_numpy()) for label, score in ext_map.items()], axis=0)
		s_eq_est = np.sum([self.score_eq("EST", label, est_data[label].to_numpy()) for label, score in est_map.items()], axis=0)
		s_eq_agr = np.sum([self.score_eq("AGR", label, agr_data[label].to_numpy()) for label, score in agr_map.items()], axis=0)
		s_eq_csn = np.sum([self.score_eq("CSN", label, csn_data[label].to_numpy()) for label, score in csn_map.items()], axis=0)
		s_eq_opn = np.sum([self.score_eq("OPN", label, opn_data[label].to_numpy()) for label, score in opn_map.items()], axis=0)

		self.processed_data.update({"EXT" : s_eq_ext})
		self.processed_data.update({"EST" : s_eq_est})
		self.processed_data.update({"AGR" : s_eq_agr})
		self.processed_data.update({"CSN" : s_eq_csn})
		self.processed_data.update({"OPN" : s_eq_opn})

	""" Rearranging the data into bins for bar chart. """
	def pool(self) -> None:
		print("Pooling...")
		
		bar_ext = np.zeros(self.n_bins)
		bar_est = np.zeros(self.n_bins)
		bar_agr = np.zeros(self.n_bins)
		bar_csn = np.zeros(self.n_bins)
		bar_opn = np.zeros(self.n_bins)

		for k in range(self.n_data):
			bar_ext[int((self.n_bins-1)*(self.processed_data["EXT"][k]/IND_PER_CAT-MIN_SCORE)/(MAX_SCORE-MIN_SCORE))] += 1
			bar_est[int((self.n_bins-1)*(self.processed_data["EST"][k]/IND_PER_CAT-MIN_SCORE)/(MAX_SCORE-MIN_SCORE))] += 1
			bar_agr[int((self.n_bins-1)*(self.processed_data["AGR"][k]/IND_PER_CAT-MIN_SCORE)/(MAX_SCORE-MIN_SCORE))] += 1
			bar_csn[int((self.n_bins-1)*(self.processed_data["CSN"][k]/IND_PER_CAT-MIN_SCORE)/(MAX_SCORE-MIN_SCORE))] += 1
			bar_opn[int((self.n_bins-1)*(self.processed_data["OPN"][k]/IND_PER_CAT-MIN_SCORE)/(MAX_SCORE-MIN_SCORE))] += 1

		self.bins_data.update({"EXT" : bar_ext})
		self.bins_data.update({"EST" : bar_est})
		self.bins_data.update({"AGR" : bar_agr})
		self.bins_data.update({"CSN" : bar_csn})
		self.bins_data.update({"OPN" : bar_opn})

	""" Total pipeline process. """
	def process(self, pipeline, *args):
		for func in pipeline:
			if func == "load":
				self.load()
			elif func == "parse":
				self.parse()
			elif func == "pool":
				self.pool()
			elif func == "correlate":
				self.correlate()
			elif func == "plot":
				self.plot(*args)

		print("Total available data: ", self.n_data)

	""" Computing the correlations between each factors. """
	def correlate(self):
		print("Computing correlation...")
		data_matrix = np.array([self.processed_data["EXT"],
								self.processed_data["EST"],
								self.processed_data["AGR"],
								self.processed_data["CSN"],
								self.processed_data["OPN"]],
								dtype=float)
		self.corr_matrix = np.corrcoef(data_matrix).round(3)

	""" Plotting as bar charts or correlation. """
	def plot(self, *args):
		if len(args) == 0:
			query = "bar"
		else:
			query = args[0]

		print("Plotting {}...".format(query))
		if query == "bar_chart" or query == "bar" or query == "bar_plot":
			bins_range = np.arange(IND_PER_CAT*MIN_SCORE, IND_PER_CAT*MAX_SCORE, IND_PER_CAT*(MAX_SCORE-MIN_SCORE)//self.n_bins)
			fig, ax = plt.subplots(1, 5, figsize=(13, 4))

			ax[0].bar(bins_range , self.bins_data["EXT"], width=3*10//self.n_bins, color='goldenrod', edgecolor='k', linewidth=1)
			ax[1].bar(bins_range , self.bins_data["EST"], width=3*10//self.n_bins, color='crimson', edgecolor='k', linewidth=1)
			ax[2].bar(bins_range , self.bins_data["AGR"], width=3*10//self.n_bins, color='limegreen', edgecolor='k', linewidth=1)
			ax[3].bar(bins_range , self.bins_data["CSN"], width=3*10//self.n_bins, color='navy', edgecolor='k', linewidth=1)
			ax[4].bar(bins_range , self.bins_data["OPN"], width=3*10//self.n_bins, color='lightblue', edgecolor='k', linewidth=1)
			
			ax[0].set_title('Extraversion')
			ax[1].set_title('Emotional Stability')
			ax[2].set_title('Agreeableness')
			ax[3].set_title('Conscienciousness')
			ax[4].set_title('Openness')

			fig.tight_layout()

		elif query == "correlation":
			# default
			x, y = self.processed_data["EXT"], self.processed_data["EST"]
			corr = self.corr_matrix[0,1]

			try:
				cat_1, cat_2 = args[1], args[2]
			except:
				print("No arguments provided! Continuing with first against second.")	
			else:
				x, y = self.processed_data[cat_1], self.processed_data[cat_2]
				corr = self.corr_matrix[categories[cat_1], categories[cat_2]]
			finally:
				# create colors
				k_min, k_max = IND_PER_CAT*MIN_SCORE, IND_PER_CAT*MAX_SCORE
				n = k_max - k_min + 1

				colors = np.zeros((n, n, 3), dtype=int)
				for xx, yy in list(zip(x,y)):
					colors[int(xx) - k_min, int(yy) - k_min, 2] += 1

				colors = colors / np.max(colors)

				fig, ax = plt.subplots(1, 1, figsize=(4, 4))
				ax.imshow(colors)
				ax.invert_yaxis()
				ax.set_title(r'{0} against {1}: $\rho = {2}$'.format(cat_1, cat_2, np.round(corr, 2)))

		return fig, ax