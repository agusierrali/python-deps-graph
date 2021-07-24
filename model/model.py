import networkx as nx, json
from base64 import b64decode
import csv
import operator
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from keras.preprocessing.sequence import pad_sequences
from spektral.layers import GCNConv
from keras import backend as K
import matplotlib.pyplot as plts

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

G4 = nx.read_gml('graphv6.gml')
adjacency = nx.adjacency_matrix(G4)
data = pd.read_csv("data.csv") 
classification = data['classification']
dataset = data.drop(columns=['classification','Unnamed: 0'])
labels = classification.values
m_labels=[]
count_baja=0
count_media=0
count_alta=0
count_muyalta=0
for i in range(len(labels)):
    if labels[i]=='baja':
        new=[1,0,0,0]
        count_baja=count_baja+1
    elif labels[i]=='media':
        new=[0,1,0,0]
        count_media=count_media+1
    elif  labels[i]=='alta':
        new=[0,0,1,0]
        count_alta=count_alta+1
    else:
        new=[0,0,0,1]
        count_muyalta=count_muyalta+1
    m_labels.append(new)  
print("Cantidad de instancias con clasificacion baja:",count_baja)
print("Cantidad de instancias con clasificacion media:",count_media)
print("Cantidad de instancias con clasificacion alta:",count_alta)
print("Cantidad de instancias con clasificacion muy alta:",count_muyalta)
labels_matrix = np.array(m_labels) #Matriz nx4 con las clasificaciones de las instancias
f_matrix=dataset #Matriz de fealtures
index_of_labeled = classification[classification.notnull()].index #Instancias clasificadas que son todas
np_index = np.array(index_of_labeled)
np.random.shuffle(np_index) 
train_indices = np_index[0:2423] # 70% para train
test_indices = np_index[2424:3116] #20% test 
valid_indices = np_index[3117:3462] #10% validación
training_mask = np.zeros((len(classification),),dtype=bool)
testing_mask = np.zeros((len(classification),),dtype=bool)
validating_mask = np.zeros((len(classification),),dtype=bool)

training_mask[train_indices] = True
testing_mask[test_indices] = True
validating_mask[valid_indices] = True

##Predict
predicting_mask = np.ones((len(classification),),dtype=bool)
predicting_mask[train_indices] = False
predicting_mask[test_indices] = False
print(predicting_mask)

    
#INPUT
A = adjacency #Matriz de adyasencia 
X = f_matrix #Matriz de fealtures
y = labels_matrix #Matriz nx4 con las clasificaciones de las instancias
train_mask = np.array(training_mask)
val_mask = np.array(validating_mask)
test_mask = np.array(testing_mask)        

#Parametros
channels = 16
N = X.shape[0] 
F = X.shape[1] 
n_classes = 4       
dropout = 0.01         
l2_reg = 5e-4 / 2    
learning_rate = 1e-3    
epochs = 100

#Definir capas
fltr = GCNConv.preprocess(A).astype('f4')
X_in = Input(shape=(F, ))
fltr_in = Input((N, ), sparse=True)
dropout_1 = Dropout(dropout)(X_in)
graph_conv_1 = GCNConv(channels,activation='relu',kernel_regularizer=l2(l2_reg),use_bias=False)([dropout_1, fltr_in])
dropout_2 = Dropout(dropout)(graph_conv_1)
graph_conv_2 = GCNConv(n_classes,activation='softmax',use_bias=False)([dropout_2, fltr_in])

#Constuir el modelo
model = Model(inputs=[X_in, fltr_in], outputs=graph_conv_2)
optimizer = Adam(lr=learning_rate)
model.compile(optimizer=optimizer,loss='categorical_crossentropy',metrics=['acc',f1_m,precision_m, recall_m])
model.summary()

#Entrenando el modelo 
X = np.asarray(X).astype(np.float32)
y=np.asarray(y).astype(np.float32)
validation_data = ([X, fltr], y, val_mask)
history=model.fit([X, fltr],y,sample_weight=train_mask,epochs=epochs,batch_size=N,validation_data=validation_data,shuffle=False)


#Graficando metricas durante el entrenamiento
acc=history.history['acc']
f_1=history.history['f1_m']
pre=history.history['precision_m']
recc=history.history['recall_m']
Epo=[i for i in range(100)]
plts.plot(Epo,acc,)
plts.show()

plts.plot(recc,pre)
plts.show()
##Evaluando el modelo
loss, accuracy, f1_score, precision, recall = model.evaluate([X, fltr],y,sample_weight=test_mask,batch_size=N)
print(loss, accuracy, f1_score, precision, recall)

#Clasificacion de instancias
preddd=model.predict([X, fltr],batch_size=N)
for i, p in enumerate(preddd):
    clasificacion=list(p).index(np.max(p))

