import os
import json
import time
import logging
from dotenv import load_dotenv
from web3 import Web3
from goat_sdk.client import GoatClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TrendForecaster")

load_dotenv()

class TrendForecaster:
    """
    RWA Trend Forecasting Engine with Goat SDK integration
    """
    def __init__(self):
        # --- Blockchain Setup ---
        self.rpc_url = os.getenv("XDC_RPC_URL")
        if not self.rpc_url:
            raise ValueError("XDC_RPC_URL environment variable not set")
            
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to XDC network")

        # --- Goat SDK Setup ---
        self.goat = GoatClient(
            api_key=os.getenv("GOAT_API_KEY"),
            rpc_url=self.rpc_url
        )

        # --- Contract Configuration ---
        self.rwa_address = os.getenv("RWA_CONTRACT_ADDRESS")
        if not self.rwa_address:
            raise ValueError("RWA_CONTRACT_ADDRESS environment variable not set")

        # Load contract ABI
        abi_path = os.getenv("RWA_CONTRACT_ABI_PATH", "./RWAabi.json")
        with open(abi_path) as f:
            self.rwa_abi = json.load(f)["abi"]

        # --- Trading Parameters ---
        self.short_window = int(os.getenv("SHORT_MA_WINDOW", 3))
        self.long_window = int(os.getenv("LONG_MA_WINDOW", 5))
        self.poll_interval = int(os.getenv("POLL_INTERVAL", 60))  # seconds

    def start(self):
        """Main monitoring loop"""
        logger.info("Starting Trend Forecaster...")
        logger.info(f"Connected to XDC Network: {self.w3.is_connected()}")
        logger.info(f"Monitoring RWA Contract: {self.rwa_address}")

        while True:
            try:
                # Get all asset IDs from contract
                asset_ids = self._get_asset_ids()
                
                for asset_id in asset_ids:
                    signal = self.analyze_asset(asset_id)
                    logger.info(f"Asset {asset_id} Signal: {signal}")
                    # Implement your trading logic here

                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                logger.info("Shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(5)

    def analyze_asset(self, asset_id: int) -> str:
        """Full analysis pipeline for an asset"""
        prices = self._fetch_historical_prices(asset_id)
        return self._calculate_signal(prices)

    def _get_asset_ids(self) -> list[int]:
        """Get list of asset IDs from contract"""
        contract = self.w3.eth.contract(
            address=self.rwa_address,
            abi=self.rwa_abi
        )
        return contract.functions.getAssetIds().call()

    def _fetch_historical_prices(self, asset_id: int) -> list[float]:
        """Fetch prices through Goat Oracle"""
        try:
            data = self.goat.oracle.get_historical_prices(
                contract_address=self.rwa_address,
                asset_id=asset_id,
                hours=self.long_window * 24  # Assuming daily prices
            )
            return [float(entry['price']) for entry in data['prices']]
        except Exception as e:
            logger.warning(f"Price fetch failed: {e}. Using fallback data")
            return [100.0, 101.5, 102.0, 101.0, 103.5]

    def _calculate_signal(self, prices: list[float]) -> str:
        """Calculate trading signal with moving averages"""
        if len(prices) < self.long_window:
            logger.warning("Insufficient data for reliable signal")
            return "HOLD"

        short_ma = sum(prices[-self.short_window:]) / self.short_window
        long_ma = sum(prices[-self.long_window:]) / self.long_window

        if short_ma > long_ma * 1.015:
            return "BUY"
        elif short_ma < long_ma * 0.985:
            return "SELL"
        return "HOLD"

if __name__ == "__main__":
    try:
        forecaster = TrendForecaster()
        forecaster.start()
    except Exception as e:
        logger.error(f"Failed to initialize: {str(e)}")