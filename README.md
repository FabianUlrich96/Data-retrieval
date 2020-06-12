# Data-retrieval

Data used in the study: 
Stack Exchange Data Dump 01.06.2020: https://archive.org/download/stackexchange


#Files and their use

|File| Description|
|----|------------|
|parse_xml.py|Function file to parse the XML files from the Data Dump to .csv files|
|related_tags.py|Function file to count the tags related to one given search term|
|related_tag_count.py|Function file to merge the tag counts of two files generated with related_tags.py|
|total_tag_count.py|Function file to generate a .csv file with the total count of tags in a dataset|
|threshold_calculation.py|Function file to calculate the TRT<sub>1</sub> and TST<sub>2</sub> threshold|
|UserSelection.py|Class file with general functions for the user input|
|CsvAction.py|Class file with general functions to edit .csv files|
