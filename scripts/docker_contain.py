from pandas import DataFrame
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn2docker.constructor import Sklearn2Docker
from requests import post
from pandas import read_json
from os import system

iris = load_iris()
input_df = DataFrame(data=iris['data'], columns=iris['feature_names'])
clf = DecisionTreeClassifier(max_depth=2)
clf.fit(input_df.values, iris['target'])


s2d = Sklearn2Docker(
    classifier=clf,
    feature_names=iris['feature_names'],
    class_names=iris['target_names'].tolist()
)
s2d.save(name="classifier", tag="iris")

system("docker run -d -p 5000:5000 classifier:iris && sleep 5")


request = post("http://localhost:5000/predict_proba/split", json=input_df.to_json(orient="split"))
result = read_json(request.content.decode(), orient="split")
print(result.head())

request = post(
    "http://localhost:5000/predict/split",
    json=input_df.to_json(orient="split")
)
