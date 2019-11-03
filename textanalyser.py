from packs import *


class TextProcessor():
    """Class providing variaous functions for sentiment analysis.

    Parameters
    ----------
    valid arguments : 'doc','regex','func_string','funcstr_args','remove_urls','Clean'

    Attributes used in instantiation
    ----------
    Clean : Boolean
        True by default,Removes punctuation,lowers all letters,removes addition white spaces between words
    doc : String
        Sting to be processed
    func_string : Function
        Callable obj that process input string and returns a new string 
    funcstr_args : Dictionary 
        Arguments for func_string
    regex : Regex pattern 
        Currently not implemented    
    remove_urls : Boolean
        Remove urls from string if True

    """
    def filter(self,**kwargs):
        valid_keys = {'doc','regex','func_string','funcstr_args','remove_urls','Clean'}
        self.__dict__.update((k,v) for k,v in kwargs.items() if k in valid_keys)
        if 'doc' in self.__dict__:
            if len(self.doc.strip()) != 0:
                if 'remove_urls' in self.__dict__:
                    if self.remove_urls is True:
                        self.doc = re.sub(r"http\S+", "", self.doc) 
                # if 'regex' in self.__dict__:
                #     pass
                if 'func_string' in self.__dict__:
                    assert isinstance(self.func_string, types.FunctionType),'Requires a callable obj that returns string as type'    
                    if 'funcstr_args' in self.__dict__:
                        self.doc = self.func_string(self.doc,self.funcstr_args)
                    else:
                        self.doc = self.func_string(self.doc)
                Clean = self.__dict__.get('Clean',True)
                if Clean is True:    
                    self.doc = (self.doc.translate(str.maketrans('','',string.punctuation))).lower()
                    self.doc = ' '.join(self.doc.split())
            else:
                return ''        
    def get_string(self):
        """Method for obtaining the processed string

        Returns
        -------
        type String
            Returns processed string

        """
        return self.doc    
    def get_word_count(self):
        """Method for obtaining word count for each words in a string

        Returns
        -------
        type Count object
            Count object containing count of each word in the string.

        """
        tokens = self.doc.split()
        self.count = Counter(tokens)    
        return self.count
    def encode_words(self,vocab_to_int_dict):
        """Method for encoding the words in a string using a list of integers 

        Parameters
        ----------
        vocab_to_int_dict : Dictionary
            Dictionary consisting of word as key and integer as value

        Returns
        -------
        type list
            Returns string as list of integers

        """
        return [vocab_to_int_dict[wrd] for wrd in self.doc.split()]



def csv_read_modifiy(filename,encoding = "ISO-8859-1"):
    """Function for cleaning csv file and preprocessing,then writes new file

    Parameters
    ----------
    filename : String
        Name of the csv file
    encoding: String
        Encoding used in file
    
        

    """
    with open(filename,'r',encoding = encoding) as f:
        lines = csv.reader(f)
        new_name = filename.split('/')[-1]
        cleaner = TextProcessor()
        
        with open('modified'+new_name,'w',encoding = encoding) as f1:
            writer = csv.writer(f1, delimiter=',')
            for line in tqdm(lines):
                row = []
                cleaned = cleaner.filter(doc = line[2],func_string = remove_words_startingwith,remove_urls = True).get_string()
                if cleaned:
                    row.append(cleaned)
                    row.append(line[0])
                    writer.writerow(row)
                else:
                    continue    
                
    return 0                

            
            
def vocab_to_int(count_dump_file):
    """Function for encoding word using integer.Uses count of each words in whole file.Dumps encoding for each word in a dictionary

    Parameters
    ----------
    count_dump_file : String
        Name of dumped count file obtained by using count_modifier function

    Returns
    -------
    type Dictionary
        Integer encoding for all unique words in file

    """
    with open(count_dump_file, 'rb') as f:
        counts = pickle.load(f)
    sorted = counts.most_common()    
    vocab_to_int = {w:i+1 for i, (w,c) in enumerate(sorted)}
    with open('vocab_to_int','wb') as f1:
        pickle.dump(vocab_to_int,f1)    
    return vocab_to_int            
                            
def encode_text(vocab_to_int_dump,filename,encoding = "ISO-8859-1"):
    """Function for encoding whole file using integers with dictionary dumped by vocab_to_int function 
    and dumps featues and labels using pickle
    
    Parameters
    ----------
    vocab_to_int_dump : String
        Name of dumped dictionary obtained by executing vocab_to_int function 
    filename : String
        Name of csv file
    encoding : String
        Encoding used in the csv file

    Returns
    -------
    type Dictionary
        Dictionary consisting of encoded features and their respective labels

    """
    whole_feature = []
    whole_label = []
    whole = {}
    cln = TextProcessor()
    with open(vocab_to_int_dump, 'rb') as f:
        vocab_to_int_dict = pickle.load(f)
        with open(filename,'r',encoding = encoding) as f1:
            lines = csv.reader(f1)
            for line in tqdm(lines):
                whole_feature.append(cln.filter(doc = line[0],Clean = False).encode_words(vocab_to_int_dict))
                whole_label.append(int(line[1]))
            with open('encoded_wrds_labels','wb') as f2:
                whole['feature'] = whole_feature
                whole['label'] = whole_label
                pickle.dump(whole,f2)      
    return whole  
    
    

# def center_word_context_word_extractor(encoded_dump,window_size):
#     """Function for preprocessing word embedding data
#     write center word and corresponding context word to file
# 
#     Parameters
#     ----------
#     encoded_dump : pickle file
#         encoded string list
#     window_size : integer
#         Size of window
# 
# 
# 
# 
#     """
#     final = []
#     with open(encoded_dump, 'rb') as f:
#         whole = pickle.load(f)
#     with open('skipgram_context.txt','w') as f1:
#         for encoded_sentence in tqdm(whole['feature']):
#             out = skipgram(window_size,encoded_sentence)
#             if out is not None:
#                 json_string = json.dumps(out) + '\n'
#                 f1.write(json_string)
#     return 0

    
    
def reverse_vocab_to_int(vocab_to_int_dump):
    """Reversing vocab to int mapping to create  int to vocab mapping

    Parameters
    ----------
    vocab_to_int_dump : Pickle dump 
        Pickle dump of vocabulary to integer mapping

    """
    with open(vocab_to_int_dump,'rb') as f:
        vocab_to_int = pickle.load(f)
    int_to_vocab = reverse_dict(vocab_to_int)
    with open('int_to_vocab','wb') as f1:
        pickle.dump(int_to_vocab,f1)

    return 0
    
    
    
                """ Recently I came across Gensim package.It is super easy to create word embeddings with gensim.Also there a word embedding using very large data set.So I decided 
                to use the pretrained word embedding models.
                """    
                
                
                