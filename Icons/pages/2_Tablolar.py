import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(layout="wide")


@st.cache_data()
def verı_yukle():
      df = pd.read_csv("veri_setleri/elo_xg.csv")
      df.rename(columns={"EvSahibi":"Ev Sahibi"},inplace=True)
      return df 

def elo_yukle():
      df = pd.read_csv("veri_setleri/sezon_sonu_elo.csv")
      df.rename(columns={"EvSahibi":"Ev Sahibi"},inplace=True)
      return df 

def puan_yukle():
      df = pd.read_csv("veri_setleri/tablolar.csv")
      df.rename(columns={"EvSahibi":"Ev Sahibi"},inplace=True)
      # a = ['Man City', 'Arsenal', 'Man United', 'Newcastle', 'Liverpool',
      #  'Brighton', 'Aston Villa', 'Tottenham', 'Brentford', 'Fulham',
      #  'Crystal Palace', 'Chelsea', 'Wolves', 'West Ham', 'Bournemouth',
      #  'Everton', 'Leicester', 'Leeds', 'Southampton', 'Nottingham Forest']
      a =df.index
      df["takim"] = a

      return df 




df = verı_yukle()
df1= elo_yukle()
df2= puan_yukle()
# st.write(df)
df_2 = df2[["Sıra","takim","Ev Sahibiyken Gol","Deplasmandeyken Gol","goal_difference","Ev Sahibiyken Puan","Deplasmandayken Puan","Toplam Puan"]].copy()
df_1 = df1[["Sıra","Takım","Elo"]]
df_= df[["Tarih","Maç Haftası","Ev Sahibi","Ev Gol","Deplasman","Deplasman Gol","Ev xG","Deplasman xG","Ev Sonraki Elo","Deplasman Sonraki Elo","Elo_ev_onceki","Elo_dep_onceki","EvYenixG","DepYenixG"]]

st.header("**:blue[Buradan görüntülemek istediğin tabloyu seçebilirsin.]**")
options = st.selectbox("Hangi tabloyu görüntülemek istiyorsun?",
                         ["Elo","Puan Tablosu","Model Tablosu"])
button5 = st.button("Getir")    
if button5:
    if options=="Elo":
        st.dataframe(
            df_1,
            column_config={
                  "Sıra":st.column_config.NumberColumn(
                        "Sıra",
                        help="Takım elo puanına göre sırası",
                        format="%d",
                  ),

                  "Elo":st.column_config.NumberColumn(
                        "Elo Puanı",
                        help="Takımların her maç sonucunda yenilenen elo puanları.",
                        format="%d",
                  ),
            },

            hide_index=True,
            use_container_width=True,

        )
    elif options=="Model Tablosu":
        
        st.dataframe(
            df_,
            column_config={
                 
                  "Sıra":st.column_config.NumberColumn(
                        "Sıra",
                        help="Takım elo puanına göre sırası",
                        format="%d",
                  ),
                  "takim":"Takım",
                  "Ev Sahibiyken Gol":st.column_config.NumberColumn(
                        "Ev Sahibi Gol",
                        help="Kendi sahasında rakibe attığı gol sayısı.",
                        format="%d",
                  ),
                  "Deplasmandeyken Gol":st.column_config.NumberColumn(
                        "Deplasman Ekibi Attığı Gol",
                        help="Rakibin sahasında rakibe attığı gol sayısı.",
                        format="%d",
                  ),
                  "Ev xG":st.column_config.NumberColumn(
                        "Ev Gol Beklentisi",
                        help="Ev sahibinin maçtaki toplam gol beklentisi(xG).",
                        format="%d",
                  ),
                   "Dep xG":st.column_config.NumberColumn(
                        "Deplasman Gol Beklentisi",
                        help="Deplasman ekibinin maçtaki toplam gol beklentisi(xG).",
                        format="%d",
                  ),
                    "Ev Sonraki Elo":st.column_config.NumberColumn(
                        "Ev Maçtan Sonraki Elo",
                        help="Maçın durumuna göre arttırılmış veya azaltılmış elo puanı.",
                        format="%d",

                  ),
                    "Dep Sonraki Elo":st.column_config.NumberColumn(
                        "Deplasman  Maçtan Sonraki Elo",
                        help="Maçın durumuna göre arttırılmış veya azaltılmış elo puanı.",
                        format="%d",
                  ),
                "Elo_ev_onceki":st.column_config.NumberColumn(
                        "Ev Maçtan Önceki Elo",
                        
                        format="%d",
                  ),
                    "Elo_dep_onceki":st.column_config.NumberColumn(
                        "Deplasman  Maçtan Önceki Elo",
                       
                        format="%d",
                  ),
                    "EvYenixG":st.column_config.NumberColumn(
                        "Ev Sahte Gol",
                        help="Modelin kurguladığı sahte gol.Ayrıntılı bilgiye 'Hakkında' bölümünden ulaşabilirsin.",
                        format="%d",
                  ),
                   "DepYenixG":st.column_config.NumberColumn(
                        "Deplasman Sahte Gol",
                        help="Modelin kurguladığı sahte gol.Ayrıntılı bilgiye 'Hakkında' bölümünden ulaşabilirsin.",
                        format="%d",
                  ),



            },

            hide_index=True,
            use_container_width=True,

        )
    elif options=="Puan Tablosu":
        
        st.dataframe(
            df_2,
            column_config={
                 
                  "EvSahibi":"Ev Sahibi",
                  
                  "Ev Gol":st.column_config.NumberColumn(
                        "Ev Gol",
                        help="Kendi sahasında rakibe attığı gol sayısı.",
                        format="%d",
                  ),
                  "Deplasman Gol":st.column_config.NumberColumn(
                        "Deplasman Gol",
                        help="Rakibin sahasında rakibe attığı gol sayısı.",
                        format="%d",
                  ),
                  "goal_difference":st.column_config.NumberColumn(
                        "Gol Farkı",
                        help="Attığı gol ve yediği gollerin farkı.",
                        format="%d",
                  ),
            },

            hide_index=True,
            use_container_width=True,

        )



