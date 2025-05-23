const { ethers } = require("hardhat");

async function main() {
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545"); // Localhost RPC
  const signer = await provider.getSigner();

  const rwaAssetAddress = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512";
  const rwaAssetAbi = [
    // Add only the functions you need here
    "function createAsset(string memory metadata, uint256 value) public returns (uint256)",
    "function getAsset(uint256 assetId) public view returns (string memory, uint256, address)"
  ];

  const rwaAsset = new ethers.Contract(rwaAssetAddress, rwaAssetAbi, signer);

  const tx = await rwaAsset.createAsset("Gold-backed token", 1000);
  const receipt = await tx.wait();

  console.log("Asset Created, TX Hash:", receipt.hash);
}

main().catch(console.error);
