def load_data():
    import pandas as pd

    # Load dataset
    data = pd.read_csv('data/data.csv')

    # Split into train and test
    train = data.sample(frac=0.8, random_state=200)
    test = data.drop(train.index)

    # Save train and test data
    train.to_csv('../data/train.csv', index=False)
    test.to_csv('../data/test.csv', index=False)

    print('Data loaded and split into train and test data')

    return train, test