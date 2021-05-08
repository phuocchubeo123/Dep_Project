import torch
import torch.nn as nn
import numpy as np
import numpy.random as random
import json

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(RNN, self).__init__()
        self.gru = nn.GRU(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.foc = nn.Linear((hidden_size), (num_classes))

    def forward(self, x):
        x, h_n = self.gru(x)
        output = self.foc(h_n[-1])
        return output

def load_word_dict():
    tf = open("E:/project deep/word_list_111.json", "r")
    word_dict = json.load(tf)
    tf.close()
    return word_dict

def load_model():
    model = RNN(input_size=2 * 21 * 3, hidden_size=512, num_layers=2, num_classes=111)
    model.load_state_dict(torch.load('E:/project deep/final_model1.pt', map_location=torch.device('cpu')))
    model.eval()
    return model


def clear_zero(np_arr):
    indx = []
    for i in range(np_arr.shape[0]):
        if np.sum(np_arr[i]) == 0:
            indx.append(i)
    np_arr_del = np.delete(np_arr, indx, 0)
    return np_arr_del


def seq_len_filter(np_arr, seq_len):
    b_len = np_arr.shape[0]
    lucky_index = []
    for i in range(seq_len):
        lucky_index.append(random.randint(0, b_len - 1))
    lucky_index.sort()
    new_np_arr = np_arr[lucky_index]
    new_np_arr = new_np_arr.reshape((1, seq_len, 126))
    return new_np_arr


def topk_correct(outputs, topk):
    outputs = outputs.topk(topk, dim=-1).indices
    return outputs
