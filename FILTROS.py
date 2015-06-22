#IMPORTANTE PARA NOMBRES DE CAMPOS DE JSON, SE DEBE HACER SIEMPRE QUE SE CARGUE UN NUEVO DF DEL ARCHIVO
df.rename(columns={'OrigenCiudad': 'cityOrigen', 'OrigenLatitud': 'latOrigen', 'OrigenLongitud': 'lonOrigen',
                  'DestinoCiudad': 'cityDestino', 'DestinoLatitud': 'latDestino', 'DestinoLongitud': 'lonDestino',
                  'CrashCiudad': 'cityAccidente', 'CrashPais': 'countryAccidente', 'CrashLatitud': 'latAccidente',
                  'CrashLongitud': 'lonAccidente'}, inplace=True)



#TRIMESTRAL
trimestre = 3 #ESTE ES EL TRIMESTRE, va de 1 a 4
mesInicial = 0
mesFinal = 0
if(trimestre == 1):
    mesInicial = 1
    mesFinal = 3
elif(trimestre == 2):
    mesInicial = 4
    mesFinal = 6
elif(trimestre == 3):
    mesInicial = 7
    mesFinal = 9
elif(trimestre == 4):
    mesInicial = 10
    mesFinal = 12
elif(trimestre == 0):
    mesInicial = 1
    mesFinal = 12

df["time"] = pd.to_datetime(df[df.columns[0]], format="%m/%d/%Y")
df_tri = df.loc[(df["time"].dt.month >= mesInicial) & (df["time"].dt.month <= mesFinal)]
df_final = pd.DataFrame(columns=('cityOrigen', 'latOrigen', 'lonOrigen', 'cityDestino', 'latDestino',
                        'lonDestino', 'cityAccidente', 'latAccidente', 'lonAccidente', 'Date', 'Time',
                        'Type', 'Aboard', 'Fatalities', 'Ground', 'Summary'))
for i in df_tri.index.values.tolist():
    df_final.loc[len(df_final)+1]=[df_tri['cityOrigen'][i], df_tri['latOrigen'][i], df_tri['lonOrigen'][i],
                                  df_tri['cityDestino'][i], df_tri['latDestino'][i], df_tri['lonDestino'][i],
                                  df_tri['cityAccidente'][i], df_tri['latAccidente'][i], df_tri['lonAccidente'][i],
                                  df_tri[df.columns[0]][i], df_tri['Time'][i], df_tri['Type'][i], df_tri['Aboard'][i],
                                  df_tri['Fatalities'][i], df_tri['Ground'][i], df_tri['Summary'][i]]
print df_final
