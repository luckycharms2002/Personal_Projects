# Personal_Projects

#  Excel_File_Name_Changer.py
#python code used to change names of sheets in excel files. When working with lots of data across many sheets
#it becomes tedious to have to format the sheet names for the purpose of integrating them into a database. I specifically had the trouble 
#of formatting my sheets of historical financial data, with dates of release as sheet names, done over many times for different 
#companies/funds, which I was able to do more efficiently with this program. 


#  FRB_Corr.py
#python code to correlate quarterly economic projections data released by the FRB, to an asset's price % change on the day of the data release.
#The program takes in the FRB projections from an excel file I copied and pasted in html format's tables give by the FRB website. 
#The FRB data includes the current projections as well as the previous projections, and I attempted to see if the discrepancy in projections
#have a statistically predictable impact on the % change of an asset on that day. The asset file I used is the daily of gold futures, 
#however the asset prices in question can be changed using the ASSET_DATA constant variable found in the code to any daily chart with a % change 
#coloumn (you can make the % change coloumn yourself too). The program spits out a 5 x 5 matrix of correlation coefficients to the price % change 
#per the 5 x 5 table of discrpencies of economic data projections. I was hoping, such that if the user creates their own 5 x 5 matrix of their own 
#predictions of discrepancies in the upcoming FOMC meeting and inputs it in the program, it would spit out a probability distribution
#of price % change of the data release date, in reference to the correlation coefficient matrix... however the result that showed for multiple asset
#charts was that 0 correlation was apparent, hence it is a failed attempt in generating any alpha bias.

#  Key_Words_Data_Finder.ipynb
#python code done on jupyternotebooks to help extract key words from any webpage. Copy and paste any text content onto a txt. file
#and it will return a list of the top used words on that piece of literature, as well as its frequency. It filters out for
#articles or conjunctions in english. I used it for making coverletters, and buyside institution / funds' philosophy and investment focus. 

# Fighter.py
#Python code to scrape data from the UFC website for athletes. Stores into SQL server.

# Cluster.R
#Failed/Ongoing attempt to quantitatively define different fighting styles.
#To be used using the SQL file created using Fighter.py

# RTest.R 
#Scatter Plot creator for an insight into the UFC GOAT debate... however still in process of implementing ability of opponents at time of fight, and championship status.
#To be used using the SQL file created using Fighter.py


