# get_unitids by Adam Hearn

## A Python Module to Imputate IPEDS UnitID Numbers from Non-Matching Institution Names

Have you ever worked with institutional data from multiple sources? If so, one of them is likmayely IPEDS which of course involves the infamous `unitid` variable. The secondary source, on the other hand, may only have the institution's name and no `unitid`. In this case, to join the datasets, you would need to merge on institution name and fill in the rest of the unitids manually to retrieve the IPEDS data.  

Anyone who has worked with IPEDS data would know that not all institution names perfectly line up across multiple sources. For example, Tulane University is named as Tulane University of Louisiana in the IPEDS universe. In this case of conflicting names, there would be an imperfect merge requiring you to manually enter Tulane's unitid number.

In my background, I've run into this issue several times and has gotten to the point where it would be a better use of time to create a module to automate this step rather than filling out unitids manually. That said, I've developed the Python module `unitids`. I'm making this process open-source so other higher-ed researchers can benefit, too. 

This module, available in the `pip` library, uses a cosine similarity text-analyis metric to merge partial or "non-matching" institution names with an IPEDS master file including all institutions in the IPEDS universe since 2004 and their unitid numbers.

The process works by passing a DataFrame of institutions of which you want to get their unitids into the `get_unitids` function. From there, the function populates a sparse matrix and generates a cosine-similarity metric for each insitution you passed and each institution in the IPEDS universe.

It will then return two DataFrame objects: the first DataFrame will include your original data and the unitid numbers of the institutions in the dataset, along with a "match score" (displayed on a scale of 0-100). 

The second DataFrame includes information on the institutions that were not a perfect match, alongside their top-5 closes matches so you can make adjustments as necessary.

## Example

