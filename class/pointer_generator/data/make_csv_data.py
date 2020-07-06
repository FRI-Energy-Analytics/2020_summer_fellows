import gzip
import os
import pandas as pd

data_path = os.path.dirname(os.path.abspath(__file__))

train_out = gzip.open(os.path.join(data_path, 'cnndm.gz'), 'wt')
valid_out = gzip.open(os.path.join(data_path, 'cnndm.val.gz'), 'wt')
test_out = gzip.open(os.path.join(data_path, 'cnndm.test.gz'), 'wt')
df = pd.read_csv("original_lowered.csv").drop("Unnamed: 0", 1).reset_index(drop=True)
df2 = pd.read_csv("final_test.csv").drop("Unnamed: 0", 1).reset_index(drop=True)
df = df.sample(frac=1).reset_index(drop=True)
count = 0
print_every = 100
print(df.describe())
for i in range(len(df2)):
    # if i < 908:
    #     fout = train_out
    # elif i > 908 and i < 1022:
    #     fout = valid_out
    # elif i > 1022:
    #     fout = test_out
    # **************new code starts here********** 
    fout = train_out
    # if i > 908 and i < 1022:
    #     fout = valid_out
    # **************new code ends here********** 
    lst = [df2.description[i],df2.units[i],df2.mnemonics[i]]
    summary = [df2.label[i]]
    fout.write(" ".join(lst) + "\t" + " ".join(summary) + "\n")
    count += 1
    if count % print_every == 0:
        print(count)
        fout.flush()
# **************new code starts here********** 
print(df2.describe())
for i in range(len(df2)):
    fout = test_out
    if i > len(df2)/2:
        fout = valid_out
    lst = [df2.description[i],df2.units[i],df2.mnemonics[i]]
    summary = [df2.label[i]]
    # print(lst,summary)
    fout.write(" ".join(lst) + "\t" + " ".join(summary) + "\n")
    count += 1
    if count % print_every == 0:
        print(count)
        fout.flush()
# **************new code ends here********** 

train_out.close()
valid_out.close()
test_out.close()