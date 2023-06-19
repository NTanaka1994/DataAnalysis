from eli5.sklearn import PermutationImportance
from lightgbm import LGBMClassifier, LGBMRegressor
from bs4 import BeautifulSoup
import pandas as pd
import eli5

def cvpfi_val_reg(df, y_col, cv=10):
    imp = {}
    err = {}
    cols = df.drop(y_col, axis=1).columns
    for i in range(cv):
        df_tmp = df.copy()
        train = df_tmp.drop(df.index[int(len(df)*(1/cv)*i):int(len(df)*(1/cv)*(i+1))])
        y_train = train[y_col]
        x_train = train.drop(y_col, axis=1)
        model = LGBMRegressor()
        model.fit(x_train, y_train)
        PFI = PermutationImportance(model, random_state=1).fit(x_train, y_train)
        html_data = eli5.show_weights(PFI, feature_names = x_train.columns.tolist()).data
        col = x_train.columns
        tmp = {}
        tmpe = {}
        for j in range(len(col)):
            soup = BeautifulSoup(html_data, "html.parser")
            Feature = soup.select(".eli5-weights > tbody:nth-child(2) > tr:nth-child("+str(j+1)+") > td:nth-child(2)")
            Weghits = soup.select(".eli5-weights > tbody:nth-child(2) > tr:nth-child("+str(j+1)+") > td:nth-child(1)")
            sf = 0
            sw = 0
            ef = 0
            ew = 0
            fflag = 0
            wflag = 0
            Feature = str(Feature[0])
            Weghits = str(Weghits[0])
            for k in range(len(Feature)):
                if Feature[k] == ">":
                    if fflag == 0:
                        sf = k + 1
                        fflag = 1
                if Feature[k] == "<":
                    if fflag == 1:
                        ef = k
                        break
            for k in range(len(Weghits)):
                if Weghits[k] == ">":
                    if wflag == 0:
                        sw = k + 1
                        wflag=1
                if Weghits[k] == "<":
                    if wflag == 1:
                        ew = k
                        break
            Feature = Feature[sf:ef].replace(" ", "").replace("\n", "")
            data = Weghits[sw:ew].replace(" ", "").replace("\n", "").split("±")
            Weghits = float(data[0])
            Err = float(data[1])
            tmp[Feature] = Weghits
            tmpe[Feature] = Err
        imp[i] = tmp
        err[i] = tmpe
    result = []
    for col in cols:
        total = 0
        tte = 0
        for i in range(cv):
            total = total + imp[i][col]
            tte = tte + err[i][col]
        result.append([total / cv, tte/cv])
    df_cvpfi = pd.DataFrame(result)
    df_cvpfi.columns = ["CVPFI", "±Err"]
    df_cvpfi.index = cols
    return df_cvpfi

def cvpfi_val_cla(df, y_col, cv=10):
    imp = {}
    err = {}
    cols = df.drop(y_col, axis=1).columns
    for i in range(cv):
        df_tmp = df.copy()
        train = df_tmp.drop(df.index[int(len(df)*(1/cv)*i):int(len(df)*(1/cv)*(i+1))])
        y_train = train[y_col]
        x_train = train.drop(y_col, axis=1)
        model = LGBMClassifier()
        model.fit(x_train, y_train)
        PFI = PermutationImportance(model, random_state=1).fit(x_train, y_train)
        html_data = eli5.show_weights(PFI, feature_names = x_train.columns.tolist()).data
        col = x_train.columns
        tmp = {}
        tmpe = {}
        for j in range(len(col)):
            soup = BeautifulSoup(html_data, "html.parser")
            Feature = soup.select(".eli5-weights > tbody:nth-child(2) > tr:nth-child("+str(j+1)+") > td:nth-child(2)")
            Weghits = soup.select(".eli5-weights > tbody:nth-child(2) > tr:nth-child("+str(j+1)+") > td:nth-child(1)")
            sf = 0
            sw = 0
            ef = 0
            ew = 0
            fflag = 0
            wflag = 0
            Feature = str(Feature[0])
            Weghits = str(Weghits[0])
            for k in range(len(Feature)):
                if Feature[k] == ">":
                    if fflag == 0:
                        sf = k + 1
                        fflag = 1
                if Feature[k] == "<":
                    if fflag == 1:
                        ef = k
                        break
            for k in range(len(Weghits)):
                if Weghits[k] == ">":
                    if wflag == 0:
                        sw = k + 1
                        wflag=1
                if Weghits[k] == "<":
                    if wflag == 1:
                        ew = k
                        break
            Feature = Feature[sf:ef].replace(" ", "").replace("\n", "")
            data = Weghits[sw:ew].replace(" ", "").replace("\n", "").split("±")
            Weghits = float(data[0])
            Err = float(data[1])
            tmp[Feature] = Weghits
            tmpe[Feature] = Err
        imp[i] = tmp
        err[i] = tmpe
    result = []
    for col in cols:
        total = 0
        tte = 0
        for i in range(cv):
            total = total + imp[i][col]
            tte = tte + err[i][col]
        result.append([total / cv, tte / cv])
    df_cvpfi = pd.DataFrame(result)
    df_cvpfi.columns = ["CVPFI", "±Err"]
    df_cvpfi.index = cols
    return df_cvpfi
