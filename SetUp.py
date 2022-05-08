import pandas as pd
import io
from sklearn import preprocessing
from collections import deque
import numpy as np
import random
import time
import ipfshttpclient
import csv
import json
import web3
import tensorflow as tf
import config as cfg
# %load_ext tensorboard


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from web3 import Web3
from coinpaprika import client as Coinpaprika

cfg.DEBUG='TRUE'

### FETCHING DATA FROM A REAL TIME API

client = Coinpaprika.Client()
coins = client.coins()
coinList = []
listHashes = []
symbols = ["BTC", "ETH", "LTC", "BCH"]
names = ["Bitcoin", "Ethereum", "Litecoin","Bitcoin Cash"]

def check_if_exists(x, ls):
    if x in ls:
      return True
    else:
      return False

for coin in coins:
  if(check_if_exists(coin['symbol'], symbols) and check_if_exists(coin['name'],names)):
       coinList.append({"id": coin['id'], "symbol": coin['symbol']})

print(coinList)

def createFiles (id,symbol): 
  response = client.historical(f"{id}", start="2022-05-08T00:00:00Z")  #YYY-MM-DD
  ourdata = []
  #csvheader = ['TimeStamp','Price','Volume','Market_Cap']

  for x in response:
    listing = [x["timestamp"], x["price"], x["volume_24h"], x["market_cap"]]
    ourdata.append(listing)

  with open(f"{symbol}-USD.csv",'w', encoding='UTF8',newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(csvheader)
    writer.writerows(ourdata)
  
  return("done")

### CONNECTING TO IPFS TO STORE FILES

ipfsClient = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
print(ipfsClient)

for coin in coinList:
  print(f"{createFiles(coin['id'], coin['symbol'])}")
  res = ipfsClient.add(f"{coin['symbol']}-USD.csv")
  listHashes.append(f"{res['Hash']}_{coin['symbol']}-USD")


### CONNECTING TO BLOCKCHAIN

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:9545",request_kwargs={'timeout':60}))
web3.isConnected()

# READING THE CONTRACT
with open('contracts/jsons/MainContract.json') as json_file:  
    data = json.load(json_file)


print("Are we Connected to the local blockchain node?: ",web3.isConnected())

# PREPARE THE CONTRACT FOR DEPLOYMENT
web3.eth.defaultAccount=web3.eth.accounts[0]
myContract_instance = web3.eth.contract(abi=data['abi'], bytecode=data['bytecode'])
tx_hash=myContract_instance.constructor().transact()

# CONFIRMATION OF CONTRACT DEPLOYMENT
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)


# CREATE A HANDLE TO THE CONTRACT INSTANCE WITH THE NEWLY-DEPLOYED ADDRESS
myContractaddress = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=data['abi'],
)
print('Contract deployed at address: ' , myContractaddress.address)

# DEFINE ACTORS
offer_account = web3.eth.accounts[0]
solver_1 = web3.eth.accounts[1]
solver_2 = web3.eth.accounts[2]
solver_3 = web3.eth.accounts[3]

# CHECK INITAL BALANCES
print('Initial balance of the Primary Challenge Offerer account is: ', web3.fromWei(web3.eth.getBalance(offer_account),'ether'))
print('Initial balance of the Solver_1 account is: ', web3.fromWei(web3.eth.getBalance(solver_1),'ether'))
print('Initial balance of the Solver_2 account is: ', web3.fromWei(web3.eth.getBalance(solver_2),'ether'))
print('Initial balance of the Solver_3 account is: ', web3.fromWei(web3.eth.getBalance(solver_3),'ether'))
print('Initial balance of the COntract  account is: ', web3.fromWei(web3.eth.getBalance(myContractaddress.address),'ether'))

# FUNDING CONTRACT
fund_tx = web3.eth.sendTransaction({
    'from': offer_account,
    'to': myContractaddress.address,
    'value': web3.toWei(10, "ether")
})
print('After funding, balance of the COntract  account is: ', web3.fromWei(web3.eth.getBalance(myContractaddress.address), 'ether'))
print('After funding, balance of the Primary Challenge Offerer account is: ', web3.fromWei(web3.eth.getBalance(offer_account),'ether'))

