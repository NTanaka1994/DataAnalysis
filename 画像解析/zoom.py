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
            if dst[y][x] < 0:
                dst[y][x] = 0
    return dst.astype(int)

#雑音除去
def noise(imary):
    src = imary.copy()
    for y in range(len(src)):
        for x in range(len(src[y])):
            tmp = []
            if y == 0 and x == 0:
                tmp.append([src[y+1][x+1],
                            src[y+1][x],
                            src[y][x+1],
                            src[y][x]])
            elif y == 0 and x == (len(src[y]) - 1):
                tmp.append([src[y+1][x-1],
                            src[y+1][x],
                            src[y][x-1],
                            src[y][x]])
            elif y == (len(src) - 1) and x == (len(src[y]) - 1):
                tmp.append([src[y-1][x-1],
                            src[y-1][x],
                            src[y][x-1],
                            src[y][x]])
            elif y == (len(src) - 1) and x == 0:
                tmp.append([src[y-1][x+1],
                            src[y-1][x],
                            src[y][x+1],
                            src[y][x]])
            elif y == 0:
                tmp.append([src[y+1][x+1],
                            src[y+1][x],
                            src[y+1][x-1],
                            src[y][x+1],
                            src[y][x],
                            src[y][x-1]])
            elif y == (len(src) - 1):
                tmp.append([src[y-1][x+1],
                            src[y-1][x],
                            src[y-1][x-1],
                            src[y][x+1],
                            src[y][x],
                            src[y][x-1]])
            elif x == 0:
                tmp.append([src[y+1][x+1],
                            src[y+1][x],
                            src[y][x+1],
                            src[y][x],
                            src[y-1][x+1],
                            src[y-1][x]])
            elif x == (len(src[y]) - 1):
                tmp.append([src[y+1][x-1],
                            src[y+1][x],
                            src[y][x-1],
                            src[y][x],
                            src[y-1][x-1],
                            src[y-1][x]])
            else:
                tmp.append([src[y+1][x-1],
                            src[y+1][x],
                            src[y+1][x+1],
                            src[y][x-1],
                            src[y][x],
                            src[y][x+1],
                            src[y-1][x-1],
                            src[y-1][x],
                            src[y-1][x+1]])
            tmp = np.array(tmp)
            imary[y][x] = np.median(tmp)
    return imary

#拡大鮮明化(形の鮮明化→バイリニア補完法→色の鮮明化→ノイズ除去)
def zoom_clear(imary, height, width):
    tmp1 = np.zeros((height, width))
    imary = shape(imary)
    h = imary.shape[0]
    w = imary.shape[1]
    ax = width / w
    ay = height / h
    for yd in range(height):
        for xd in range(width):
            x = xd / ax
            y = yd / ay
            ox = int(x)
            oy = int(y)
            if ox > (w - 2):
                ox = w - 2
            if oy > (h - 2):
                oy = h - 2
            dx = x - ox
            dy = y - oy
            tmp1[yd][xd] = (1 - dx) * (1 - dy) * imary[oy][ox] + dx * (1 - dy) * imary[oy][ox+1] + (1 - dx) * dy * imary[oy][ox+1] + dx * dy * imary[oy+1][ox+1]
            if tmp1[yd][xd] > 255:
                tmp1[yd][xd] = 255
            if tmp1[yd][xd] < 0:
                tmp1[yd][xd] = 0
    tmp1 = contrast(tmp1.astype(int))
    tmp1 = noise(tmp1)
    return tmp1.astype(int)


#画像を白黒で読み込み
image = Image.open("Lenna.png").convert("L")
image.convert("RGB").save("mono.png")
imary = np.array(image)
tmp = zoom_clear(imary, imary.shape[1]*3, imary.shape[0]*3)
clrim = Image.fromarray(tmp).convert("RGB")
clrim.save("dst/clea4.png")
plt.imshow(tmp, cmap="gray")
plt.show()
