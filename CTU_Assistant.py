import pickle
import re
from tensorflow.keras.models import load_model
import json
import nltk 
import numpy as np
import random
import handletext
MORE_REQUEST = "Bạn cần tôi giúp thêm điều gì không?"


content = json.load(open("test.json",encoding='utf_8'))

words = pickle.load(open('model_words.pkl','rb'))
classes = pickle.load(open('model_classes.pkl', 'rb'))
model = load_model('model.h5')

continueList = ['Bạn có cần tôi giúp thêm điều gì không?',
                'Mời bạn đặt thêm câu hỏi!',
                'Bạn vẫn còn câu hỏi chứ',
                'Tôi vẫn ở đây. Xin mời bạn tiếp tục!']

def clean_word(sentence):
    sentence_word = nltk.word_tokenize(sentence)
    return sentence_word


def words_achive(sentence):
    sentence_word = clean_word(sentence)
    bag = [0] * len(words)
    for s in sentence_word:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)



def label_predict(sentence):
    i = words_achive(sentence)
    res =  model.predict(np.array([i]))[0]
    ERROR_POINT= 0.1
    result = [[i,r] for i, r in enumerate(res) if r > ERROR_POINT]

    result.sort(key=lambda x:x[1], reverse=True) #Sort result > (if result >1)
    return_list = []
    for r in result:   
        return_list.append({'intents': classes[(r[0])], 'probability': str(r[1])})
    return return_list

def get_responces(label, cont):
    tag = label[0]['intents']
    list_content = cont['intents']
    for i in list_content:
        if i['tag'] == tag:
            result = i['responces']
            break
    return result


#voice 

#handle text 

def exit(data):
    for i in data["intents"]:
        if i['tag'] == "bye":
            result = random.choice(i["responces"])
    # test_Pytts3.speak(result)
    return result

def greeting(data):
    for i in data["intents"]:
        if i['tag'] == "greeting":
            result = random.choice(i["responces"])
    # else:
    #     result = random.choice(continueList)
    print(result)
    return result


def conversation(label, command,predict,content):
    founder = ''
    cont = ''
    if label == 'greeting':
        numOflist = get_responces(predict,content)
        founder = random.choice(numOflist)

    if founder:
        return founder
        # test_Pytts3.speak(founder)
    elif label == 'bye':
        return exit(content)
    else:
        numOflist = get_responces(predict,content)
        print(numOflist)
        f_location = handletext.file_location(numOflist)
        handletext.handleContent(command, label, numOflist, f_location)

        with open('backup.txt','r', encoding='UTF-8') as p:
            cont = p.read() + "\n" +MORE_REQUEST
            # if cont:
            #     test_Pytts3.speak(cont)
            # else:
            #     print("Nothing")
    return cont






# command = "một năm có bao nhiêu học kỳ"


# i = 0
# stop = 0
# loop = True
# while loop:
#     greeting(content,i)
#     print("đang lắng nghe")
#     print("....")
#     commands = testvoice.listen()
#     if commands:
#         print(commands)
def shothand(commands):
    predicts = label_predict(commands)
    print(predicts)
    label = predicts[0]['intents']
    print('label:',label)
    return conversation(label,commands,predicts,content)  

#     else:
#         if stop == 2 :
#             print("Kết thúc phiên làm việc!")
#             test_Pytts3.speak("Kết thúc phiên làm việc!")
#             loop = False
#         else:
#             print("Không nhận diện được giọng nói. Vui lòng thử lại!")
#             test_Pytts3.speak("Không nhận diện được giọng nói. Vui lòng thử lại!")
#             stop +=1
#     i+=1
