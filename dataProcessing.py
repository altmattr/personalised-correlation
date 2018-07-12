
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


def create_freq_stats_per_avg(data):
	"""
	Q1|2.9
	Q2|2.5
	Q3|2.2
	"""
	i_response = data.iloc[-1].fillna(0)
	questions = {}
	for col in data.columns:
	    # score, count for this col
	    values = data[col].value_counts()

	    if 0 in values.index:
	        values = values.drop(0)
	    # calc average
	    count = 0
	    total = 0
	    for k,v in values.items():
	        total+= v
	        count+=int(k)*v
	    # add average response for question, and individual response for that question
	    questions[col] = ['%.2f' % (count/total), int(i_response[col])]

	ser = pd.Series(*questions.values())
	ser.to_csv('data/freq.csv', header=True)

			
			
def main(create_stats=False, verbose=True):
	if verbose: print('begun main processing')

	# read in data, most resource intensive operation
	data = pd.read_csv('data/qualtrics.csv')
	# only get test values
	data = data[data.DistributionChannel == 'test']
	# drop null columns and non-question columns
	drop_cols = [col for col, val in data.isnull().sum().items() if val > 5000]
	# drop questions with invalid data
	drop_cols.extend(['Q31','Q32'])
	data.drop(drop_cols, axis=1,inplace=True)

	data = data[[col for col in data.columns if col.startswith("Q")]]

	if verbose: print('trimmed csv loaded')
	
	# create frequency statistics
	if create_stats:
		# CHANGE THIS to create_freq_stats_per_value if needed
		create_freq_stats_per_avg(data)

		if verbose: print('freq stats created.')

	# replace nulls with 0 for corr matrix
	#data.fillna(0,inplace=True)


	# cast values to int
	data = data.astype(float)
	
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

if __name__ == '__main__':
	import time
	start = time.time()

	main()

	end = time.time()
	print('main() process took ',end - start, ' seconds to execute.')