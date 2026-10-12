import io

import qrcode
import streamlit as st

SIZES = {
    "Pequeno": 150,
    "Médio": 300,
    "Grande": 600,
    "Extra grande": 1000,
}


def generate_qr(data: str, size: int) -> bytes:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), resample=0)  # NEAREST mantém os quadrados nítidos
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


st.set_page_config(page_title="Gerador de QR Code", page_icon="🔳", layout="wide")
st.title("🔳 Gerador de QR Code")

link = st.text_input("Cole o link aqui", placeholder="https://exemplo.com")

if st.button("Gerar QR Code", type="primary"):
    if not link.strip():
        st.warning("Informe um link antes de gerar.")
        st.session_state.pop("qrs", None)
    else:
        # Guarda no session_state para os QR codes não sumirem ao clicar em "Baixar"
        st.session_state.qrs = {
            size: generate_qr(link.strip(), size) for size in SIZES.values()
        }

if "qrs" in st.session_state:
    cols = st.columns(len(SIZES))
    for col, (label, size) in zip(cols, SIZES.items()):
        png = st.session_state.qrs[size]
        with col:
            st.subheader(f"{label}")
            st.caption(f"{size} × {size} px")
            st.image(png, width=min(size, 250))
            st.download_button(
                "Baixar PNG",
                data=png,
                file_name=f"qrcode_{size}px.png",
                mime="image/png",
                key=f"dl_{size}",
            )
