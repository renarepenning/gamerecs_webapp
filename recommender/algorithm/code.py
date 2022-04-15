"""https://towardsdatascience.com/set-up-heroku-postgresql-for-your-app-in-python-7dad9ceb0f92"""
import pandas as pd
import numpy as np
import os
import threading
import time
import psycopg2
import sys
# WHITE DB
DATABASE_URL = "postgres://jfqbocymbesqkd:b0bdc1a7ecbf26b512954e7620a57c186be91d88ef9aee30a6ae12913b986d00@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d6ula8hn40666q"
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()
# query 
query = f"""SELECT * FROM public."dataframe";"""
# return results as a dataframe
df = pd.read_sql(query, con)#.set_index('id')
# print("cols:", df.columns)
master_cols = ['genres', 'themes', 'game_modes', 'tags', 'platforms', 'keywords']#, 'Indie']

"""indie_df = pd.read_csv("recommender/algorithm/igdb_indie.csv").set_index('id')
indie_df['Indie'] = '[1]'
#df = pd.read_csv('recommender/algorithm/IGDB_games.csv').set_index('id')
df['Indie'] = indie_df['Indie']
df['Indie'].fillna('[0]', inplace=True)"""


def conjunction(lst1, lst2):
    return list(set(lst1) & set(lst2))


def disjunction(lst1, lst2):
    return list(set(set(lst1) | set(lst2)))


def clean(array):
    try:
        array = array.split('[')[1].split(']')[0].split(', ')
    except:
        print(array)
    return list(map(lambda x: int(x), array))


def transform_column(target, column, df=df):
    start = time.time()
    test = clean(target[column])
    clean_time = time.time()
    print('Singular Clean Time', clean_time - start)
    col = df[column].dropna().apply(clean)
    clean_col_time = time.time() - clean_time
    print('Column Clean Time', clean_col_time)
    func = lambda x: conjunction(x, test)
    conj = col.apply(func)
    func = lambda x: disjunction(x, test)
    disj = col.apply(func)
    score = conj.apply(lambda x: len(x)) / disj.apply(lambda x: len(x))
    score_time = time.time() - clean_time - clean_col_time
    print('Score Time', score_time)

    return score


def get_input(game, df=df):
    """try:
        df = df[df['name'] == game].iloc[0]
        df['Indie'] = '[1]'
        return df
    except:
        print('ERR -- Get Input')"""
    try:
        return df[df['name'] == game].iloc[0]
    except:
        print('ERR - getinput')


def transform( test, columns=master_cols, df=df):
    df = df.set_index("name")
    df['name'] = df.index

    master = pd.DataFrame(columns=df.index.tolist(),
                          index=df.index.tolist())
    out_columns = ['name']
    df['Columns Counted'] = 0
    start = time.time()
    df['Total'] = 0
    master = df[['Total']]
    out_cols = list()
    for col in columns:

        try:
            ser = pd.DataFrame(transform_column(test, col, df=df))
            master = master.join(ser)
            out_cols.append(col)
        except:
            #print("ERR -- ", col)
            pass
    weights = np.random.dirichlet(np.ones(len(columns)), size=1)[0]

    weight_dict = {}
    print("TEST ", test)
    weight_dict['Game'] = test.name
    for index, weight in enumerate(weights):
        weight_dict[columns[index]] = weight
        try:
            master[columns[index]] = master[columns[index]] * weight
        except:
            pass

    master = master[out_cols]

    wdf = pd.DataFrame(pd.Series(weight_dict)).T
    if 'HistoricalData.csv' not in os.listdir():
        wdf.to_csv("HistoricalData.csv")
       
    else:
        pdf = pd.read_csv('HistoricalData.csv', index_col=0)
        pdf = pdf.append(weight_dict, ignore_index=True)
        pdf.to_csv('HistoricalData.csv')
        print(pdf)
   
    #print(pd.DataFrame(master))
    master['Total'] = master.sum(axis=1)
    end = time.time() - start
    print('Transform Time', end)
    master = master.drop(test.loc['name'])
    return master.sort_values('Total'), weight_dict


def get_game(game:str or list, num=6):
    if type(game) == str:
        test = get_input(game)
        df, weights = transform(test)
        return df.sort_values('Total', ascending=False).head(num).index.tolist(), weights
    else:
        df, weights = multiple_games(game)
        return df.head(num).index.tolist(), weights
def save_file(game, columns: list, df: pd.DataFrame = df):
    if not os.path.exists("Saver"):
        os.mkdir('Saver')

    try:
        row = get_input(game)
        df = transform(row)
        df.to_csv(f'Saver/{game}.csv')


    except:
        print(game, ' ERR')


def multiple_games(games: list, df=df,
                   columns: list = ['genres', 'themes', 'game_modes', 'tags', 'platforms', 'keywords'],
                   num=6):
    # print(df.name.tolist())
    SAVE_DIR = 'Saver'
    """if os.path.exists(SAVE_DIR):
        for file in os.listdir(SAVE_DIR):
            os.remove(os.path.join(SAVE_DIR, file))
        os.rmdir(SAVE_DIR)
    """
    if not os.path.exists(SAVE_DIR):
        print("ERR")
        os.mkdir(SAVE_DIR)
    threads = list()
    master = pd.DataFrame(index=df['name'], columns=['Total'])
    master['Total'] = 0
    for game in games:
        print(game)
        # save_file(game, columns, df)

        x = threading.Thread(target=save_file, args=(game, columns, df,))
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()

    for game in games:
        pdf = pd.DataFrame(pd.read_csv(f'Saver/{game}.csv',index_col=0)['Total'])
        pdf[game] = pdf['Total']
        master = master.join(pdf[[game]])

    master['Total'] = master.sum(axis=1)
    return master[['Total']].sort_values('Total', ascending=False)


def preprocess(df: pd.DataFrame, columns=master_cols):
    df = df.set_index("name")
    df = df[columns]
    df['name'] = df.index
    master = pd.DataFrame(columns=df.index.tolist(),
                          index=df.index.tolist())
    start = time.time()
    threads = list()

    for game in df.index:
        x = threading.Thread(target=save_file, args=(game, columns))
        threads.append(x)
        x.start()
        print(game)
        # save_file(game, columns)
    for thread in threads:
        thread.join()

    end = time.time() - start
    print('Start to Finish', end, 'Seconds')
    print('Average Time per sample', end / len(df), 'Seconds')

def formatOutput(recs):
    outputStr = "\n\n"
    for i in range(1, len(recs)):
        outputStr += str(i) + ". " + recs[i] + "\n\n"
    return outputStr

def getRec(game):
    games, weights = get_game(game)
    return formatOutput(games)

# # Pandas DataFrame of IGDB games
# def build_ul(df=df):
#     front = '''<li><a href="#">'''
#     back = '''</a></li>'''
#     with open(PATH_TO_DATA, 'x') as f:
#         f.write('''<ul id="myUL">\n''')
#         print('''<ul id="myUL">''')
#         for game in df.name.tolist():
#             try:
#                 line = '\t' + front + game + back + '\n'
#                 print(line)
#                 f.write(line)
#             except:
#                 pass

#         f.write('</ul>')
#         print('</ul>')
#         f.close()

