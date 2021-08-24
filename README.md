# DSM Visualisation

## About
The goal of this project is to display survey data from qualtrics in an informative manner via a 3D Force Graph.

- Nodes = questions, 
- Edges = correlation between two questions (pearson correlation coefficient normalised to range -10 to +10), 
- Node Size = relative average response to question, 
- Edge Colour = green for positive correlation, red for negative correlation
- Edge Size = strength of correlation (absolute)


## Front-end

### 3D Force Graph using d3.js


## Back-end

### Page serving with Flask
Communication between the data processing and the JavaScript handled with Flask.

### Data Processing with Python and Pandas
#### Data Cleaning
The initial data was retrieved from qualtrics via their API. Due to restrictions on the current version of their API, we were unable to filter out any irrelevant columns.

The csv data was loaded into a pandas DataFrame. From there the question columns and the response id column were isolated.
Questions were dropped if > 90% of responses were missing. Only numerical responses were accepted, any text-response question was also dropped.

#### Retrieving Individual Responses

Individual responses were identified by the response_id. The response is then searched for in the main cleaned DataFrame, then sent to the graph to change the colours of the nodes. 



    IF response_id found:

        load individual responses

    ELIF response_id not found OR response_id is null:

        fill a dictionary with (question,1) key, val pairs

#### Frequency Calculations

The frequency data is returned in this format:

question_str,individual_response, average (rounded to int), average  (scaled to range 1:100), average (with increased standard deviation) 

average: basic calculation, does not account for different maximum values, 

​	e.g. two questions could have an average of 2.5, but they could have a maximum value of 4 and 6 	respectively

scaled average: fixes the above problem, and converts the values into a range between 1 and 100.

average with increased std: if all of the previous averages are too similar to see any differences, this can be used to distinguish differences between data for visualisation.

#### Correlation matrix

pandas has the ability to create a pearson correlation matrix from a numeric DataFrame (based on numpy implementation). The values are decimals, which required scaling to a new range 1:100, in the same way that the scaled average was computed.

# Authors

<li><a href="https://researchers.mq.edu.au/en/persons/matt-roberts">Matthew Roberts</a></li>
<li><a href="https://researchers.mq.edu.au/en/persons/miri-forbes">Miri Forbes</a></li>
<li>Emma Walker</li>
<li>Tam Du</li>
<li>Oscar Gardiner</li>
<li>Kyle Long</li>
</ul>

# Use

This plugin is open-sourced under the Mozilla public licence and thus there are very few restriction on its use. As an academic project the authors ask that when the code or the public instance are used that citation (in the case of academic use) or donation (in the case of for-profit use) be considered.

