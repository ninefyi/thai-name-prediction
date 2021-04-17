import pandas as pd

df_db = pd.read_csv(u'db.csv')
df_input = pd.read_csv(u'input.csv')
df_number = pd.read_csv(u'number.csv')

def read_char_score(val: str):
    score = 0
    df_f = df_db[df_db['char'].str.contains(val, na=False)]
    found_index = len(df_f.index)
    if df_f is not None and found_index > 0:
        score = df_f.iloc[0]['score']
    return score

def read_tone_score(val: str):
    score = 0
    df_f = df_db[df_db['tone'].str.replace('อ','').str.contains(val, na=False)]
    found_index = len(df_f.index)
    if df_f is not None and found_index > 0:
        score = df_f.iloc[0]['score']
    return score

def translate_score_to_name(score: int):
    title = ''
    desc = ''
    df_n = df_number[df_number['number'] == score]
    found_index = len(df_n.index)
    if df_n is not None and found_index > 0:
        title = df_n.iloc[0]['title']
        desc = df_n.iloc[0]['desc']
        level = df_n.iloc[0]['level']
    
    return [f"{title}: {desc}", level]

def calculate_score(val: str):
    score = 0
    for v in val:
        char_score = 0
        tone_score = 0
        char_score = read_char_score(v)
        score = score + char_score
        if char_score == 0:
            tone_score = read_tone_score(v)
            score = score + tone_score
            # print(f"{v}={tone_score}, ", end='')
        else:
            pass
            # print(f"{v}={char_score}, ", end='')
    # if score == 27 or score == 50 or score == 28:
    #     print(f"{val}={score}")
    return score

def highlight_good_meaning(data):
    # is_max = s.loc[column] > threshold
    return ['color: yellow' for v in data]

name_list = []
for input in df_input.itertuples():
    total = 0
    sname_desc = ''
    fname_desc = ''
    sname_level = 0
    fname_level = 0
    # print(f"{input.name}, {input.surname}", end='')
    
    name_total = calculate_score(input.name)
    sname_total = calculate_score(input.surname)
    fname_total = name_total + sname_total

    [sname_desc, sname_level] = translate_score_to_name(sname_total)
    [fname_desc, fname_level] = translate_score_to_name(fname_total)
    
    name = {
        'name': input.name,
        'name_score': name_total,
        'surname': input.surname,
        'surname_score': sname_total,
        'full_score': fname_total,
        'surname_desc': sname_desc,
        'full_desc' : fname_desc,
        'sname_level': sname_level,
        'fname_level': fname_level
    }
    # print(name)
    name_list.append(name)
    # print("")
df = pd.DataFrame(name_list)
df.columns =['name', 'name_score', 'surname', 'surname_score', 'full_score', 'surname_desc', 'full_desc', 'sname_level', 'fname_level']

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

df.to_excel(writer, sheet_name='Naming', index=False)

worksheet = writer.sheets['Naming']

format = writer.book.add_format({'bg_color': 'yellow'})

for row in df.itertuples():
    rowNumber = row.Index+2
    if row.fname_level == 0:
        columns = f"A{rowNumber}:J{rowNumber}"
        worksheet.conditional_format(columns, {'type': 'no_blanks', 'format': format})

writer.save()