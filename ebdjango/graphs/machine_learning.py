import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
from pandas.plotting import scatter_matrix
from sklearn.model_selection import train_test_split
from activities.models import Activity
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import PolynomialFeatures


def split_train_test(data, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

def machine_learning(activities):
    df = pd.DataFrame([t.__dict__ for t in activities ])
    df = df[df['activity_type'] == "Run"]
    df = df.drop(['_state','user','id', 'strava_id','activity_type','date'], axis=1)

    # Data selection
    df = df[["timestamp","heartrate","distance","moving_time"]]
    print(df)
    train_set, test_set = train_test_split(df, test_size=0.2, random_state=41)
    dataset = train_set.copy()
    activities = dataset.drop("moving_time", axis=1) # drop labels for training set
    activities_labels = dataset["moving_time"].copy()
    #activities, activities_labels = make_regression(n_samples=200, random_state=1)

    #Prepare
    num_pipeline = Pipeline([
        ('poly', PolynomialFeatures(degree=2)),
        ('mm_scaler',MinMaxScaler())
    ])
    activities_prepared = num_pipeline.fit_transform(activities)

    #Model  
    print("Start Training")
    lin_regr = LinearRegression()
    print("Training Complete")
    lin_regr.fit(activities_prepared, activities_labels)

    #Output
    some_data = activities.iloc[:5]
    some_labels = activities_labels.iloc[:5]
    some_data_prepared = num_pipeline.transform(some_data)

    #Checking stats
    scores = cross_val_score(lin_regr, activities_prepared,activities_labels,scoring='neg_mean_squared_error', cv=10)
    tree_rmse_scores = np.sqrt(-scores)
    print(tree_rmse_scores)
    param_grid = [
    # try 12 (3×4) combinations of hyperparameters
    {'fit_intercept':[True,False],'normalize':[True,False]}
    ]

    grid_search = GridSearchCV(lin_regr, param_grid, cv=5,
                           scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(activities_prepared,activities_labels)
    print("--------------------")
    print(grid_search.best_params_)
    print("--------------------")

    cvres = grid_search.cv_results_
    for mean_score,params in zip(cvres['mean_test_score'], cvres['params']):
        print(np.sqrt(-mean_score),params)

    final_model = grid_search.best_estimator_

    X_test = test_set.drop("moving_time", axis=1)
    y_test = test_set["moving_time"].copy()
    X_test_prepared = num_pipeline.transform(X_test)

    final_predictions = final_model.predict(X_test_prepared)
    final_mse = mean_squared_error(y_test, final_predictions)
    final_rmse = np.sqrt(final_mse)
    print("-------------------------")
    print("Final Verdict")
    print(final_rmse)
    X = np.array([1605913200,160,18.5]).reshape(1,-1)
    X_prepared = num_pipeline.transform(X)
    predictions = final_model.predict(X_prepared)
    print(predictions[0]/60)
    