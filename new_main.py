import streamlit as st
import sklearn
import pickle
import pandas as pd
import numpy as np
import xgboost
from xgboost import XGBRegressor
from PIL import Image
import requests



# excel_file = 'avg_score.xlsx'
# df = pd.read_excel(excel_file)





pipe = pickle.load(open('pipe2.pkl','rb'))

teams = ['Sunrisers Hyderabad', 'Mumbai Indians',
    'Royal Challengers Bangalore','Kolkata Knight Riders', 'Delhi Capitals', 'Punjab Kings',
       'Rajasthan Royals', 'Chennai Super Kings']

cities = ['Hyderabad', 'Mumbai', 'Indore', 'Kolkata',
       'Bangalore', 'Delhi', 'Chandigarh', 'Chennai', 'Jaipur', 'Pune',
       'Visakhapatnam', 'Abu Dhabi', 'Dubai', 'Sharjah', 'Ahmedabad',
       'Navi Mumbai', 'Cape Town', 'Port Elizabeth', 'Durban',
       'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Cuttack', 'Nagpur', 'Dharamsala', 'Raipur',
       'Ranchi']
over = [6,7,8,9,10,11,12,13,14,15,16,17,18,19]
wkt = [1,2,3,4,5,6,7,8,9,10]
image2 = Image.open('2.jpg')

st.sidebar.image(image2)


st.title('IPL Score Predictor')

col1, col2 = st.sidebar.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting Team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

city = st.sidebar.selectbox('Select City',sorted(cities))

col3,col4 = st.sidebar.columns(2)
col5,last_five = st.sidebar.columns(2)

with col3:
    current_score = st.number_input('Current Score', min_value=1, max_value=300, step=1)
with col4:
    overs = st.selectbox('Overs done(over>5)', sorted(over))
with col5:
    wickets = st.selectbox('Wickets out', sorted(wkt))
with last_five:
    last_five = st.number_input('Last Five Over Runs', min_value=1, max_value=180, step=1)

if st.button('Predict Score'):
   if batting_team == bowling_team:
        st.text("Bowling and bating team should be not be same. Please select diffrent team name")
   else:
    balls_left = 120 - (overs*6)
    wickets_left = 10 - wickets
    Current_runrate = current_score/overs

    input_df = pd.DataFrame(
     {'batting_team': [batting_team], 'bowling_team': [bowling_team],'city':city, 'current_score': [current_score],'balls_left': [balls_left], 'wickets_left': [wickets_left], 'Current_runrate': [Current_runrate], 'last_five': [last_five]})
   # st.table(input_df)
    result = pipe.predict(input_df)
    st.header("Predicted Score :  " + str(int(result[0])))
    g = df[df['city'] == city]['total_runs_x'].values[0]
    avgscore = round(g)
    p = int( round(result[0]))

   # if avgscore >= p:
   #     st.header("The predicated score is "+ str(p) + " which is lower than average score. The average score of this ground is " + str(avgscore) )
    #else:
    #    st.header( "The predicated score is " + str(p) + " which is good score for this ground. The average score of this ground is " + str(avgscore))
    if avgscore >= p + 10:
        st.metric( label="Bad Score", value=p, delta=avgscore,
                   delta_color="inverse" )
    elif avgscore >= p + 5:
        st.metric( label="Average Score", value=p, delta=avgscore,
                   delta_color="off")
    elif avgscore  <= p  <= avgscore + 5 :
        st.metric( label="Average Score", value=p, delta=avgscore,
                   delta_color="off" )
    else:
        st.metric( label="Good Score", value=p, delta=avgscore,
                   delta_color="normal" )

