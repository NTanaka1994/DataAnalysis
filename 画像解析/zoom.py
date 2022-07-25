from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

#色の鮮明化
def contrast(imary):
    hist = np.zeros(256)
    for y in range(len(imary)):
        for x in range(len(imary[y])):
            hist[imary[y][x]] = hist[imary[y][x]] + 1
    histsum = np.zeros(256)
    for i in range(len(hist)):
        if i==0:
            histsum[i] = hist[i]
        else:
            histsum[i] = histsum[i-1] + hist[i]
    histsum = ((histsum - min(histsum)) / (max(histsum) - min(histsum))) * 255
    dst = np.zeros((len(imary), len(imary[0])))
    for y in range(len(imary)):
        for x in range(len(imary[y])):
            dst[y][x] = int(histsum[imary[y][x]])
    return dst

#形の鮮明化
def shape(imary):
    mask = np.zeros((len(imary), len(imary[0])))
    src = imary.copy()
    for y in range(len(imary)-2):
        for x in range(len(imary[y])-2):
            mask[y][x] = 10 * src[y][x] - src[y-1][x] - src[y+1][x] - src[y][x-1] - src[y][x+1] - src[y-1][x-1] - src[y-1][x+1] - src[y+1][x-1] - src[y+1][x+1]
    mask = mask / 9
    dst = src + mask
    for y in range(len(imary)-2):
        for x in range(len(imary[y])-2):
            if dst[y][x] > 255:
               dst[y][x] = 255
    return dst.astype(int)

#拡大鮮明化
def zoom_clear(imary):
    mask = np.zeros((len(imary), len(imary[0])))
    tmp1 = np.zeros((2*len(imary), 2*len(imary[0])))
    #imary = contrast(imary)
    imary = shape(imary)
    for y in range(len(imary)):
        for x in range(len(imary[y])):
            tmp1[y*2][x*2] = imary[y][x]
    for y in range(len(tmp1)-1):
        for x in range(len(tmp1[y])-1):
            if (y % 2) == 0:
                if (x % 2) == 1 and x != (len(tmp1[y])-1):
                    tmp1[y][x] = (tmp1[y][x-1] + tmp1[y][x+1]) / 2
    for y in range(len(tmp1)-1):
        for x in range(len(tmp1[y])-1):
            if (y % 2) == 1 and y != (len(tmp1)-1):
                tmp1[y][x] = (tmp1[y-1][x] + tmp1[y+1][x]) / 2
    #tmp1 = shape(tmp1.astype(int))
    tmp1 = contrast(tmp1.astype(int))
    return tmp1.astype(int)


#画像を白黒で読み込み
image = Image.open("Lenna.png").convert("L")
image.convert("RGB").save("mono.png")
imary = np.array(image)
tmp = zoom_clear(imary)
#tmp = contrast(tmp)
clrim = Image.fromarray(tmp).convert("RGB")
clrim.save("dst/clear2.png")
plt.imshow(tmp, cmap="gray")
plt.show()
