import json
import requests
import pandas as pd

def depth(jsn, var=""):
    if isinstance(jsn, dict):
        for row in jsn:
            depth(jsn[row], var=var+"[\""+row+"\"]")
    elif isinstance(jsn, list) and jsn != []:
        for i in range(len(jsn)):
            depth(jsn[i], var=var+"["+str(i)+"]")
    else:
        print(var+"="+str(jsn))
        pass

def width(jsn, ed=[]):
    ptmp = []
    path = []
    if isinstance(jsn, dict):
        for row in jsn:
            ed.append(row)
            ptmp.append(row)
        path.append(ptmp)
        ptmp = []
    elif isinstance(jsn, list):
        for i in range(len(jsn)):
            ed.append(i)
            ptmp.append(i)
        path.append(ptmp)
        ptmp = []
    tmp = []
    while len(ed) > 0:
        node = ed[0]
        del ed[0]
        if tmp == []:
            jsn = jsn[node]
        else:
            jsn = tmp[0][node]
            del tmp[0]
        ptmp.append(node)
        if isinstance(jsn, dict):
            for row in jsn:
                tmp.append(jsn)
                ptmp.append(row)
                ed.append(row)
            path.append(ptmp)
            ptmp = []
        elif isinstance(jsn, list) and jsn != []:
            for i in range(len(jsn)):
                tmp.append(jsn)
                ptmp.append(i)
                ed.append(i)
            path.append(ptmp)
            ptmp = []
        else:
            ptmp.append("END:"+str(jsn))
            path.append(ptmp)
            ptmp = []
    return path

url = "https://raw.githubusercontent.com/NTanaka1994/DataAnalysis/main/JSON%E3%81%AE%E8%A7%A3%E6%9E%90/json_sample.json" #ここにJSONのあるURLを入れる

res = requests.get(url)

data = json.loads(res.text)

depth(data, "data")
path = width(data)
df = pd.DataFrame(path)
col = []
for i in range(len(df.columns)):
    if i == 0:
        col.append("親ノード")
    else:
        col.append("子ノード"+str(i))
df.columns = col
print(df)
df.to_csv("result.csv", encoding="shift-jis", index=False)
