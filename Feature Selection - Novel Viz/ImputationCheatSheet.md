# Imputation Cheat Sheet
#### When to use Imputation?: When the data is missing mostly or completely at random (MAR or MCAR)
##### Modules such as Missingno are helpful to determine this
##### Additional Note: If the data is Not Missing at Random (NMAR), most imputation (Quantitative) will not work, and the missing values will have to be deduced manually

###### Our Dataset has Missing Values mostly at random
###### All of the datasets described below do not have certain features that pertain to only entries of a certain completion type

## 1. Dropping the Missing Data: Quantitative and Qualitative
<b>Pros:</b> Keeps pair-wise relationships, Useful in dealing with some multivariate relationships between features (that are captured by the "complete" data entries.

<b>Cons:</b> Potential loss in information from a significant amount of entries to entire features. Loss in descriptive and inferential statistics per feature. Loss in some multivariate relationships as entries (or features) are lost.

<b>What is the most appropriate usage?</b> When a certain feature has only a few missing entries (<5% is a good rule), (or the entire feature if it is missing the majority (>50~60% is a good rule) of its values and it is inconsequential)
### Dataset in the repository: NoNanDataset.csv

## 2. Single-Variate Mean Imputation: Quantitative
<b>Pros:</b> The only change in descriptive statistics will occur in the Modal concentration and a decrease in the variability. Quick to implement.

<b>Cons:</b> Decrease in the variance, and modal concentration. Only focuses on a single feature when imputing values. Loss in pair-wise relationships along with multivariate relationships. This is especially apparent when the percentage of data missing is significant (>5%, but ultimately depends on the data).

<b>What is the most appropriate Usage?</b> This is almost never the right answer to dealing with missing data, it is used more so as a quick fix when potential loss of feature relationships is at a mininimum (<5% is a good rule); however, if the missing data is that low, dropping the missing values is a more favorable method.
### Dataset in the repository: MeanImputationDS.csv

## 3. Sklearn Multivariate Iterative Imputation: Quantitative
###### Based on MICE Imputation
<b>Pros:</b> Incorporates other features when imputing missing values.This method not only maintains descriptive and inferential statistics, but maintains multivariate relations (or at least more so than single variate methods) Useful in predictive/exploratory analysis

<b>Cons:</b> This is still in the experimental phase, so parameters are prone to change. Despite the accuracy in predictive analysis, and in inferential/descriptive statitistics, this imputation method still takes liberties (such as incorporating some negative values when the feature could not be negative). Interesting relations are formed (especially in features with significant amounts of missing values) that may or may not be accurate.

<b>What is the most appropriate Usage?</b> This seems to be one of the best ways to impute data that are missing mostly or completely at random. The Multivariate nature of this imputation technique makes it prime for predictive analysis.
### Dataset in the repository: IterativeImputeDS.csv
#### *Additional Note: This dataset only has the quantitative data, and qualitative data needs to be added 

## 4. Single-Variate K-Nearest Neighbor: Quantitative
<b>Pros:</b> At a k-value higher than 1, maintains inferential/descriptive statistics per feature.

<b>Cons:</b> Loss in multivariate relations between features. Can be slow to impute (depending on the k-value).

<b>What is the most appropriate usage?</b> When a user wants to look for inferential, and descriptive statistics of a feature; however, this method performs poorly when trying to maintain multivariate relationships
### Dataset in the repository: NA (If necessary, one can access it by running through the K-NN portion of the ImputationAnalysis notebook)
#### *Additional Note: This dataset only has the quantitative data. Qualitative data will need to be added back

## 5. Multiple Imputation through Chained Equations (MICE): Quantitative
###### Similar to Iterative Imputation from sklearn, but with a touch or randomness (can be influenced by a random(seed))
<b>Pros:</b> Similar to Iterative Imputation from sklearn. Based upon the paper MICE was described in. Can potentially be used to check feature relations described in other models.

<b>Cons:</b> Similar to iterative Imputation from sklearn.

<b>What is the most appropriate Usage?</b> See Iterative Imputation
### Dataset in the repository: NA (If necessary, one can access it by running through the MICE portion of the ImputationAnalysis notebook)
#### *Additional Note: This dataset only has the quantitative data. Qualitative data will need to be added back.

## 6. Conditional Imputation: Qualitative
This is a method to deal with qualitative/categorical data within a dataset, using conditional probability to impute the missing data. I have a crude implementation in Imputation Analysis; however, it is fairly slow to impute as it goes entry per entry, and can definitely be optimized. Moreover, it currently does not have a feature weighting system to account for the importance of certain features.
### Dataset in Repository: DatasetIIandCI.csv
#### *Additional Note: I would not run conditional imputation portion of the Imputation analysis notebook, as it will take the longest to run, instead use this dataset to add qualitative data to other datasets.

## Other Qualitative Imputation Methods
k-modal imputation is another qualitative imputation method; however, this really only works with features with a few missing values and that are missing at random. Our qualitative data at least is significantly interrelated.
