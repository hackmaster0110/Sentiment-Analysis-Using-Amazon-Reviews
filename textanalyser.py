from packs import *


class SentimentAnalyser():
    """Short summary.

    Parameters
    ----------
    **kwargs : type
        Description of parameter `**kwargs`.

    Attributes
    ----------
    __dict__ : type
        Description of attribute `__dict__`.
    doc : type
        Description of attribute `doc`.
    func_string : type
        Description of attribute `func_string`.
    funcstr_args : type
        Description of attribute `funcstr_args`.

    """
    def __init__(self,**kwargs):
        """Short summary.

        Parameters
        ----------
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        valid_keys = {'doc','regex','rewrite_new','func_string','funcstr_args','remove_urls','Clean'}
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
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        return self.doc    
    def get_word_count(self):
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

        """
        tokens = self.doc.split()
        self.count = Counter(tokens)    
        return self.count
    def encode_words(self,vocab_to_int_dict):
        return [vocab_to_int_dict[wrd] for wrd in self.doc.split()]


def csv_read_modifiy(filename,encoding = "ISO-8859-1"):
    """Short summary.

    Parameters
    ----------
    filename : type
        Description of parameter `filename`.

    Returns
    -------
    type
        Description of returned object.

    """
    # one_hot_dic = {'4':1,'0':0}
    with open(filename,'r',encoding = encoding) as f:
        lines = csv.reader(f)
        new_name = filename.split('/')[-1]
        with open('modified'+new_name,'w',encoding = encoding) as f1:
            writer = csv.writer(f1, delimiter=',')
            for line in tqdm(lines):
                row = []
                cleaned = SentimentAnalyser(doc = line[2],func_string = remove_words_startingwith,remove_urls = True).get_string()
                if cleaned:
                    row.append(cleaned)
                    row.append(line[0])
                    writer.writerow(row)
                else:
                    continue    
                
                    

# For very large file
def count_modifier(filename,encoding = "ISO-8859-1"):        
    """Short summary.

    Parameters
    ----------
    filename : type
        Description of parameter `filename`.
    encoding : type
        Description of parameter `encoding`.

    Returns
    -------
    type
        Description of returned object.

    """
    Net_Count = Counter()
    with open(filename,'r',encoding = encoding) as f:
        lines = csv.reader(f)
        for line in tqdm(lines):
            count = SentimentAnalyser(doc = line[0],Clean = False).get_word_count()
            Net_Count.update(count)
        with open('dumped_counts','wb') as f:
            pickle.dump(Net_Count,f)    
        return Net_Count    
            
#Faster,but uses more ram as it loads whole file,not suitable for very large files 
def count_modifier_rapid(filename,header=None,encoding = "ISO-8859-1"):        
    """Short summary.

    Parameters
    ----------
    filename : type
        Description of parameter `filename`.
    header : type
        Description of parameter `header`.
    encoding : type
        Description of parameter `encoding`.

    Returns
    -------
    type
        Description of returned object.

    """
    Net_Count = Counter()
    csv_file = pd.read_csv(filename,encoding = encoding,header = header,engine = 'c')
    for line in tqdm(csv_file[0]):
        count = SentimentAnalyser(doc = line,Clean = False).get_word_count()
        Net_Count.update(count)
    with open('dumped_counts','wb') as f:
        pickle.dump(Net_Count,f)    
    return Net_Count            
            
def vocab_to_int(count_dump_file):
    """Short summary.

    Parameters
    ----------
    count_dump_file : type
        Description of parameter `count_dump_file`.

    Returns
    -------
    type
        Description of returned object.

    """
    with open(count_dump_file, 'rb') as f:
        counts = pickle.load(f)
    sorted = counts.most_common()    
    vocab_to_int = {w:i+1 for i, (w,c) in enumerate(sorted)}
    with open('vocab_to_int','wb') as f1:
        pickle.dump(vocab_to_int,f1)    
    return vocab_to_int            
                            
def encode_text(vocab_to_int_dump,filename,encoding = "ISO-8859-1"):
    whole_feature = []
    whole_label = []
    whole = {}
    with open(vocab_to_int_dump, 'rb') as f:
        vocab_to_int_dict = pickle.load(f)
        with open(filename,'r',encoding = encoding) as f1:
            lines = csv.reader(f1)
            for line in tqdm(lines):
                whole_feature.append(SentimentAnalyser(doc = line[0],Clean = False).encode_words(vocab_to_int_dict))
                whole_label.append(int(line[1]))
            with open('encoded_wrds_labels','wb') as f2:
                whole['feature'] = whole_feature
                whole['label'] = whole_label
                pickle.dump(whole,f2)      
    return whole    
                