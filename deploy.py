import os
from thirdweb import ThirdwebSDK, BaseSepolia
from dotenv import load_dotenv

load_dotenv()
sdk = ThirdwebSDK(BaseSepolia, os.getenv("THIRDWEB_SECRET_KEY"))

contract = sdk.deployer.deploy_nft_collection({
    "name": "Kemet Resonance",
    "symbol": "KEMET",
    "primary_sale_recipient": "0x8b17377452f1d8069af59C96Db96113563CFC054",  # Replace with your address
    "platform_fee_basis_points": 500,  # 5%
    "platform_fee_recipient": "0x8b17377452f1d8069af59C96Db96113563CFC054"
})

print(f"Deployed at: {contract.address}")
# Copy this address to .env as CONTRACT_ADDRESS
