import pandas as pd
with open('C:\\Users\\thuylt15\\PycharmProjects\\aday\\anki\\the_atmostphere.txt', 'r') as f:
    lines = f.readlines()

    data = [line.strip() for line in lines if line.strip()!='']

    print(data)
    questions = data[0::6]
    col2 = data[1::6]
    col3 = data[2::6]
    col4 = data[3::6]
    col5 = data[4::6]
    answers = data[5::6]
    print(len(questions))
    print(len(col2))
    print(len(col3))
    print(len(col4))
    print(len(col5))
    print(len(answers))
    print(questions[-2:])
    df = pd.DataFrame({'question': questions,
                       'col2': col2,
                       'col3': col3,
                       'col4': col4,
                       'col5': col5,
                       'answer': answers})
    df.head()

