import talib
import pyupbit
import numpy as np
import pandas as pd
import CreateCsv


def slope(x, y, t):
    return (y - x) / t

df = pd.read_csv("data.csv")

va = 1.00
High = pd.DataFrame()
Low = pd.DataFrame()

for i in range(1, len(df.index) - 1):
    if df.iloc[i][1] > df.iloc[i-1][1]*va and df.iloc[i][1] > df.iloc[i+1][1]*va:
        High = High.append([df.iloc[i]])
    if df.iloc[i][2] < df.iloc[i - 1][2] * va and df.iloc[i][2] < df.iloc[i + 1][2] * va:
        Low = Low.append([df.iloc[i]])

High["what"] = 1
Low["what"] = 0

all = pd.DataFrame()
all = all.append(High)
all = all.append(Low)
all = all.sort_index()

all_tmp = pd.DataFrame()
zigzag1 = pd.DataFrame() #저고저고
zigzag2 = pd.DataFrame() #고저고저
i_tmp_max = 0
i_tmp_low = 0
i=-1

while True:
    i = i+1
    if i >= len(all.index)-1: break
    chk = 0
    chk_wht = all.iloc[i][5]
    i_tmp_low = i
    i_tmp_max = i
    if chk_wht == 0:
        while True:
            i = i+1
            if i > len(all.index): break
            if chk_wht == all.iloc[i][5]:
                if chk == 1: break
                elif all.iloc[i_tmp_low][2] > all.iloc[i][2]: i_tmp_low = i
            else:
                if chk == 0:
                    i_tmp_max = i
                elif all.iloc[i_tmp_max][1] < all.iloc[i][1]: i_tmp_max = i
                chk = 1
        all_tmp = all_tmp.append([all.iloc[i_tmp_low]])
        all_tmp = all_tmp.append([all.iloc[i_tmp_max]])
        i=i-1
    else:
        while True:
            i = i+1
            if i >= len(all.index): break
            if chk_wht == all.iloc[i][5]:
                if chk == 1: break
                elif all.iloc[i_tmp_max][2] < all.iloc[i][2]: i_tmp_max = i
            else:
                if chk == 0:
                    i_tmp_low = i
                elif all.iloc[i_tmp_low][1] > all.iloc[i][1]: i_tmp_low = i
                chk = 1
        all_tmp = all_tmp.append([all.iloc[i_tmp_max]])
        all_tmp = all_tmp.append([all.iloc[i_tmp_low]])
        i=i-1

#all_tmp = all_tmp.groupby(level=0).first()

val_per = 1.1

#저고저고

i = 0
if all_tmp.iloc[0][5] == 0:
    i = i+1
    zigzag1 = zigzag1.append([df.iloc[0]])
    zigzag1["what"] = 0
    zigzag1 = zigzag1.append([all_tmp.iloc[i]])
    i = i-1
    while True:
        i = i+2
        if i >= len(all_tmp.index): break
        if zigzag1.iloc[len(zigzag1.index)-1][5] == 1:
            if zigzag1.iloc[len(zigzag1.index)-1][1] * (2 - val_per) > all_tmp.iloc[i][2]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][2] * val_per < all_tmp.iloc[j+1][1]:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][2] > all_tmp.iloc[j+2][2]:
                        i_tmp = j+2
                    j = j+2
        else:
            if zigzag1.iloc[len(zigzag1.index)-1][2] * val_per < all_tmp.iloc[i][1]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][1] * (2 - val_per) > all_tmp.iloc[j+1][2]:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][1] < all_tmp.iloc[j+2][1]:
                        i_tmp = j+2
                    j = j+2

else:
    zigzag1 = zigzag1.append([df.iloc[0]])
    zigzag1["what"] = 0
    zigzag1 = zigzag1.append([all_tmp.iloc[i]])
    i = i-1
    while True:
        i = i+2
        if i >= len(all_tmp.index): break
        if zigzag1.iloc[len(zigzag1.index)-1][5] == 1:
            if zigzag1.iloc[len(zigzag1.index)-1][1] * (2 - val_per) > all_tmp.iloc[i][2]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][2] * val_per < all_tmp.iloc[j+1][1]:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][2] > all_tmp.iloc[j+2][2]:
                        i_tmp = j+2
                    j = j+2
        else:
            if zigzag1.iloc[len(zigzag1.index)-1][2] * val_per < all_tmp.iloc[i][1]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][1] * (2 - val_per) > all_tmp.iloc[j+1][2]:
                        zigzag1 = zigzag1.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][1] < all_tmp.iloc[j+2][1]:
                        i_tmp = j+2
                    j = j+2

#고저고저

i = 0
if all_tmp.iloc[0][5] == 0:
    zigzag2 = zigzag2.append([df.iloc[0]])
    zigzag2["what"] = 1
    zigzag2 = zigzag2.append([all_tmp.iloc[i]])
    i = i-1
    while True:
        i = i+2
        if i >= len(all_tmp.index): break
        if zigzag2.iloc[len(zigzag2.index)-1][5] == 1:
            if zigzag2.iloc[len(zigzag2.index)-1][1] * (2 - val_per) > all_tmp.iloc[i][2]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][2] * val_per < all_tmp.iloc[j+1][1]:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][2] > all_tmp.iloc[j+2][2]:
                        i_tmp = j+2
                    j = j+2
        else:
            if zigzag2.iloc[len(zigzag2.index)-1][2] * val_per < all_tmp.iloc[i][1]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][1] * (2 - val_per) > all_tmp.iloc[j+1][2]:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][1] < all_tmp.iloc[j+2][1]:
                        i_tmp = j+2
                    j = j+2

else:
    i = i+1
    zigzag2 = zigzag2.append([df.iloc[0]])
    zigzag2["what"] = 1
    zigzag2 = zigzag2.append([all_tmp.iloc[i]])
    i = i-1
    while True:
        i = i+2
        if i >= len(all_tmp.index): break
        if zigzag2.iloc[len(zigzag2.index)-1][5] == 1:
            if zigzag2.iloc[len(zigzag2.index)-1][1] * (2 - val_per) > all_tmp.iloc[i][2]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][2] * val_per < all_tmp.iloc[j+1][1]:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][2] > all_tmp.iloc[j+2][2]:
                        i_tmp = j+2
                    j = j+2
        else:
            if zigzag2.iloc[len(zigzag2.index)-1][2] * val_per < all_tmp.iloc[i][1]:
                j = i
                i_tmp = i
                while True:
                    if j >= len(all_tmp.index)-2:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = j
                        break
                    if all_tmp.iloc[i_tmp][1] * (2 - val_per) > all_tmp.iloc[j+1][2]:
                        zigzag2 = zigzag2.append([all_tmp.iloc[i_tmp]])
                        i = i_tmp-1
                        break
                    if all_tmp.iloc[i_tmp][1] < all_tmp.iloc[j+2][1]:
                        i_tmp = j+2
                    j = j+2

print(zigzag1)
print(zigzag2)