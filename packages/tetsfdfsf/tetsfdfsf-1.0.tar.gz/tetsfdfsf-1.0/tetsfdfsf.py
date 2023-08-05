def ave(a):    #列表求平均价格
    b=0
    for c in a:
        b+=float(c)
    return b/len(a)