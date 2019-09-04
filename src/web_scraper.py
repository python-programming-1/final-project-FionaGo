import requests
import lxml.html as lh
import pandas as pd

# websites with GMAT scores by school by ranking
url = 'https://www.mbacrystalball.com/gmat/gmat-average-score'

#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

#Create empty list
col=[]
i=0

#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    #print ('%d:"%s"'%(i,name))
    col.append((name,[]))

# Since out first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]
    # If row is not of size 3, the //tr data is not from our table
    if len(T) != 3:
        break
    # i is the index of our column
    i = 0
    # Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content()
        # Check if row is empty
        if i > 0:
            # Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        # Append the data to the empty list of the i'th column
        col[i][1].append(data)
        # Increment i for the next column
        i += 1

gmat_score_dict = {title:column for (title,column) in col}
gmat_score_df = pd.DataFrame(gmat_score_dict)
print(gmat_score_df)
