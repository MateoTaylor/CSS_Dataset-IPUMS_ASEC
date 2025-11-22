### Main dataset for sociology RA work w/ Matt McKeever

compiles variables from IPUMS CPS - ASEC's Child Support Supplement (CSS)

#### Workflow
After getting your own IPUMS API Key, can reproduce the dataset by running the
sequence of python files in /processing/. Note that I've put a variable EXTRACT_NUM at the top of each, this 
can be used to select which dataset you'd like to run on.

#### IPUMS Variables
descriptions of each variable can be found in variables_notes.txt.
you can change the variables pulled from IPUMS by adding/removing lines in variables_clean.txt

#### Additional Variables
The add_famid and family_processing files add a couple variables to the dataset. add_famid adds a
family id variable across both IPUMS and Census definitions for families. family_processing adds the following variables for both IPUMS and Census definitions of families:
- total family income, 
- number of children,
- number of adults, 
- number of armed forces,
- if family has CSS eligible adult


Data is extracted via IPUMS API from Ipums CPS:

Sarah Flood, Miriam King, Renae Rodgers, Steven Ruggles, J. Robert Warren, Daniel Backman, Etienne Breton, Grace Cooper, Julia A. Rivera Drew, Stephanie Richards, David Van Riper. Integrated Public Use Microdata Series, Current Population Survey: Version 13.0 [dataset]. Minneapolis, MN: IPUMS, 2025. https://doi.org/10.18128/D030.V13.0