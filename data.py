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

	    questions[col] = '%.2f' % (count/total)

	ser = pd.Series(questions) \
	    .rename('Average')
	ser.to_csv('data/freq.csv', index_label='Question', header=True)



def main(create_stats=True, verbose=True):
	if verbose: print('begun main processing')

	# read in data, most resource intensive operation
	data = pd.read_csv('data/qualtrics.csv', usecols=lambda x: x.startswith("Q"))
	data.drop([0,1,5537],inplace=True)
	drop_cols = [col for col, val in data.isnull().sum().items() if val > 5000]
	drop_cols.extend(['Q31','Q32'])
	data.drop(drop_cols, axis=1,inplace=True)

	if verbose: print('trimmed csv loaded')

	# create frequency statistics
	if create_stats:
		# CHANGE THIS to create_freq_stats_per_value if needed
		create_freq_stats_per_avg(data)

		if verbose: print('freq stats created.')

	# replace nulls with 0 for corr matrix
	data.fillna(0,inplace=True)

	# cast values to int
	data = data.astype(int)

	# create corr corr-matrix
	data_corr = data.corr()

	# replacing negative correlations with zeroes
	data_corr[data_corr < 0] = 0

	# save corr matrix
	data_corr.to_csv('data/corr-matrix.csv')
	if verbose: print('saved corr-matrix')

if __name__ == '__main__':
	main()
