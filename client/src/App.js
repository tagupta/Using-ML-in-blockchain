import React, { Component } from "react";
import SimpleStorageContract from "./jsons/SimpleStorage.json";
import getWeb3 from "./getWeb3";
import "./App.css";
import ipfs from './ipfs';

class App extends Component {
  state = { 
    storageValue: 0, 
    web3: null, 
    accounts: null, 
    contract: null,
    buffer: null,
    ipfsHash: '', 
  };

  componentDidMount = async () => {
    try {
      const web3 = await getWeb3();
      const accounts = await web3.eth.getAccounts();
      const networkId = await web3.eth.net.getId();
      console.log("networkId: "+ networkId);
      const deployedNetwork = SimpleStorageContract.networks[networkId];
      const instance = new web3.eth.Contract(
      SimpleStorageContract.abi, deployedNetwork && deployedNetwork.address);

      this.setState({ web3, accounts: accounts[0], contract: instance },this.runExample); 
    } catch (error) {
      alert(
        `Failed to load web3, accounts, or contract. Check console for details.`,
      );
      console.error(error);
    }
  };

  runExample = async () => {
    const { accounts, contract } = this.state;
    // Get the value from the contract to prove it worked.
    const response = await contract.methods.get().call({from: accounts});
    console.log("ipfsHash: "+ response);
    this.setState({ ipfsHash: response });
  };

   onSubmit = async (event) => {
    const {buffer, accounts, contract} = this.state;
    event.preventDefault();
    console.log('OnSubmit.....');
    const result = await ipfs.add(buffer);
    if(result){
      console.log("IPFS Hash: " + result.path);
      this.setState({ipfsHash : result.path});
      await contract.methods.set(result.path).send({from: accounts}, (error, txHash) => {
        if(error){
          console.error(error);
        }
        else{
          console.log('Successfully written to blockchain');
        }
      });

    }
    else{
      console.error('Error while storing file');
    }
  }

  captureFile = async(event)=>{
    event.preventDefault();
    const file = event.target.files[0];
    const reader = new window.FileReader();
    reader.readAsArrayBuffer(file);
    reader.onloadend = () => {
      this.setState({buffer: Buffer(reader.result)});
      console.log(this.state.buffer);
    }
  }

  render() {
    const {web3,ipfsHash} = this.state;
    if (!web3) {
      return <div>Loading Web3, accounts, and contract...</div>;
    }
    return (
      <div className="App">
        <h1>IPFS File Upload DApp</h1>
        <p>This dApp is built to store healthcare data to blockchain using IPFS. 
           <br></br>
           Validity of data is checked using explicit ML model
        </p> 
         
         <h4>Your file</h4>
         <span>This file is stored on IPFS and the Ethereum Blockchain </span>
         <br></br>
         <img src={`https://ipfs.io/ipfs/${ipfsHash}`} alt=""/>
         <h4>Upload File</h4>
         <form onSubmit={this.onSubmit}>
          <input type="file" onChange={this.captureFile}/>
          <input type="submit"/>
         </form>
      </div>
    );
  }
}

export default App;
