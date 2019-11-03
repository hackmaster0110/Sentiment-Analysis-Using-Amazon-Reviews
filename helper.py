import os
from tqdm import tqdm
import json
import glob
import numpy as np
import pickle

def remove_words_startingwith(sentence,*args):
    """Function for removing words starting with particular characters

    Parameters
    ----------
    sentence : String
        String to be processed
    
    Returns
    -------
    type String
        Processed string 

    """
    valid_keys = {'remove_char':'@'}
    for lst in args:
        for dic in lst:
            for key,val in dic.items():
                if key in valid_keys:
                    valid_keys[key] = val
    new_sen = ''
    for word in sentence.split():
        if not(word.startswith(valid_keys['remove_char'])):
            new_sen = new_sen + ' ' + word
    return new_sen.strip()        
    
    
# def skipgram_gn(window_size,arr):
#     """Function for performing skip gram windowing
# 
#     Parameters
#     ----------
#     window_size : integer
#         Size of the window.
#     arr : list
#         string encoded using intgers
# 
#     Returns
#     -------
#     type list
#         Returns list of tuple containing center word and context words
# 
#     """
#     max_index = len(arr) - 1
#     assert window_size < max_index,"window_size must be less than length of array"  
#     assert window_size > 0,"window_size must be greater than 0"
#     assert len(arr) > 0,"List must not be empty"
#     assert isinstance(window_size,int) is True,"window_size must be an integer"
#     tmp = window_size
#     rel = []
#     for index,elem in enumerate(arr):
#         center_word = elem
#         val = index
#         val2 = index
#         for itm in range(window_size):
#             if val > 0:
#                 val -= 1
#                 rel.append((elem,arr[val]))
# 
#             if val2 < max_index:
#                 val2 += 1
#                 rel.append((elem,arr[val2]))
#     return rel

# For softmax             
def skipgram(window_size,arr):
    """Function for performing skip gram windowing

    Parameters
    ----------
    window_size : integer
        Size of the window.
    arr : list
        string encoded using intgers

    Returns
    -------
    type list
        Returns list of tuple containing center word and context words

    """
    max_index = len(arr) - 1
    if max_index <= 0:
        return None
    elif max_index+1 < window_size:
        window_size = max_index     
    assert len(arr) > 0,"List must not be empty"
    assert isinstance(window_size,int) is True,"window_size must be an integer"
    tmp = window_size
    rel = []
    for index,elem in enumerate(arr):
        center_word = elem
        val = index
        val2 = index
        new = []
        for itm in range(window_size):
            
            if val > 0:
                val -= 1
                new.append(arr[val])
                        
            if val2 < max_index:
                val2 += 1
                new.append(arr[val2])
        rel.append((arr[index],new))
    
    return rel


def reverse_dict(dict):
    """Function to reverse dictionary(Only dictionary with unique keys and values)

    Parameters
    ----------
    dict : Dictionary
        Dictionary to be reversed

    Returns
    -------
    type Dictionary
        Reversed dictionary

    """
    return {v: k for k, v in dict.items()}
    
    
            
# def split_to_batch(size_per_batch,file):
#     """Splits file to batches
# 
#     Parameters
#     ----------
#     size_per_batch : integer
#         Number of lines in one batch
#     file : string
#         Name of file which is to be splited into batches
# 
#     Returns
#     -------
#     type integer
#         Returns 0 if succeeded
# 
#     """
#     batch_num = 1
#     current_row = 1
#     if not os.path.exists('batches'):
#         os.makedirs('batches')
#     with open(file,'r') as f:
#         while True:
#             f1 = open('batches/batch' + str(batch_num) + '_' + file,'w')
#             while current_row <= size_per_batch: 
#                 line = next(f,'end')
#                 if line == 'end':
#                     return 0
#                 else:    
#                     f1.write(line)
#                 current_row += 1
#                 if current_row > size_per_batch:
#                     f1.close()
#                     batch_num += 1
#             current_row = 1
# 

def center_word_context_word_extractor_and_batcher(encoded_dump,window_size,batch_size,vocab_size,dtype):
    """Function for preprocessing word embedding data
    write center word and corresponding context word to file
    
    Parameters
    ----------
    encoded_dump : pickle file
        encoded string list
    window_size : integer
        Size of window

     """
    if not os.path.exists('npbatches'):
        os.makedirs('npbatches')
    with open(encoded_dump, 'rb') as f:
        whole = pickle.load(f)
    count = 1
    x,y = [],[]
    for encoded_sentence in tqdm(whole['feature']):
        out = skipgram(window_size,encoded_sentence)
        
        if out is not None:
            for index,sub_arr in enumerate(out):
                if len(x) == len(y):
                    if len(x) < batch_size:
                        x.append(to_one_hot([sub_arr[0]],vocab_size,dtype))
                        y.append(to_one_hot(sub_arr[1],vocab_size,dtype))
                    else:    
                        np.save('npbatches/features'+str(count),np.asarray(x))
                        np.save('npbatches/label'+str(count),np.asarray(y))
                        count += 1
                        x,y = [],[]
                        x.append(to_one_hot([sub_arr[0]],vocab_size,dtype))
                        y.append(to_one_hot(sub_arr[1],vocab_size,dtype))
                else:
                    return 'Error,Unequal feature and label size'
    if len(x) > 0:
        if len(x) == len(y):
            np.save('npbatches/features'+str(count),np.asarray(x))
            np.save('npbatches/label'+str(count),np.asarray(y))                
    return 0

def to_one_hot(word_id_list,vocab_size,dtype):
    """Short summary.

    Parameters
    ----------
    word_id_list : type
        Description of parameter `word_id_list`.
    vocab_size : type
        Description of parameter `vocab_size`.

    Returns
    -------
    type
        Description of returned object.

    """
    temp = np.zeros(vocab_size,dtype = dtype)
    for id in word_id_list:
        temp[id-1] = 1
    return temp
                    
                    
                    