Take, for example, the data present in [this article](https://www.forbes.com/sites/schifrin/2019/11/27/dawn-of-the-dead-for-hundreds-of-the-nations-private-colleges-its-merge-or-perish/#77a18358770d). The cleaned data is available on my Github [here](https://raw.githubusercontent.com/ahearn15/get_unitids/master/example_dta.csv).

Suppose we want to see the relationshpi between Forbes' Financial GPA and endowment, as reported to IPEDS. I've included a sample dataset of FY2018 endowment for all institutions in the IPEDS universe [here](https://raw.githubusercontent.com/ahearn15/get_unitids/master/ipeds_example.csv).


```python
# Import necessary modules (no unitid, yet)
import pandas as pd
import numpy as np

# First we read in the Forbes data:
url = 'https://raw.githubusercontent.com/ahearn15/get_unitids/master/example_dta.csv'
forbes = pd.read_csv(url)
forbes.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>College</th>
      <th>State</th>
      <th>Financial GPA</th>
      <th>Financial Grade</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Stanford University</td>
      <td>CA</td>
      <td>4.5</td>
      <td>A+</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Massachusetts Institute of Technology</td>
      <td>MA</td>
      <td>4.5</td>
      <td>A+</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Notre Dame</td>
      <td>IN</td>
      <td>4.5</td>
      <td>A+</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Princeton University</td>
      <td>NJ</td>
      <td>4.5</td>
      <td>A+</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Pennsylvania</td>
      <td>PA</td>
      <td>4.5</td>
      <td>A+</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Now we read in the IPEDS data
url = 'https://raw.githubusercontent.com/ahearn15/get_unitids/master/ipeds_example.csv'
ipeds = pd.read_csv(url).drop(columns = 'Unnamed: 0')
ipeds.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>unitid</th>
      <th>institution</th>
      <th>endowment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>177834</td>
      <td>A T Still University of Health Sciences</td>
      <td>32420.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>180203</td>
      <td>Aaniiih Nakoda College</td>
      <td>9212.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>491464</td>
      <td>ABC Adult School</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>459523</td>
      <td>ABC Beauty Academy</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>485500</td>
      <td>ABCO Technology</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Now we merge together
forbes = forbes.rename(columns = {'College' : 'institution'}) # need to rename for merge
merged = pd.merge(forbes, ipeds, on = 'institution', how = "left")
merged.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>institution</th>
      <th>State</th>
      <th>Financial GPA</th>
      <th>Financial Grade</th>
      <th>unitid</th>
      <th>endowment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Stanford University</td>
      <td>CA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>243744.0</td>
      <td>1496715.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Massachusetts Institute of Technology</td>
      <td>MA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>166683.0</td>
      <td>1454419.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Notre Dame</td>
      <td>IN</td>
      <td>4.5</td>
      <td>A+</td>
      <td>152080.0</td>
      <td>837184.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Princeton University</td>
      <td>NJ</td>
      <td>4.5</td>
      <td>A+</td>
      <td>186131.0</td>
      <td>3053449.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Pennsylvania</td>
      <td>PA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>215062.0</td>
      <td>562092.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# How many did not merge?
merged['unitid'].isna().sum()
```




    40



If we merge our Forbes data with this 2018 list of IPEDS institutions, we get a successful merge rate of 95.7% (892 of 932 institutions). However, we still have 40 unitids we need to manually encode, taking up 40 lines of code and tedious trips to the IPEDS Data Center. What if we used the new `get_unitids` function though?

## get_unitids


```python
# Installing the module
!pip install unitids==0.0.92

# Import required functions
import numpy as np
import pandas as pd
from unitids import unitids

#For viewing nonmatches
pd.set_option('display.max_rows', 100)
```

    Requirement already satisfied: unitids==0.0.92 in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (0.0.92)
    Requirement already satisfied: numpy in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (from unitids==0.0.92) (1.18.1)
    Requirement already satisfied: pandas in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (from unitids==0.0.92) (1.0.1)
    Requirement already satisfied: nltk in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (from unitids==0.0.92) (3.4.5)
    Requirement already satisfied: textblob in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (from unitids==0.0.92) (0.15.3)
    Requirement already satisfied: pytz>=2017.2 in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (from pandas->unitids==0.0.92) (2019.3)
    Requirement already satisfied: python-dateutil>=2.6.1 in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (from pandas->unitids==0.0.92) (2.8.1)
    Requirement already satisfied: six in /Users/adamhearn/anaconda3/lib/python3.7/site-packages (from nltk->unitids==0.0.92) (1.14.0)


### Running the algorithm

The first argument we pass to the function, `forbes`, is our original dataset with the institutions of which we want to retreive unitids. The second argument, `stateFlag`, is an indicator of whether or not we have state abbreviations in our data. This makes the merge much faster and much cleaner, which I'll get to shortly.

The funciton returns two DataFrames: `merged` is our original dataset with the fancy new unitids. The second dataframe returned, `nonmatches`, allows us to investigate the institutions that did not perfectly merge and make adjustments as necessary. Now we're ready to call the function!

Sidenote: For the algorithm to run error-free, the institution name variable must be listed the first column and the state variable (if available) must be in the second column.


```python
# Calling the function
forbes_unitids, nonmatches = unitids.get_unitids(forbes, stateFlag = True)

#viewing the new data
forbes_unitids.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>institution</th>
      <th>State</th>
      <th>Financial GPA</th>
      <th>Financial Grade</th>
      <th>unitid</th>
      <th>match</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Stanford University</td>
      <td>CA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>243744.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Massachusetts Institute of Technology</td>
      <td>MA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>166683.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Notre Dame</td>
      <td>IN</td>
      <td>4.5</td>
      <td>A+</td>
      <td>152080.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Princeton University</td>
      <td>NJ</td>
      <td>4.5</td>
      <td>A+</td>
      <td>186131.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Pennsylvania</td>
      <td>PA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>215062.0</td>
      <td>100.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# How many did not merge?
forbes_unitids['unitid'].isna().sum()
```




    0



100% of the institutions merged! We have significantly fewer unitids we need to fill in ourselves. We can investigate the institutions that were not perfect merges by viewing the second DataFrame, `nonmatches`:


```python
nonmatches
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th>similarity</th>
      <th>unitid</th>
    </tr>
    <tr>
      <th>institution</th>
      <th>match</th>
      <th>Top 5</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">Baptist College of Health Sciences  (TN)</th>
      <th>1.0</th>
      <th>Baptist Memorial College of Health Sciences (TN)</th>
      <td>0.925820</td>
      <td>219639</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>Huntington College of Health Sciences (TN)</th>
      <td>0.833333</td>
      <td>488068</td>
    </tr>
    <tr>
      <th>3.0</th>
      <th>Huntington University of Health Sciences (TN)</th>
      <td>0.666667</td>
      <td>488068</td>
    </tr>
    <tr>
      <th>4.0</th>
      <th>American Baptist College (TN)</th>
      <td>0.612372</td>
      <td>219505</td>
    </tr>
    <tr>
      <th>5.0</th>
      <th>Fayetteville College of Cosmetology Arts and Sciences (TN)</th>
      <td>0.577350</td>
      <td>220163</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Calumet College of St. Joseph  (IN)</th>
      <th>1.0</th>
      <th>Calumet College of Saint Joseph (IN)</th>
      <td>0.833333</td>
      <td>150172</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>American College of Education (IN)</th>
      <td>0.547723</td>
      <td>449889</td>
    </tr>
    <tr>
      <th>Lincoln College of Technology (IN)</th>
      <td>0.547723</td>
      <td>151661</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">3.0</th>
      <th>College of Court Reporting Inc (IN)</th>
      <td>0.500000</td>
      <td>150251</td>
    </tr>
    <tr>
      <th>PJ's College of Cosmetology (IN)</th>
      <td>0.500000</td>
      <td>152150</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Franklin &amp; Marshall College  (PA)</th>
      <th>1.0</th>
      <th>Franklin and Marshall College (PA)</th>
      <td>0.894427</td>
      <td>212577</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>Harcum College (PA)</th>
      <td>0.577350</td>
      <td>212869</td>
    </tr>
    <tr>
      <th>Juniata College (PA)</th>
      <td>0.577350</td>
      <td>213251</td>
    </tr>
    <tr>
      <th>Rosemont College (PA)</th>
      <td>0.577350</td>
      <td>215691</td>
    </tr>
    <tr>
      <th>Wilson College (PA)</th>
      <td>0.577350</td>
      <td>217013</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Golden Gate University  (CA)</th>
      <th>1.0</th>
      <th>Golden Gate University-San Francisco (CA)</th>
      <td>0.816497</td>
      <td>115083</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>Ashford University (CA)</th>
      <td>0.577350</td>
      <td>154022</td>
    </tr>
    <tr>
      <th>Saybrook University (CA)</th>
      <td>0.577350</td>
      <td>123095</td>
    </tr>
    <tr>
      <th>Simpson University (CA)</th>
      <td>0.577350</td>
      <td>123457</td>
    </tr>
    <tr>
      <th>Stanbridge University (CA)</th>
      <td>0.577350</td>
      <td>446561</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Hobart and William Smith Colleges  (NY)</th>
      <th>1.0</th>
      <th>Hobart William Smith Colleges (NY)</th>
      <td>0.912871</td>
      <td>191630</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>The Sage Colleges (NY)</th>
      <td>0.408248</td>
      <td>195128</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">3.0</th>
      <th>Berk Trade and Business School (NY)</th>
      <td>0.333333</td>
      <td>189219</td>
    </tr>
    <tr>
      <th>Bryant and Stratton College-Lackawanna (NY)</th>
      <td>0.333333</td>
      <td>374972</td>
    </tr>
    <tr>
      <th>Elim Bible Institute and College (NY)</th>
      <td>0.333333</td>
      <td>488305</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Jefferson (Philadelphia University + Thomas Jefferson University)  (PA)</th>
      <th>1.0</th>
      <th>Thomas Jefferson University (PA)</th>
      <td>0.904534</td>
      <td>216366</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>Philadelphia Biblical University-Langhorne (PA)</th>
      <td>0.539360</td>
      <td>215114</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">3.0</th>
      <th>Bucknell University (PA)</th>
      <td>0.522233</td>
      <td>211291</td>
    </tr>
    <tr>
      <th>Lehigh University (PA)</th>
      <td>0.522233</td>
      <td>213543</td>
    </tr>
    <tr>
      <th>Widener University (PA)</th>
      <td>0.522233</td>
      <td>216852</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">LeMoyne-Owen College  (TN)</th>
      <th>1.0</th>
      <th>Le Moyne-Owen College (TN)</th>
      <td>0.670820</td>
      <td>220604</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>Bethel College (TN)</th>
      <td>0.577350</td>
      <td>219718</td>
    </tr>
    <tr>
      <th>Maryville College (TN)</th>
      <td>0.577350</td>
      <td>220710</td>
    </tr>
    <tr>
      <th>Rhodes College (TN)</th>
      <td>0.577350</td>
      <td>221351</td>
    </tr>
    <tr>
      <th>Welch College (TN)</th>
      <td>0.577350</td>
      <td>220206</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Mount St Joseph University  (OH)</th>
      <th>1.0</th>
      <th>Mount Saint Joseph University (OH)</th>
      <td>0.800000</td>
      <td>204200</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>College of Mount St Joseph (OH)</th>
      <td>0.730297</td>
      <td>204200</td>
    </tr>
    <tr>
      <th>College of Mount St. Joseph (OH)</th>
      <td>0.730297</td>
      <td>204200</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">3.0</th>
      <th>Mount Vernon Nazarene University (OH)</th>
      <td>0.600000</td>
      <td>204194</td>
    </tr>
    <tr>
      <th>University of Mount Union (OH)</th>
      <td>0.600000</td>
      <td>204185</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Paul Smith's College of Arts and Science  (NY)</th>
      <th>1.0</th>
      <th>Paul Smiths College of Arts and Science (NY)</th>
      <td>0.824958</td>
      <td>194392</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>SUNY College of Environmental Science and Forestry (NY)</th>
      <td>0.589256</td>
      <td>196103</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">3.0</th>
      <th>St. Joseph's College of Nursing (NY)</th>
      <td>0.503953</td>
      <td>195191</td>
    </tr>
    <tr>
      <th>Vaughn College of Aeronautics and Technology (NY)</th>
      <td>0.503953</td>
      <td>188340</td>
    </tr>
    <tr>
      <th>4.0</th>
      <th>St. Peter's Hospital College of Nursing (NY)</th>
      <td>0.471405</td>
      <td>192961</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Saint John's University  (MN)</th>
      <th>1.0</th>
      <th>Saint Mary's University of Minnesota (MN)</th>
      <td>0.676123</td>
      <td>174817</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>Saint Johns University (MN)</th>
      <td>0.670820</td>
      <td>174792</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">3.0</th>
      <th>Concordia University-Saint Paul (MN)</th>
      <td>0.600000</td>
      <td>173328</td>
    </tr>
    <tr>
      <th>Saint Cloud State University (MN)</th>
      <td>0.600000</td>
      <td>174783</td>
    </tr>
    <tr>
      <th>4.0</th>
      <th>Herzing University (MN)</th>
      <td>0.516398</td>
      <td>174154</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. Ambrose University  (IA)</th>
      <th>1.0</th>
      <th>Saint Ambrose University (IA)</th>
      <td>0.750000</td>
      <td>154235</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>Dordt University (IA)</th>
      <td>0.577350</td>
      <td>153250</td>
    </tr>
    <tr>
      <th>Drake University (IA)</th>
      <td>0.577350</td>
      <td>153269</td>
    </tr>
    <tr>
      <th>Shiloh University (IA)</th>
      <td>0.577350</td>
      <td>480499</td>
    </tr>
    <tr>
      <th>Waldorf University (IA)</th>
      <td>0.577350</td>
      <td>154518</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. Edward's University  (TX)</th>
      <th rowspan="3" valign="top">1.0</th>
      <th>Saint Edward's University (TX)</th>
      <td>0.800000</td>
      <td>227845</td>
    </tr>
    <tr>
      <th>St Mary's University (TX)</th>
      <td>0.800000</td>
      <td>228149</td>
    </tr>
    <tr>
      <th>St. Mary's University (TX)</th>
      <td>0.800000</td>
      <td>228149</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>King's University (TX)</th>
      <td>0.670820</td>
      <td>439701</td>
    </tr>
    <tr>
      <th>St Marys University (TX)</th>
      <td>0.670820</td>
      <td>228149</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. John Fisher College  (NY)</th>
      <th>1.0</th>
      <th>Saint John Fisher College (NY)</th>
      <td>0.800000</td>
      <td>195720</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>St Francis College (NY)</th>
      <td>0.670820</td>
      <td>195173</td>
    </tr>
    <tr>
      <th>St. Francis College (NY)</th>
      <td>0.670820</td>
      <td>195173</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">3.0</th>
      <th>St Thomas Aquinas College (NY)</th>
      <td>0.600000</td>
      <td>195243</td>
    </tr>
    <tr>
      <th>St. Thomas Aquinas College (NY)</th>
      <td>0.600000</td>
      <td>195243</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. Norbert College  (WI)</th>
      <th>1.0</th>
      <th>Saint Norbert College (WI)</th>
      <td>0.750000</td>
      <td>239716</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>Carroll College (WI)</th>
      <td>0.577350</td>
      <td>238458</td>
    </tr>
    <tr>
      <th>Edgewood College (WI)</th>
      <td>0.577350</td>
      <td>238661</td>
    </tr>
    <tr>
      <th>Lakeland College (WI)</th>
      <td>0.577350</td>
      <td>238980</td>
    </tr>
    <tr>
      <th>Shepherds College (WI)</th>
      <td>0.577350</td>
      <td>481137</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Tulane University  (LA)</th>
      <th>1.0</th>
      <th>Tulane University of Louisiana (LA)</th>
      <td>0.774597</td>
      <td>160755</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>Dillard University (LA)</th>
      <td>0.666667</td>
      <td>158802</td>
    </tr>
    <tr>
      <th>Herzing University (LA)</th>
      <td>0.666667</td>
      <td>433536</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">3.0</th>
      <th>McNeese State University (LA)</th>
      <td>0.577350</td>
      <td>159717</td>
    </tr>
    <tr>
      <th>Nicholls State University (LA)</th>
      <td>0.577350</td>
      <td>159966</td>
    </tr>
  </tbody>
</table>
</div>



For example, we can see that Franklin & Marshall College merged successfully with its official name in the IPEDS universe, "Franklin and Marshall College". Also, Tulane University merged successfully with "Tulane University of Louisiana", Hobart and William Smith Colleges merged with "Hobart William Smith Colleges", etc. 

Further, the algorithm accounts for institutions with changed names. For example, Dordt did not merge in the original dataset (since Forbes called it "Dordt College" and it's official IPEDS name is "Dordt University". The same issue is raised with Calvin College (now Calvin Univeristy). The IPEDS dictionary nested in the algorithm accounts for these historical name-changes. That is why there are only 15 non-perfect matches with this algorithm as opposed to 40 merging the "old fashioned way".

However, this wasn't perfect: Saint John's University (MN) merged with Saint Mary's University of Minnesota instead, so we will need to correct that ourselves. We can find the correct unitid in the `nonmatches` dataframe above. Still, one line of code compared to 40 is a big time-saver!


```python
# Replaces unitid for Saint John's University (MN) only
# For Stata folks, same as replace unitid = 174792 if institution == "Saint John's University (MN)"
forbes_unitids['untid'] = np.where(forbes_unitids['institution'] == "Saint John's University (MN)", 174792, forbes_unitids['unitid'])
```

Running this algorithm on this dataset as opposed to merging on institution-name gives us an accuracy of 99.9% (931 of 932 institutions), up from 95.7% earlier (892 of 932 institutions). It's a marginal improvement, but a big time-saver.

To answer our original research question of how endowment impacts Forbes' "Financial GPA" measure, we can merge in our IPEDS data cleanly here.


```python
dta = pd.merge(forbes_unitids, ipeds, on = 'unitid', how = 'left')
dta = dta.drop(columns = "institution_y") # no need for duplicate column
dta = dta.rename(columns = {"institution_x" : "institution"}) # renaming
dta.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>institution</th>
      <th>State</th>
      <th>Financial GPA</th>
      <th>Financial Grade</th>
      <th>unitid</th>
      <th>match</th>
      <th>untid</th>
      <th>endowment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Stanford University</td>
      <td>CA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>243744.0</td>
      <td>100.0</td>
      <td>243744.0</td>
      <td>1496715.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Massachusetts Institute of Technology</td>
      <td>MA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>166683.0</td>
      <td>100.0</td>
      <td>166683.0</td>
      <td>1454419.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Notre Dame</td>
      <td>IN</td>
      <td>4.5</td>
      <td>A+</td>
      <td>152080.0</td>
      <td>100.0</td>
      <td>152080.0</td>
      <td>837184.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Princeton University</td>
      <td>NJ</td>
      <td>4.5</td>
      <td>A+</td>
      <td>186131.0</td>
      <td>100.0</td>
      <td>186131.0</td>
      <td>3053449.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of Pennsylvania</td>
      <td>PA</td>
      <td>4.5</td>
      <td>A+</td>
      <td>215062.0</td>
      <td>100.0</td>
      <td>215062.0</td>
      <td>562092.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

#using logged endowment, as any sane econometrician would
sns.scatterplot(x=np.log(dta["endowment"]), y=dta["Financial GPA"]) 
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1a19878950>




![png](output_31_1.png)


Seems like endowment plays a pretty significant role in Forbes' grading of Financial GPA!

### What if we have no state data?

Note that the original merge went very well mostly due to us having access to state codes in our secondary dataset. Suppose our Forbes data did not have state codes, in which case the merge would have gone like this:


```python
forbes_unitids, nonmatches = unitids.get_unitids(forbes, stateFlag = False)
```

Running the algorithm with `stateFlag = False` takes significantly longer, considering we can no longer "throw out" institutions that do not match the same state. Instead, the algorithm must cross-check institutions across all states, not just the ones within states like it did when `stateFlag` was set to `True`.


```python
nonmatches
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th></th>
      <th>similarity</th>
      <th>unitid</th>
    </tr>
    <tr>
      <th>institution</th>
      <th>match</th>
      <th>Top 5</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">Baptist College of Health Sciences</th>
      <th>1.0</th>
      <th>Baptist Memorial College of Health Sciences (TN)</th>
      <td>0.912871</td>
      <td>219639</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>Australasian College of Health Sciences (OR)</th>
      <td>0.800000</td>
      <td>443599</td>
    </tr>
    <tr>
      <th>Bryan College of Health Sciences (NE)</th>
      <td>0.800000</td>
      <td>180878</td>
    </tr>
    <tr>
      <th>Jefferson College of Health Sciences (VA)</th>
      <td>0.800000</td>
      <td>231837</td>
    </tr>
    <tr>
      <th>Sentara College of Health Sciences (VA)</th>
      <td>0.800000</td>
      <td>232885</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Calumet College of St. Joseph</th>
      <th>1.0</th>
      <th>College of St Joseph (VT)</th>
      <td>0.894427</td>
      <td>231077</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">2.0</th>
      <th>Calumet College of Saint Joseph (IN)</th>
      <td>0.800000</td>
      <td>150172</td>
    </tr>
    <tr>
      <th>College of Mount St Joseph (OH)</th>
      <td>0.800000</td>
      <td>204200</td>
    </tr>
    <tr>
      <th>College of Mount St. Joseph (OH)</th>
      <td>0.800000</td>
      <td>204200</td>
    </tr>
    <tr>
      <th>3.0</th>
      <th>St. Joseph's College of Nursing (NY)</th>
      <td>0.730297</td>
      <td>195191</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Franklin &amp; Marshall College</th>
      <th>1.0</th>
      <th>Franklin and Marshall College (PA)</th>
      <td>0.866025</td>
      <td>212577</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>Franklin College (IN)</th>
      <td>0.816497</td>
      <td>150604</td>
    </tr>
    <tr>
      <th>Franklin College (TX)</th>
      <td>0.816497</td>
      <td>225788</td>
    </tr>
    <tr>
      <th>3.0</th>
      <th>Franklin Pierce College (NH)</th>
      <td>0.666667</td>
      <td>182795</td>
    </tr>
    <tr>
      <th>4.0</th>
      <th>Marshall Community and Technical College (WV)</th>
      <td>0.516398</td>
      <td>444954</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Golden Gate University</th>
      <th>1.0</th>
      <th>Golden Gate University-San Francisco (CA)</th>
      <td>0.774597</td>
      <td>115083</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>Chapman University-University College (CA)</th>
      <td>0.471405</td>
      <td>262086</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">3.0</th>
      <th>Indiana University-Purdue University-Indianapolis (IN)</th>
      <td>0.436436</td>
      <td>151111</td>
    </tr>
    <tr>
      <th>University of Illinois University Administration (IL)</th>
      <td>0.436436</td>
      <td>149587</td>
    </tr>
    <tr>
      <th>University of Maryland-University College (MD)</th>
      <td>0.436436</td>
      <td>163204</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Hobart and William Smith Colleges</th>
      <th>1.0</th>
      <th>Hobart William Smith Colleges (NY)</th>
      <td>0.894427</td>
      <td>191630</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>College of William and Mary (VA)</th>
      <td>0.400000</td>
      <td>231624</td>
    </tr>
    <tr>
      <th>3.0</th>
      <th>Texas Barber Colleges and Hairstyling Schools (TX)</th>
      <td>0.365148</td>
      <td>440989</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">4.0</th>
      <th>Richard Bland College of William and Mary (VA)</th>
      <td>0.338062</td>
      <td>233338</td>
    </tr>
    <tr>
      <th>State Board for Community and Junior Colleges (MS)</th>
      <td>0.338062</td>
      <td>247737</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Jefferson (Philadelphia University + Thomas Jefferson University)</th>
      <th>1.0</th>
      <th>Thomas Jefferson University (PA)</th>
      <td>0.912871</td>
      <td>216366</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>Thomas University (GA)</th>
      <td>0.670820</td>
      <td>141167</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">3.0</th>
      <th>Saint Thomas University (FL)</th>
      <td>0.547723</td>
      <td>137476</td>
    </tr>
    <tr>
      <th>St Thomas University (FL)</th>
      <td>0.547723</td>
      <td>137476</td>
    </tr>
    <tr>
      <th>St. Thomas University (FL)</th>
      <td>0.547723</td>
      <td>137476</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">LeMoyne-Owen College</th>
      <th>1.0</th>
      <th>Le Moyne-Owen College (TN)</th>
      <td>0.577350</td>
      <td>220604</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>Hussian College-Daymar College Clarksville (TN)</th>
      <td>0.436436</td>
      <td>368443</td>
    </tr>
    <tr>
      <th>Hussian College-Daymar College Columbus (OH)</th>
      <td>0.436436</td>
      <td>205559</td>
    </tr>
    <tr>
      <th>Hussian College-Daymar College Murfreesboro (TN)</th>
      <td>0.436436</td>
      <td>444255</td>
    </tr>
    <tr>
      <th>Hussian College-Daymar College Nashville (TN)</th>
      <td>0.436436</td>
      <td>220002</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Mount St Joseph University</th>
      <th>1.0</th>
      <th>Mount Saint Joseph University (OH)</th>
      <td>0.750000</td>
      <td>204200</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">2.0</th>
      <th>College of Mount St Joseph (OH)</th>
      <td>0.670820</td>
      <td>204200</td>
    </tr>
    <tr>
      <th>College of Mount St. Joseph (OH)</th>
      <td>0.670820</td>
      <td>204200</td>
    </tr>
    <tr>
      <th>Mount St Mary's University (MD)</th>
      <td>0.670820</td>
      <td>163462</td>
    </tr>
    <tr>
      <th>Mount St. Mary's University (MD)</th>
      <td>0.670820</td>
      <td>163462</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Paul Smith's College of Arts and Science</th>
      <th>1.0</th>
      <th>Paul Smiths College of Arts and Science (NY)</th>
      <td>0.801784</td>
      <td>194392</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>University of Science and Arts of Oklahoma (OK)</th>
      <td>0.589256</td>
      <td>207722</td>
    </tr>
    <tr>
      <th>3.0</th>
      <th>Hope College of Arts and Sciences (FL)</th>
      <td>0.577350</td>
      <td>488332</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">4.0</th>
      <th>Baker University College of Arts and Sciences (KS)</th>
      <td>0.534522</td>
      <td>154688</td>
    </tr>
    <tr>
      <th>Mayo Clinic College of Medicine and Science (MN)</th>
      <td>0.534522</td>
      <td>173957</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Saint John's University</th>
      <th rowspan="5" valign="top">1.0</th>
      <th>Saint Edward's University (TX)</th>
      <td>0.750000</td>
      <td>227845</td>
    </tr>
    <tr>
      <th>Saint John's Seminary (MA)</th>
      <td>0.750000</td>
      <td>167677</td>
    </tr>
    <tr>
      <th>Saint Joseph's University (PA)</th>
      <td>0.750000</td>
      <td>215770</td>
    </tr>
    <tr>
      <th>Saint Martin's University (WA)</th>
      <td>0.750000</td>
      <td>236452</td>
    </tr>
    <tr>
      <th>Saint Peter's University (NJ)</th>
      <td>0.750000</td>
      <td>186432</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. Ambrose University</th>
      <th rowspan="5" valign="top">1.0</th>
      <th>St Bonaventure University (NY)</th>
      <td>0.666667</td>
      <td>195164</td>
    </tr>
    <tr>
      <th>St Lawrence University (NY)</th>
      <td>0.666667</td>
      <td>195216</td>
    </tr>
    <tr>
      <th>St. Andrews University (NC)</th>
      <td>0.666667</td>
      <td>199698</td>
    </tr>
    <tr>
      <th>St. Catherine University (MN)</th>
      <td>0.666667</td>
      <td>175005</td>
    </tr>
    <tr>
      <th>St. Thomas University (FL)</th>
      <td>0.666667</td>
      <td>137476</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. Edward's University</th>
      <th rowspan="3" valign="top">1.0</th>
      <th>Saint Edward's University (TX)</th>
      <td>0.750000</td>
      <td>227845</td>
    </tr>
    <tr>
      <th>St Mary's University (TX)</th>
      <td>0.750000</td>
      <td>228149</td>
    </tr>
    <tr>
      <th>St. Mary's University (TX)</th>
      <td>0.750000</td>
      <td>228149</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>Mount St Mary's University (MD)</th>
      <td>0.670820</td>
      <td>163462</td>
    </tr>
    <tr>
      <th>Mount St. Mary's University (MD)</th>
      <td>0.670820</td>
      <td>163462</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. John Fisher College</th>
      <th rowspan="5" valign="top">1.0</th>
      <th>Saint John Fisher College (NY)</th>
      <td>0.750000</td>
      <td>195720</td>
    </tr>
    <tr>
      <th>St John's College (MD)</th>
      <td>0.750000</td>
      <td>163976</td>
    </tr>
    <tr>
      <th>St John's College (NM)</th>
      <td>0.750000</td>
      <td>245652</td>
    </tr>
    <tr>
      <th>St. John's College (MD)</th>
      <td>0.750000</td>
      <td>163976</td>
    </tr>
    <tr>
      <th>St. John's College (NM)</th>
      <td>0.750000</td>
      <td>245652</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">St. Norbert College</th>
      <th rowspan="5" valign="top">1.0</th>
      <th>Saint Norbert College (WI)</th>
      <td>0.666667</td>
      <td>239716</td>
    </tr>
    <tr>
      <th>St Johns College (IL)</th>
      <td>0.666667</td>
      <td>148593</td>
    </tr>
    <tr>
      <th>St Petersburg College (FL)</th>
      <td>0.666667</td>
      <td>137078</td>
    </tr>
    <tr>
      <th>St Philips College (TX)</th>
      <td>0.666667</td>
      <td>227854</td>
    </tr>
    <tr>
      <th>St. Olaf College (MN)</th>
      <td>0.666667</td>
      <td>174844</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Tulane University</th>
      <th>1.0</th>
      <th>Tulane University of Louisiana (LA)</th>
      <td>0.707107</td>
      <td>160755</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>Chapman University-University College (CA)</th>
      <td>0.577350</td>
      <td>262086</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">3.0</th>
      <th>Indiana University-Purdue University-Indianapolis (IN)</th>
      <td>0.534522</td>
      <td>151111</td>
    </tr>
    <tr>
      <th>University of Illinois University Administration (IL)</th>
      <td>0.534522</td>
      <td>149587</td>
    </tr>
    <tr>
      <th>University of Maryland-University College (MD)</th>
      <td>0.534522</td>
      <td>163204</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Union College</th>
      <th rowspan="3" valign="top">1.0</th>
      <th>Union College (KY)</th>
      <td>1.000000</td>
      <td>157863</td>
    </tr>
    <tr>
      <th>Union College (NE)</th>
      <td>1.000000</td>
      <td>181738</td>
    </tr>
    <tr>
      <th>Union College (NY)</th>
      <td>1.000000</td>
      <td>196866</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>Columbia Union College (MD)</th>
      <td>0.816497</td>
      <td>162210</td>
    </tr>
    <tr>
      <th>Union County College (NJ)</th>
      <td>0.816497</td>
      <td>187198</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">University of St. Thomas</th>
      <th rowspan="3" valign="top">1.0</th>
      <th>University of St Thomas (MN)</th>
      <td>1.000000</td>
      <td>174914</td>
    </tr>
    <tr>
      <th>University of St Thomas (TX)</th>
      <td>1.000000</td>
      <td>227863</td>
    </tr>
    <tr>
      <th>University of St. Thomas (MN)</th>
      <td>1.000000</td>
      <td>174914</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">2.0</th>
      <th>St Thomas University (FL)</th>
      <td>0.866025</td>
      <td>137476</td>
    </tr>
    <tr>
      <th>St. Thomas University (FL)</th>
      <td>0.866025</td>
      <td>137476</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Westminster College</th>
      <th rowspan="3" valign="top">1.0</th>
      <th>Westminster College (MO)</th>
      <td>1.000000</td>
      <td>179946</td>
    </tr>
    <tr>
      <th>Westminster College (PA)</th>
      <td>1.000000</td>
      <td>216807</td>
    </tr>
    <tr>
      <th>Westminster College (UT)</th>
      <td>1.000000</td>
      <td>230807</td>
    </tr>
    <tr>
      <th>2.0</th>
      <th>Utah College of Massage Therapy-Westminster (CO)</th>
      <td>0.577350</td>
      <td>469151</td>
    </tr>
    <tr>
      <th>3.0</th>
      <th>Hussian College-Daymar College Nashville (TN)</th>
      <td>0.534522</td>
      <td>220002</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">Wheaton College</th>
      <th rowspan="2" valign="top">1.0</th>
      <th>Wheaton College (IL)</th>
      <td>1.000000</td>
      <td>149781</td>
    </tr>
    <tr>
      <th>Wheaton College (MA)</th>
      <td>1.000000</td>
      <td>168281</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">2.0</th>
      <th>Hussian College-Daymar College Clarksville (TN)</th>
      <td>0.534522</td>
      <td>368443</td>
    </tr>
    <tr>
      <th>Hussian College-Daymar College Columbus (OH)</th>
      <td>0.534522</td>
      <td>205559</td>
    </tr>
    <tr>
      <th>Hussian College-Daymar College Murfreesboro (TN)</th>
      <td>0.534522</td>
      <td>444255</td>
    </tr>
  </tbody>
</table>
</div>



There were still 913 perfect merges, but the accuracy on imputing the remaining 19 unitids is not as high: we only got 13 of these (accuracy of 68% within the nonperfect matches, 99.4% for the whole dataset). 

For example, Calumet College of St. Joseph merged with College of St. Joseph (VT) when it should have merged with Calumet College of Saint Joseph (IN). Plus, we must now account for institutions with the same name, such as Wheaton College (IL and MA). Still, not terrible, but it is alwasy a good idea to check for what unitids were imputed. Luckily this module makes it easy to do that. 

# Conclusion

I hope this can be a valuable tool for higher ed researchers out there. While this is currently only available in Python, I hope to get around to making it available on Stata and R soon. Please leave any feedback or bug reports on my GitHub repository [here](www.github.com/ahearn15/get_unitds). 
