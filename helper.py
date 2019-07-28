
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

            
            
            