# 2020 Summer Fellows

A repository for the 2020 FRI Energy Analytics summer fellows. Contains code and work from the 2020 FRI Summer Fellows from June 1 to July 24 2020. Includes Sat2Geo, Feature Selection, and Well Log Mnemonics teams.

## Organization

Contents:
* Feature Selection - Novel Viz
* Sat2Geo
* Well Log Mnemonics

## Description

#### Feature Selection - Novel Viz 

The focus of our research was to apply interdisciplinary concepts to geostatistical data to gain novel insights. By creating a review process that scouted, tested, and rated models from various fields, we were able to test their effectiveness on our set well log data. By focusing on these models' interrelatedness, we were able to combine ideas from the various models then and use that to inform the creation of new novel applications for said models. Examples include using the Edgeworth Box economic model and applying it to oil well production by equating groups who seek to maximize profits to wells that seek to maximize efficiency and production. Similarly, the Solow model is an economic model applied to oil well production by connecting technological growth, population growth, and production saving rates to optimize cumulative production. Likewise, the Pareto Chart is an economic model that calculates how each feature contributes to the cumulative percentage of production, highlighting its most impactful features. Throughout this process, what has become clear is that the integration of interdisciplinary models and concepts into the geoscience field can only be beneficial and should be incorporated into future research.  

### Sat2Geo

The different methods that we took to try to optimize the GAN is by adding different numbers of dropout layers, each with different percentages to drop out for both the generator and the discriminator.

We also did more work to try to get image collection and image splitting to be as clean as possible. This involved making sure that the three different sets used to train the model (testing, training, and validation) were connected to each other in different ways. For example, one model, the testing and training sets were pulling subimages from the same source of images while the validation set was pulling subimages from a completely different set of images.

The metrics that we were using to make sure that the model was doing well was by looking at individual generator and discriminator losses along with looking at a rolling average for those two metrics to see how the model did overtime.

A program first generated Sequential Gaussian Simulat imaging, then overlayed that image on top of a satellite image with a random shift in both the x and y direction with overlap for each image. This removed the ability for the GAN to simply memorize the pixel opacity and colors of the pattern and instead forced the GAN to utilize it's ability to recognize multi-pixel subpatterns in the data when determining image recreation.

I also varied opacity to increased the intensity of the training, using datasets with 40%, 60% and 80% opacity of noise.

### Well Log Mnemonics

Aliaser is a Python package that reads mnemonics from LAS files and outputs an aliased dictionary of mnemonics and its
aliases, as well as a list of mnemonics that cannot be found. It uses three different methods to find aliases to mnemonics:
locates exact matches of a mnemonic in an alias dictionary, identifies keywords in mnemonics' description then returns
alias from the keyword extractor, and predicts alias using all attributes of the curves.
