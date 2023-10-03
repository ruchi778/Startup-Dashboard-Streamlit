import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='startup Analysis')

df= pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_investor_details():
    st.title("Overall Analysis")
    total = round(df['amount'].sum())

    #max amount infused in startup
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #avg ticket size
    avg_funding =  df.groupby('startup')['amount'].sum().mean()

    total_funded_startup=df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max',str(max_funding) + 'Cr')

    with col3:
        st.metric('Avg', str(round(avg_funding)) + 'Cr')

    with col4:
        st.metric('Total Funded Startup', str(total_funded_startup))

    st.header('MoM graph')
    selected_option=st.selectbox('Select Type',['Total','Count'])

    if selected_option =='Total':

        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        #temp_df[['amount', 'axis']]

    fig0,ax0=plt.subplots()
    ax0.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig0)


def load_investor_details(investor):
    st.title(investor)
    #show recent investors
    recent5=df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]

    st.subheader('most recent investments')
    st.dataframe(recent5)

    col1,col2 = st.columns(2)
    with col1:
        # biggest investment
        biggest_investment = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head(5)
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(biggest_investment.index, biggest_investment.values)
        st.pyplot(fig)

    with col2:
        #sector wise investoment
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f%%')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        #stage wise investment
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('stage invested in')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.01f%%')
        st.pyplot(fig2)

    with col4:
        #stage wise investment
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('city invested in')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    yoy_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YOY investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(yoy_series.index,yoy_series.values)
    st.pyplot(fig4)

    investor_by_vertical = df.groupby(['city', 'vertical'])['investors'].apply(list)

    for vertical, i in investor_by_vertical.items():
        print(vertical[1], i)
    st.subheader('Similar investors')

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    load_overall_investor_details()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('startup details')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Investor details')
    if btn2:
        load_investor_details(selected_investor)
