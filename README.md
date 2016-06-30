# Multi Armed Bandits

The code used to tackle the Multi Armed Bandit problem. The Bandits.py file includes three different methods.

## Thompson Sampling

The Thompson Sampling is done with the BetaBandit class. It keeps track of a beta distribution for every option. The code is based on https://gist.github.com/stucchio/5383149#file-beta_bandit-py, but adapted to allow a weighting (for example to predict a price). In the RunBetaBandit.py is an example used for a project.

## Bootstrap Sampling

The Bootstrap Sampling is done with the SampleMean class. It keeps track of many MeanBandits, which only keep track of the mean. The Bootstrap Sampling method of updating every MeanBandit with 0.5 probability introduces the exploration. In the RunSampleMean.py is an example used for a project.

## Linear Bootstrap Sampling

The Linear Bootstrap Sampling is done with the SampleLinear class. It keeps track of many LinearBandits, which linearly model the success rate given some variables. In the RunLinearMean.py is an example used for a project.
