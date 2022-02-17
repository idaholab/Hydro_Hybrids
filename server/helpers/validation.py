import pandas as pd

ALLOWED_EXTENSIONS = {'csv'}

def validate_schema(file, profile):
    """This function ensures that uploaded .csv files match the desired Hydro+Storage Tool schema. This schema is dictated by the machine learning model."""

    df = pd.read_csv(file)

    # The Energy Profile .csv has two columns, denoted in the column_names array below.
    if profile == "electricity":
        
        rows, cols = df.shape
        if(cols != 2):
            raise IndexError(f'The energy profile .csv you uploaded doesn\'t have the right number of columns. Expected 2, received {cols}')


        column_names = ['datetime', 'total hydro generation (mwh)']
        for column in df.columns.values:
            if column.lower() not in column_names:
                raise KeyError(f'The field \'{column.lower()}\' was not recognized as valid. Please ensure your data is composed by one of these fields, with units: {column_names}')


    # The Price Profile .csv has six columns, denoted in the column_names array below.
    elif profile == "price":
        
        rows, cols = df.shape
        if(cols != 6):
            raise IndexError(f'The price profile .csv you uploaded doesn\'t have the right number of columns. Expected 6, received {cols}')
        
        column_names = ['datetime', 'price: energy ($/mwh)', 'price: regup ($/mwh)', 'price: regdn ($/mwh)', 'price: spin ($/mwh)', 'price: nonspin ($/mwh)',]
        for column in df.columns.values:
            if column.lower() not in column_names:
                raise KeyError(f'The field \'{column.lower()}\' was not recognized as valid. Please ensure your data is composed by one of these fields, with units: {column_names}')

        
def allowed_extensions(filename):
    """This function ensures that only .csv files, as written in 'ALLOWED_EXTENSIONS' are passed through to the machine learning model."""

    file_ext = filename.rsplit('.', 1)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise TypeError(f'Only comma separated value (.csv) files are allowed to be uploaded as Energy Generation and Price Profiles. Received: .{file_ext}')
