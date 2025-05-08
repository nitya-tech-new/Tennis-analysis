import streamlit as st
import pandas as pd
import pymysql 
from PIL import Image 
import data_structure as ds
# Connect to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='nitya',
    database='Sports'
)
cursor = conn.cursor()
def querry(a, b, c):
    query_str = f"SELECT * FROM {a} WHERE {b} = %s"
    cursor.execute(query_str, (c,))
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    return df

st.sidebar.title(":tennis: Navigation")
page = st.sidebar.radio("Go to", [
    ":house: Homepage Dashboard",
    " Search & Filter Competitors",
    ":clipboard: Competitor Details Viewer",
    "🌍 Country-Wise Analysis",
    ":trophy: Leaderboards",
    "Venues and complexes",
    "Categories and Competitions"
])

if page == ":house: Homepage Dashboard":
    st.title(":tennis: Sports Analysis ")
    st.write ("This Application helps user Visualize the distribution of events by type, gender, and competition level and allows user to analyze player participation across singles and doubles events with data-driven insights to event organizers or sports bodies for resource allocation")
elif page == " Search & Filter Competitors":
    st.title("Search and Filter Competitors")
    name_query = st.text_input("Search by Name")
    MIN1, Max1 = ds.MIN_MAX_Commands("ranks","ranks")
    rank_range = st.slider("Rank Range", min_value=MIN1[0], max_value=Max1[0], step=1)

    cursor.execute("Select country from competitors")
    country_list = cursor.fetchall()
    df = ds.select_commands("competitors", "country")
    country_filter = st.multiselect("Filter by Country", options=df[0].unique())
    
    MIN2,Max2 = ds.MIN_MAX_Commands("points", "ranks")
    points_threshold = st.slider("Minimum Points", MIN2[0], Max2[0], 900)
      # Add a button to apply the filters
    if st.button('Filter Results'):
        # Build the SQL query with applied filters
        filters = []
        if name_query:
            filters.append(f"competitors.C_name LIKE '%{name_query}%'")
        if country_filter:
            countries_str = ",".join(f"'{c}'" for c in country_filter)
            filters.append(f"competitors.country IN ({countries_str})")
        filters.append(f"ranks.ranks BETWEEN {1} AND {rank_range}")
        filters.append(f"ranks.points >= {points_threshold}")
        filtered_df = ds.special_query(filters)
        
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.write("No competitors match your filters.")
    # Initializing the dataframe based on the filters
    dataframe1 = pd.DataFrame()
    st.dataframe(dataframe1)

# 📋 Competitor Details Viewer
elif page == ":clipboard: Competitor Details Viewer" :
    st.title(":clipboard: Competitor Details Viewer")
    competitor1= ds.select_commands("competitors","C_name")
    selected_name = st.selectbox("Select Competitor", competitor1)
    data_comp=querry("competitors", "C_name", selected_name)
    st.dataframe(data_comp)
elif page == "🌍 Country-Wise Analysis":
    st.title("🌍 Country-Wise Analysis")
    country_stats=ds.select_join_commands("Competitors", ("competitors.Country, COUNT(competitors.C_name) AS Total_Competitors, ROUND(AVG(ranks.Points), 2) AS Average_Points"), "Country")
    country_stats=country_stats.rename(columns={0: "Country", 1:"Total Competitors", 2:"Average Points"})
    st.dataframe(country_stats)
   
    st.bar_chart(
        country_stats.set_index("Country")[["Total Competitors"]],
        use_container_width=True
    )
    st.write("Rank display chart above")
    st.line_chart(
        country_stats.set_index("Country")[["Average Points"]],
        use_container_width=True
    )
    st.write("Average points chart display above")
    
elif page == ":trophy: Leaderboards":
    st.title("Leaderboards")
    rank_leaderboard= ds.select_join_commands("competitors","ranks.ranks, competitors.C_name")
    rank_leaderboard=rank_leaderboard.rename(columns={0: "Ranks", 1:"Competitor's name"})
    st.subheader("Top-Ranked Competitors")
    top_ranked = rank_leaderboard.sort_values(by="Ranks").head(10)
    st.dataframe(top_ranked)
    top_point_board=ds.select_join_commands("competitors","ranks.points, competitors.C_name")
    top_point_board=top_point_board.rename(columns={0: "Points", 1:"Competitor's name"})
    st.subheader("Highest Points Scored")
    top_points = top_point_board.sort_values(by="Points", ascending=False).head(10)
    st.dataframe(top_points)
elif page== "Venues and complexes":
    st.title("Venues and complexes")
    name_query1 = st.text_input("Search by Name of venue ")
    df = ds.select_commands( "venues", "country_name")
    country_filter2 = st.multiselect("Filter by Country", options=df[0].unique())
    code_query = st.text_input("Search by code of country ")
      # Add a button to apply the filters
    if st.button('Venues'):
        # Build the SQL query with applied filters
        venues_list = []
        if name_query1:
            venues_list.append(f"venue_name LIKE '%{name_query1}%'")
        if country_filter2:
            countries_str = ",".join(f"'{c}'" for c in country_filter2)
            venues_list.append(f"country_name IN ({countries_str})")
        if code_query:
            venues_list.append(f"venues.country_code LIKE '%{code_query}%'")
        filtered_df = ds.spcl( venues_list)
        
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.write("No competitors match your filters.")
    # Initializing the dataframe based on the filters
    dataframe1 = pd.DataFrame()
    st.dataframe(dataframe1)
elif page== "Categories and Competitions":
    st.title("Categories and Competitions")
    name_query1 = st.text_input("Search by Name of Competition ")
    df = ds.select_commands( "competitions", "Type_c")
    country_filter2 = st.multiselect("Filter by type", options=df[0].unique())
    code_query = st.text_input("Category name : ")
      # Add a button to apply the filters
    if st.button('category'):
        # Build the SQL query with applied filters
        comp_list1 = []
        if name_query1:
            comp_list1.append(f"competition_name LIKE '%{name_query1}%'")
        if country_filter2:
            countries_str = ",".join(f"'{c}'" for c in country_filter2)
            comp_list1.append(f"type_c IN ({countries_str})")
        if code_query:
            comp_list1.append(f"Category_names LIKE '%{code_query}%'")
        filtered_dfa = ds.special_1( comp_list1)
        
        if not filtered_dfa.empty:
            st.dataframe(filtered_dfa)
        else:
            st.write("No competitors match your filters.")
        st.dataframe(comp_list1)
