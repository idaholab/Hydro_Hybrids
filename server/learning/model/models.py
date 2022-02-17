from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers,optimizers
from tensorflow.keras import metrics
from tensorflow.keras.layers import concatenate
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint


def ann_5(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    model.add(Dense(units=128,activation='relu'))
    model.add(Dense(units=256,activation='relu'))
    model.add(Dense(units=128,activation='relu'))
    model.add(Dense(units=64,activation='relu'))
    model.add(Dense(units=32,activation='relu'))
    model.add(Dense(units=16,activation='relu'))
    model.add(Dense(units=5,activation='linear'))
    
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    
    return model,results