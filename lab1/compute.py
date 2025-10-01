import pandas as pd
from concurrent.futures import ProcessPoolExecutor as Pool

FILES = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv', 'file5.csv']

def read_csv(file: str):
    df = pd.read_csv(file, sep=',')
    return df

def compute_median_std(df: pd.DataFrame):
    A_list, B_list, C_list, D_list = [], [], [], []
    for i in range(len(df)):
        if df.loc[i, 'category'] == 'A':
            A_list.append([df.iloc[i, 0], float(df.iloc[i, 1])])
        elif df.loc[i, 'category'] == 'B':
            B_list.append([df.iloc[i, 0], float(df.iloc[i, 1])])
        elif df.loc[i, 'category'] == 'C':
            C_list.append([df.iloc[i, 0], float(df.iloc[i, 1])])
        else:
            D_list.append([df.iloc[i, 0], float(df.iloc[i, 1])])
    
    A_df = pd.DataFrame(A_list, columns=['category', 'value'])
    B_df = pd.DataFrame(B_list, columns=['category', 'value'])
    C_df = pd.DataFrame(C_list, columns=['category', 'value'])
    D_df = pd.DataFrame(D_list, columns=['category', 'value'])

    result = []
    result.append(['A', A_df['value'].median(), A_df['value'].std()])
    result.append(['B', B_df['value'].median(), B_df['value'].std()])
    result.append(['C', C_df['value'].median(), C_df['value'].std()])
    result.append(['D', D_df['value'].median(), D_df['value'].std()])
    result_df = pd.DataFrame(result, columns=['category', 'median', 'std'])

    return result_df

def process_file(file: str):
    df = read_csv(file)
    return compute_median_std(df)

def main():
    with Pool(max_workers=5) as executor:
        results = list(executor.map(process_file, FILES))

    print('Вычисления для каждого файла:')
    for res in results:
        print(res)
        print()

    df = pd.concat(results, ignore_index=True)
    final_df = compute_median_std(df)
    print('Итоговые вычисления:')
    print(final_df)


if __name__ == '__main__':
    main()