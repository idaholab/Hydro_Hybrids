import numpy as np
import pandas as pd
import datetime

import matplotlib as mpl
from matplotlib import pyplot as plt




def plotModelTrainingLoss(results,save=None,show=False):
    fig,ax=plt.subplots(dpi=120,figsize=(6,4))
    plt.plot(results.history['loss'])
    plt.plot(results.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Training', 'Validation'], loc='upper right')
    if show:
        plt.show()
    if save is not None:
        fig.savefig(save,dpi=300,bbox_inches='tight')
    plt.close()

def plotPredsVsActuals(preds,labels,save=None,title=None,show=False):
    fig,ax=plt.subplots(dpi=180,figsize=(6,4))
    plt.scatter(preds,labels,c='black',s=1)
    plt.xlabel('Predictions')
    plt.ylabel('Actual')
    plt.title(title)
    #plt.xlim(0,1)
    #plt.ylim(0,1)
    if show:
        plt.show()
    if save is not None:
        fig.savefig(save,dpi=300,bbox_inches='tight')
    plt.close()


def plotPCA_ratios(variance,save=None,title=None):
    fig,ax=plt.subplots(dpi=180,figsize=(6,4))
    plt.plot(variance,c='black')
    #plt.xlabel('Predictions')
    #plt.ylabel('Actual')
    plt.title(title)
    #plt.xlim(0,1)
    #plt.ylim(0,1)
    if save is not None:
        fig.savefig(save,dpi=300,bbox_inches='tight')
    plt.show()
    plt.close()

def plot_2d_image(data,save=None):
    fig,ax=plt.subplots(dpi=120,figsize=(6,6))
    plt.imshow(data)
    if save is not None:
        fig.savefig(save,dpi=300,bbox_inches='tight')
    plt.colorbar()
    plt.show()
    plt.close()
    
def plot_histogram(data,title=None,save=None):
    fig,ax=plt.subplots(dpi=120,figsize=(6,6))
    plt.hist(data,bins=500,color='black')
    plt.title(title)
    if save is not None:
        fig.savefig(save,dpi=300,bbox_inches='tight')
    plt.show()
    plt.close()
    
def plotTimeSeries(pred,actual,ylbl,title=None,save=None,show=False):
    fig,ax=plt.subplots(dpi=120,figsize=(6,4))
    plt.plot(pred,color='red',label='Predicted',linewidth=0.75)
    plt.plot(actual,color='black',label='Actual',linewidth=0.75)
    plt.xticks(rotation=45)
    plt.ylabel(ylbl)
    plt.legend()
    plt.title(title)
    if show:
        plt.show()
    if save is not None:
        fig.savefig(save,dpi=300,bbox_inches='tight')
    plt.close()
    
    
def addDays(df):
    df['month']=df.index.month
    df['day']=df.index.day
    df['year']=df.index.year
    df['month']=df['month'].astype(str)
    df['day']=df['day'].astype(str)
    df['year']=df['year'].astype(str)
    df['month_day']=df['month']+'/'+df['day']+'/'+df['year']
    del df['month']
    del df['day']
    del df['year']
    return df

def buildWindows(X,y,X_feats,y_feats,size):
    X_array=[]
    y_array=[]
    for name,group in X.groupby(by='month_day'):
        start=0
        end=size    
        X_day=group[X_feats].values
        y_day=y[y['month_day']==name]
        y_day=y_day[y_feats].values

        while end<289:
            X_array.append(X_day[start:end,:].flatten())
            y_array.append(y_day[start:end,:].sum(axis=0))
            start+=1
            end+=1
    X_array=np.array(X_array)
    y_array=np.array(y_array)
    return X_array,y_array

def buildWindows_groups(X,y,X_feats,y_feats,size):
    X_array=[]
    y_array=[]
    for group_name,group_group in X.groupby(by='group'):
        for name,group in group_group.groupby(by='month_day'):
            start=0
            end=size    
            X_day=group[X_feats].values
            y_group=y[y['group']==group_name]
            y_day=y_group[y_group['month_day']==name]
            y_day=y_day[y_feats].values

            while end<289:
                X_array.append(X_day[start:end,:].flatten())
                y_array.append(y_day[start:end,:].sum(axis=0))
                start+=1
                end+=1
    X_array=np.array(X_array)
    y_array=np.array(y_array)
    return X_array,y_array

def buildWindows_cnn(X,y,X_feats,y_feats,size):
    X_array=[]
    y_array=[]
    for name,group in X.groupby(by='month_day'):
        start=0
        end=size    
        X_day=group[X_feats].values
        y_day=y[y['month_day']==name]
        y_day=y_day[y_feats].values

        while end<289:
            hour_array=X_day[start:end,:]
            hour_array=hour_array.reshape(hour_array.shape+(1,))
            X_array.append(hour_array)
            y_array.append(y_day[start:end,:].sum(axis=0))
            start+=1
            end+=1
    X_array=np.array(X_array)
    y_array=np.array(y_array)
    return X_array,y_array

def buildTestWindows(X,y,X_feats,y_feats,size):
    X_array=[]
    y_array=[]
    index_array=[]

    for name,group in X.groupby(by='month_day'):
        start=0
        end=size
        X_day=group[X_feats].values
        y_day=y[y['month_day']==name]
        y_day=y_day[y_feats].values
        i=0
        while end<289:
            if i<10:
                hour='0{0}:00'.format(i)
            else:
                hour='{0}:00'.format(i)
            datetime_string='{0} {1}'.format(name,hour)
            index_array.append(datetime.datetime.strptime(datetime_string,'%m/%d/%Y %H:%M'))
            X_array.append(X_day[start:end,:].flatten())
            y_array.append(y_day[start:end,:].sum(axis=0))
            start+=12
            end+=12
            i+=1
    X_array=np.array(X_array)
    y_array=np.array(y_array)
    index_array=np.array(index_array)
    return X_array,y_array,index_array

def buildTestWindows_groups(X,y,X_feats,y_feats,size):
    X_array=[]
    y_array=[]
    index_array=[]
    group_array=[]
    for group_name,group_group in X.groupby(by='group'):
        for name,group in group_group.groupby(by='month_day'):
            start=0
            end=size
            X_day=group[X_feats].values
            y_group=y[y['group']==group_name]
            y_day=y_group[y_group['month_day']==name]
            y_day=y_day[y_feats].values
            i=0
            while end<289:
                if i<10:
                    hour='0{0}:00'.format(i)
                else:
                    hour='{0}:00'.format(i)
                datetime_string='{0} {1}'.format(name,hour)
                index_array.append(datetime.datetime.strptime(datetime_string,'%m/%d/%Y %H:%M'))
                X_array.append(X_day[start:end,:].flatten())
                y_array.append(y_day[start:end,:].sum(axis=0))
                group_array.append(group_name)
                start+=size
                end+=size
                i+=int(size/12)
    X_array=np.array(X_array)
    y_array=np.array(y_array)
    index_array=np.array(index_array)
    group_array=np.array(group_array)
    return X_array,y_array,index_array,group_array

def buildTestWindows_groups_inference(X,X_feats,size):
    X_array=[]
    #y_array=[]
    index_array=[]
    group_array=[]
    for group_name,group_group in X.groupby(by='group'):
        for name,group in group_group.groupby(by='month_day'):
            start=0
            end=size
            X_day=group[X_feats].values
            #y_group=y[y['group']==group_name]
            #y_day=y_group[y_group['month_day']==name]
            #y_day=y_day[y_feats].values
            i=0
            while end<289:
                if i<10:
                    hour='0{0}:00'.format(i)
                else:
                    hour='{0}:00'.format(i)
                datetime_string='{0} {1}'.format(name,hour)
                index_array.append(datetime.datetime.strptime(datetime_string,'%m/%d/%Y %H:%M'))
                X_array.append(X_day[start:end,:].flatten())
                #y_array.append(y_day[start:end,:].sum(axis=0))
                group_array.append(group_name)
                start+=size
                end+=size
                i+=int(size/12)
    X_array=np.array(X_array)
    #y_array=np.array(y_array)
    index_array=np.array(index_array)
    group_array=np.array(group_array)
    return X_array,index_array,group_array

def buildTestWindows_cnn(X,y,X_feats,y_feats,size):
    X_array=[]
    y_array=[]
    index_array=[]

    for name,group in X.groupby(by='month_day'):
        start=0
        end=size
        X_day=group[X_feats].values
        y_day=y[y['month_day']==name]
        y_day=y_day[y_feats].values
        i=0
        while end<289:
            if i<10:
                hour='0{0}:00'.format(i)
            else:
                hour='{0}:00'.format(i)
            datetime_string='{0} {1}'.format(name,hour)
            index_array.append(datetime.datetime.strptime(datetime_string,'%m/%d/%Y %H:%M'))
            hour_array=X_day[start:end,:]
            hour_array=hour_array.reshape(hour_array.shape+(1,))
            X_array.append(hour_array)
            y_array.append(y_day[start:end,:].sum(axis=0))
            start+=12
            end+=12
            i+=1
    X_array=np.array(X_array)
    y_array=np.array(y_array)
    index_array=np.array(index_array)
    return X_array,y_array,index_array

def add_X_features(df,feats_df):
    x_cols=feats_df.columns
    new_df_array=[]
    for name,group in df.groupby(by='group'):
        feats=feats_df[feats_df['group']==name]   
        for col in x_cols:
            if col!='group': 
                #group[col]=feats_df.loc[name,col]
                group[col]=feats.loc[name, col]
        new_df_array.append(group)
    new_df=pd.concat(new_df_array)
    return new_df


def ann_0(xTrain,yTrain,epochs,batchSize,lRate,val,patience,
          verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=10000,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=10000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(units=5000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=5000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=5000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=5000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(units=2000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=2000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=2000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=2000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(units=1000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=1000,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=1000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(Dense(units=250,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=100,activation='relu'))
    #model.add(BatchNormalization())
    #model.add(Dropout(0.2))
    model.add(Dense(units=4,activation='linear'))
    
    opt=optimizers.Nadam(learning_rate=lRate)
    #opt=optimizers.Adamax(lr=lRate,decay=decay)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_data=val,verbose=verb,callbacks=[es,checkpoint])
    return model,results


def ann_1(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(units=64,activation='relu'))
    #model.add(BatchNormalization())    
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=4,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results


def ann_2(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=4,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results


def ann_3(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    input_features=keras.layers.Input(shape=xTrain.shape[1])
    dense0_0=Dense(units=128,activation='relu')(input_features)
    dense0_1=Dense(units=256,activation='relu')(dense0_0)
    dense0_2=Dense(units=128,activation='relu')(dense0_1)
    dense0_3=Dense(units=64,activation='relu')(dense0_2)
    dense0_4=Dense(units=32,activation='relu')(dense0_3)
    dense0_5=Dense(units=16,activation='relu')(dense0_4)
    out0=Dense(units=1,activation='relu')(dense0_5)
    
    dense1_0=Dense(units=128,activation='relu')(input_features)
    dense1_1=Dense(units=256,activation='relu')(dense1_0)
    dense1_2=Dense(units=128,activation='relu')(dense1_1)
    dense1_3=Dense(units=64,activation='relu')(dense1_2)
    dense1_4=Dense(units=32,activation='relu')(dense1_3)
    dense1_5=Dense(units=16,activation='relu')(dense1_4)
    out1=Dense(units=1,activation='relu')(dense1_5)
    
    dense2_0=Dense(units=128,activation='relu')(input_features)
    dense2_1=Dense(units=256,activation='relu')(dense2_0)
    dense2_2=Dense(units=128,activation='relu')(dense2_1)
    dense2_3=Dense(units=64,activation='relu')(dense2_2)
    dense2_4=Dense(units=32,activation='relu')(dense2_3)
    dense2_5=Dense(units=16,activation='relu')(dense2_4)
    out2=Dense(units=1,activation='relu')(dense2_5)
    
    dense3_0=Dense(units=128,activation='relu')(input_features)
    dense3_1=Dense(units=256,activation='relu')(dense3_0)
    dense3_2=Dense(units=128,activation='relu')(dense3_1)
    dense3_3=Dense(units=64,activation='relu')(dense3_2)
    dense3_4=Dense(units=32,activation='relu')(dense3_3)
    dense3_5=Dense(units=16,activation='relu')(dense3_4)
    out3=Dense(units=1,activation='relu')(dense3_5)
    
    output=concatenate([out0,out1,out2,out3])
    
    model=keras.models.Model(inputs=input_features,outputs=output)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results



def cnn_4(xTrain,yTrain,epochs,batchSize,lRate,patience,inshape,
          val=None,verb=0,decay=None,model_save=None):
    '''
    This model matches the FireNet architecture (Dunnings)
    '''
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    model.add(layers.Conv2D(16,(3,3),activation='relu',input_shape=inshape,padding='same'))
    #model.add(layers.MaxPooling2D(pool_size=(3,3),padding='same'))
    model.add(BatchNormalization())
    
    model.add(layers.Conv2D(32,(3,3),activation='relu',padding='same'))
    #model.add(layers.MaxPooling2D(pool_size=(3,3),padding='same'))
    model.add(BatchNormalization())
    
    model.add(layers.Conv2D(64,(3,3),activation='relu',padding='same'))
    #model.add(layers.MaxPooling2D(pool_size=(3,3),padding='same'))
    model.add(BatchNormalization())
        
    model.add(layers.Flatten())
    
    model.add(layers.Dense(64,activation='tanh'))
    #model.add(Dropout(0.5))
    model.add(layers.Dense(32,activation='tanh'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=4,activation='linear'))
    
    ##try Nadam optimizer
    #opt=optimizers.Nadam(learning_rate=learningRate)
    #opt=optimizers.Adamax(lr=learningRate,decay=decay)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results


def ann_5(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=6,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results


def ann_6(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=5,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results

def ann_7(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=5,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results

def ann_8(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=5,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results

def ann_9(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=5,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results


def ann_10(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=5,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results

def ann_11(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=5,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results

def ann_12(xTrain,yTrain,epochs,batchSize,lRate,patience,
          val=None,verb=0,decay=None,model_save=None):
    
    es=EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=patience)
    checkpoint=ModelCheckpoint(model_save,monitor='val_loss',verbose=1,
                              save_best_only=True,mode='min',save_weights_only=False)
    
    model=Sequential()
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu',input_dim=xTrain.shape[1]))
    #model.add(Dropout(0.1))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dense(units=2000,activation='relu'))
    #model.add(BatchNormalization())
    model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=1024,activation='relu'))
    #model.add(Dropout(0.1))
    #model.add(Dense(units=512,activation='relu'))
    #model.add(BatchNormalization())    
    #model.add(Dense(units=256,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=128,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=64,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=32,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=16,activation='relu'))
    #model.add(Dropout(0.2))
    model.add(Dense(units=5,activation='linear'))
    
    #opt=optimizers.Nadam(learning_rate=lRate)
    opt=optimizers.Adam(learning_rate=lRate)
    model.compile(optimizer=opt,loss='mse',metrics=['mae'])
    #results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
    #                  validation_split=0.1,verbose=0,callbacks=[es])
    results=model.fit(xTrain,yTrain,epochs=epochs,batch_size=batchSize,
                      validation_split=0.1,verbose=verb,
                      shuffle=True,callbacks=[es,checkpoint])
    return model,results