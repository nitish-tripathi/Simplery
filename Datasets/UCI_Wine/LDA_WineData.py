
import pandas as pd
import numpy as np
from sklearn.lda import LDA
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def plot_decision_regions(_data_, _target_, classifier, resolution=0.02):
    """ Plot decision boundary mesh """
    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(_target_))])

    # plot the decision surface
    x1_min, x1_max = _data_[:, 0].min() - 1, _data_[:, 0].max() + 1
    x2_min, x2_max = _data_[:, 1].min() - 1, _data_[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    predicted_class = classifier.predict(
        np.array([xx1.ravel(), xx2.ravel()]).T)
    predicted_class = predicted_class.reshape(xx1.shape)
    plt.contourf(xx1, xx2, predicted_class, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # plot class samples
    for idx, cl in enumerate(np.unique(_target_)):
        plt.scatter(x=_data_[_target_ == cl, 0], y=_data_[_target_ == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)

def main():
    """ Main """
    df_wine = pd.read_csv('wine.data', header=None)
    _x_ = df_wine.iloc[:, 1:].values
    _y_ = df_wine.iloc[:, 0].values

    # 1. Standarize data
    x_train, x_test, y_train, y_test = train_test_split(_x_, _y_, test_size=0.3, random_state=0)
    sc_ = StandardScaler()
    sc_.fit(x_train)
    x_std = sc_.transform(_x_)
    x_train_std = sc_.transform(x_train)
    x_test_std = sc_.transform(x_test)

    lda = LDA(n_components=2)
    lda.fit(x_train_std, y_train)
    x_train_lda = lda.transform(x_train_std)
    x_lda = lda.transform(x_std)
    x_test_lda = lda.transform(x_test_std)

    print lda.coef_
    print lda.explained_variance_ratio_
    
    classifier_ = LogisticRegression()
    classifier_.fit(x_train_lda, y_train)
    
    y_pred = classifier_.predict(x_test_lda)
    print "Accuracy: %0.3f" % accuracy_score(y_test, y_pred)

    plot_decision_regions(x_test_lda, y_test, classifier=classifier_)
    plt.show()

if __name__ == "__main__":
    main()
