import pandas as pd
import datetime
import os

path = "C:/Users/Seni/PycharmProjects/adayofTracy/anki/filetxt"

file_names = [ str(f).replace('.txt','') for f in os.listdir(path)]
print(file_names)
for file_name in file_names:
    file_path = path + "/" + file_name + '.txt'
    with (open(file_path, 'r') as f):
        lines = f.read()

        data_str = lines.replace('\n','$').replace('$$','$').replace('$$','$').replace('\t','')
        data_str = data_str.replace('$a)', '\n').replace('$b)', '\n').replace('$c)', '\n').replace('$d)', '\n')
        data_str = data_str.replace('$B$', '\n2\n').replace('$A$','\n1\n').replace('$C$','\n3\n').replace('$D$','\n4\n')
        data_str = data_str.replace('$b$', '\n2\n').replace('$a$', '\n1\n').replace('$c$', '\n3\n').replace('$d$',
                                                                                                            '\n4\n')
        data = data_str.split('\n')
        print(data)
        print(len(data[0:-1:6]), len(data[1::6]), len(data[2::6]), len(data[3::6]), len(data[4::6]), len(data[5::6]))
        stt = [str(i)+ file_name for i in range(len(data[1::6]))]
        with pd.ExcelWriter('test.xlsx', mode='a') as writer:
            pd.DataFrame(data[0:-1:6]).to_excel('test.xlsx', sheet_name='sheet1')

        data_df = pd.DataFrame({'stt': stt,
                                'type': '',
                                'question': data[0:-1:6],
                                'answer1': data[1::6],
                                'answer2': data[2::6],
                                'answer3': data[3::6],
                                'answer4': data[4::6],
                                'key':data[5::6]
                                })
        data_df = data_df.dropna()

        file_path_csv = 'C:/Users/Seni/PycharmProjects/adayofTracy/anki/filecsv' + "/" + file_name + '.csv'
        data_df.to_csv(file_path_csv, sep = '|', index = None)




