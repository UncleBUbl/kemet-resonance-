import streamlit as st
import requests
import re
import json
import os
from dotenv import load_dotenv
from pinata import Pinata
from web3 import Web3

load_dotenv()

# ================== YOUR THEME ==================
st.set_page_config(page_title="KEMET RESONANCE", page_icon="🖤", layout="centered")

ANKH_URL = "https://files.oaiusercontent.com/file-fac6b769d7e2e1d3f7e8e9c0a8e7d6c5?se=2025-11-19T23%3A59%3A59Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D31536000%2C%20immutable&rscd=attachment%3B%20filename%3D%22ankh_final.jpg%22&sig=████████████████████"

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

# ================== WALLET CONNECT (Enhanced with Persistent Manual Input) ==================
if "address" not in st.session_state:
    st.markdown("### Connect Your Wallet")
    if st.button("🦊 Connect MetaMask"):
        st.components.v1.html("""
        <script>
        async function connect() {
            let ethereum = window.ethereum || (window.parent ? window.parent.ethereum : null);
            if (ethereum) {
                try {
                    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                    alert('Connected! Address: ' + accounts[0] + '\\n\\nCopy this and paste it into the manual input below. Then refresh if needed.');
                    console.log('Wallet connected: ' + accounts[0]);
                } catch (error) {
                    alert('Connection failed: ' + error.message + '. Check MetaMask network (Base Sepolia).');
                }
            } else {
                alert('MetaMask not detected! Install from metamask.io.');
            }
        }
        </script>
        <button onclick="connect()" style="padding:15px; font-size:20px; background:gold; color:black; border:none; border-radius:10px;">
        Connect Wallet Now
        </button>
        """, height=150)
    
    # Always-visible manual input for persistence
    st.markdown("**Or paste wallet address manually:**")
    manual_addr = st.text_input("0x...", placeholder="Enter your address (0x...)", key="manual_wallet")
    if manual_addr and manual_addr.startswith("0x"):
        st.session_state.address = manual_addr.lower()
        st.success(f"🖤 Connected: `{st.session_state.address}`")
        st.rerun()
else:
    st.success(f"🖤 Connected: `{st.session_state.address}`")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Disconnect"):
            st.session_state.clear()
            st.rerun()

# ================== AUDIO INPUT ==================
mint_mode = st.radio("How do you bring the fire?", ("Upload file", "Paste Suno link"), horizontal=True)

title = description = genre = audio_url = None

if mint_mode == "Paste Suno link":
    suno_url = st.text_input("🔗 Paste Suno share link", placeholder="https://suno.com/song/...")
    if suno_url:
        with st.spinner("Calling the ancestors…"):
            try:
                html = requests.get(suno_url, headers={'User-Agent': 'Mozilla/5.0'}).text
                title_match = re.search(r'<title>(.*?)</title>', html)
                title = title_match.group(1).split("·")[0].strip() if title_match else "Untitled Suno Flame"
                audio_match = re.search(r'"audio_url":"(https://[^"]+\.mp3)"', html)
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

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title of this flame", value=title or "Untitled Resonance")
with col2:
    genre = st.text_input("Vibration / Genre", value=genre or "Afro-Quantum")
description = st.text_area("Speak your intention", value=description or "Minted in pure resonance • From Alkebulan with Love • 2025")

# ================== MINT BUTTON ==================
if st.button("🖤 MINT THIS TRACK • ETERNAL LIFE ON CHAIN", type="primary"):
    if "address" not in st.session_state:
        st.error("Connect wallet first!")
        st.stop()
    if not (audio_file or audio_url):
        st.error("Upload or paste a track!")
        st.stop()

    with st.spinner("The scarab rolls your sound into eternity…"):
        try:
            # Pinata IPFS Upload
            pinata = Pinata(os.getenv("PINATA_API_KEY"), os.getenv("PINATA_SECRET_API_KEY"))
            
            if audio_file:
                audio_bytes = audio_file.read()
                audio_name = audio_file.name
            else:
                audio_response = requests.get(audio_url)
                audio_bytes = audio_response.content
                audio_name = f"{title}.mp3"

            audio_result = pinata.pin_file_to_ipfs(audio_bytes, audio_name)
            audio_ipfs = f"https://gateway.pinata.cloud/ipfs/{audio_result['IpfsHash']}"

            # Metadata
            metadata = {
                "name": title,
                "description": description,
                "image": ANKH_URL,
                "animation_url": audio_ipfs,
                "attributes": [{"trait_type": "Genre", "value": genre}]
            }
            metadata_result = pinata.pin_json_to_ipfs(metadata)
            token_uri = f"https://gateway.pinata.cloud/ipfs/{metadata_result['IpfsHash']}"

            # Real Mint on Base Sepolia (Testnet)
            w3 = Web3(Web3.HTTPProvider('https://sepolia.base.org'))
            contract_addr = os.getenv("CONTRACT_ADDRESS")
            if not contract_addr:
                st.error("Add CONTRACT_ADDRESS to .streamlit/secrets.toml first!")
                st.stop()

            abi = [{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"string","name":"uri","type":"string"}],"name":"mintTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]
            contract = w3.eth.contract(address=contract_addr, abi=abi)

            tx = contract.functions.mintTo(st.session_state.address, token_uri).build_transaction({
                'chainId': 84532,
                'gas': 300000,
                'gasPrice': w3.to_wei('1', 'gwei'),
                'nonce': w3.eth.get_transaction_count(st.session_state.address),
            })

            st.success("MINT PREPARED 🖤")
            st.code(f"Copy this TX JSON and import into MetaMask:\n{json.dumps(tx, default=str)}", language="json")
            st.markdown("**In MetaMask: Activity > Import Transaction > Paste JSON > Sign.** (Use test ETH)")
            tx_hash = st.text_input("Paste signed TX hash here to verify")
            if tx_hash:
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                st.success(f"MINT CONFIRMED 🖤 [View on Basescan](https://sepolia.basescan.org/tx/{tx_hash})")
                st.balloons()

            st.markdown(f"### {title}")
            st.markdown(f"**Creator:** {st.session_state.address}")
            st.markdown(f"**Token URI:** {token_uri}")
            st.audio(audio_ipfs)
            st.markdown("The ancestors just pressed play — forever.")

        except Exception as e:
            st.error(f"Ancestors say: {str(e)} — Check keys/network/gas.")

st.markdown("---")
st.markdown('<div class="footer">From Alkebulan with Love</div>', unsafe_allow_html=True)
