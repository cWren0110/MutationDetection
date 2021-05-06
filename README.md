# MutationDetection

### Project Assumptions

1. 1e6 is a near enough order of magnitude to an actual set of data that to reduce computational resources needed we can construct out individuals at 1e6 nucleotides.
2. Mutations naturally occur at a rate of about 1 in every 1500 nucleotides
3. A realistic sample set to model after is 100 individuals with 50% sick.
4. Enough similarities exist across species to say what mutation is (1) and what a mutation isn’t (0). (Rather than to "map entire genome")

### Methods for generating groups

#### Common between groups:

1. Groups are made of 100 individuals.
2. Individuals are made of 1e6 binary locations, where 0 indicated no mutation and 1 indicates a mutation at that given nucleotide location.
3. Every location has a 1/1500 chance of being a mutation.
50% of the group was made sick with the following different methods:
Options for making group sick
Option 1: Single, randomly placed mutation indicates sickness
Classification quality:  For the most part this simple scenario was handled quite well by all the classification algorithms and could even be potentially used in situations with some low noise.
Option 2: One of two randomly placed mutations indicates sickness
Classification quality:  Similar to option 1, this option could be was handled fairly well by the algorithms and could also handle some noise in the data.
Option 3: A mutation at any 2 of 5 randomly selected mutation locations indicates sickness
Classification quality:  The classification returned decent results for this option, but there seems to be little to no ability to handle noise in the data.
Option 4: Given a randomly selected range of 1000 nucleotides, if there are at least 3 mutations present that indicates sickness
Classification quality:  The classification returned quite poor results  for this option.  Results seemed to improve as compression is increased, which makes sense because the densities causing illness are combined into high values in theory.
Option 5: Given a randomly selected range of 1000 nucleotides, if there are at least 3 mutations present and another 2 mutations are present elsewhere that indicates sickness
Classification quality:  The classification returned decent results for this option, but this not much of a success as this option is just a slightly more complicated version of 1 and 2.
The attached files correspond to plots analysing the classification results of the Elastic Net with alpha = .01 for  each of these options, using different compression methods as well as different noise levels.
Noise
There were also tests done with noise, such that the groups were generated in the ways above, then each individual was given a p percent chance of switching from being health to sick or sick to being healthy until p % of the group has been changed.
What this does is create individuals who are sick without the mutations that the other sick individuals have, as well as healthy individuals who have the mutations that would normally indicate sickness.
For the most part no compression method or classification method could deal particularly well with noise.
Group Compression
Windows
For a window of size n, an individual’s mutation values (0-no mutation, or 1-mutation) would be added up for every n indices in the individual.  Window sizes that were examined were 500, 1000, 1500, 2500, 5000, 7000, and 10000.  In the end the method of compression individuals using windows proved to eliminate too much data indiscriminately and resulted in poor classification results.
Haar Discrete Wavelet Transform https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html#multilevel-decomposition-using-wavedec
Using the Discrete Wavelet Transform for a variety of levels resulted in the best results for overall. Levels 1-7 were examined and the reduced individual size is as follows.
Level 0 (original group) - 1000000
Level 1 - 500000
Level 2 - 250000
Level 3 - 125000
Level 4 - 62500
Level 5 - 31250
Level 6 - 15625
Level 7 - 7812
Quality results would could be seen up to level 4 (individual size of  about 62500), but as individual sized got below about 60000 the classification results would degrade.
Zero-reduction + Haar Discrete Wavelet Transform
Because variation is what is being looked at in determining mutations that cause genetic illness, there are many nucleotide positions that are mutation free across the entire group.  This method removes every nucleotide position that is mutation press across the group.  This results in a baseline individual size of about 65000.  From this baseline, Haar Discrete Wavelet Transform was then applied as well for levels 1-7.  The results for most tests could at most reach Level 1 before results began to degrade.
Level 0 (original group) - ~65000
Level 1 - ~32500
Level 2 - ~16250
Level 3 - ~8125
Level 4 - ~4062
Level 5 - ~2031
Level 6 - ~1015
Level 7 - ~507
Similar to just doing Haar Discrete Wavelet Transform individual sizes of about 60000 were required for decent results
Classification methods examined
Elastic Net
http://scikit-learn.org/stable/modules/linear_model.html#elastic-net
Ridge
http://scikit-learn.org/stable/modules/linear_model.html#ridge-regression
Lasso
http://scikit-learn.org/stable/modules/linear_model.html#lasso
LassoLars
http://scikit-learn.org/stable/modules/linear_model.html#lars-lasso

After running each classification method for all group types, compression types as well as a number of alpha, the method that showed the most versatility and accuracy was the Elastic Net method with an alpha value of about .01.
