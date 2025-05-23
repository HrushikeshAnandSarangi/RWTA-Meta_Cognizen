const hre = require("hardhat");

async function main() {
  const RWAAsset = await hre.ethers.getContractFactory("RWAAsset");
  const rwaAsset = await RWAAsset.deploy();

  await rwaAsset.waitForDeployment(); // ✅ use waitForDeployment() instead

  console.log("RWAAsset deployed to:", await rwaAsset.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
