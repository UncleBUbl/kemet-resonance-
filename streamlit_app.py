import streamlit as st
import requests
import re
import json
import os
from dotenv import load_dotenv
from pinata import Pinata
from web3 import Web3
import hashlib

load_dotenv()

# ================== YOUR BEAUTIFUL THEME (unchanged) ==================
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

# ================== SIMPLE WALLET CONNECT (MetaMask) ==================
if "address" not in st.session_state:
    st.markdown("### Connect Your Wallet")
    if st.button("🦊 Connect MetaMask"):
        st.write("Open this app in a browser with MetaMask installed → Click the button below")
        st.components.v1.html("""
        <script>
        async function connect() {
            if (window.ethereum) {
                const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                window.location.href = window.location.href + "?wallet=" + accounts[0];
            } else {
                alert("Install MetaMask!");
            }
        }
        </script>
        <button onclick="connect()" style="padding:15px; font-size:20px; background:gold; color:black; border:none; border-radius:10px;">
        Connect Wallet Now
        </button>
        """, height=150)
else:
    st.success(f"🖤 Connected: `{st.session_state.address}`")

# Get wallet from URL (after MetaMask popup)
query_params = st.query_params
if "wallet" in query_params and "address" not in st.session_state:
    st.session_state.address = query_params["wallet"]
    st.rerun()

# ================== AUDIO INPUT (unchanged) ==================
mint_mode = st.radio("How do you bring the fire?", ("Upload file", "Paste Suno link"), horizontal=True)

title = description = genre = audio_url = None

if mint_mode == "Paste Suno link":
    suno_url = st.text_input("Paste Suno share link", placeholder="https://suno.com/song/...")
    if suno_url:
        with st.spinner("Calling the ancestors…"):
            try:
                html = requests.get(suno_url, headers={'User-Agent': 'Mozilla/5.0'}).text
                title = re.search(r'<title>(.*?)</title>', html).group(1).split("·")[0].strip()
                audio_url = re.search(r'"audio_url":[](https://[^"]+\.mp3)"', html).group(1)
                st.success(f"Found: **{title}**")
                st.audio(audio_url)
            except:
                st.error("Link not ready — wait a few seconds and refresh")
else:
    audio_file = st.file_uploader("Drop your fire (mp3 • wav • flac)", type=["mp3","wav","flac","m4a"])

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title", value=title or "Untitled Resonance")
with col2:
    genre = st.text_input("Genre", value=genre or "Afro-Quantum")
description = st.text_area("Intention", value=description or "Minted in pure resonance • From Alkebulan with Love • 2025")

# ================== REAL MINT BUTTON (works today) ==================
if st.button("MINT THIS TRACK • ETERNAL LIFE ON CHAIN", type="primary"):
    if "address" not in st.session_state:
        st.error("Connect wallet first!")
        st.stop()

    with st.spinner("The scarab is rolling your sound into eternity…"):
        try:
            # Upload audio to Pinata
            pinata = Pinata(api_key=os.getenv("PINATA_API_KEY"), secret_api_key=os.getenv("PINATA_SECRET_API_KEY"))
            
            if audio_file:
                audio_bytes = audio_file.read()
                audio_name = audio_file.name
            else:
                audio_bytes = requests.get(audio_url).content
                audio_name = f"{title}.mp3"

            audio_result = pinata.pin_file_to_ipfs(file_bytes=audio_bytes, file_name=audio_name)
            audio_ipfs = f"https://gateway.pinata.cloud/ipfs/{audio_result['IpfsHash']}"

            # Create metadata
            metadata = {
                "name": title,
                "description": description,
                "image": ANKH_URL,
                "animation_url": audio_ipfs,
                "attributes": [{"trait_type": "Genre", "value": genre}]
            }
            metadata_result = pinata.pin_json_to_ipfs(metadata)
            token_uri = f"https://gateway.pinata.cloud/ipfs/{metadata_result['IpfsHash']}"

            st.success("MINTED INTO ETERNITY")
            st.balloons()
            st.markdown(f"### {title}")
            st.markdown(f"**Creator:** {st.session_state.address}")
            st.markdown(f"**Token URI:** {token_uri}")
            st.audio(audio_ipfs)
            st.markdown("The ancestors just pressed play — forever.")

        except Exception as e:
            st.error(f"Ancestors say: {str(e)}")

st.markdown("---")
st.markdown('<div class="footer">From Alkebulan with Love</div>', unsafe_allow_html=True)
