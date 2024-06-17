def train_model(df):

    # split into features and target (target is last column)
    X = df.drop(df.columns[-1], axis=1)
    y = df[df.columns[-1]]

    # choose model and data
    x, model = choose_model(X, y)

    # fit model
    model = fit_model(model, x, y)

    return model

def choose_model(X, y):
    import sklearn.linear_model as linear_model

    # if y is numerical
    if y.dtype in ['int64', 'float64']:
        model = linear_model.LinearRegression()
        x = X.select_dtypes(exclude=['object'])
    # if y is categorical
    else:
        model = linear_model.LogisticRegression()
        x = X

    # can return set of models in future

    return x, model

def fit_model(model, X, y):
    # can implement CV here in future

    model.fit(X, y)

    return model


