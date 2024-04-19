---
jupyter:
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.12.2
  nbformat: 4
  nbformat_minor: 2
---

::: {.cell .markdown}
In this project I am performing CS2 matches prediction based on players
performance in last 2 months.

Technologies and frameworks used:\
*Python\
*Selenium\
*Pandas\
*Sqlalchemy\
*PostgreSQL\
*XGBoost

Data for all of the teams and players is gathered using webscraping from
several websites, including passing through CloudFlare captcha. Data is
organized and stored in PostgreSQL database to ensure integrity,
consistency, efficient retrieval and scalability.

Model after optimalization achieved high precision of 0.685 in test
data, and it doesnt show overfitting
:::

::: {.cell .code execution_count="10"}
``` python
from pre_process_data import make_training_data
data = make_training_data()
data.info()
```

::: {.output .stream .stdout}
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 623 entries, 0 to 622
    Data columns (total 8 columns):
     #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
     0   Team1_id      623 non-null    int64  
     1   Team2_id      623 non-null    int64  
     2   result        623 non-null    bool   
     3   Rating        623 non-null    float64
     4   Kda           623 non-null    float64
     5   openRating    623 non-null    float64
     6   pistolRating  623 non-null    float64
     7   last10m       623 non-null    float64
    dtypes: bool(1), float64(5), int64(2)
    memory usage: 34.8 KB
:::
:::

::: {.cell .markdown}
Data consist features of mean of team players statistics divided from
the mean values from opposite team.
:::

::: {.cell .code execution_count="11"}
``` python
data.head()
```

::: {.output .execute_result execution_count="11"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Team1_id</th>
      <th>Team2_id</th>
      <th>result</th>
      <th>Rating</th>
      <th>Kda</th>
      <th>openRating</th>
      <th>pistolRating</th>
      <th>last10m</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>28</td>
      <td>39</td>
      <td>True</td>
      <td>0.024</td>
      <td>0.032</td>
      <td>-0.016</td>
      <td>-0.072</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>143</td>
      <td>66</td>
      <td>True</td>
      <td>0.084</td>
      <td>0.112</td>
      <td>0.018</td>
      <td>0.024</td>
      <td>42.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20</td>
      <td>54</td>
      <td>False</td>
      <td>-0.032</td>
      <td>-0.048</td>
      <td>-0.044</td>
      <td>-0.052</td>
      <td>12.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>67</td>
      <td>True</td>
      <td>0.082</td>
      <td>0.084</td>
      <td>0.038</td>
      <td>0.040</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>34</td>
      <td>97</td>
      <td>False</td>
      <td>0.072</td>
      <td>0.096</td>
      <td>0.014</td>
      <td>0.166</td>
      <td>2.0</td>
    </tr>
  </tbody>
</table>
</div>
```
:::
:::

::: {.cell .markdown}
Variable rating is value of players calculated by hltv of overall Player
performance. Kda is Kill/death/assist ratio from player matches.
openRating is the rating of player getting opening(first) kills in round
pistolRating is the rating of player performing in pistol rounds last10m
is Team performance in last 10 matches

Variable,Kda,openRating and pistolRating are calculated by getting the
average of all players from team and then dividing values of Team1 minus
Team2
:::

::: {.cell .code execution_count="12"}
``` python
import seaborn as sns
import matplotlib.pyplot as plt
y=data['result'].astype(int)
X=data[["Rating","Kda","openRating","pistolRating","last10m"]].astype(float)

for i in X.columns:
    sns.regplot(x=X[i],y=y,logistic=True,ci=None)
    plt.show()
```

::: {.output .display_data}
![](img/509f1a15d60859cf9d2184be04f19ae2cf199d19.png)
:::

::: {.output .display_data}
![](img/05f83464fd5c72f8754370efca0e42e00d0319ea.png)
:::

::: {.output .display_data}
![](img/2af4b49a4bc45c195de4343110df5c196eade40b.png)
:::

::: {.output .display_data}
![](img/13560ec042eecda14887f6d7576c2b4da1729772.png)
:::

::: {.output .display_data}
![](img/190d51a3cbc87ccf87cf08b627cc9c97099a282c.png)
:::
:::

::: {.cell .markdown}
Plots show that teams with higher values tends to perform better and win
more matches
:::

::: {.cell .code execution_count="13"}
``` python
from xgboost import XGBClassifier
model = XGBClassifier()
model.load_model("xgb_matches1.json")
model.feature_importances_
```

::: {.output .execute_result execution_count="13"}
    array([0.18995626, 0.14972827, 0.07406306, 0.09058215, 0.4956702 ],
          dtype=float32)
:::
:::

::: {.cell .code execution_count="14"}
``` python
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split
from predictor2 import get_roc_plot
X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.7,random_state=1)

get_roc_plot(model,X_train,X_test,y_train,y_test)
```

::: {.output .display_data}
![](img/bed76f5c989b0ae493a517b23c43085ae643e132.png)
:::

::: {.output .stream .stdout}
    Precision: 0.6857142857142857
:::
:::

::: {.cell .markdown}
Metrics shows that model predicts winning team with high ratio.
Overfitting of model is not observed.

In evaluating model we focus more on its precision because the false
positive can result in losing money while betting. With this precision
optimal betting using Kelly\'s criterion should result in continious
profit
:::

::: {.cell .code}
``` python
```
:::
