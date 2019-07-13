
def remove_words_startingwith(sentence,*kwargs):
    """Short summary.

    Parameters
    ----------
    sentence : type
        Description of parameter `sentence`.
    *kwargs : type
        Description of parameter `*kwargs`.

    Returns
    -------
    type
        Description of returned object.

    """
    valid_keys = {'remove_char':'@'}
    for lst in kwargs:
        for dic in lst:
            for key,val in dic.items():
                if key in valid_keys:
                    valid_keys[key] = val
    new_sen = ''
    for word in sentence.split():
        if not(word.startswith(valid_keys['remove_char'])):
            new_sen = new_sen + ' ' + word
    return new_sen.strip()        