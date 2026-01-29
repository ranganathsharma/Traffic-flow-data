Data regarding traffic count for M50 can be found at https://data.gov.ie/dataset/traffic-counter-data

Follow the steps provided in the file download.py to download the data of particular dataset
This error appears while downloading 

DtypeWarning: Columns (12,24,25) have mixed types. Specify dtype option on import or set low_memory=False.
data = pd.read_csv(url(temp1[i]))

This does not hinder the processing 

Explanation of data downloading and processing to get the flow, speed data

Select the start and end date for the downloading process. The location sets the id of the counter and is set as 1506 following the previous research

direction is set as 'South bound' which filters out a single direction out of the bidirectional highway data. 

The speed limit 'vf' function is unclear.

The time format is year, month, date, hour, min, second in separate columns. It is put together to form the datetime format. This new column is set as the index to help with further aggregation

# Processing to get the fundamental diagram

Based on the direction we want to process, the data selection is done. If Southbound 2 is in the data, different numbers are tried i.e. Southbound {i} to cover all the possibilities. If such cases do not exist, all the data are just named as Southbound.
These names could be particular to the counter we are processing

Flow is calculated as the total number of vehicles travelling through the counter in a duration
Velocity is calculated as the average velocity
Density is derived as the ratio of Flow to velocity given by the hydrodynamic flow equation. Based on the aggregation, the units have to be changed to plot the fundamental diagram.
