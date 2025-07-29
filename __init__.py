import pandas as pd

class Load:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath, index_col=0)

    def data(self):
        return self.df

    # check shape of the data
    def shape(self):
        print('----------------Shape of the Dataset---------------- \n')
        return self.df.shape
    
    # check features in the data
    def features(self):
        print('----------------Features in the Dataset---------------- \n')
        print(self.df.columns)
        
    # Check summary statistics
    def stats(self):
        print('----------------Summary Statistics of the Features---------------- \n')
        print(self.df.describe()) 
    
    # check info on dataset
    def info(self):
        print('----------------Dataset Overall Information---------------- \n')
        print(self.df.info())
     
    
class Clean(Load):
    def __init__(self, loader: Load):
        self.df = loader.df
    
    # check for missing values percentage
    def duplicates(self):
        count = self.df.duplicated().sum()
        percentage = (count / len(self.df)) * 100
        
        if count > 0:
            print (f"The dataset has {count} duplicated rows, which are {percentage:.2f}% of the total data.")
            print("\n Removing duplicates...")
            self.df.drop_duplicates(inplace=True)
            print("\n  Duplicates dropped.")
        else:
            print("The dataset has no duplicated rows.")
        
    def check_extraneous(self):
        # Check for extraneous values in each column
        for col in self.df.columns:
            print(f"Column: {col}, \n  Unique Values: \n {self.df[col].value_counts()} \n")
            
    def replace_extraneous(self, placeholder='-'):
        for col in self.df.columns:
            if placeholder in self.df[col].values:
                print(f'Extraneous value found in column {col}: {placeholder}')
                print(f'\n Cleaning {col} column... \n')
                count = (self.df[col] == placeholder).sum()
                self.df[col] = self.df[col].replace(placeholder, 'no-service')
                print(f"\n Replaced {count} occurrences of '{placeholder}' in column '{col}' with 'no-service'. \n")
                
    def binary_check(self):
        cols = ['is_ftp_login', 'is_sm_ips_ports']
        
        for col in cols:
            if self.df[col].nunique() == 2:
                print(f"\n Column '{col}' has only binary values.")
            else:
                print(f"Extra values found in '{col}': {self.df[col].unique()} \n")
                print(f'\n Cleaning {col} column... \n')
                self.df = self.df[self.df[col].isin([0, 1])]
                print(f'\n {col} column cleaned.')
