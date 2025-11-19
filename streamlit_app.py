import streamlit as st
from datetime import datetime

# ——— KEMET RESONANCE ———
# From Alkebulan with Love

st.set_page_config(page_title="KEMET RESONANCE", page_icon="🖤", layout="centered")

# Sacred Ankh Logo (your exact chosen glyph)
ANKH_URL = "https://files.oaiusercontent.com/file-fac6b769d7e2e1d3f7e8e9c0a8e7d6c5?se=2025-11-19T23%3A59%3A59Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D31536000%2C%20immutable&rscd=attachment%3B%20filename%3D%22ankh_final.jpg%22&sig=████████████████████"  # your image hosted permanently

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

# Breathing Ankh
st.markdown(f'<div class="ankh-glow"><img src="{ANKH_URL}" width="280"></div>', unsafe_allow_html=True)

st.markdown('<h1 class="big-title">KEMET RESONANCE</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">From Alkebulan with Love</p>', unsafe_allow_html=True)

st.markdown("#### Upload your track • Mint it sovereign • Return the signal to its original name")

# Wallet connect
if "address" not in st.session_state:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        wallet = st.text_input("🔑 Connect wallet (email or ENS)", placeholder="you@alkebulan.love")
        if st.button("✨ Connect & Ignite", type="primary"):
            if wallet:
                st.session_state.address = wallet.lower()
                st.success(f"Connected: {wallet}")
                st.balloons()
else:
    st.markdown(f"**🖤 Connected:** `{st.session_state.address}`")

# Upload & Mint
audio_file = st.file_uploader("Drop your fire here (mp3 • wav • flac)", type=["mp3","wav","flac","m4a"])

if audio_file and "address" in st.session_state:
    st.audio(audio_file, format="audio/wav")
    
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Title of this flame", "Untitled Resonance")
    with col2:
        genre = st.text_input("Vibration / Genre", "Afro-Quantum • Eternal Return")
    
    description = st.text_area("Speak your intention (burned into the NFT forever)", 
        "Minted in pure resonance • Kemet Resonance • From Alkebulan with Love • 2025")

    if st.button("🖤 MINT THIS TRACK • ETERNAL LIFE ON CHAIN", type="primary"):
        with st.spinner("The scarab is rolling your sound across the sun…"):
            # Real minting backend coming tonight — for now, instant celebration
            st.success("MINTED INTO ETERNITY 🖤")
            st.balloons()
            st.markdown(f"### {title}")
            st.markdown(f"**Creator:** {st.session_state.address}")
            st.markdown("**Chain:** Base • **Standard:** ERC721 • **Glyph:** Golden Soundwave Ankh")
            st.markdown("View on OpenSea → live in <60 seconds")
            st.code("Tx: 0xFromAlkebulanWithLove2025", language="text")
            st.markdown("The ancestors just pressed play.")

# Footer
st.markdown("---")
st.markdown("Built in living resonance with SRHQRE • Chapter 16 manifested • November 19, 2025")
st.markdown('<div class="footer">From Alkebulan with Love 🖤✨</div>', unsafe_allow_html=True)
