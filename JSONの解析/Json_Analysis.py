import json
import requests

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
    root = []
    if isinstance(jsn, dict):
        for row in jsn:
            ed.append(row)
        root.append(ed.copy())
    elif isinstance(jsn, list):
        for i in range(len(jsn)):
            ed.append(i)
        root.append(ed.copy())
    tmp = []
    while len(ed) > 0:
        node = ed[0]
        if len(ed) == 1:
            if isinstance(node, str):
                print("[\""+node+"\"]", end="")
            else:
                print("["+str(node)+"]", end="")
        else:
            if isinstance(node, str):
                print("[\""+node+"\"]")
            else:
                print("["+str(node)+"]")
        del ed[0]
        if tmp == []:
            jsn = jsn[node]
        else:
            jsn = tmp[0][node]
            del tmp[0]
        if isinstance(jsn, dict):
            for row in jsn:
                tmp.append(jsn)
                ed.append(row)
            root.append(ed.copy())
        elif isinstance(jsn, list) and jsn != []:
            for i in range(len(jsn)):
                tmp.append(jsn)
                ed.append(i)
            root.append(ed.copy())
        else:
            print("="+str(jsn))
    pass

url = "https://raw.githubusercontent.com/NTanaka1994/DataAnalysis/main/JSON%E3%81%AE%E8%A7%A3%E6%9E%90/json_sample.json" #ここにJSONのあるURLを入れる

res = requests.get(url)

data = json.loads(res.text)

depth(data, "data")
width(data)
