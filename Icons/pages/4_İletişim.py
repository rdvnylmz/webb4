import streamlit as st

st.header(":mailbox: İletişim")


form = """
<form action="https://formsubmit.co/ridvanyilmaz333@gmail.com" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder="İsminiz" required>
    <input type="email" name="email" placeholder="Mail Adresiniz" required>
    <textarea name="message" placeholder="Mesajınız"></textarea>
    <button type ="submit">Gönder</button>
</form>
"""

st.markdown(form, unsafe_allow_html=True)


def css_d(dosya_ismi):
    with open(dosya_ismi) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


css_d("style/style.css")