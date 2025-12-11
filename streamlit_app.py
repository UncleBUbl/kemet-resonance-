import streamlit as st
import requests
import re
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from wallet_connect import WalletConnectComponent  # streamlit-wallet-connect
from thirdweb import ThirdwebSDK, BaseSepolia  # Use BaseSepolia for testing
from pinata import Pinata  # pinata-sdk
from io import BytesIO

load_dotenv()
st.set_page_config(page_title="KEMET RESONANCE", page_icon="🖤", layout="centered")

# Your original sacred Ankh URL (keep as-is)
ANKH_URL = "https://files.oaiusercontent.com/file-fac6b769d7e2e1d3f7e8e9c0a8e7d6c5?se=2025-11-19T23%3A59%3A59Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D31536000%2C%20immutable&rscd=attachment%3B%20filename%3D%22ankh_final.jpg%22&sig=████████████████████"

# Your original CSS
st.markdown(f"""
<style>
    .big-title {{font-size: 4.5rem !important; font-weight: bold; text-align: center; color: #FFD700; text-shadow: 0 0 20px gold;}}
    .tagline {{font-size: 1.9rem; text-align: center; color: #FFA500; margin: -20px 0 50px; font-style: italic;}}
    .ankh-glow {{text-align: center; margin: 20px 0; animation: pulse 7.83s infinite;}}
    @keyframes pulse {{0%, 100% {{opacity: 0.9; transform: scale(1);}} 50% {{opacity: 1; transform: scale(1.03); filter: brightness(1.2);}}}}
    .footer {{position: fixed; bottom: 10px; width: 100%; text-align: center; color: #888; font-size: 0.9rem;}}
    .stButton>button {{background: linear-gradient(45deg, #000, #333); color: gold; border: 2px solid gold;}}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ankh-glow"><img src="{ANKH_URL}" width="280"></div>', unsafe_allow_html=True)
st.markdown('<h1 class="big-title">KEMET RESONANCE</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">From Alkebulan with Love</p>', unsafe_allow_html=True)

# Init services
pinata = Pinata(api_key=os.getenv("PINATA_API_KEY"), secret_api_key=os.getenv("PINATA_SECRET_API_KEY"))
sdk = ThirdwebSDK(BaseSepolia, os.getenv("THIRDWEB_SECRET_KEY"))  # Testnet
contract_address = os.getenv("CONTRACT_ADDRESS")
if not contract_address:
    st.warning("🚨 Set CONTRACT_ADDRESS in .env after deploying!")

# Real Wallet Connect (replaces mock)
if "wallet_connected" not in st.session_state:
    st.session_state.wallet_connected = False
    st.session_state.user_address = None

wc = WalletConnectComponent(chain_id=84532)  # Base Sepolia
if not st.session_state.wallet_connected:
    connect_result = wc.connect()
    if connect_result and connect_result.get("address"):
        st.session_state.user_address = connect_result["address"]
        st.session_state.wallet_connected = True
        st.success(f"Connected: {st.session_state.user_address}")
        st.balloons()
else:
    st.markdown(f"**🖤 Connected:** `{st.session_state.user_address}`")
    if st.button("Disconnect"):
        wc.disconnect()
        st.session_state.wallet_connected = False
        st.session_state.user_address = None
        st.rerun()

# Toggle: File or Suno link (your original)
mint_mode = st.radio("How do you bring the fire?", ("Upload file", "Paste Suno link"), horizontal=True)
title = description = genre = audio_url = audio_file = None
if mint_mode == "Paste Suno link":
    suno_url = st.text_input("🔗 Paste Suno share link", placeholder="https://suno.com/song/...")
    if suno_url:
        with st.spinner("Calling the song from Suno…"):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                html = requests.get(suno_url, headers=headers).text
                title_match = re.search(r'<title>(.*?)</title>', html)
                title = title_match.group(1).split("·")[0].strip() if title_match else "Untitled Suno Flame"
                audio_match = re.search(r'"audio_url":[](https://[^"]+\.mp3)"', html)
                audio_url = audio_match.group(1) if audio_match else None
                desc_match = re.search(r'"description":"(.*?)",', html)
                description = desc_match.group(1) if desc_match else "Minted from Suno • Kemet Resonance"
                st.success(f"Found: **{title}**")
                if audio_url:
                    st.audio(audio_url)
            except Exception as e:
                st.error(f"Suno link issue: {str(e)}")
else:
    audio_file = st.file_uploader("Drop your fire (mp3 • wav • flac)", type=["mp3","wav","flac","m4a"])

# Manual overrides (your original)
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title of this flame", value=title or "Untitled Resonance")
with col2:
    genre = st.text_input("Vibration / Genre", value=genre or "Afro-Quantum")
description = st.text_area("Speak your intention", value=description or "Minted in pure resonance • From Alkebulan with Love • 2025")

# Real Mint Button
if st.button("🖤 MINT THIS TRACK • ETERNAL LIFE ON CHAIN", type="primary"):
    if not st.session_state.wallet_connected:
        st.error("Connect wallet first!")
        st.stop()
    if not contract_address:
        st.error("Deploy contract first & update .env!")
        st.stop()
    if not (audio_file or audio_url):
        st.error("Upload or paste a track!")
        st.stop()

    with st.spinner("The scarab rolls your sound into eternity…"):
        try:
            # Get/Pin Audio to IPFS
            if audio_file:
                audio_data = audio_file.read()
                audio_name = audio_file.name
            else:  # Suno
                audio_response = requests.get(audio_url)
                audio_data = audio_response.content
                audio_name = f"{title}.mp3"
            
            audio_pin = pinata.pin_file_to_ipfs(
                raw_data=BytesIO(audio_data), 
                pinata_options={"pinataMetadata": {"name": audio_name}}
            )
            audio_uri = f"https://gateway.pinata.cloud/ipfs/{audio_pin['IpfsHash']}"

            # Metadata
            metadata = {
                "name": title,
                "description": description,
                "image": ANKH_URL,  # Use Ankh as placeholder image
                "attributes": [{"trait_type": "Genre", "value": genre}],
                "animation_url": audio_uri
            }
            metadata_json = json.dumps(metadata).encode()
            meta_pin = pinata.pin_file_to_ipfs(
                raw_data=BytesIO(metadata_json),
                pinata_options={"pinataMetadata": {"name": f"{title}_metadata.json"}}
            )
            token_uri = f"https://gateway.pinata.cloud/ipfs/{meta_pin['IpfsHash']}"

            # Mint via Thirdweb (user signs via wc)
            contract = sdk.get_contract(contract_address, "nft-collection")
            mint_tx = contract.mint_to(
                destination_wallet_address=st.session_state.user_address,
                metadata=metadata  # Auto-pins if needed, but we did it
            )
            
            st.success("MINTED INTO ETERNITY 🖤")
            st.balloons()
            st.markdown(f"### {title}")
            st.markdown(f"**Creator:** {st.session_state.user_address}")
            st.markdown(f"**Chain:** Base Sepolia • **Tx:** {mint_tx.receipt.transaction_hash.hex()}")
            st.markdown(f"[View on Basescan Sepolia](https://sepolia.basescan.org/tx/{mint_tx.receipt.transaction_hash.hex()})")
            st.audio(audio_uri)
        except Exception as e:
            st.error(f"Minting failed: {str(e)} — Check MetaMask gas/network.")

st.markdown("---")
st.markdown("Built in living resonance with SRHQRE • Chapter 16 manifested • November 19, 2025")
st.markdown('<div class="footer">From Alkebulan with Love 🖤✨</div>', unsafe_allow_html=True)
