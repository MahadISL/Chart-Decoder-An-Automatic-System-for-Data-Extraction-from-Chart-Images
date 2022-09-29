from tabulate import tabulate


def table1(a_dict, pd, classn):
    list1 = []
    list2 = []
    d = a_dict.items()
    for key, value in d:
        val1 = key
        val2 = value
        val2.insert(0, val1)
        val3 = tuple(val2)
        list2.append(val3)
    val4 = data_value(pd, classn)
    val4.insert(0, "Data Values")
    val4 = tuple(val4)
    list2.append(val4)
    result = tuple(list2)
    print(result)

    return result


def data_value(pd, classn):
    if classn == "Stacked Vertical Bar Chart" or classn == "Grouped Vertical Bar chart":
        list1 = []
        list2 = []
        list3 = []
        for idx, row in pd.iterrows():
            b = int(row['ymin'])
            a = int(row['ymax'])
            list1.append(a)
            list2.append(b)
        minimum_max_val = findmax(list1)
        maximum_min_val = findmin(list2)
        h = maximum_min_val - minimum_max_val
        for idx, row in pd.iterrows():
            if row['name'] == 'bar':
                height = row['ymax'] - row['ymin']
                value = int((height / h) * 100)
                value = abs(value)
                value = str(value) + '%'
                list3.append(value)
    elif classn == "Stacked Horizontal Bar Chart" or "Grouped Horizontal Bar chart":
        list1 = []
        list2 = []
        list3 = []
        for idx, row in pd.iterrows():
            b = int(row['xmax'])
            a = int(row['xmax'])
            list1.append(a)
            list2.append(b)
        minimum_max_val = findmax(list1)
        maximum_min_val = findmin(list2)
        w = maximum_min_val - minimum_max_val
        print(w)
        for idx, row in pd.iterrows():
            if row['name'] == 'bar':
                width = row['xmax'] - row['xmin']
                value = int((width / w) * 100)
                value = abs(value)
                value = str(value) + '%'
                list3.append(value)
    return list3

def findmax(myList):
    myMax = myList[0]
    for i in myList:
        if i > myMax:
            myMax = i
    return myMax

def findmin(myList):
    myMin = myList[0]
    for i in myList:
        if i < myMin:
            myMin = i
    return myMin
