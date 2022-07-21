from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

#色の鮮明化
def contrast(imary):
    hist = np.zeros(256)
    for y in range(len(imary)):
        for x in range(len(imary[y])):
            hist[imary[y][x]] = hist[imary[y][x]] + 1
    #plt.bar(np.arange(0, 256, 1), hist)
    #plt.show()
    histsum = np.zeros(256)
    for i in range(len(hist)):
        if i==0:
            histsum[i] = hist[i]
        else:
            histsum[i] = histsum[i-1] + hist[i]
    #plt.bar(np.arange(0, 256, 1), histsum)
    #plt.show()
    histsum = ((histsum - min(histsum)) / (max(histsum) - min(histsum))) * 255
    #plt.bar(np.arange(0, 256, 1), histsum)
    #plt.show()
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

#画像を白黒で読み込み
image = Image.open("Lenna.png").convert("L")
image.convert("RGB").save("mono.png")
imary = np.array(image)
imaryim = Image.fromarray(imary).convert("RGB")
imaryim.save("dst/mono.png")
cont = contrast(imary)
contim = Image.fromarray(cont).convert("RGB")
contim.save("dst/contrast.png")
shap = shape(imary)
shapim = Image.fromarray(shap).convert("RGB")
shapim.save("dst/shape.png")
clr = contrast(shap)
clrim = Image.fromarray(clr).convert("RGB")
clrim.save("dst/clear.png")
