import json

import pandas as pd
from flask import Flask, request


app = Flask(__name__)


def get_mf_per_year(data_lab, data_pers):
    """Devuelve un dataframe con la cantidad de hombres y mujeres por anio.
    
    Parameters
    ----------
        data_lab pd.DataFrame:
            Dataframe con la informacion laboral de los/las empleados/as.
           
        data_pers pd.DataFrame:
            Dataframe con la informacion personal de los/las empleados/as.
    
    Returns
    -------
        Dataframe con el analisis de hombre y mujeres por año.
    """
    df_lab = data_lab[["EmpID", "DateofHire", "DateofTermination"]]
    df_pers = data_pers[["EmpID", "Sex"]]
    df_tot = pd.merge(df_lab, df_pers, on="EmpID", how="inner")
    df_tot["year_hire"] = df_tot["DateofHire"].str.split("/").str[-1]
    df_tot["year_term"] = df_tot["DateofTermination"].str.split("/").str[-1]

    # Además cambio la columna a tipo entero con el fin de manejar números.
    df_tot["year_hire"] = df_tot["year_hire"].astype(int)

    # Dado que en year_term tenemos NaN los rellenamos con el año máximo de contratación
    df_tot["year_term"].fillna(df_tot["year_hire"].max(), inplace=True)
    df_tot["year_term"] = df_tot["year_term"].astype(int)

    # Nos vamos a quedar de nuevo solo con las columnas que nos interesan
    df_tot = df_tot[["EmpID", "year_hire", "year_term", "Sex"]]
    
    hiring_years = df_tot["year_hire"].unique()

    igualdad_info = dict()
    for year in hiring_years:
        igualdad_info[year] = df_tot[(df_tot["year_hire"] <= year) & (df_tot["year_term"] > year)] \
                                .groupby(["Sex"])["EmpID"].count().to_dict()
        
    igualdad = pd.DataFrame(igualdad_info).unstack()  # Mediante esto obtendríamos una Serie
    igualdad.index.set_names(["year", "sex"], inplace=True)  # Con esto renombramos el multi-indice
    igualdad = igualdad.reset_index()  # Con esto estaríamos convirtiendo a DataFrame
    igualdad.rename(columns={0: "total"}, inplace=True)  # Con esto estamos renombrando la columna de total de personas
    igualdad.fillna(0, inplace=True)  # Con esto estamos rellenando los posible vacíos
    
    df_grp = igualdad.groupby("year", as_index=False)["total"].sum()
    df_ig = pd.merge(igualdad, df_grp, on="year", how="inner", suffixes=("_sex", "_year"))
    df_ig["percent"] = (100 * df_ig["total_sex"] / df_ig["total_year"]).round(2)
    return df_ig

@app.route("/etl/", methods=["POST"])
def etl():
    """Esta funcion esta alojada en la ruta /etl/ y ejecuta la etl para
    extraer la cantidad de mujeres y hombres por anio.
    
    Es un metodo POST al cual se le pasa por el cuerpo de ejecucion un diccionario
    transformado en string (json) con dos claves, vease el siguiente ejemplo.
    
    {
        'datos_laborales': json_df_laborales,
        'datos_personales': json_df_personales
    }
    
    los valores de las claves van a ser dataframes preprocesados previamente
    pasados a json.
    
    Returns
    -------
        str: Resultado de la ETL
    """
    data = request.get_json()
    data_lab = data.get("datos_laborales")
    data_lab = pd.read_json(data_lab)
    data_pers = data.get("datos_personales")
    data_pers = pd.read_json(data_pers)
    result = get_mf_per_year(data_lab, data_pers)
    
    return json.dumps({"resultado": result.to_json()})

@app.route("/etl_salary/", methods=["POST"])
def etl_salary():
    # TODO: Terminar la funcion
    return "Not Implemented"

@app.route("/etl_udf/", methods=["POST"])
def etl_udf():
    # TODO: Terminar la funcion
    return "Not Implemented"


if __name__ == "__main__":
    
    app.run(host="localhost", port=9090)