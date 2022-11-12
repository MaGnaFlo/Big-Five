MAX_SCORE = 5 # max score of each item
MIN_SCORE = 1 # min score of each item
IND_PER_CAT = 10 # number of items per category
N_BINS = 20 # number of bins for bar chart

categories = {"EXT" : 0, "EST" : 1, "AGR" : 2, "CSN" : 3, "OPN" : 4}

# Series of maps regarding the various items per category.
ext_map = { "EXT1" : 1,
			"EXT2" : 0,
			"EXT3" : 1,
			"EXT4" : 0,
			"EXT5" : 1,
			"EXT6" : 0,
			"EXT7" : 1,
			"EXT8" : 0,
			"EXT9" : 1,
			"EXT10" : 0}

est_map = { "EST1" : 0,
			"EST2" : 1,
			"EST3" : 0,
			"EST4" : 1,
			"EST5" : 0,
			"EST6" : 0,
			"EST7" : 0,
			"EST8" : 0,
			"EST9" : 0,
			"EST10" : 0}

agr_map = { "AGR1" : 0,
			"AGR2" : 1,
			"AGR3" : 0,
			"AGR4" : 1,
			"AGR5" : 0,
			"AGR6" : 1,
			"AGR7" : 0,
			"AGR8" : 1,
			"AGR9" : 1,
			"AGR10" : 1}

csn_map = { "CSN1" : 1,
			"CSN2" : 0,
			"CSN3" : 1,
			"CSN4" : 0,
			"CSN5" : 1,
			"CSN6" : 0,
			"CSN7" : 1,
			"CSN8" : 0,
			"CSN9" : 1,
			"CSN10" : 1}

opn_map = { "OPN1" : 1,
			"OPN2" : 0,
			"OPN3" : 1,
			"OPN4" : 0,
			"OPN5" : 1,
			"OPN6" : 0,
			"OPN7" : 1,
			"OPN8" : 1,
			"OPN9" : 1,
			"OPN10" : 1}