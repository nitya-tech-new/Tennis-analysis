import pymysql
import pandas as pd

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='nitya',
    database='Sports'
)
cursor = conn.cursor()
def select_commands(table, what="*", column=None, where=None):
    where_querry=f"select {what}from {table} where {column}=%s",(where,)
    simple_querry=f'select {what} from {table}'
    if column == None:
        cursor.execute(simple_querry)
    else:
        cursor.execute(where_querry)
    data= cursor.fetchall()
    df= pd.DataFrame(data)
    return df
def select_join_commands(table, what="*",column=None):
    join_query = f"select {what} from {table} LEFT JOIN ranks ON competitors.competitor_id = ranks.competitor_id"
    join_group_query = f"select {what} from {table} LEFT JOIN ranks ON competitors.competitor_id = ranks.competitor_id GROUP BY Competitors.{column}"
    if column == None:
        cursor.execute(join_query)
    else:
        cursor.execute(join_group_query)
    data= cursor.fetchall()
    df= pd.DataFrame(data)
    return df
def MIN_MAX_Commands(column, table):
    cursor.execute(f"Select Min({column}) from {table} ")
    min2 = cursor.fetchone()
    cursor.execute(f"Select Max({column}) from {table} ")
    Max2 = cursor.fetchone()
    return min2, Max2
def special_query(filter):
        filter_query = f"""
        SELECT competitors.C_name, competitors.country, ranks.ranks, ranks.points
        FROM competitors
        JOIN ranks ON competitors.competitor_id = ranks.competitor_id
        WHERE {" AND ".join(filter)}
        """
        cursor.execute(filter_query)
        data_frame= cursor.fetchall()
        filtered_df = pd.DataFrame(data_frame)
        filtered_df= filtered_df.rename(columns={0: "Competitor's name", 1: 'Country', 2:"Rank", 3:"Points"})
        return filtered_df

def join_venues(table, what="*",column=None):
    join_query1 = f"select {what} from {table} LEFT JOIN venues ON complexes.complex_id = venues.complex_id"
    join_group_query1 = f"select {what} from {table} LEFT JOIN venues ON complexes.complex_id = venues.complex_id GROUP BY Competitors.{column}"
    if column == None:
        cursor.execute(join_query1)
    else:
        cursor.execute(join_group_query1)
    data= cursor.fetchall()
    df= pd.DataFrame(data)
    return df
def join_category(table, what="*",column=None):
    join_query2 = f"select {what} from {table} LEFT JOIN competitions ON categories.category_id = competitions.category_id"
    join_group_query2 = f"select {what} from {table} LEFT JOIN competitions ON categories.category_id = competitions.category_id GROUP BY Competitors.{column}"
    if column == None:
        cursor.execute(join_query2)
    else:
        cursor.execute(join_group_query2)
    data= cursor.fetchall()
    df= pd.DataFrame(data)
    return df
def spcl(enter):
    new_venue = f"""
        SELECT *
        FROM venues
        WHERE {" AND ".join(enter)}
        """
    cursor.execute(new_venue)
    data_frame= cursor.fetchall()
    filtered_df = pd.DataFrame(data_frame)
    filtered_df= filtered_df.rename(columns={0: "Venue ID", 1: "Venue's Name", 2:"City", 3:"Country",4:"County Code",5: "Timezone", 6:"Complex ID"})
    return filtered_df
def special_1(join1):
    competitions_123 = f"""
        SELECT competitions.Competition_id, competitions.competition_name, competitions.gender, competitions.type_c, categories.category_name
        FROM categories
        LEFT JOIN competitions ON categories.category_id= competitions.category_id
        WHERE {" AND ".join(join1)}
        """
    cursor.execute(competitions_123)
    data_frame= cursor.fetchall()
    filtered_df = pd.DataFrame(data_frame)
    filtered_df= filtered_df.rename(columns={0: "Competition Id", 1: "Competition Name", 2:"Gender", 3:"Type",4:"Category Name"})
    return filtered_df