#Storing the list of ipfs hash to blockchain by the owner of the contract
# 50% => 0.5 * 10000 => 5000
# this function is called by offer account to perform the initialization
init_tx_hash = myContractaddress.functions.initialization(50000,listHashes,1, 3).transact()
init_tx_receipt = web3.eth.wait_for_transaction_receipt(init_tx_hash)

# this function is called by any other solver
web3.eth.defaultAccount = solver_1
getList = myContractaddress.functions.get_train_data().call()
print(getList)

# Let's suppose the user wants to train the model for LTC-USD
# use the list to get the hash value for LTC-USD
RATIO_TO_PREDICT = 'LTC-USD'
FUTURE_PERIOD_PREDICT = myContractaddress.functions.future_predict_peroid().call()
SEQ_LEN = myContractaddress.functions.sequence_len().call()
EPOCHS = 50
BATCH_SIZE = 64
# getfile = ipfsClient.cat(f"{myHash}")
# getfile = getfile.decode('utf-8')
# print(getfile)

def classify(current, future):
  if float(future) > float(current):
    return 1
  else:
    return 0

def preprocess_df(df):
  df = df.drop('future',1)

  for col in df.columns:
    if col != 'target':
      df[col] = df[col].pct_change() # normalizing values
      df.dropna(inplace=True)
      df[col] = preprocessing.scale(df[col].values)
  df.dropna(inplace=True)
  
  sequential_data = []
  prev_days = deque(maxlen=SEQ_LEN)
  
  for i in df.values:
    prev_days.append([n for n in i[:-1]])
    if len(prev_days) == SEQ_LEN:
      sequential_data.append([np.array(prev_days), i[-1]])
    
  random.shuffle(sequential_data)

  # buys = []
  # sells = []

  # for seq, target in sequential_data:
  #   if target == 0:
  #       sells.append([seq,target])
  #   elif target == 1:
  #       buys.append([seq,target])

  # random.shuffle(buys)
  # random.shuffle(sells)

  # lower = min(len(buys), len(sells))
  
  # buys = buys[:lower]
  # sells = sells[:lower]

  #sequential_data = buys+sells
  
  random.shuffle(sequential_data)    

  X = []
  y = []

  for seq,target in sequential_data:
    X.append(seq)
    y.append(target)

  return np.array(X), np.array(y)


main_df = pd.DataFrame()

for data in getList:
  x = data.split('_')
  myHash = x[0]
  dataset = f"{x[1]}.csv"
  df = pd.read_csv(dataset,names=["time",f"{x[1]}_close",f"{x[1]}_volume","market_cap"])
  df.set_index("time", inplace=True)
  df = df[[f"{x[1]}_close",f"{x[1]}_volume"]]

  if len(main_df) == 0:
      main_df = df
  else:
      main_df = main_df.join(df)

main_df['future'] = main_df[f"{RATIO_TO_PREDICT}_close"].shift(-FUTURE_PERIOD_PREDICT)
main_df['target'] = list(map(classify, main_df[f"{RATIO_TO_PREDICT}_close"], main_df['future']))

# Considering last 20 percent data for testing
times = sorted(main_df.index.values)
last_5pct = times[-int(0.2*len(times))] #unix time stamp value of last 5%
print(last_5pct)

validation_main_df = main_df[(main_df.index >= last_5pct)] # testing data set
main_df = main_df[(main_df.index < last_5pct)]


train_x, train_y = preprocess_df(main_df)
validation_x,validation_y = preprocess_df(validation_main_df)

# print(f"traindata: {len(train_x)}  validation: {len(validation_x)}")
# unique, counts = np.unique(train_y, return_counts=True)
# print(unique, counts)
# for i in unique:
#   index = np.where(train_y == i)[0][0]
#   if i == 0:
#     print('tain_y dont buys:', counts[index])
#   elif i == 1:
#     print('train_y buys:', counts[index])

