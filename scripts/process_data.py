def process_data(data):
    import pandas as pd

    # split into features and target (target is last column)
    X = data.drop(data.columns[-1], axis=1)
    y = data[data.columns[-1]]

    # split into categorical and numerical features
    categorical = X.select_dtypes(include=['object'])
    numerical = X.select_dtypes(exclude=['object'])

    # process categorical features
    categorical = process_categorical_df(categorical)

    # process numerical features
    numerical = process_numerical_df(numerical)

    # Assume no Nan rows in target

    return pd.concat([categorical, numerical, y], axis=1)

def process_categorical_df(df):
    import pandas as pd

    # Assume binary catergorical features
    # Fill Nan with Mode
    for col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df

def process_numerical_df(df):
    import pandas as pd
    import sklearn.preprocessing as preprocessing

    # Fill Nan with Mean
    for col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

    # Scale
    scaler = preprocessing.StandardScaler()
    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    return df

