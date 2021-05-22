"""
Funcion que recibe los datos en un diccionario en Json lo reenvia a la funcion genera_resultado y devuelve
el dataframe para pintar.
"""

import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
def recibe_datos(data_dict):

    df_lab = pd.DataFrame.from_dict(json_normalize(data_dict.get('lab')), orient='columns')
    df_lab = data_dict.get('lab')
    df_pers = pd.DataFrame.from_dict(json_normalize(data_dict.get('pers')), orient='columns')
    de_desemp = pd.DataFrame.from_dict(json_normalize(data_dict.get('desemp')), orient='columns')

    df_lab = de_datos_lab[['EmpID', 'DateofHire', 'DateofTermination']]
    df_pers = de_datos_pers[['EmpID', 'Sex']]
    df_tot = pd.merge(df_lab, df_pers, on='EmpID', how='inner')
    df_tot['year_hire'] = df_tot['DateofHire'].str.split('/').str[-1]
    df_tot['year_term'] = df_tot['DateofTermination'].str.split('/').str[-1]
    """
    Además cambio la columna a tipo entero con el fin de manejar números.
    """
    df_tot['year_hire'] = df_tot['year_hire'].astype(int)
    """
    # Dado que en year_term tenemos NaN los rellenamos con el año máximo de contratación
    # TODO: De hacer ese fillna se puede derivar un error el cual no vamos a tener en
    #    consideración para facilitar el ejercicio pero hay que controlar las suposiciones que
    #    se realizan y porque se realizan.
    """
    df_tot['year_term'].fillna(df_tot['year_hire'].max(), inplace=True)
    df_tot['year_term'] = df_tot['year_term'].astype(int)
    """
    # Nos vamos a quedar de nuevo solo con las columnas que nos interesan
    """
    df_tot = df_tot[['EmpID', 'year_hire', 'year_term', 'Sex']]

    igualdad_info = dict()
    for year in hiring_years:
        igualdad_info[year] = df_tot[(df_tot['year_hire'] <= year) & (df_tot['year_term'] > year)] \
            .groupby(['Sex'])['EmpID'].count().to_dict()

    igualdad = pd.DataFrame(igualdad_info).unstack()  """Mediante esto obtendríamos una Serie kk"""
    igualdad.index.set_names(['year', 'sex'], inplace=True)  """Con esto renombramos el multi-indice"""
    igualdad = igualdad.reset_index()  """Con esto estaríamos convirtiendo a DataFrame"""
    igualdad.rename(columns={0: 'total'}, inplace=True) """ Con esto estamos renombrando la columna de total de personas"""
    igualdad.fillna(0, inplace=True) """Con esto estamos rellenando los posible vacíos"""
    df_grp = igualdad.groupby('year', as_index=False)['total'].sum()
    df_ig = pd.merge(igualdad, df_grp, on='year', how='inner', suffixes=('_sex', '_year'))
    df_ig['percent'] = (100 * df_ig['total_sex'] / df_ig['total_year']).round(2)

    return df_ig.to_json(orient = 'table')