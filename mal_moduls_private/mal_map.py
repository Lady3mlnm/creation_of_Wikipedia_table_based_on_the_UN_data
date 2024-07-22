import pandas as pd


def bin_values_in_dataframe(df, selected_col, *, step=None, prec=2, fn_bin=None, tp_combine_bins=None):
    '''
    The function looks at vulues in one of columms in dataframe and assigns to these values bins/ranges (that will be used in legend on map)
    df: dataframe
    selected_col: name of column in dataframe
    step: one of values 0.5, 1, 2, None
        determs width of bins. In it is None than function fn_bin have to be given.
    prec: integer >=1
        presicion of the second value in legend record
    fn_bin: function
        Function that make binning. These function is required only if step in None or unexpected
    tp_combine_bins: tuple in the form (('5.0–5.49', '5.5–5.99'), '5.0–5.99') or None
        this tuple allows to combine several bins into one bin
    return: two-column dataframe
        The first column contains values in alanysed column. The second columns range to that these values belong
    '''
    
    # get only selected column
    filtered_df = df.loc[:, [selected_col]]   \
                    .sort_values(by=selected_col, ascending=False)

    # depending on step, use different functions for assingning values to bins
    if step == 0.5:
        addition = float("0.499999"[:prec+2])
        fn_bin = lambda x: f"{x * 4 // 2 / 2:.1f}–{round(x * 4 // 2 / 2 + addition, prec)}" if pd.notna(x) else pd.NA
    if step == 1:
        addition = float("0.999999"[:prec+2])
        fn_bin = lambda x: f"{int(x):.1f}–{round(int(x) + addition, prec)}" if pd.notna(x) else pd.NA
    if step == 2:
        addition = float("1.999999"[:prec+2])
        fn_bin = lambda x: f"{x//2*2:.1f}–{round(x//2*2 + addition, prec)}" if pd.notna(x) else pd.NA

    # assign values to bins according function
    filtered_df['group_label'] = filtered_df[selected_col].map(fn_bin)
    
    # if it is required to combine several bins to one, do this
    if tp_combine_bins:
        filtered_df['group_label'] = filtered_df['group_label'].replace(*tp_combine_bins)

    
    min_value = filtered_df[selected_col].min()
    max_value = filtered_df[selected_col].max()
    print(f"Range: {min_value:.2f} – {max_value:.2f}   " +
          f"({filtered_df[selected_col].idxmin()} – {filtered_df[selected_col].idxmax()})")
    print(f"Number of groups: {filtered_df['group_label'].nunique()}")
    print(f"Number of values: {len(filtered_df)}")

    return filtered_df
