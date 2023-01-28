import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import openpyxl
from datetime import datetime, timedelta

#start

st.set_page_config(page_title='ENSEM-AWS')
st.header('ENSEM-AWS Weather Forcasting')
st.subheader('Dynamic data forcast')

#Load data frame
excel_file = 'EnsemAWS.xlsx'
sheet_name = 'Prediction'
sheet_name_2 = 'Loss'


df_Pred = pd.read_excel(excel_file,
                    sheet_name=sheet_name,
                    usecols='A:D',
                    header=0)
df_Loss = pd.read_excel(excel_file,
                    sheet_name=sheet_name_2,
                    usecols='A:H',
                    header=0)

#filters
df_Pred['Iteration'] = df_Pred['Iteration'].dt.date
#st.markdown(f'*Available records: {df_Pred['Iteration']}*') data["expected_Date"].dt.date
#st.dataframe(df_Pred)

accuracy = df_Pred['Accuracy'].unique().tolist()
iteration = df_Pred['Iteration'].unique().tolist()

#b=min(iteration)
#st.markdown(f'*Available records: {b}*')

iteration_selection = st.slider('Dataset records range:',
                                    min_value = min(iteration),
                                    max_value = max(iteration),
                                    #value = (min(iteration),max(iteration)),
                                    #st.markdown(f'*Available records: {datetime.fromtimestamp(max(iteration))}*'),
                                    value = (min(iteration), max(iteration)),
                                    format="MM/DD/YY")

accuracy_selection = st.multiselect('Resedual value between prediction and real records:',
                                    accuracy,
                                    default = accuracy)

#Filter Dataframe based on multiselect

mask = (df_Pred['Iteration'].between(*iteration_selection)) & (df_Pred['Accuracy'].isin(accuracy_selection))
nombre_of_result = df_Pred[mask].shape[0]
st.markdown(f'*Available records: {nombre_of_result}*')

#Goup dataframe

df_grouped = df_Pred[mask].groupby(by=['Accuracy']).count()[['Iteration']]
df_grouped = df_grouped.rename(columns={'Accuracy':'Iteration'})
df_grouped = df_grouped.reset_index()


bar_chart = px.bar(df_grouped,
                   x='Accuracy',
                   y='Iteration',
                   text='Iteration')
st.plotly_chart(bar_chart)


Line_chart = px.line(df_Pred[mask], x="Iteration", y=df_Pred[mask].columns[1:3], title='Ensem AWS Predictions')
st.plotly_chart(Line_chart)




#st.dataframe(df_Pred)

numbre_rows=df_Pred.shape[0]

#pie_chart=px.pie(df_Pred,
#                    title='Prediction Plot',
#                    values='Pred,Test',
#                    names='Iteration')
#st.plotly_chart(pie_chart)



#pie_chart2 = px.pie(df,
#                    title= '2nd Region vs Unit',
#                    values='Units',
#                    names='Item')
#st.plotly_chart(pie_chart2)
#delete streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
