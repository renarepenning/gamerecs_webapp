"""https://towardsdatascience.com/set-up-heroku-postgresql-for-your-app-in-python-7dad9ceb0f92"""
import pandas as pd
import numpy as np
import os
import threading
import time
import psycopg2
import sys
# WHITE DB -- Polished
global OUTPUT
OUTPUT = ""
DATABASE_URL = "postgres://jfqbocymbesqkd:b0bdc1a7ecbf26b512954e7620a57c186be91d88ef9aee30a6ae12913b986d00@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d6ula8hn40666q"
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()
# query 
query = f"""SELECT * FROM public."dataframe";"""
# return results as a dataframe
df = pd.read_sql(query, con)#.set_index('id')

master_cols = ['genres', 'themes', 'game_modes', 'tags', 'platforms', 'keywords']#, 'Indie']

indie_df = pd.read_csv("recommender/algorithm/igdb_indie.csv")#.set_index('id')
indie_df['Indie'] = '[1]'
df['Indie'] = indie_df['Indie']
df['Indie'].fillna('[0]', inplace=True)


def conjunction(lst1, lst2):
    return list(set(lst1) & set(lst2))


def disjunction(lst1, lst2):
    return list(set(set(lst1) | set(lst2)))


def clean(array):
    try:
        #array = array.split('[')[1].split(']')[0].split(', ')
        array = array.split(', ')
    except:
        print(array)
    return list(map(lambda x: int(x), array))


def transform_column(target, column, df=df):
    global OUTPUT
    start = time.time()
    test = clean(target[column])
    clean_time = time.time()
    o1 = ' -- Singular Clean Time: ' + str("{:.2f}".format(clean_time - start)) + '\n'
    print(o1)
    col = df[column].dropna().apply(clean)
    clean_col_time = time.time() - clean_time
    o2 = ' Column Clean Time: ' + str("{:.2f}".format(clean_col_time)) + '\n'
    print(o2)
    func = lambda x: conjunction(x, test)
    conj = col.apply(func)
    func = lambda x: disjunction(x, test)
    disj = col.apply(func)
    score = conj.apply(lambda x: len(x)) / disj.apply(lambda x: len(x))
    score_time = time.time() - clean_time - clean_col_time
    o3 = ' Score Time: ' + str("{:.2f}".format(score_time)) + '\n'
    print(o3)
    # OUTPUT += o1 + o2 + o3

    return score


def get_input(game, df=df):
    try:
        df = df[df['name'] == game].iloc[0]
        df['Indie'] = '[1]'
        return df
    except:
        print('ERR -- Get Input')
    # print("GET INPUT")
    # try:
    #     # print("looking for name column.....")
    #     return df[df['name'] == game].iloc[0]
    # except:
    #     print('ERR - getinput')


def transform( test, columns=master_cols, df=df):
    global OUTPUT
    df = df.set_index("name")
    df['name'] = df.index
    # print("got name")
    master = pd.DataFrame(columns=master_cols,
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
    print("before historical data")
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
    o1 = ' Transform Time: ' + str("{:.2f}".format(end)) + '\n'
    print(o1)
    OUTPUT += o1
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



"""
Possible future add on
"""
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
    global OUTPUT
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
    out1 = 'Start to Finish: ' + str("{:.2f}".format(end)) + 'Seconds\n'
    out2 = 'Average Time per sample: ' + str("{:.2f}".format(end / len(df))) + 'Seconds\n'
    print(out1)
    print(out2)
    OUTPUT += out1 + out2

def formatOutput(recs):
    outputStr = "\n\n"
    for i in range(1, len(recs)):
        outputStr += str(i) + ". " + recs[i] + "\n\n"
    return outputStr

def getRec(game):
    games, weights = get_game(game)
    return formatOutput(games), OUTPUT


"""
USED FOR TESTING
"""
def build_ul(df=df):
    front = '''<li><a href="#">'''
    back = '''</a></li>'''
    with open("PATH_TO_DATA", 'x') as f:
        f.write('''<ul id="myUL">\n''')
        print('''<ul id="myUL">''')
        for game in df.name.tolist():
            try:
                line = '\t' + front + game + back + '\n'
                print(line)
                f.write(line)
            except:
                pass

        f.write('</ul>')
        print('</ul>')
        f.close()
def save_file(game, columns: list, df: pd.DataFrame = df):
    if not os.path.exists("Saver"):
        os.mkdir('Saver')
    try:
        row = get_input(game)
        df = transform(row)
        df.to_csv(f'Saver/{game}.csv')
    except:
        print(game, ' ERR')
