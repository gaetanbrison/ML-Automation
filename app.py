import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling


    
def main():

    def _max_width_():
        max_width_str = f"max-width: 1000px;"
        st.markdown(
            f"""
        <style>
        .reportview-container .main .block-container{{
            {max_width_str}
        }}
        </style>
        """,
            unsafe_allow_html=True,
        )

    # Hide the Streamlit header and footer
    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)


    # increases the width of the text and tables/figures
    _max_width_()

    # hide the footer 
    hide_header_footer()
    
    images = Image.open('images/hi-paris-lancement-ecole-polytechnique-x.png')
    st.image(images, width=200,caption="Image 'Hi! PARIS' Research Center.")
    
    
    st.markdown("# Data Quality Check 🔍 ✅")
    st.markdown("### Check the basic quality of any dataset and generate data reports 🧐")
    st.markdown("     ")
    st.error("###### Only upload non confidential data!!")

    st.markdown("---")
    def file_select(folder='./datasets'):
        filelist=os.listdir(folder)
        st.markdown("OR")
        selectedfile=st.selectbox('Select a default dataset',filelist)
        return os.path.join(folder,selectedfile)


    if st.button('Upload Data'):
        data=st.file_uploader('Upload Dataset in .CSV',type=['CSV'])
        if data is not None:
            df=pd.read_csv(data)
    else:
        filename=file_select()
        st.info('You selected {}'.format(filename))
        if filename is not None:
            df=pd.read_csv(filename)
    st.markdown("---")
    

    #show data
    if st.checkbox('Show  Dataset'):
        num=st.number_input('No. of Rows',5,10)
        head=st.radio('View from top (head) or bottom (tail)',('Head','Tail'))

        if head=='Head':
            st.dataframe(df.head(num))
        else:
            st.dataframe(df.tail(num))
        
    st.markdown("---")
    
    if st.checkbox('Rows & Columns size'):
        st.markdown("Number of rows and columns helps us to determine how large the dataset is.")
        st.text('(Rows,Columns)')
        st.write(df.shape)

    st.markdown("---")   
 
    if st.checkbox('Distribution of values'):
       st.markdown("This is a simple check to see the distribution of values and look for outliers")
       st.write(df.describe())

    st.markdown("---")
    
    #check for null values
    if st.checkbox('Missing Values'):
        st.markdown("Missing values are known as null or NaN values. Missing data tends to **introduce bias that leads to misleading results.**")

        st.write("Number of rows:", len(df))
        dfnull = df.isnull().sum()/len(df)*100
        totalmiss = dfnull.sum().round(2)
        st.write("Percentage of total missing values:",totalmiss)
        st.write(dfnull)
        if totalmiss <= 30:
           st.success("Looks good! as we have less then 30 percent of missing values.")
           
        else:
           st.error("Poor data quality due to greater than 30 percent of missing value.")
           
       

        st.markdown(" > Theoretically, 25 to 30 percent is the maximum missing values are allowed, there’s no hard and fast rule to decide this threshold. It can vary from problem to problem.")

    st.markdown("---")   


    #check for completeness ratio 
    if st.checkbox('Completeness Ratio'):
        st.markdown(" Completeness is defined as the ratio of non-missing values to total records in dataset.") 
        # st.write("Total data length:", len(df))
        nonmissing = (df.notnull().sum().round(2))
        completeness= round(sum(nonmissing)/len(df),2)
        st.write("Completeness ratio:",completeness)
        st.write(nonmissing)

        if completeness >= 0.80:
           st.success("Looks good! as we have completeness ratio greater than 0.85.")
           
        else:
           st.error("Poor data quality due to low completeness ratio( less than 0.85).")

    st.markdown("---")

    #check dupication rate
    if st.checkbox('Duplication Rate'):
        st.markdown(" Duplication rate is defined as the ratio of  number of duplicates to total records in dataset.") 
        
        duplicated = df.duplicated().sum()
        dupratio= round(duplicated/len(df),2)
        st.write("Duplication rate:",dupratio)
        st.markdown(" > There’s no hard and fast rule to decide the threshold. It can vary from problem to problem.")
      
            
    st.markdown("---")

    #check for normality test
    if st.checkbox('Normality'):


        images=Image.open('images/n.png')
        st.image(images,width=600, caption="Image from ALVARO.")


        st.markdown("Normality tests are used to determine if a dataset is well-modeled by a normal distribution. For normality test we can use skewness technique which is a quantification of how much a distribution is pushed left or right, a measure of asymmetry in the distribution.")
        aa= pd.DataFrame(df).skew()
        normalityskew= round(aa.mean(),4)
        st.write("How far is my dataset from Normal Distribution:", normalityskew)

        if normalityskew == 0 :
           st.success("Your dataset is in  Normal Distribution i.e mean, mode and median are all equal ")
           
        elif normalityskew > 0:
           st.success("Positively Skew so Mean  >  Median  >  Mode")

        elif normalityskew < 0:
            st.success("Negatively Skew so Mode  >  Median  > Mean")   


    st.markdown("---")

    if st.checkbox('Generate Data Quality Report'):
        st.markdown("We are generating for you a data quality report with the help of Pandas Profiling.")
        st.text('In function of the dataset size might take up to 3min')
        pr = df.profile_report()
        st_profile_report(pr)

    st.markdown("---")


    

  

if __name__=='__main__':
    main()


st.markdown("   ")
st.markdown("   ")
st.markdown("   ")
st.markdown("   ")
st.markdown("### 👨🏼‍💻  For more support contact the Engineering Team: engineer@hi-paris.fr  🚀")


     


  
