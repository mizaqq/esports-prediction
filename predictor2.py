import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from pre_process_data import make_training_data
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score

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

X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.7)

model = XGBClassifier(max_depth=2, learning_rate=0.05, subsample = 0.5,eval_metric='map',objective='binary:logistic')
model.fit(X_train,y_train)

get_roc_plot(model,X_train,X_test,y_train,y_test)

model.save_model('xgb_matches1.json')

