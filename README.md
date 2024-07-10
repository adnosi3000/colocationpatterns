<h1>Co-location Patterns Library</h1>
Python package for discovaring co-location patterns from POIs datasets (spatial data).

<h2>Package overview</h2>
Based on [1] a generalized algortihm for mining co-location patterns was implemented. It allows to find
co-locations in dataset containig POIs of different types. Required attributes are: unique id, feature
class name (event type name) and geoemtry (lon/lat or x/y point). It uses euclidean distance as neighbor relation definition. 
<br>
For example based on sample POIs data following co-locations may be found if R-proximity for neighbourhood
is set for 2.95 and participation index threshold is 0.5:
<ol>
    <li>{B, C}</li>
    <li>{C, A}</li>
</ol>

<img src="img/sample_dataset.png">


<h2>Further work</h2>
<ul>
    <li>Implement other algorithms</li>
    <li>Transfer the burden of calculations to the database engine</li>
    <li>Handle neighborhood definitions other than Euclidean distance, e.g. isohrones</li>
</ul>
<h2>Known issues</h2>
<ul>
    <li>Inefficient memory usage: pandas.DataFrame duplicated objects. May affect processing for big data sets</li>
</ul>
<h2>Installation</h2>
Package not released yet. For now, just copy git repository and add it's location to Python path in order
to allow imports.<br><br>
<code>
git clone https://github.com/adnosi3000/colocationpatterns.git
</code>

<h2>References</h2>
[1] Huang, Y., Shekhar, S., Xiong, H., 2004. Discovering colocation patterns from spatial data sets: a general approach. IEEE Transactions on Knowledge and Data Engineering 16, 1472–1485. https://doi.org/10.1109/TKDE.2004.90
