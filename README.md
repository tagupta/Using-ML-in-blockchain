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

![image11](https://user-images.githubusercontent.com/45707143/173199426-dee99ecf-935c-4eb8-839a-fff9d2b465c6.PNG)

### Preprocessing stage
Preparing the data for training for the participants of the model.
![image22](https://user-images.githubusercontent.com/45707143/173199626-e0f938dd-b067-4bb1-9667-34a616954c4d.PNG)

### Initialization Stage
* Reward is deposited in the contract by the owner in form of funds, 10 ETH to be specific.
* IPFS hashes of the files are added for training data for the users.
* A minimum accuracy metric is added to eliminate low-performance models.
* A sequence length and a future predict period are also submitted.
* Make sure that the initial level of the contract is zero for the successful execution of the function.

![image33](https://user-images.githubusercontent.com/45707143/173199741-4590495c-d752-46d6-9cc0-5f28ab43cb62.PNG)

### Submission Stage
Before submitting the solution, a user gets the dataset from IPFS hashes. Using these hashes they can download the files. The user trains the model independently at his end using the given dataset. During this stage, any user can submit the potential model in a given time frame.

1. User submits the model solution by calling the submit_model function with the following parameters:
  * The address of the user.
  * The number of dense layers needed.
  * The number of units needed in each LSTM layer
  * The number of LSTM layers required.
  * The activation function
  * The loss function.
  
  ![image44](https://user-images.githubusercontent.com/45707143/173199901-ec5782f4-ae9f-4cde-b993-f1aa3d841970.PNG)
  
  ### Evaluation Stage
  The evaluation stage begins after the submission stage. In this stage, the owner fetches all the model solutions submitted by the users to evaluate the model at his end. 

1. Owner trains the model using the definitions specified by the users and passes the accuracy metric to the evaluation function for each solution.

* In the set_evaluaion_metrics function, models with accuracies less than the minimum are eliminated and the best submission ID along with its accuracy is stored on the blockchain.





