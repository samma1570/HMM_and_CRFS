from bilstm.preprocess import read_file, tag_to_ix
from bilstm.model import *
import torch
from torch import nn
import torch.utils.data as Data
from torch import optim
EMBEDDING_DIM = 5
HIDDEN_DIM = 4
epochs=2


_,content,label=read_file('C:\\Users\\15708\\Desktop\\HMM_and_CRFS\\bilstm\\word.txt')

def train_data(content,label):
    train_data=[]
    for i in range(len(label)):
        train_data.append((content[i],label[i]))
    return train_data
data=train_data(content,label)

word_to_ix = {}
for sentence, tags in data:
    for word in sentence:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
model = BiLSTM_CRF(len(word_to_ix), tag_to_ix, EMBEDDING_DIM, HIDDEN_DIM)
#optimizer = optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)
optimizer=optim.Adam(model.parameters(),lr=1e-3)
#训练
# '''
for epoch in range(epochs):
    i = 0
    for sentence, tags in data:
        model.zero_grad()
        # print(sentence)
        # print(tags)
        sentence_in = prepare_sequence(sentence, word_to_ix)
        # print(sentence_in)
        targets = torch.tensor([tag_to_ix[t] for t in tags], dtype=torch.long)
        # print(targets)
        loss = model.neg_log_likelihood(sentence_in, targets)
        # print('i:{} , loss: {}'.format(i, loss.data[0]))
        loss.backward()
        optimizer.step()
        i+=1
    if epoch%10==0:
        print('epoch/epochs:{}/{},loss:{:.6f}'.format(epoch+1,epochs,loss.data[0]))

#保存
torch.save(model,'cws.model')
torch.save(model.state_dict(),'cws_all.model')
# '''