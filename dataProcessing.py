
# coding: utf-8
from random import randrange
import pandas as pd
import re

def main(data, response_id):
  print('begun main processing', flush=True)

  # find response_id regardless of string format
  pattern = re.compile('(?i)response ?_?id') # case insensitive, 'responseid', with '_',' ' or '' separating the words.
  for col in data.columns:
    match = re.search(pattern,col)
    if match:
      response_id_colname = match.group(0)
      break

  data.set_index(response_id_colname, inplace=True)

  # lets see what indexes we have
  # print(data.index.tolist(), flush=True)


  print(response_id_colname, 'column found.', flush=True)

  # question_df = data.iloc[0]

  # drop first 2 rows to remove irrelevant data
  # data = data.iloc[2:]

  # keep question columns
  # TODO: not needed anymore
  keep_cols = [col for col in data.columns if col.lower().startswith('q')]
  data = data[keep_cols]


  # drop columns if 90% of it's values are null
  drop_cols = [col for col, val in data.isnull().sum().iteritems() if val > int(data.shape[0]*0.9)]
  data.drop(drop_cols, axis=1,inplace=True)

  # filter the quesiton string row
  # question_df = question_df[keep_cols].drop(drop_cols)

  # grab the questions before we wipe them out with the numeric coersion
  questions = data.iloc[0]
  print('DataFrame has been cleaned', flush=True)

  data = data.apply(pd.to_numeric, errors='coerce')

  # create pearson corr-matrix 
  data_corr = data.corr()
 

  data_corr = data_corr.fillna(1)
  # replacing negative correlations with (not needed)
  #data_corr[data_corr < 0] = 0


  # dump correlation matrix for debugging help
  data_corr.to_csv('static/data/corr-matrix.csv')
  
  # from the correlation matrix, create a list of nodes
  nodes = pd.DataFrame(index=data.columns)
  nodes.index.name = "name"

  # for each node, work out it's frequency of response > 1
  for i, row in nodes.iterrows():
    nodes.loc[i,'freq'] = data[i][lambda x: x >= 1].dropna().mean() 


  # for each node, get this participants response
  for i, row in nodes.iterrows():
    try: # if we don't have that response_id, just give 0
      nodes.loc[i,'response'] = data.loc[response_id, i]
    except KeyError:
      nodes.loc[i, 'response'] = 0

  #for each node, add the question text
  print(data.iloc[0], flush=True)
  for i, row in nodes.iterrows():
    nodes.loc[i,'text'] = questions.loc[i].removeprefix("Now we ask you to respond to a number of statements about your thoughts, feelings, experiences, a...-")

  nodes.to_csv("static/data/nodes.csv")

  # dumps data in a form that d3 can read
  links = correleation_matrix_to_nodes_and_forces(data_corr)

  return (nodes, links)

def fake_nodes_from_correlation_matrix(data_corr):
  # from the correlation matrix, create a list of nodes
  nodes = pd.DataFrame(index=data_corr.index)
  nodes.index.name = "name"
  
  # for each node, work out it's frequency of response > 1
  for i, row in nodes.iterrows():
    nodes.loc[i,'freq'] = randrange(3,20)

  # for each node, get this participants response
  for i, row in nodes.iterrows():
    nodes.loc[i,'response'] = randrange(1,5)

  nodes.to_csv("static/data/nodes.csv")
  return nodes

def correleation_matrix_to_nodes_and_forces(data_corr):

  threshold = 0.55

  # From the correlation matrix, create a frame in the form that d3 would prefer for forces
  force_frame = pd.DataFrame(columns=['force', 'target'])
  processed = []
  for col in data_corr:
    processed.append(col)
    c = data_corr[col]
    df = c.to_frame(name="force")
    df["target"] = col
    df = df.drop(processed) # this prevents doubling up
    force_frame = force_frame.append(df)
  force_frame.index.name = "source"
  # filter all negative
  force_frame = force_frame[(force_frame["force"] > 0)].dropna()
  # filter every row with force of 1
  force_frame = force_frame[(force_frame["force"] != 1)].dropna()
  # filter every row under threshold
  force_frame = force_frame[(force_frame["force"] > threshold)].dropna()
  force_frame["normalisedforce"] = ((force_frame["force"] - force_frame["force"].min())/(force_frame["force"].max() - force_frame["force"].min()))
  force_frame.to_csv('static/data/forces.csv')
  return force_frame