# Arquivo de extração de dados do Koppen
# Imports ----
import pandas as pd

# Setup ----
df_controle = pd.read_csv("municipios_brasil.csv",decimal=",", index_col=1)
df = pd.read_excel("koppen/Koppen Brazilian municipalities.xls", sheet_name="Data", index_col = 1)

df_join = df_controle.join(df)

# Retira temperatura média anual para todas as cidades


print(df_join)
