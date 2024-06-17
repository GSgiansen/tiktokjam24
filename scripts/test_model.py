def test_model(model, test):
    import pandas as pd
    import numpy as np

    # process data
    from process_data import process_data
    test = process_data(test)

    # split into features and target (target is last column)
    X_test = test.drop(test.columns[-1], axis=1)
    y_test = test[test.columns[-1]]

    # test model
    if y_test.dtype in ['int64', 'float64']:
        y_pred = model.predict(X_test.select_dtypes(exclude=['object']))
        metric = get_metric(y_test, y_pred)
    else:
        y_pred = model.predict(X_test)
        metric = get_metric(y_test, y_pred)

    return metric

def get_metric(y_true, y_pred):
    from sklearn.metrics import mean_squared_error, accuracy_score

    if y_true.dtype in ['int64', 'float64']:
        return mean_squared_error(y_true, y_pred)
    else:
        return accuracy_score(y_true, y_pred)
