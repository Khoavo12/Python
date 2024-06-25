import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
    
if 'started' not in st.session_state:
    st.session_state.started = False

def main_page():
    df = pd.read_csv("dataset_free-tiktok-scraper_2022-07-27_21-44-20-266.csv")
    # tạo sidebar chứa các thông tin về dataset Nickname,Verified,CommentCount,PlayCount,ShareCount,Duration

    st.sidebar.title('Functions')
    choose = st.sidebar.selectbox('Select information', ['Student information and dataset','Verified',"Annual Spending","Fake Gegament","Number of Tiktok dowload","TikTokUsersCountryTotal2023"])
    if choose == 'Student information and dataset':
        st.header('Student information')
        st.write('First and last name: Tran Viet Long, Vo Minh Khoa, Thach Thi Thanh Ngan, Vu Thi Ha Vy, Tran Yen Thanh')
        st.write('ID: 10623028, 10623058, 10623030, 10323074, 10323029')
        st.write('Class: Python')
        st.header('Main database')
        st.write(df)
        st.write("In addition to the above data set, the group also uses some other data taken from the page")
        st.markdown("[Statista](https://www.statista.com/)")
    if choose == 'Verified':
        # Vẽ biểu đồ tròn thể hiện số lượng Verified và Not Verified
        # Chuyển true và false thành Verified và Not Verified
        df['Verified'] = df['Verified'].replace({True: 'Verified', False: 'Not Verified'})

        # Plotting
        fig, ax = plt.subplots()

        # Custom colors
        colors = ['#4CAF50', '#FF5722']  # Green and Red

        # Plot pie chart
        df['Verified'].value_counts().plot.pie(
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colors, 
            explode=(0.05, 0.05),  # Slightly explode both slices
            shadow=True, 
            wedgeprops={'edgecolor': 'black'}
        )

        # Customize the title and layout
        ax.set_title('The graph shows the percentage of Verified and Not Verified', fontsize=14, weight='bold')
        ax.set_ylabel('')  # Remove y-axis label for better appearance

        # Display the plot in Streamlit
        st.pyplot(fig)
        # Nhận xét về biểu đồ 
        st.write('The chart above shows a quite high percentage of Not Verified, accounting for nearly 3/4, showing the lack of account verification on TikTok.')
    if choose == 'Annual Spending':
    # Read the Excel file with specified column names
        sheet_name = 'Data'
        column_names = ['Year', 'Millions Dollar']
        df = pd.read_excel("annual-consumer-spending-2016-2023.xlsx", sheet_name=sheet_name, header=None, names=column_names)

        # Streamlit user input for year
        st.title('Annual Consumer Spending Visualization')
        year = st.number_input('Enter the year to view data for:', min_value=int(df['Year'].min()), max_value=int(df['Year'].max()))

        # Filter the DataFrame based on user input
        filtered_df = df[df['Year'] == year]

        # Plotting with Plotly for interactivity
        fig = px.line(df, x='Year', y='Millions Dollar', title='Annual Consumer Spending', markers=True)
        fig.add_scatter(x=filtered_df['Year'], y=filtered_df['Millions Dollar'], mode='markers+lines', marker=dict(color='red', size=10))

        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig)
    if choose == 'Fake Gegament':
        # data có 3 cột là Time, Fake likes, Fake followers requests
        # visualization với các chart thích hợp
        sheet_name = 'Data'
        df = pd.read_excel("fake_gagement.xlsx", sheet_name=sheet_name)
        # Biểu đồ thể hiện sự thay đổi của Fake likes và Fake followers requests theo thời gian
        fig = px.line(df, x='Time', y=['Fake likes', 'Fake followers requests'],
                    labels={
                        'Time': 'Time',
                        'value': 'Count',
                        'variable': 'Metrics'
                    },
                    title='Changes in Fake Likes and Fake Followers Requests Over Time')

        # Customize the figure
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title='Count',
            legend_title='Metrics',
            hovermode='x unified'
        )

        # Display the Plotly figure in Streamlit
        st.title('Fake Engagement Metrics Over Time')
        st.plotly_chart(fig)
    if choose == 'Number of Tiktok dowload':
        # data có 2 cột là Date và Number of Tiktok dowload
        # visualization với các chart thích hợp
        column_names = ['Time', 'Millions of Downloads']
        sheet_name = 'Data'
        df = pd.read_excel("quarterly-downloads-2018-2023.xlsx", sheet_name=sheet_name,header=None, names=column_names)
        fig = px.scatter(df, x='Time', y='Millions of Downloads', title='Number of TikTok Downloads Over Time',
                        color='Millions of Downloads', color_continuous_scale='Viridis')

        fig.update_xaxes(title='Time')
        fig.update_yaxes(title='Millions of Downloads')

        # Tùy chỉnh hover information
        fig.update_traces(marker=dict(size=12, opacity=0.8),
                        hovertemplate='<b>Date</b>: %{x}<br>'+
                                        '<b>Downloads</b>: %{y:.2f} millions')
        # Thiết lập highlight
        fig.update_traces(selected=dict(marker=dict(opacity=1)),
                    unselected=dict(marker=dict(opacity=0.2)))

        st.plotly_chart(fig)
    if choose == 'TikTokUsersCountryTotal2023':
        df = pd.read_csv('tiktok-users-by-country-2024.csv')
        st.sidebar.header("Map Size")
        map_width = st.sidebar.slider("Map Width", 500, 1500, 1000)
        map_height = st.sidebar.slider("Map Height", 500, 1000, 700)
        st.title('Population Distribution by Country on World Map')

        # Hiển thị bản đồ thế giới với dữ liệu dân số
        fig = px.scatter_geo(df, 
                            locations="country", 
                            locationmode='country names', 
                            size="TikTokUsersCountryTotal2023",
                            projection="natural earth", 
                            hover_name="country", 
                            color="TikTokUsersCountryTotal2023",
                            #title="Population Distribution by Country",
                            color_continuous_scale=px.colors.sequential.Plasma, # Chọn một bảng màu khác cho dữ liệu
                            size_max=50) # Điều chỉnh kích thước tối đa của các điểm

        fig.update_traces(textfont=dict(size=12, color='white')) # Điều chỉnh font chữ của hover

        fig.update_layout(geo=dict(showocean=True, oceancolor="LightBlue"), 
                  margin={"r":10,"t":10,"l":10,"b":10},
                                    width=map_width, # Điều chỉnh chiều rộng của bản đồ
                  height=map_height) # Điều chỉnh màu của biển
        
        
        st.plotly_chart(fig)
def landing_page():


    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.pexels.com/photos/5081926/pexels-photo-5081926.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }
    .stApp {
    background-color: rgba(0, 0, 0, 0.5);  # Optional: Add a dark overlay
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    st.markdown(
        """
        <h1 style="text-align: center;">
            TIKTOK DATASET
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <h2 style="text-align: center;">
        INTRODUCTION
    </h2>
    """,
    unsafe_allow_html=True
    )
    st.write(
"Welcome to our TikTok analytics dashboard. "
"Here, you'll discover information about user behavior, popular content, and audience characteristics.  "
"Our data will help you gain a deeper understanding of TikTok and create a creative strategy for success on the platform."
    )
    st.markdown("Currently, TikTok has become one of the most popular social networking platforms globally, attracting millions of users from all ages. This platform stands out for short, creative, and easily viral videos, helping users share content and connect with the community quickly. However, TikTok also faces many issues such as data security, privacy, and inappropriate content. TikTok's rapid growth requires regulators to put in place effective controls and management measures to protect users and maintain a safe environment online..")

    if st.button("Get Started"):
        st.session_state.started = True
        st.experimental_rerun()


if st.session_state.started:
    main_page()
else:
    landing_page()
