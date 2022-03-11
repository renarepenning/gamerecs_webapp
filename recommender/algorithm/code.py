"""https://github.com/renarepenning/VideoGameRecommender/tree/main/Algorithm_Current"""

import pandas as pd
import numpy as np
import os
import threading
import time

""" MATT'S CODE AS OF 3/11 """
#df = pd.read_csv('C:/Users/Trader00/Downloads/IGDB_games.csv').set_index('id')
df = pd.read_csv("recommender/algorithm/IGDB_games.csv").set_index('id')
test = df.iloc[5005]

master_cols = ['genres', 'themes', 'game_modes','tags', 'platforms', 'keywords']

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

def get_input(game):
    print("CALL GET INPUT")
    try:
        return df[df['name'] == game].iloc[0]
    except:
        print('ERROR - get input')

   
def transform(columns, test, df=df):
    print("CALL TRANSFORM")
    df = df.set_index("name")
    df['name'] = df.index
    
    master = pd.DataFrame(columns=df.index.tolist(),
                          index=df.index.tolist())    
    out_columns = ['name']
    df['Columns Counted'] = 0
    start = time.time()
    for col in columns:
        col_name = col + ' score'
        out_columns.append(col_name)
        df[col_name] = 0
        try:
            ser = transform_column(test, col, df=df)
            df[col_name] = ser

        except:
            pass
    col_map = list(map(lambda x: x + ' score', columns))
    df['Total'] = df[col_map].sum(axis=1)
    end = time.time() - start
    print('Transform Time', end)
    return df[out_columns + ['Total']]

def save_file(game, columns:list, df:pd.DataFrame=df):
    if not os.path.exists("Saver"):
        os.mkdir('Saver')
    
    try:
        row = get_input(game)
    except:
        print(game, 'ERROR - get input')
   

    df = transform(columns, row)
    df.to_csv(f'Saver/{game}.csv')



def multiple_games(games:list, df=df, columns:list=['genres', 'themes', 'game_modes','tags', 'platforms', 'keywords']):
    #print(df.name.tolist())
    SAVE_DIR = 'Saver'
    """if os.path.exists(SAVE_DIR):
        for file in os.listdir(SAVE_DIR):
            os.remove(os.path.join(SAVE_DIR, file))
        os.rmdir(SAVE_DIR)
    """
    if not os.path.exists(SAVE_DIR):
        print("ERRor - path")
        os.mkdir(SAVE_DIR)
    threads = list()
   
    for game in games:
        print(game)
        #save_file(game, columns, df)
        
        x = threading.Thread(target=save_file, args=(game, columns, df,))
        threads.append(x)
        x.start()
        
    for thread in threads:
        thread.join()
    if len(games) == 1:
        master = pd.read_csv(f'Saver/{games[0]}.csv')['Total']
    else:
        master = pd.read_csv(f'Saver/{games[0]}.csv')['Total']
        
    for game in games[1:]:
        print(pd.read_csv(f'Saver/{game}.csv')['Total'].sort_values())
        print(f'Saver/{game}.csv')
        master = master + pd.read_csv(f'Saver/{game}.csv')['Total']

    print(master.sort_values())
    return master


def preprocess(df:pd.DataFrame, columns=master_cols):
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
        #save_file(game, columns)
    for thread in threads:
        thread.join()
    
    end = time.time() - start
    print('Start to Finish', end, 'Seconds')
    print('Average Time per sample', end/len(df), 'Seconds')
    
    
    
#out = save_file('Out of the Park Baseball 12', master_cols)

#print(out)


#preprocess(df.iloc[125:130])
#save_file()
#print(get_input('Out of the Park Baseball 12'))

#print(transform(master_cols, get_input('Out of the Park Baseball 12')))

# Pandas DataFrame of IGDB games
def build_ul(df=df):
    front = '''<li><a href="#">'''
    back = '''</a></li>'''
    with open('C:/Users/Trader00/Downloads/UL File.txt', 'x') as f:
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
        
        
#build_ul(df)

"""multiple_games(games=['Spy Snatcher', 'Mirage', 'Boom Brothers', 'Minecraft Starter Collection',
                      'Siesta Fiesta'])"""

def cleanOutput(output):
    return output.iloc[:-2, 0][0:6] # series

def getRec(game):
    print("call GET REC")
    rec = transform(master_cols, get_input(game))
    print("OUTPUT RETURNING ", type(rec))
    """ # testing
    with open('readme.txt', 'w') as f:
        f.write(rec)"""

    return cleanOutput(rec)