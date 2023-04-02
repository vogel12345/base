import streamlit as st
import pandas as pd
import plotly.express as px
import pymongo

st.title('Carros usados')
st.subheader('Luis Arnoldo Vogel Romero')

# Conexión a la base de datos de MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["carros"]
collection = db["usados"]

uploaded_file = st.file_uploader('Subir archivo', type='csv')
if uploaded_file:
    st.markdown('--')

    # Lectura del archivo CSV y transformación a un formato compatible con MongoDB
    df = pd.read_csv(uploaded_file)
    data = df.to_dict(orient='records')

    # Insertar los registros en la colección de MongoDB
    collection.insert_many(data)

    st.dataframe(df)

    groupby_column = st.selectbox(
        'Selecciona la informacion de carros que te gustaria saber',
        ('abtest','vehicleType','gearbox','model','kilometer','fuelType','brand')
    )

    # Agregación de los datos por columna seleccionada
    df_grouped = pd.DataFrame(list(collection.aggregate([
        {"$group": {"_id": f"${groupby_column}", "count": {"$sum": 1}}}
    ])))

    fig = px.bar(
        df_grouped,
        x="_id",
        y="count",
        color="_id",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        template='plotly_white',
        title=f'<b>Numero de carros usados por {groupby_column}</b>'
    )

    # Actualizar el label del eje X
    fig.update_xaxes(title_text=groupby_column)

    # Actualizar el label del eje Y
    fig.update_yaxes(title_text="Cantidad de carros usados")

    st.plotly_chart(fig)