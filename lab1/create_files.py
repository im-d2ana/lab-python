import random
import pandas as pd
from concurrent.futures import ProcessPoolExecutor as Pool

FILES = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv', 'file5.csv']

def create_data():
    lst = ['A', 'B', 'C', 'D']
    data_lst = []
    for i in range(50):
        elem = [random.choice(lst), random.random()]
        data_lst.append(elem)
    return data_lst

def create_csv(data: list, file_name: str):
    df = pd.DataFrame(data, columns=['category', 'value'])
    df.to_csv(file_name, index=False)

def process_file(file_name: str):
    lst = create_data()
    return create_csv(lst, file_name)

def main():
    with Pool() as executor:
        executor.map(process_file, FILES)

if __name__ == '__main__':
    main()