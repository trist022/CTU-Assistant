import json


fname = ['noiquy_quyche.txt',
        'daotao.txt',
        'danhgiaketqua.txt',
        'totnghiep.txt',
        'nhahoc.txt']

def getIndexofLine(key, floc):
    f = open(floc,'r', encoding='UTF-8')
    check = open(floc,'r', encoding='UTF-8')
    eof = check.readlines()
    index = []
    nLine = 0
    file_eof = 0
    orderedlist = []
    keyIndex = 'Điều thứ'
    LineIndex = 0
    flag = False
    for i, line in enumerate(f):
        if keyIndex in line:
            index.append(i)
        if key in line:
            # print(line)
            LineIndex = i
            flag = True
        if flag and line == '\n': #dong trong chi co duy nhat 1 ky tu la \n
            nLine = i
            flag = False
        if line[0].isdigit():
            orderedlist.append(i)
        if line == eof[len(eof)-1]:
            file_eof = i+1
    f.close()
    check.close()
    return LineIndex, index, file_eof, nLine, orderedlist

#get end point of data
def Endpoint(startpoint, index, file_eof, nLine, orderedlist):
    endpoint = 0
    if not index and not orderedlist:
        endpoint = nLine
        return endpoint
    elif startpoint not in orderedlist:
        for i, num in enumerate(index): 
            if startpoint == num and index[-1]!=num:
                endpoint = index[i+1]
                break
            elif startpoint == num and index[-1]==num:
                endpoint = file_eof  
            elif startpoint != num:
                endpoint = nLine
        return endpoint
    else:
        for i, num in enumerate(orderedlist):
            for x in range(len(index)):
                if startpoint == num and orderedlist[-1]!=num:
                    if num < index[-1]:
                        if num > index[x] and  num < index[x+1]:
                            if orderedlist[i+1] < index[x+1]:
                                endpoint = orderedlist[i+1]
                                break 
                        elif num < index[x]:
                            print(num,index[x])
                            endpoint = index[x]
                            break
                    else:
                        endpoint = orderedlist[i+1]
                        break
                elif startpoint == num and orderedlist[-1]==num:
                    if num < index[x]:
                        endpoint = index[x]
                        break
                    else:
                        endpoint = file_eof
                        break
        return endpoint

#get result by start point and end point
def getContent(key, location):
    isFound = []
    startpoint, indexs, file_eof, nLine, orderedlist = getIndexofLine(key,location)
    endpoint = Endpoint(startpoint, indexs, file_eof, nLine, orderedlist)
    # print("index",indexs,'eof',file_eof,'nline',nLine,"od",orderedlist)
    # print(startpoint, endpoint)
    with open(location,'r', encoding='UTF-8') as backup:
        content =backup.readlines()
        isFound = content[startpoint:endpoint]
     
    # print(line)
    backup.close()
    return isFound

    
def WFile(element):
    with open('backup.txt','w',encoding='UTF-8') as b:
        b.write(element)
    b.close()

def handleContent( request, label, numOflist, floc):
    # print('endpoint',endpoint)
    if numOflist == 4:
        content = json.load(open("tag.json",encoding='utf_8'))
        tag = []
        for intent in content["intents"]:
            for patt in intent["patterns"]:
                tag.append(patt)
        flag = True
        for key in tag:
            if key in request.upper():
                print("ok", key)
                buiding = key
        num = ""
        result = getContent(buiding,floc)
        for w in request.split():
            if w.isdigit() and int(w)/100 > 1: #kiem tra dam bao so phong la 3 chu so > 100
                print(int(w)/100)
                num = w
                flag = True
                break
            else:
                flag = False
        if num and flag:
            TextResult = "Phòng học "+ num + " lầu "+ num[0] +" "+ result[0]
            # print("phòng học "+num, "lầu "+num[0], result)
            print(TextResult)
            WFile(TextResult)
            
        else:
            print(result)
            WFile(result)
    else:
        FileContent = getContent(label,floc)
        FileContent = ' '.join(FileContent)
        print(FileContent)
        WFile(FileContent)

def file_location(index):
    floc = 'Database/' + fname[index]
    return floc

# request = "phòng học 201 TTGDQP: ở đâu?"
# numOflist = 0
# buiding = ""
# requi = "CLCxCN"
# floc = 'Database/' + fname[0]
# handleContent("Học kỳ chính kéo dài", "Học kỳ chính kéo dài", 0, floc)


# with open('backup.txt','r', encoding='UTF-8') as p:
#     cont = p.read()
#     speak(cont)