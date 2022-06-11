# Using-ML-in-blockchain
Inducing ML in smart contracts to solve the problem of hyperparameter optimization.

## Problem Statement
In ML/DL, a model is defined or represented by the model parameters. However, the process of training a model involves choosing the optimal hyperparameters that the learning algorithm will use to learn the optimal parameters that correctly map the input features (independent variables) to the labels or targets (dependent variable) in order to achieve some form of intelligence.
There are several hyperparameters that can be changed in order to get the best configuration of these parameters for optimal performance.

To address the aforementioned issue, I've presented a model that can serve as a common platform for individuals looking for an AI-based solution and those who can deliver it.

## Abstract
My work presents a methodology that allows a machine learning model to be trained in a trust-less manner. This drives the market wherein individuals with excellent machine learning skills may
monetize their expertise, and any business or software agent with an AI challenge can seek answers from around the world. Utilizing the capabilities of a smart contract of
Blockchain for the submission of optimal solutions to particular datasets. This smart contract delivers a compensation in exchange for a machine learning model that has been
trained. 

In order to overcome the challenges of storing large files and datasets on the blockchain, I've employed IPFS (InterPlanetary File System) for storing data in a distributed network. To demonstrate the methodology, I'm using using time series data with RNN
(Recurrent neural network) on Ethereum Blockchain.

## Working of the model
IPFS file sharing system is used to store files that contain data obtained via API. After that, the organizer interacts with the blockchain to store the IPFS hashes. A participant, on the other hand, can access the chain to download the data and train the model independently at their end. Users are expected to submit their responses within a certain amount of time. No solution will be accepted from any user after this time window has expired. Following that, the owner reviews all of the submitted models and adds the ID of the best model to the blockchain. If the model of a user is chosen, he receives a reward else the reward will be paid back to the user.
The model is divided into several stages:
* Preprocessing stage
* Initialization stage
* Submission Stage
* Evaluation stage
* Final stage



