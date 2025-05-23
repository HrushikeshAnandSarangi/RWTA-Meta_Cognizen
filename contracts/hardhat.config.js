require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: "0.8.28",
  networks: {
    xdcTestnet: {
      url: "https://erpc.apothem.network", // XDC Apothem Testnet
      accounts: [process.env.PRIVATE_KEY] // Use .env to store private key securely
    }
  }
};
