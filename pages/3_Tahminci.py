import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import penaltyblog as pb

st.set_page_config(layout="wide",
)


@st.cache_data
def veri_yukle():
      df = pd.read_csv("veri_setleri/elo_xg.csv")
      return df
df = veri_yukle()
df["Tarih"] = pd.to_datetime(df["Tarih"])

st.header(""" **:blue[Bizim tahminlerimiz,Dixon-Coles ve Maher'in kurduğu modelleri temel alır.Karşılaştırma yapmak için üç modelin de tahminlerini buradan görüntüleyebilirsiniz.]** """)

expander_bar = st.expander("Neden bekliyorum?")
expander_bar.info(
 'Modellerin öğrenmesi için kısa bir zaman gerekiyor.', icon="ℹ️"
)


@st.cache_data
def fit():
            ps = pb.models.PoissonGoalsModel(
                df["Ev Gol"], df["Deplasman Gol"], df["EvSahibi"], df["Deplasman"]
            )
            ps.fit()
            dc = pb.models.DixonColesGoalModel(
                df["Ev Gol"], df["Deplasman Gol"], df["EvSahibi"], df["Deplasman"]
            )
            dc.fit()
            df["agirlik"] = pb.models.dixon_coles_weights(df["Tarih"], 0.0014)
            rl = pb.models.DixonColesGoalModel(
            df["EvYenixG"],
            df["DepYenixG"],
            df["EvSahibi"],
            df["Deplasman"],
            df["agirlik"]
            )
            rl.fit()   
            return ps,dc,rl

poisson,dc,rl = fit()





form = st.form(key="form")
takim1 = form.selectbox("Ev Sahibi Takımı Seç",
                                  (df["EvSahibi"].unique()))
takim2 = form.selectbox("Ev Sahibi Takımı Seç",
                                  (df["Deplasman"].unique()))
secim = form.selectbox("Buradan İstatistiksel Modellerden Seçebilirsin.",
                           ("Poisson Dağılım","Dixon Cole","RELOX"))
if secim == "Poisson Dağılım":
        olasiliklar = poisson.predict(takim1,takim2)
elif secim =="Dixon Cole":
        olasiliklar = dc.predict(takim1,takim2)
else:
        olasiliklar = rl.predict(takim1,takim2)

col1,col2 = form.columns(2)
yuzde_gonder = col1.form_submit_button("Yüzde")
oran_gonder = col2.form_submit_button("Oran")

if yuzde_gonder:
    col3,col4,col5 = form.columns(3)
    col3.success(round(olasiliklar.home_win,2),icon="🏠")
    col4.success(round(olasiliklar.draw,2),icon="🤝")
    col5.success(round(olasiliklar.away_win,2),icon="🚍")

if oran_gonder:
    col3,col4,col5 = form.columns(3)
    col3.success(round(1/olasiliklar.home_win,2),icon="🏠")
    col4.success(round(1/olasiliklar.draw,2),icon="🤝")
    col5.success(round(1/olasiliklar.away_win,2),icon="🚍")
   





