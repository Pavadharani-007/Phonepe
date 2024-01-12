import json
import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pava12345S",
   
)

print(mydb)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("USE phonepephonepe")


img=Image.open("C:\\Users\\HP\\Desktop\\vs code\\phonepe_logo.png")
st.set_page_config(page_title="PhonePe Pulse", page_icon=img, layout="wide", )
icons = {
    "Home": "🏠",
    "Top Charts" :"📈",              
    "Explore Data": "🔍",
    "ABOUT": "📊"
}
SELECT = st.sidebar.selectbox("Choose an option", list(icons.keys()), format_func=lambda option: f'{icons[option]} {option}', key='selectbox')

if SELECT == "Home":
    col1,col2 = st.columns(2)
    col1.image(Image.open("C:\\Users\\HP\\Desktop\\vs code\\phonepe_logo.png"),width = 300)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:\\Users\\HP\\Desktop\\vs code\\upi.mp4")




            
if SELECT == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
            )
        
    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")

        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT State, SUM(Transaction_count) as Total_Transactions_Count, SUM(Transaction_amount) as Total FROM aggregated_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_count','Transaction_amount'])
            fig = px.pie(df, values='Transaction_amount',
                            names='State',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transaction_count'],
                            labels={'Transaction_count':'Transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f"SELECT district , SUM(map_count) as Total_Count, SUM(map_amount) as Total from map_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district ORDER BY Total DESC LIMIT 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'map_count','map_amount'])

                fig = px.pie(df, values='map_amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['map_count'],
                                labels={'map_count':'map_count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"SELECT district_pincode, SUM(top_count) as Total_Transactions_Count, SUM(top_amount) as Total from top_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district_pincode ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['district_pincode', 'top_count','top_amount'])
            fig = px.pie(df, values='top_amount',
                                names='district_pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['top_count'],
                                labels={'top_count':'top_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    # Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"SELECT user_brand, SUM(user_count) AS Total_Count, AVG(user_percentage)*100 AS Avg_Percentage FROM aggregated_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY user_brand order by Total_Count DESC LIMIT 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['user_brand', 'user_count','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="user_count",
                             y="user_brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"SELECT district, SUM(RegisteredUserS) as Total_Users FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)                        

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"SELECT district_pincode, SUM(registeredUsers) AS Total_Users FROM top_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district_pincode ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['district_pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='district_pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT State, SUM(registeredUsers) AS Total_Users  FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Users'],
                             labels={'Total_Users':'Total_Users'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# MENU 3 - EXPLORE DATA
if SELECT == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)

    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            world = pd.read_csv('C:\\Users\\HP\\Desktop\\vs code\\state2.csv')
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute("SELECT State, SUM(map_count) AS Total_Transactions, SUM(map_amount) AS Total_amount FROM map_transaction WHERE Year = 2018 AND Quarter = 3 GROUP BY State ORDER BY State")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('C:\\Users\\HP\\Desktop\\vs code\\state2.csv')
            df1.state = df2

            df1 = df1.merge(df2, left_on='State', right_on='state')
                                               
            fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='state',
            color='Total_amount',
            color_continuous_scale='sunset'
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

    with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"SELECT State, SUM(map_count) AS Total_Transactions, sum(map_amount) AS Total_amount FROM map_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY State")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('C:\\Users\\HP\\Desktop\\vs code\\state2.csv')
            #df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.state = df2
            df1 = df1.merge(df2, left_on='State', right_on='state')
            
           
            
           
            




            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            
                      featureidkey='properties.ST_NM',
                      locations='state',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

    # BAR CHART - TOP PAYMENT TYPE
    st.markdown("## :violet[Top Payment Type]")
    mycursor.execute(f"SELECT Transaction_type, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_amount FROM aggregated_transaction WHERE Year= '{Year}' AND Quarter = '{Quarter}' GROUP BY transaction_type ORDER BY Transaction_type")
    df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

    fig = px.bar(df,
                    title='Transaction Types vs Total_Transactions',
                    x="Transaction_type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=False) 

    # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
    st.markdown("# ")
    st.markdown("# ")
    st.markdown("# ")
    st.markdown("## :violet[Select any State to explore more]")
    selected_state = st.selectbox("",
                            ('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                            'Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa','Gujarat','Haryana',
                            'Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                            'Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                            'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                            'Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'),index=30)
        
    mycursor.execute(f"SELECT State, district,Year,Quarter, SUM(map_count) AS Total_Transactions, SUM(map_amount) AS Total_amount FROM map_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' AND State = '{selected_state}' GROUP BY State, District,Year,Quarter ORDER BY State,district")
    
    df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','district','Year','Quarter',
                                                        'Total_Transactions','Total_amount'])
    fig = px.bar(df1,
                x="district",
                y="Total_Transactions",
                title='selected_state',
                orientation='v',
                color='Total_amount',
                color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=True) 

# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"SELECT State, SUM(district), SUM(registeredUsers) AS Total_Users FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY Total_Users ")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','district', 'Total_Users'])
        df2 = pd.read_csv('C:\\Users\\HP\\Desktop\\vs code\\state2.csv')
        df1.State = df2
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA
         
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("Select State",
                             ('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                            'Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa','Gujarat','Haryana',
                            'Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                            'Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                            'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                            'Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'),index=30)
        
        mycursor.execute(f"SELECT State,Year,Quarter,district,SUM(registeredUsers) AS Total_Users FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' AND State = '{selected_state}' GROUP BY State, district,Year,Quarter ORDER BY State,Year,Quarter,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=[ 'State','Year','Quarter','district','Total_Users'])
       
        
        fig = px.bar(df,
                     title=selected_state,
                     x="district",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)


    

if SELECT == "ABOUT":
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("")
        st.markdown("") 
        st.markdown("")
        st.markdown("")
        st.markdown("")              
        #st.video("C:\PhonepeProject\pulse-video.mp4")
    with col2:
        st.video("C:\\Users\\HP\\Desktop\\vs code\\Phonepe.mp4")
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    st.title("THE BEAT OF PHONEPE")
    col1,col2 = st.columns(2)    
    with col1:        
        st.write("---")
        st.subheader("Third ET BFSI Innovation Tribe Virtual Summit & Awards")
        st.image(Image.open("C:\\Users\\HP\\Desktop\\vs code\\youtube\\award.jpg"),width = 300)
    with col2:
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("C:\\Users\\HP\\Desktop\\vs code\\youtube\\phonepe_image.png"),width = 500)


    
    
                            
   


                   
