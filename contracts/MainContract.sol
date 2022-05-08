// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <8.10.0;
pragma experimental ABIEncoderV2;


contract MainContract {

  string [] ipfsHash;
  address owner;   //organizer
  uint public best_submission_index;
  uint public best_submission_accuracy = 0;
  uint public best_model_accuracy;
  uint public model_accuracy_criteria;
  bool public use_train_data = false;
  // bool public use_test_data = false;
  uint public sequence_len;
  uint public future_predict_peroid;
  string public test_data_hash;

  // Deadline for submitting solutions in terms of block size
  uint public submission_stage_block_size = 241920; //6 week time frame
  // Deadline for revealing the testing dataset
  // uint public reveal_test_data_groups_block_size = 17280; // 3 days time frame
  // Deadline for evaluating the submissions
  uint public evaluation_stage_block_size = 40320; // 7 day time frame
  uint public init1_block_height;
  // uint public init3_block_height;
  uint public init_level = 0;
  int constant int_precision = 10000;

  struct Submission{
    address submitter;
    uint dense_layer;
    uint layer_size;
    uint lstm_layers;
    string activation_function;
    string loss_function;
    uint submission_time;
  }

  Submission[] submission_queue;
  bool public contract_terminated = false;

  constructor() {
    owner = msg.sender;
  }

  modifier onlyOwner {
    require(owner == msg.sender, 'MainContract: Only owner can call this function');
    _ ;
  }
  
  function initialization(uint accuracy_criteria, 
                          string[] memory hashes, 
                          uint _sequence_len, 
                          uint _future_predict_peroid) onlyOwner external{

    //Make sure that the contract is not terminated
    require(contract_terminated == false, 'MainContract: This contract has been terminated');

    //Make sure that this is called in order
    require(init_level == 0, 'MainContract: Incorrect order of calling the function');
    require(hashes.length > 0, 'MainContract: IPFS hashes are missing');

    ipfsHash = hashes;
    use_train_data = true;
    init1_block_height = block.number;
    init_level = 1;

    require(accuracy_criteria > 0, 'MainContract: Accruacy must be more than 0');
    //100% => 10,000 => 1 * 10,000
    model_accuracy_criteria = accuracy_criteria;
    
    sequence_len = _sequence_len;
    future_predict_peroid = _future_predict_peroid;

  }

  function get_train_data() public returns(string[] memory){
    require(contract_terminated == false,'MainContract: This contract has been terminated');
    require(init_level == 1, 'MainContract: Contract has not been initialized yet');
    //Make sure the initialization function is called first
    //require(block.number > init1_block_height, 'MainContract: Train data is not set yet');
    use_train_data = true;
    return  ipfsHash;
  }

  function get_submission_queue_length() public view returns(uint) {
    return submission_queue.length;
  }
  
  function submit_model(address _submitter,
                        uint _dense_layer,
                        uint _layer_size,
                        uint _lstm_layers,
                        string memory _activation_function,
                        string memory _loss_function) public{

    //Make sure that the contract is not terminated
    require(contract_terminated == false, 'MainContract: This contract has been terminated');
    require(init_level == 1, 'MainContract: Contract has not been initialized yet');
    //require(block.number < init1_block_height + submission_stage_block_size, 'MainContract: Submission stage is over');
    
    submission_queue.push(Submission(
                          _submitter,
                          _dense_layer,
                          _layer_size,
                          _lstm_layers,
                          _activation_function,
                          _loss_function,
                          block.timestamp
                        ));
  }

  function get_submission_id(address _submitter,
                        uint _dense_layer,
                        uint _layer_size,
                        uint _lstm_layers,
                        string memory _activation_function,
                        string memory _loss_function) public view returns(int){
    
    uint queue_length = submission_queue.length;

    for(uint i = 0 ; i < queue_length ; i++){
        Submission memory model =  submission_queue[i];

        if(model.submitter != _submitter){
          continue;
        }
        if(model.dense_layer != _dense_layer){
          continue;
        }
        if(model.layer_size != _layer_size){
          continue;
        }
        if(model.lstm_layers != _lstm_layers){
          continue;
        }
        if(!compareStrings(model.activation_function, _activation_function)){
          continue;
        }
        if(!compareStrings(model.loss_function, _loss_function)){
          continue;
        }

        return int(i);
    }
    require(false,'MainContract: Model had not been submitted');
    return(-1);
  }

  // function reveal_test_data(string memory _hash) external onlyOwner{
  //   require(contract_terminated == false,'MainContract: This contract has been terminated');
  //   require(init_level == 1, 'MainContract: Contract has not been initialized yet');
  //   //Make sure that the test data is revealed after the submission stage
  //   //assert(block.number < init1_block_height + submission_stage_block_size + reveal_test_data_groups_block_size);
  //   test_data_hash = _hash;
  //   use_test_data = true;
  // }

  // function get_test_data() public view returns(string memory){
  //   require(contract_terminated == false,'MainContract: This contract has been terminated');
  //   require(init_level == 1, 'MainContract: Contract has not been initialized yet');
  //   require(use_test_data == true, 'MainContract: Test data is not revealed yet');

  //   return test_data_hash;
  // }
  function get_all_submissions() onlyOwner view external returns(Submission [] memory){
      return submission_queue;
  }

  function set_evaluation_metrics(uint submission_accuracy,uint submission_index) external onlyOwner{
   //assert(block.number >= init1_block_height + submission_stage_block_size );

   //Keep track of the most acurate model
   if(submission_accuracy > best_submission_accuracy){
      best_submission_index = submission_index;
      best_submission_accuracy = submission_accuracy;
   }

   if(submission_accuracy == best_submission_accuracy){
     if (submission_index < best_submission_index) {
        best_submission_index = submission_index;
        best_submission_accuracy = submission_accuracy;
      }
   }

  }

  function cancel_contract() external onlyOwner{
    require(contract_terminated == false, 'MainContract: This contract has been terminated');
    require(init_level < 1, 'MainContract: Contract can only be cancelled if initialization has failed');
    // Refund remaining balance to organizer
    payable(owner).transfer(address(this).balance);
    // Terminate contract
    contract_terminated = true;

  }

  function finalize_contract() external onlyOwner{
    require(contract_terminated == false, 'MainContract: This contract has been terminated');
    require(init_level == 1, 'MainContract: Contract has not been initialized yet');
    //Make sure contract is finalized after the evaluation stage
    //assert(block.number >= init1_block_height + submission_stage_block_size + evaluation_stage_block_size);
    Submission memory best_submission = submission_queue[best_submission_index];
    // If best submission passes criteria, payout to the submitter
    if (best_submission_accuracy >= model_accuracy_criteria) {
      payable(best_submission.submitter).transfer(address(this).balance);
    // If the best submission fails the criteria, refund the balance back to the organizer
    } 
    else {
      payable(owner).transfer(address(this).balance);
    }

    contract_terminated = true;
  } 

  function compareStrings(string memory a, string memory b) public pure returns (bool) {
    return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
  }

  receive() external payable {
  }

  fallback() external{
  }
}
