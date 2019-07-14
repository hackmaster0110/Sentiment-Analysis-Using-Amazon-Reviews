
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