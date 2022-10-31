#Create a function that takes in a DataFrame as input parameter and plots a barplot with the columns that have missing values. Put this function into a file called data_utils.py.
#When you come across more useful functions, you can store them in your data_utils module. 


def plot_null_columns(df) -> None:
    """Skapar ett stapeldiagram med staplar för alla kolumner med NaN-värden"""
    import seaborn as sns
    # Kolumner med null-värden
    nullkolumner = df.columns[df.isnull().sum() > 0]
    
    # Antalet null-värden i varje kolumn
    antal_null = df[nullkolumner].isnull().sum()

    # Plotta 
    ax = sns.barplot(x= nullkolumner, y= antal_null)
    ax.set_title("Null värden/ NaN Values" ) 
    ax.set_xlabel("Kolumn")
    ax.set_ylabel("Antal")