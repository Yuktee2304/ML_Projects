#import all libraries
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Data Science App",
    page_icon="📊"
)

#title
st.title(":rainbow[Data Analytics Portal]")
#st.header('Explore Data with ease..')
st.subheader(':gray[Explore Data with ease..]',divider='rainbow') # to get the text in smaller size

#Uploading files
file=st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data=pd.read_csv(file)
    else:
        data=pd.read_excel(file)    

    st.dataframe(data)
    st.info('File is successfully Uploaded',icon='🚨')

    #To get the info of the dataset
    st.subheader(":rainbow[Basic Information of the Dataset]",divider="rainbow")
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top and bottom Rows','Data Types','Columns'])
    
    with tab1:
        st.write(f"There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset")
        st.subheader(':rainbow[Statistical summary of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':rainbow[Top Rows]')
        toprows=st.slider('Number of rows you want',1,data.shape[0],key="topslider")
        st.dataframe(data.head(toprows))
        st.subheader(':rainbow[Bottom Rows]')
        bottomrows=st.slider('Number of columns you want',1,data.shape[0],key="bottomslider")
        st.dataframe(data.tail(bottomrows))
    with tab3:
        st.subheader(':rainbow[Data types of columns]')   
        st.dataframe(dict(data.dtypes))
    with tab4:
        st.subheader(':rainbow[Column Names in Dataset]')
        st.write(list(data.columns))    
    st.subheader(':rainbow[Column Values To Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2=st.columns(2)
        with col1:
            column=st.selectbox('Choose column name',options=list(data.columns))
        with col2:
            toprows=st.number_input('Top Rows',min_value=1,step=1)    
        count=st.button('Count')
        if(count==True):
            result=data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='rainbow')
            fig=px.bar(data_frame=result,x=column,y='count',template='plotly_white') # you can add this also text='count'
            st.plotly_chart(fig)
            fig1=px.line(data_frame=result,x=column,y='count',text='count',template='seaborn')
            st.plotly_chart(fig1)
            fig3=px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig3)

    st.subheader(':rainbow[Groupby: Simplify your data analysis]',divider='rainbow')
    st.write(':grey[The Groupby lets you summarize data by specific categories and groups]') 
    with st.expander('Groupby your columns'):
        col1,col2,col3=st.columns(3)   
        with col1:
            groupby_cols=st.multiselect('Choose your columns by groupby',options=list(data.columns))   
        with col2:
            op_col=st.selectbox('Choose column for operation',options=list(data.columns))
        with col3:
            type_op_col=st.selectbox('Choose operation to perform',options=['sum','max','avg','mean','median','count'])
        if(groupby_cols):
            result=data.groupby(groupby_cols).agg(
            newcol=(op_col,type_op_col)
            ).reset_index()
            st.dataframe(result)

            st.subheader(':rainbow[Data Visualization]',divider='rainbow')
            graphs_col=st.selectbox('Choose your graphs',options=['line','bar','scatter','pie','sunburst'])
            if(graphs_col=='line'):
                    x_axis_col=st.selectbox('Choose X axis',options=list(result.columns))
                    y_axis_col=st.selectbox('Choose Y axis',options=list(result.columns))
                    color_col=st.selectbox('Color Information',options=[None]+list(result.columns))
                    fig=px.line(data_frame=result,x=x_axis_col,y=y_axis_col,color=color_col,markers='o')
                    st.plotly_chart(fig)
            elif(graphs_col=='bar'):
                    x_axis_col=st.selectbox('Choose X axis',options=list(result.columns))
                    y_axis_col=st.selectbox('Choose Y axis',options=list(result.columns))
                    color_col=st.selectbox('Color Information',options=[None]+list(result.columns))
                    facet_column=st.selectbox('Column Information',options=[None]+list(result.columns))
                    fig=px.bar(data_frame=result,x=x_axis_col,y=y_axis_col,color=color_col,facet_col=facet_column,barmode='group')
                    st.plotly_chart(fig)    
            elif(graphs_col=='scatter'):
                    x_axis_col=st.selectbox('Choose X axis',options=list(result.columns))
                    y_axis_col=st.selectbox('Choose Y axis',options=list(result.columns))
                    color_col=st.selectbox('Color Information',options=[None]+list(result.columns))
                    size_col=st.selectbox('Size Column',options=[None]+list(result.columns))
                    fig=px.scatter(data_frame=result,x=x_axis_col,y=y_axis_col,color=color_col,size=size_col)
                    st.plotly_chart(fig)    
            elif(graphs_col=='pie'):
                   values_col=st.selectbox('Choose Numerical values',options=list(result.columns))
                   names_col=st.selectbox('Choose labels',options=list(result.columns))
                   fig=px.pie(data_frame=result,names=names_col,values=values_col)
                   st.plotly_chart(fig)
            elif(graphs_col=='sunburst'):
                 path_col=st.multiselect('Choose your path',options=list(result.columns))
                 fig=px.sunburst(data_frame=result,path=path_col,values='newcol')
                 st.plotly_chart(fig)       

