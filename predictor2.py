import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from pre_process_data import make_training_data
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import precision_score
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
def get_roc_plot(model,X_train,X_test,y_train,y_test):
    y_train_proba = model.predict_proba(X_train)[:, 1]
    y_test_proba = model.predict_proba(X_test)[:, 1]

    fpr_train, tpr_train, _ = roc_curve(y_train, y_train_proba)
    roc_auc_train = roc_auc_score(y_train, y_train_proba)

    fpr_test, tpr_test, _ = roc_curve(y_test, y_test_proba)
    roc_auc_test = roc_auc_score(y_test, y_test_proba)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr_train, tpr_train, label=f'Training ROC Curve (AUC = {roc_auc_train:.2f})')
    plt.plot(fpr_test, tpr_test, label=f'Test ROC Curve (AUC = {roc_auc_test:.2f})')
    plt.plot([0, 1], [0, 1], 'k--') 
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()
    
    predict_test = model.predict(X_test)
    precision = precision_score(y_test, predict_test)
    print("Precision:", precision)


data = make_training_data()
y=data['result'].astype(int)
X=data[["Rating","Kda","openRating","pistolRating","last10m"]].astype(float)

X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.5,random_state=1)

param_dist = {
    'max_depth': np.arange(2, 5),
    'learning_rate': np.arange(0.0001, 0.1, 0.05),
    'subsample': np.linspace(0.5, 1.0, 5),
    'colsample_bytree': np.linspace(0.5, 1.0, 5),
    'reg_lambda': np.logspace(-5, 2, 10),
    'reg_alpha': np.logspace(-5, 2, 10),  # L1 Regularization
    'n_estimators': np.arange(10, 100, 10),
    'min_child_weight': np.arange(1, 10, 1)
}

# Initialize the model
model = XGBClassifier(eval_metric='map', objective='binary:logistic')

random_search = RandomizedSearchCV(
    model,
    param_distributions=param_dist,
    n_iter=50,  # Number of parameter settings sampled
    scoring='roc_auc',  # Use ROC-AUC as the evaluation metric
    n_jobs=-1,  # Use all available cores
    cv=5,       # 5-fold cross-validation
    random_state=42
)
random_search.fit(X_train, y_train)

# Output the best parameters and score
print("Best parameters found: ", random_search.best_params_)
print("Best ROC-AUC score: ", random_search.best_score_)

# Evaluate the best model on the test set
best_model = random_search.best_estimator_
test_score = best_model.score(X_test, y_test)

print(test_score)

model_final = XGBClassifier(**random_search.best_params_)

model_final.fit(X_train,y_train,verbose=True)

model_final.save_model('xgb_matches2.json')

