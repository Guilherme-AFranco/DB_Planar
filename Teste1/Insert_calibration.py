import os
import pymysql
import dotenv
from tqdm import tqdm
import pandas as pd
from nptdms import TdmsFile

dotenv.load_dotenv()

connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
)

from planar_functions import *
from planar_new_functions import *

def insert_into_db(cursor, mean_df, table_name):
    for index, row in mean_df.iterrows():
        sql = f"INSERT INTO {table_name} (Rx00, Rx01, Rx02, Rx03, Rx04, Rx05, Rx06, Rx07, Rx08, Rx09, Rx10, Rx11, Rx12, Rx13, Rx14, Rx15) VALUES (%s, %s, %s)"
        cursor.execute(sql, (index, row['Rx00'], row['Rx01'], row['Rx02'], row['Rx03'], row['Rx04'], row['Rx05'], row['Rx06'], row['Rx07'], row['Rx08'], row['Rx09'], row['Rx10'], row['Rx11'], row['Rx12'], row['Rx13'], row['Rx14'], row['Rx15']))

def main():
    current_directory = os.getcwd()
    lista_tdms = absoluteFilePaths(current_directory + "\\A")
    calibrations_dict_path = dict_por_espessura(lista_tdms)

    lista_medias_por_espessura = []

    with connection:
        with connection.cursor() as cursor:
            for elements in tqdm(calibrations_dict_path):
                mean_df = media_calibrations_tdsm(calibrations_dict_path[elements])
                lista_medias_por_espessura.append(mean_df)
                insert_into_db(cursor, mean_df, f"A {elements}")
            connection.commit()

if __name__ == "__main__":
    main()
