 const HDWalletProvider = require('@truffle/hdwallet-provider');
 const privateKey = "**********************************************************";
 const endpointUrl = "https://kovan.infura.io/v3/***************************";
 const mnemonicDev = "false craft rookie food village exhaust purity great farm rate draft drip";
module.exports = {

  networks: {
    development: {
     host: "127.0.0.1",     // Localhost (default: none)
     port: 8545,            // Standard Ethereum port (default: none)
     network_id: "*",       // Any network (default: none)
     gas: 999999999,           // Gas sent with each transaction (default: ~6700000) 0x3B9AC9FF
    //  gasPrice: 20000000000
    },
    // ganache: {
    //   provider: () => new HDWalletProvider(mnemonicDev, `HTTP://127.0.0.1:8545`),
    //   host: "127.0.0.1",     // Localhost (default: none)
    //   port: 8545,
    //   network_id: "*" ,      // Any network (default: none)
    //   gas: 999999999,
    //  },
    // Another network with more advanced options...
    // advanced: {
    // port: 8777,             // Custom port
    // network_id: 1342,       // Custom network
    // gas: 8500000,           // Gas sent with each transaction (default: ~6700000)
    // gasPrice: 20000000000,  // 20 gwei (in wei) (default: 100 gwei)
    // from: <address>,        // Account to send txs from (default: accounts[0])
    // websocket: true        // Enable EventEmitter interface for web3 (default: false)
    // },
    // Useful for deploying to a public network.
    // NB: It's important to wrap the provider as a function.
    // ropsten: {
    // provider: () => new HDWalletProvider(mnemonic, `https://ropsten.infura.io/v3/YOUR-PROJECT-ID`),
    // network_id: 3,       // Ropsten's id
    // gas: 5500000,        // Ropsten has a lower block limit than mainnet
    // confirmations: 2,    // # of confs to wait between deployments. (default: 0)
    // timeoutBlocks: 200,  // # of blocks before a deployment times out  (minimum/default: 50)
    // skipDryRun: true     // Skip dry run before migrations? (default: false for public nets )
    // },
    // kovan: {
    //   provider: function() {
    //     return new HDWalletProvider(privateKey,endpointUrl)
    //   },
    //   gas: 6721975,
    //   gasPrice: 120000000000,
    //   network_id: 42,
    //   networkCheckTimeout: 1000000000,
    //   timeoutBlocks: 3000,
    //   skipDryRun: true,
    //   //confirmations: 2,
    // }
    // Useful for private networks
    // private: {
    // provider: () => new HDWalletProvider(mnemonic, `https://network.io`),
    // network_id: 2111,   // This network is yours, in the cloud.
    // production: true    // Treats this network as if it was a public net. (default: false)
    // }
  },

  // Set default mocha options here, use special reporters etc.
  mocha: {
    enableTimeouts: false,
    timeout: 100000000
  },

  // Configure your compilers
  compilers: {
    solc: {
      version: "0.5.17",    // Fetch exact version from solc-bin (default: truffle's version)
      // docker: true,        // Use "0.5.1" you've installed locally with docker (default: false)
      settings: {          // See the solidity docs for advice about optimization and evmVersion
       optimizer: {
         enabled: true,
         runs: 200
       },
      //  evmVersion: "byzantium"
      }
    }
  },

  // Truffle DB is currently disabled by default; to enable it, change enabled: false to enabled: true
  //
  // Note: if you migrated your contracts prior to enabling this field in your Truffle project and want
  // those previously migrated contracts available in the .db directory, you will need to run the following:
  // $ truffle migrate --reset --compile-all

  db: {
    enabled: false
  }
};