# unique, counts = np.unique(validation_y, return_counts=True)
# print(unique, counts)
# for i in unique:
#   index = np.where(validation_y == i)[0][0]
#   if i == 0:
#     print('validation_y dont buys:', counts[index])
#   elif i == 1:
#     print('validation_y buys:', counts[index])

# print(f"dont buys: {train_y.count(0)} buys: {train_y.count(1)}")
# print(f"Validation dont buys: {validation_y.count(0)} Validation buys: {validation_y.count(1)}")
accuracies = []

def model_setup(dense_layer, layer_size, lstm_layer, activation_fun, loss_fun):

  NAME = "{}-lstm-{}-nodes-{}-dense-{}".format(lstm_layer, layer_size, dense_layer, int(time.time()))
  tensorboard = tf.keras.callbacks.TensorBoard(log_dir='logs/{}'.format(NAME))
  model = Sequential()
  
  for i in range(lstm_layer-1):
    model.add(LSTM(layer_size, input_shape=(train_x.shape[1:]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
  
  model.add(LSTM(128, input_shape=(train_x.shape[1:])))
  model.add(Dropout(0.2))
  model.add(BatchNormalization())

  for l in range(dense_layer):
    model.add(Dense(32))
    model.add(tf.keras.layers.Activation(activation_fun))
  
  model.add(Dense(2, activation="softmax"))

  opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

  model.compile(loss=loss_fun,
                optimizer=opt,
                metrics='accuracy')

  tensorboard = tf.keras.callbacks.TensorBoard(log_dir=f"logs/{NAME}")

  filepath = "RNN_Final-{epoch:02d}-{val_accuracy:.3f}" #unique file name that will include the epoch and the validation acc for that epoch
  checkpoint = ModelCheckpoint("models/{}.model".format(filepath, monitor='val_accuracy',verbose=1, save_best_only=True, mode='max')) #saves only the best ones
  history = model.fit(train_x, 
                    train_y, 
                    batch_size=BATCH_SIZE, 
                    epochs=EPOCHS, 
                    validation_data=(validation_x, validation_y),
                    callbacks=[tensorboard, checkpoint])
  x = history.history['accuracy']
  val = '%.5f'%(max(x))
  x = float(val) * 100000.0
  accuracies.append(int(x))

# SUBMITTING SOLUTION TO THE BLOCKCHAIN BY SOLVER 1
web3.eth.defaultAccount = solver_1
sol_1_hash = myContractaddress.functions.submit_model(solver_1,1,128,3,'relu', 'sparse_categorical_crossentropy').transact()
sol_1_receipt = web3.eth.wait_for_transaction_receipt(sol_1_hash)

# SUBMITTING SOLUTION TO THE BLOCKCHAIN BY SOLVER 2
web3.eth.defaultAccount = solver_2
sol_2_hash = myContractaddress.functions.submit_model(solver_2,2,64,4,'sigmoid', 'sparse_categorical_crossentropy').transact()
sol_1_receipt = web3.eth.wait_for_transaction_receipt(sol_1_hash)


# GET ALL SUBMISSIONS
web3.eth.defaultAccount = offer_account
submissions = myContractaddress.functions.get_all_submissions().call()
print(submissions)

# OWNER WILL EVALUATE THE MODEL ON HIS OWN
for sol in submissions:
  model_setup(sol[1],sol[2],sol[3],sol[4],sol[5])

# NOW OWNER WILL EVALUATE THE RESULTS
web3.eth.defaultAccount = offer_account
for i in accuracies:
   set_model_hash = myContractaddress.functions.set_evaluation_metrics(i, accuracies.index(i)).transact()
   set_model_receipt = web3.eth.wait_for_transaction_receipt(set_model_hash)

# FOR CLOSING THE PROCESS

final_hash = myContractaddress.functions.finalize_contract().transact()
final_receipt = web3.eth.wait_for_transaction_receipt(final_hash)











 











