const contractAddress = '0x...'; // Replace with your deployed contract address
const contractAbi = /* Replace with your contract ABI */;

async function init() {
  if (window.ethereum) {
    window.web3 = new Web3(window.ethereum);
    try {
      await window.ethereum.enable();
      const accounts = await window.web3.eth.getAccounts();
      document.getElementById('userAddress').innerText = accounts[0];
      window.contract = new window.web3.eth.Contract(contractAbi, contractAddress);
    } catch (error) {
      console.error("User denied account access or error:", error);
    }
  } else {
    console.error("No Ethereum provider detected");
  }
}

async function registerVoter() {
  await window.contract.methods.registerVoter(window.web3.eth.defaultAccount).send({ from: window.web3.eth.defaultAccount });
}

async function registerCandidate() {
  await window.contract.methods.registerCandidate(window.web3.eth.defaultAccount).send({ from: window.web3.eth.defaultAccount });
}

async function vote() {
  const candidateAddress = '0x...'; // Replace with the candidate's Ethereum address
  await window.contract.methods.vote(candidateAddress).send({ from: window.web3.eth.defaultAccount });
}

async function getVoteCount() {
  const candidateAddress = '0x...'; // Replace with the candidate's Ethereum address
  const voteCount = await window.contract.methods.getVoteCount(candidateAddress).call();
  console.log(`Vote count for candidate: ${voteCount}`);
}

window.addEventListener('load', init);

function redirectToHome() {
  window.location.href = 'index.html';
}