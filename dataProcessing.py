
# coding: utf-8
import pandas as pd
import csv

def create_freq_stats_total(data):
	"""
	Q1|ratio
	Q2|ratio
	Q3|ratio
	"""
	freq = []
	total = data.shape[0]
	with open('data/freq.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Question','Ratio'))
		for col in data.columns:
			ratio = round(data[col].count()/total,2)
			writer.writerow((col,ratio))


def create_freq_stats_per_value(data):
	"""
	value|Q1|Q2|Q3
	1|0.5|0.25|0.25
	2|0|0.75|0.17

	"""
	questions = {}
	for col in data.columns:
		values = data[col].value_counts()
		if 0 in values.index:
		    values = values.drop(0)

		total = values.sum()

		ratios = values.apply(lambda x: '%.2f' % (x/total))
		questions[col] = ratios.to_dict()

	df = pd.DataFrame(questions) \
		.fillna(0)

	df.to_csv('data/freq.csv')


def normalise_to_range(val, max_val, normal_range):
	"""uses magic! ... just kidding
	normalise the values to a range.
	i.e. if the possible answers were 1:max_val, then the new range of values is between 1:normal_range
	e.g. 
		normalise_to_range(4.2,5,100) = 84
		normalise_to_range(4.2,5,7) = 6
	"""
	return int((val/ max_val) * normal_range + -0.5) + 1


def create_freq_stats_per_avg(data, response_id, create_csv=False, verbose=False):
	"""
	Q1|2.9|1
	Q2|2.5|3
	Q3|3.7|2

	ind_response: cases
		response_id found: Series object with index = question, value col = response for question
		response_id not found: dict populated with 0s

	keep that in mind if you try to access the ind_response object in a diffrent way then as programmed here

	"""

	try:
		# creates series with questions as index, and individual responses as answers
		ind_response = data.loc[response_id].fillna(0)
	except KeyError:
		# populate dict with zeroes, has questions as key
		if verbose: print('response id not found')
		ind_response = {col:0 for col in data.columns}

	questions = []
	for col in data.columns:
	    # score, count for this col
	    values = data[col].value_counts()

	    # don't include zeroes in average calculation
	    if 0 in values.index:
	        values = values.drop(0)

	    # calc average
	    count = 0
	    total = 0
	    for k,v in values.items():
	        total+= v
	        count+=int(k)*v
	    # add average response for question
	    avg = float('%.2f' % (count/total))

	    max_val = int(data[col].max())

	    # change average to a scaled normalised average between 1 and 100 (for data visualisation purposes)
	    scaled_avg = normalise_to_range(avg, max_val, 100)
	    # # FOR TESTING print('{0}/{1} becomes {2}'.format(avg, max_val, scaled_avg))

	    ind_val = int(ind_response[col])
	    # normalise the values to a range: 
	    # i.e. if the possible answers were 1:max_val, then the new range of values is between 1:4
	    ind_normalised = normalise_to_range(ind_val,max_val,4)

	    # load items into list
	    row = [col, scaled_avg, ind_normalised]
	    # load row into questions list
	    questions.append(row)
	#print(*questions,sep='\n')

	return questions



def main(response_id, create_stats=True, verbose=True):
	if verbose: print('begun main processing')

	# read in data, most resource intensive operation
	data = pd.read_csv('data/qualtrics.csv', index_col='ResponseId')
	# only get test values
	data = data[data.DistributionChannel == 'test']
	# drop null columns and non-question columns
	drop_cols = [col for col, val in data.isnull().sum().items() if val > 5000]
	# drop questions with invalid data
	drop_cols.extend(['Q31','Q32'])
	data.drop(drop_cols, axis=1,inplace=True)

	data = data[[col for col in data.columns if col.startswith("Q")]]

	if verbose: print('trimmed csv loaded')

	# cast values to int
	data = data.astype(float)

	# create frequency statistics
	if create_stats:
		# CHANGE THIS to create_freq_stats_per_value if needed
		freq_data = create_freq_stats_per_avg(data, response_id, verbose=verbose)

		if verbose: print('freq stats created.')

	# replace nulls with 0 for corr matrix
	#data.fillna(0,inplace=True)


	
	# create corr corr-matrix 
	data_corr = data.corr()

	# replacing negative correlations with  (not needed)
	#data_corr[data_corr < 0] = 0

	# find maxmimum value in whole matrix
	# costly way in terms of processing
	desc_max = data_corr[data_corr < 1].max().describe()
	desc_min = data_corr[data_corr < 1].min().describe()
	max_val = max(desc_max['max'],abs(desc_min['min']))
	# rescales correlation matrix so that the old max value is now 1
	scaled_corr = data_corr / max_val
	scaled_corr[scaled_corr > 1] = 1

	# turn into integer representation
	scaled_corr = scaled_corr.round(1)*10
	scaled_corr.astype(int, inplace=True)


	# save corr matrix
	data_corr.to_csv('data/corr-matrix.csv')
	scaled_corr.to_csv('data/scaled-corr-matrix.csv')
	if verbose: print('saved corr-matrix')


	return freq_data

if __name__ == '__main__':
	# run 'python dataProcessing.py' for testing
	import time
	start = time.time()
	valid = 'R_b437z8esnOET9yd'
	invalid = 'bad_id'
	res = main(valid)
	print(*res, sep='\n')

	end = time.time()
	print('main() process took ',end - start, ' seconds to execute.')