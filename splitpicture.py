#coding:gbk
def show_fig(img, data):
    figure, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in data:
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)
    plt.show()


def first_filter(area, regions):
    candidates = []
    for r in regions:
        x, y, w, h = r['rect']
        # 重复的不要
        if r['rect'] in candidates:
            continue

        # 太小和太大的不要
        if (w <= 5) or (h <= 5):
            continue
        if (w * h) > area:
            continue
        # if (w * h) < (area / 20):
        #     continue
        # 保留1
        if ((w * h) < (area / 20)) and ((h / w) < 3):
            continue

        candidates.append((x, y, w, h))
    return candidates


def second_filter(regions):
 num_array=[]
 for  i  in  regions:
    if len(num_array)==0:
        num_array.append(i)
    else:
        content=False
        replace=-1
        index=0
        for j in num_array:
            ##新窗口在小圈 则滤除
            if i[0]>=j[0] and i[0]+i[2]<=j[0]+j[2]and i[1]>=j[1] and i[1]+i[3]<=j[1]+j[3]: 
                content=True
                break
            ##新窗口不在小圈 而在老窗口外部 替换老窗口
            elif i[0]<=j[0] and i[0]+i[2]>=j[0]+j[2] and i[1]<=j[1] and i[1]+i[3]>=j[1]+j[3]: 
                replace=index
                break
            index+=1

        if not content:
            if replace>=0:
                num_array[replace]=i
            else:
                num_array.append(i)
#窗口过滤完之后的数量
 return num_array



def order_number(img, data):
    h_list = [r[1] for r in data]
    aver = np.mean(h_list)
    v = np.var(h_list)
    print('行高均值：%.4f, 方差：%.4f' % (aver, v))
    flag = v > 500
    l1, l2 = [], []
    # 划分所属行
    if flag:
        for r in data:
            if r[1] <= aver:
                l1.append(r)
            else:
                l2.append(r)

        # 从左到右排列
        for i in range(len(l2)):
            for j in range(i + 1, len(l2)):
                if l2[i][0] > l2[j][0]:
                    l2[i], l2[j] = l2[j], l2[i]
    else:
        l1 = data
    for i in range(len(l1)):
        for j in range(i + 1, len(l1)):
            if l1[i][0] > l1[j][0]:
                l1[i], l1[j] = l1[j], l1[i]

    image_data = []
    image_data.extend(make_pic(img, l1))
    if flag:
        image_data.extend(make_pic(img, l2))
    return image_data


# 制作成28*28的黑底白字图片

def make_pic(img, data):
    padding = 4
    size = 20
    image_data = []
    for r in data:
        temp = np.zeros([28, 28], dtype='float32')
        if r[3] < r[2]:
            t = (r[2] - r[3]) // 2
            temp_img = img[(r[1]-t):(r[1]+r[3]+t), r[0]:(r[0]+r[2])]
        else:
            t = (r[3] - r[2]) // 2
            temp_img = img[r[1]:(r[1] + r[3]), (r[0]-t):(r[0] + r[2]+t)]

        temp_img = cv2.resize(temp_img, (size, size), cv2.INTER_CUBIC)
        temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        temp_img = np.array(temp_img, dtype='float32') / 255
        # temp_img = np.array(cv2.threshold(temp_img, 0, 1, cv2.THRESH_BINARY)[1], dtype='float32')
        temp[padding:(padding+size), padding:(padding+size)] = temp_img
        image_data.append(temp)
        plt.imshow(temp, cmap="gray")
        plt.show()
    return image_data


def extract_images():
    # 第二步：执行搜索工具,展示搜索结果
    image_path = "这里写你图片的路径"
    # 用cv2读取图片
    img_tmp = cv2.imread(image_path)
    
    GrayImage=cv2.cvtColor(img_tmp,cv2.COLOR_BGR2GRAY)#灰度化
    ret,img1=cv2.threshold(GrayImage,127,255,cv2.THRESH_TRUNC) 
    ret,img=cv2.threshold(img1,93,255,cv2.THRESH_BINARY)#阈值93去噪，以上两句是去掉在格子笔记本上写数字的格子背景
    
    #下边这些代码是去噪之后的图片后重新读取，如果不这样做，selective_search会报错，因为不能连续灰度化两次输出给selective_search
    cv2.imwrite(image_path,img)
    cv2.imshow('image', img)
    img = cv2.imread(image_path)
    
    # 白底黑字图 改为黑底白字图
    img = 255 - img

    # selectivesearch 调用selectivesearch函数 对图片目标进行搜索
    img_lbl, regions = selectivesearch.selective_search(img, scale=200, sigma=0.9, min_size=20)

    # print(regions[0])  # {'labels': [0.0], 'rect': (0, 0, 585, 301), 'size': 160699}  第一个为原始图的区域
    print("totally searched %d regions" % len(regions))  # 共搜索到199个区域

    # 接下来我们把窗口和图像打印出来，对它有个直观认识
    cv2.imshow('image', img)
    # 计算区域面积均值
    area = 0
    for reg in regions:
        x, y, w, h = reg['rect']
        area += w * h
    area /= len(regions)
    # 展示区域分布
    show_fig(img, [data['rect'] for data in regions])

    # 第三步：过滤掉冗余的窗口
    # 1）第一过滤
    candidates = first_filter(area, regions)
    print('after first filter left %d regions' % len(candidates))

    # 展示第一次过滤后的区域分布
    show_fig(img, candidates)

    # 2)第二次过滤 大圈套小圈的目标 只保留大圈
    num_array = second_filter(candidates)

    # 窗口过滤完之后的数量
    print('after second filter left %d regions' % len(num_array))

    # 3) 展示第二次过滤后的区域分布
    show_fig(img, num_array)

    # 第四步：将数字进行排序（从上往下，从左到右）
    image_data = order_number(img, num_array)

    # 保存结果
    np.save('./image_data.npy', image_data)#然后用image_data.npy和MNIST训练之后的结果对比即可


if __name__ == '__main__':
    extract_images()
