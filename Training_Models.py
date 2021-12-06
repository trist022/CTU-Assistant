import json
import nltk
import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import pickle

words = []      
document = []  
classes = []  


content = json.load(open("test.json",encoding='utf_8'))

for intent in content['intents']:
    for pattern in intent['patterns']:
        word = nltk.word_tokenize(pattern)
        
        words.extend(word)
        document.append((word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(list(set(words)))

print(words)
print('document:',document)
print('class:',classes)

training = []
output_empty = [0] * len(classes)


for doc in document:
    bag = []
    word_patterns = doc[0]
    for w in words:
        bag.append(1) if w in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1 # gan = 1 vao vi tri mang 3 chieu khi xuat hien tag
    training.append([bag, output_row])
    # print(bag)
    # print('doc:',doc)

random.shuffle(training)
training = np.array(training)
# print(training)
x_train = list(training[:, 0])
y_train = list(training[:, 1])
# print(x_train)
# print(y_train)

model = Sequential()
model.add(Dense(128, input_shape =(len(x_train[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]),activation='softmax'))

# model.summary()

sgd = SGD(lr = 0.01, decay = 1e-6 , momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(x_train), np.array(y_train), epochs=1000, batch_size=17, verbose=1)

#save opject of model with binary pickle file

pickle.dump(words, open('model_words.pkl', 'wb'))
pickle.dump(classes, open('model_classes.pkl', 'wb'))
model.save('model.h5')