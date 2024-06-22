def predict_model(data, model):
    # # load model
    # import pickle
    # model = pickle.load(open('model.pkl', 'rb'))

    # process data
    from process_data import process_categorical_df, process_numerical_df
    import pandas as pd
    
    # split features into categorical and numerical
    categorical = data.select_dtypes(include=['object'])
    numerical = data.select_dtypes(exclude=['object'])

    # process categorical data
    categorical = process_categorical_df(categorical)
    numerical = process_numerical_df(numerical)

    # select data depending on model
    # if linear regression model
    if model.__class__.__name__ == 'LinearRegression':
        X = numerical
    else:
        X = pd.concat([categorical, numerical], axis=1)

    # predict
    y_pred = model.predict(X)

    return y_pred


