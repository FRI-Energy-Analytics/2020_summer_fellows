import pandas as pd
import lasio
import matplotlib.pyplot as plt
from predict_from_model import make_prediction
import os.path
import gzip

class Node: 
    def __init__(self ,key): 
        self.key = key  
        self.child = [] 

df = pd.read_csv("data/original_lowered.csv").drop("Unnamed: 0", 1).reset_index(drop=True)
arr = df.label.unique()
cali_arr = ['calibration','diameter','radius']
time_arr = ['time','delta-t','dt']
gr_arr = ['gamma','ray','gr','gamma-ray']
sp_arr = ['sp','spontaneous','potential']
d_arr = ['correction','porosity']
p_arr = ['density','neutron','sonic']
p2_arr = ['dolomite','limestone']
r_arr = ['deep','shallow','medium']
sr_arr = ['a10','a20','ae10','ae20','10in','20in']
mr_arr = ['a30','ae30','30in']
dr_arr = ['a60','a90','ae60','ae90','60in','90in']
root = Node(None)
j = 0
for i in arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node(i)) 
    j += 1
for i in cali_arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node("caliper")) 
    j += 1
for i in time_arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node("sonic travel time")) 
    j += 1
for i in gr_arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node("gamma ray")) 
    j += 1
for i in sp_arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node("spontaneous potential")) 
    j += 1
root.child.append(Node("photoelectric")) 
root.child[j].child.append(Node("photoelectric effect")) 
j += 1
root.child.append(Node("bit")) 
root.child[j].child.append(Node("bit size")) 
j += 1
for i in sr_arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node("shallow resistivity")) 
    j += 1
for i in mr_arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node("medium resistivity")) 
    j += 1
for i in dr_arr:
    root.child.append(Node(i)) 
    root.child[j].child.append(Node("deep resistivity")) 
    j += 1
root.child.append(Node("density")) 
k = 0
for i in d_arr:
    root.child[j].child.append(Node(i)) 
    st = "density " + str(i)
    root.child[j].child[k].child.append(Node(st))
    k += 1
root.child.append(Node("porosity")) 
j += 1
k = 0
for i in p_arr:
    root.child[j].child.append(Node(i)) 
    st = str(i) + " porosity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
for i in p2_arr:
    root.child[j].child.append(Node(i)) 
    st = "density porosity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
root.child.append(Node("conductivity"))
j += 1
k = 0
for i in r_arr:
    root.child[j].child.append(Node(i)) 
    st = str(i) + " conductivity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
root.child.append(Node("resistivity")) 
j += 1
k = 0
for i in r_arr:
    root.child[j].child.append(Node(i)) 
    st = str(i) + " resistivity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
for i in sr_arr:
    root.child[j].child.append(Node(i)) 
    st = "shallow resistivity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
for i in mr_arr:
    root.child[j].child.append(Node(i)) 
    st = "medium resistivity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
for i in dr_arr:
    root.child[j].child.append(Node(i)) 
    st = "deep resistivity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
root.child[j].child.append(Node("micro")) 
st = "micro resistivity"
root.child[j].child[k].child.append(Node(st))
root.child.append(Node("res")) 
j += 1
k = 0
for i in r_arr:
    root.child[j].child.append(Node(i)) 
    st = str(i) + " resistivity"
    root.child[j].child[k].child.append(Node(st))
    k += 1
root.child.append(Node("cond")) 
j += 1
k = 0
for i in r_arr:
    root.child[j].child.append(Node(i)) 
    st = str(i) + " conductivity"
    root.child[j].child[k].child.append(Node(st))
    k += 1

def search(root, lst):
    arr = [root]
    arr = [c for node in arr for c in node.child if c]
    for i in lst.split():
        for node in arr:
            if i == node.key:
                return search_child(node,lst)
    return None

def search_child(node, lst):
    if len(node.child) < 1:
        return None
    elif len(node.child) == 1:
        return node.child[0].key
    else:
        for i in lst.split():
            for c in node.child:
                if i == c.key:
                    return search_child(c,lst)
    return None

class Alias(object):
      # Constructor
    def __init__ (self, dictionary = True, keyword_extractor = True, model = True):
        self.dictionary = dictionary
        self.keyword_extractor = keyword_extractor
        self.model = model
        self.duplicate, self.not_found = [], []
        self.output = {}
        
    def parse(self, path):
        las = lasio.read(path)
        mnem,desc,unit = [],[],[]
        for key in las.keys():
            mnem.append(key.lower())
            if str(las.curves[key].descr) == "" and str(las.curves[key].value) == "":
                desc.append("None")
            else:
                desc.append(str(las.curves[key].descr).lower())
            if str(las.curves[key].unit) == "":
                unit.append("Unitless")
            else:
                unit.append(str(las.curves[key].unit).lower())
        if self.dictionary == True:
            self.dictionary_parse(mnem)
        if self.keyword_extractor == True:
            self.keyword_parse(mnem, desc)
        if self.model == True:
            df = self.make_df(path)
            self.model_parse(df)
        return self.output, self.not_found
    
    def dictionary_parse(self, mnem):
        df = pd.read_csv("data/comprehensive_dictionary.csv").drop("Unnamed: 0", 1).reset_index(drop=True)
        dic = df.apply(lambda x: x.astype(str).str.lower())
        index = 0
        for i in mnem:
            if i in dic.mnemonics.unique():
                key = dic.loc[dic['mnemonics'] == i, 'label'].iloc[0] # can be reduced?
                self.output[i] = key
                self.duplicate.append(index)
            index += 1

    def keyword_parse(self, mnem, desc):
        pwls = pd.read_csv("/Users/destiny/EnergyAnalytics/Software/pwls.csv").drop("Unnamed: 0", 1)
        new_desc = [v for i, v in enumerate(desc) if i not in self.duplicate]
        new_mnem = [v for i, v in enumerate(mnem) if i not in self.duplicate]
        index = 0
        for i in new_desc:
            key = search(root, i)
            if key == None:
                if i in pwls['abbrev']:
                    self.output[new_mnem[index]] = pwls.loc[pwls['abbrev'] == i].index[0]
                else:
                    self.not_found.append(new_mnem[index])
            else:                    
                self.output[new_mnem[index]] = key
            index += 1

    def model_parse(self, df):
        path = self.build_test(df)
        new_dictionary = make_prediction(path)
        self.output.update(new_dictionary)

    def build_test(self, df):
        data_path = "data/"
        test_out = gzip.open(os.path.join(data_path, 'input.gz'), 'wt')
        for i in range(len(df)):
            fout = test_out
            lst = [df.description[i],df.units[i],df.mnemonics[i]]
            summary = [df.mnemonics[i]]
            fout.write(" ".join(lst) + "\t" + " ".join(summary) + "\n")
            fout.flush()
        test_out.close()
        return os.path.join(data_path, 'input.gz')

    def make_df(self, path):
        l,l2,l3 = [],[],[]
        las = lasio.read(path)
        for i in self.not_found:
            l.append(i)
            l2.append(str(las.curves[i].descr).lower())
            l3.append(str(las.curves[i].unit).lower())
        output_df = pd.DataFrame(
            {'mnemonics': l,
            'description': l2,
            'units': l3
            })
        return output_df