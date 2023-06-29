import streamlit as st
import numpy as np
from PIL import Imagesp
import pandas as pd
from io import StringIO
from IPython.display import HTML


#Sayfa ayarları.
st.set_page_config(layout="wide",
page_title = "Maç Tahminleri",
page_icon = ":soccer:")
st. title("Ana Sayfa")

##Bu veri tipleriyle filtreeleme yapılacak.
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
def filtre_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtreleme için UI'lar koyar.

    Args:
        df (pd.DataFrame): Orijinal veri setini alır

    Returns:
        pd.DataFrame: Filtrelenmiş veri setini döndürür
    """
    modife_et = st.checkbox("Filtrele")

    if not modife_et:
        return df

    df = df.copy()

    for satir in df.columns:
        if is_object_dtype(df[satir]):
            try:
                df[satir] = pd.to_datetime(df[satir])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[satir]):
            df[satir] = df[satir].dt.tz_localize(None)


    container = st.container()

    with container:
        filtre_satirlar = st.multiselect("Seçenekler", df.columns)
        for satir in filtre_satirlar:
            sol, sag = st.columns((1, 20))
            sol.write("↳")

            # 10'dan düşük değerleri kategorik değer olarak al.
        

            if is_categorical_dtype(df[satir]) or df[satir].nunique() < 10:
                kategorık_giris = sag.multiselect(
                    f"Değer Seçiniz {satir}",
                    df[satir].unique(),
                    default=list(df[satir].unique()),
                )
                df = df[df[satir].isin(kategorık_giris)]
            
            elif is_numeric_dtype(df[satir]):
                    _min = int(df[satir].min())
                    _max = int(df[satir].max())
                    step = 1
                    sayısal_giris = sag.slider(
                        f"Değer Aralığı Seçiniz : {satir}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[satir].between(*sayısal_giris)]
               
            elif is_datetime64_any_dtype(df[satir]):
                tarih_giris = sag.date_input(
                    f"{satir} Aralığı Seçiniz",
                    value=(
                        df[satir].min(),
                        df[satir].max(),
                    ),
                )
                if len(tarih_giris) == 2:
                    tarih_giris = tuple(map(pd.to_datetime, tarih_giris))
                    start_date, end_date = tarih_giris
                    df = df.loc[df[satir].between(start_date, end_date)]
            else:
                yazi_giris = sag.text_input(
                        f"{satir} İçin Arama Yap",
                   

                )
                if yazi_giris:
                    df = df[df[satir].astype(str).str.contains(yazi_giris)]

    return df


sol, merkez,sag = st.columns(3)
with merkez:
    st.image('Icons/logo-color.png')
    st.title("""**:blue[Futbol Tahmin Uygulaması]** """)

# st.markdown("<h1 style='text-align: center;>Futbol Tahmin Uygulaması</h1>", unsafe_allow_html=True)
# st.write('<p style="color:red;</p>', 
# unsafe_allow_html=True)
st.write("""
**:blue[Bu web uygulamasının amacı,gol beklentisi ve elo derecelendirme sistemini kullanarak 1x2,2.5 üst ve karşılıklı gol olma olasılıklarını modellemektir. Dixon ve satires'un Poisson dağılıma getirdikleri 
bakış açısı farklı bir yerden ele alınmıştır.
Çıktı olarak yüzdelik olma olasılıklarını görürsünüz. Modelin güçlü yanından faydalanmak için bahis firmalarının futbol maçları için belirlediği
oranlarla, bu çıktıları karşılaştırabilirsiniz. RELOX modeli sezon boyunca takımların form durumunu gol beklentisi üzerinden ele alır.
Bahis oranlarıysa, son anda sakatlanan oyuncudan tutun hava durumuna kadar onlarca faktörü hesaba katar.Bunun kötü yanıysa, verdikleri oranların insanları manipüle etmesidir.
Bu yüzden model ve firma oranlarını karşılaştırmak size iyi bir bakış açısı kazandıracaktır.]**
""")

##HAKKINDA BÖLÜMÜ
expander_bar = st.expander("Hakkında")
expander_bar.markdown("""
* **Modelin nasıl çalıştığını merak ediyorsanız buraya bakabilirsiniz:** [Model Tanıtımı](https://drive.google.com/file/d/1jr0Y9Aaqg_j_EgOMfxe6KEjt1G9Hjvad/view?usp=sharing)
* **Orijinal Dixon ve satires makalesi buradan görüntelenebilir. Onların oluşturdukları modele eklemeler yapılmıştır:** [Makale](https://web.math.ku.dk/~rolf/teaching/thesis/Dixonsatires.pdf)
* **Bu tarz modellerle tahmin yapmak istiyorsanız buraya bakabilirsiniz:** [Penaltyblog](https://penaltyblog.readthedocs.io/en/latest/models/index.html)
* **Bu tarz modellerin çıkış noktasını anlamak için bu blog iyi bir kaynak:** [Opisthokonta](https://opisthokonta.net/?cat=48)
""")
st.info('Yeni sezon başlayana kadar 2022/2023 Premier Lig sezonu için tahminler bulunmaktadır.Modelin nasıl çalıştığını "Hakkında" bölümünden görüntüleyebilirsiniz.', icon="ℹ️")
##Verilerin yüklendiği fonksiyon
@st.cache_data()
def veri_yukle():
      df = pd.read_csv("veri_setleri/model.csv")
      df.rename(columns={"EvSahibi":"Ev Sahibi"},inplace=True)
      df = df[["Maç Haftası","Tarih","Ev Sahibi","Deplasman","MS EV","MS BERABERLIK","MS DEPLASMAN","2.5 Üstü","KG Var"]]
      nums= df.select_dtypes(include=np.number).columns.tolist()
      nums.remove("Maç Haftası")
      df[nums] = df[nums].apply(lambda x :  round(x*100,2)).astype(int)
      return df

df = veri_yukle()
df["Listele"] = False

##Seçili sütünları al.
df_ = df[["Tarih","Maç Haftası","Ev Sahibi","Deplasman","MS EV","MS BERABERLIK","MS DEPLASMAN","2.5 Üstü","KG Var"]].copy()


#Streamlit'in dataframe fonksiyonunda bazı özellikler var,Bunları kullanmak için
st.dataframe(
    filtre_df(df_).style.background_gradient(cmap = "RdYlGn"),
    column_config={
        "Ev Sahibi": "Ev Sahibi",
        "Deplasman": "Deplasman",
        "MS EV": st.column_config.NumberColumn(
            "Maç Sonucu:Ev(%)",
            help="Ev Sahibi Takımın Tahmin Edilen Kazanma Yüzdesi",
            format="%d",
        ),
         "MS BERABERLIK": st.column_config.NumberColumn(
            "Maç Sonucu:Berabere(%)",
            help="Maçın Beraberlik Durumu İçin Tahmin Edilen Yüzdesi",
            format="%d ",
        ),
          "MS DEPLASMAN": st.column_config.NumberColumn(
            "Maç Sonucu:Deplasman(%)",
            help="Deplasman Takımının Tahmin Edilen Kazanma Yüzdesi",
            format="%d",
        ),
        "2.5 Üstü": st.column_config.NumberColumn(
            "2.5 Üstü(%)",
            help="3 veya daha fazla gol olma yüzdesi",
            format="%d",
        ),
         "KG Var": st.column_config.NumberColumn(
         "Karşılıklı Gol Var(%)",
            help="Her iki takımda gol atar.",
            format="%d",
        ),
    },
    hide_index=True,
    use_container_width=True,
)

