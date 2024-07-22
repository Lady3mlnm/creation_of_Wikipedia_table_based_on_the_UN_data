import pandas as pd


def compare_lists(ls_1, ls_2, sep=', '):
    '''
    The function compares two lists and finds unique elements in them
    ls_1: list
    ls_2: list
    sep: str
        separator used for formatting of printing elements
    return: None (result is printed as text)
    '''
    ls_1_unique = [el for el in ls_1 if el not in ls_2]
    print("Number of elements in list_1:", len(ls_1))
    print("Unique elements in list_1:")
    print(*ls_1_unique, sep=sep)
    print()
    
    ls_2_unique = [el for el in ls_2 if el not in ls_1]
    print("Number of elements in list_2:", len(ls_2))
    print("Unique elements in list_2:")
    print(*ls_2_unique, sep=sep)


def min_and_max_values(df, *, nmb=3, prec=2, max_lng=11, row_center=None, shorten=False):
    '''
    The functions shows values in with maximum and minimum values in each column of dataframe wiht indication of the record name to that this value belongs.
    df: dataframe
    nmb: int
        number of maximal and minimal elements to show
    prec: int
        precision of values
    max_lng: int
        maximum number of letters in the record name
    row_center: str, series or None
        name of record that will be shown in middle, or separate series with identical columns. If you use series than there have not to be a record with the same name in the dataframe. If None, there will be shown nothing.
    shorten: bool
        Whether the program should shorten some long names in output, e.g. 'Hong Kong SAR, China' → 'Hong Kong'.
        Positive side effect: the function works correctly if DataFrame has long country names but the passed parameter 'row_center' contain a short country name.
    return: dataframe
    '''

    print(f"Number of records: {len(df)}")
    
    # if the user wants to see in output short country names
    if shorten:
        dd_shorten = {
            'Hong Kong SAR, China' : 'Hong Kong',
            'Hong Kong, China' : 'Hong Kong',
            'Macao SAR, China' : 'Macao',
            'Macao, China' : 'Macao',
            'Taiwan, China': 'Taiwan',
            'United States': 'USA',
            'United Kingdom': 'UK',
            'United Arab Emirates': 'UAE',
            'Central African Republic': 'CAR',
            'South Korea': 'S. Korea',
            'North Korea': 'N. Korea',
            'South Africa': 'S. Africa',
            'South Sudan': 'S. Sudan',
            'Western Sahara': 'W. Sahara'
        }
        
        df = df.copy().rename(index = dd_shorten)
        if isinstance(row_center, str):
            row_center = dd_shorten.get(row_center, row_center)
        elif isinstance(row_center, list):
            row_center = [dd_shorten.get(region, region) for region in row_center]

            
    def find_largests(df):
        t_df = df.nlargest(nmb)
        t_df = t_df.reset_index()
        return t_df.apply(lambda v: f"{round(v.iloc[1], prec)} -{v.iloc[0] if len(v.iloc[0])<=max_lng else v.iloc[0][:max_lng-1]+'…'}", axis=1)

    def find_smallests(df):
        t_df = df.nsmallest(nmb).iloc[::-1]
        t_df = t_df.reset_index()
        return t_df.apply(lambda v: f"{round(v.iloc[1], prec)} -{v.iloc[0] if len(v.iloc[0])<=max_lng else v.iloc[0][:max_lng-1]+'…'}", axis=1)
    
    # Depending on type of the variable 'row_center', there are various ways to form output dataFrame
    if isinstance(row_center, list):
        df_center = df.loc[row_center] \
                      .applymap(lambda v: f" – {round(v, prec)} –")
        final_df = pd.concat([df.apply(find_largests), df_center, df.apply(find_smallests)])
        final_df.index = ['max'] + [f'max_{n}' for n in range(2, nmb+1)] + df_center.index.to_list() + [f'min_{n}' for n in range(nmb, 1, -1)] + ['min']
    elif isinstance(row_center, str) or isinstance(row_center, pd.Series):
        ser_center = (df.loc[row_center] if isinstance(row_center, str) else row_center) \
                        .map(lambda v: f" — {round(v, prec)} —")
        final_df = pd.concat([df.apply(find_largests), ser_center.to_frame().T, df.apply(find_smallests)])
        final_df.index = ['max'] + [f'max_{n}' for n in range(2, nmb+1)] + [ser_center.name] + [f'min_{n}' for n in range(nmb, 1, -1)] + ['min']
    elif row_center is None:
        final_df = pd.concat([df.apply(find_largests), df.apply(find_smallests)])
        final_df.index = ['max'] + [f'max_{n}' for n in range(2, nmb+1)] + [f'min_{n}' for n in range(nmb, 1, -1)] + ['min']
    else:
        raise TypeError("Parameter row_center has wrong type")
    
    return final_df.style.set_properties(**{'text-align': 'left'})