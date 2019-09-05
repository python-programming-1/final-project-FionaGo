import requests
import lxml.html as lh
import pandas as pd

def main():
    gmat_score_df = gmat_requirements()
    #print(gmat_score_df)

    school_ranking = gmat_score_df['school_ranking']

    gmat_score_df['avg_GPA'] = 0.0
    avg_GPA = gmat_score_df['avg_GPA']

    admission_requirements_by_school = \
        gpa_requirements(gmat_score_df,
                        school_ranking,
                        avg_GPA)

    print(admission_requirements_by_school)

    decision_support(gmat_score_df)

def gmat_requirements():
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

    #rename the columns
    gmat_score_df.rename(columns={"GMAT Ranking": "school_ranking",
                                  "Business School": "school_name",
                                  "Average GMAT Score": "average_GMAT_score"},
                         inplace=True)

    gmat_score_df['school_ranking'] = gmat_score_df['school_ranking'].astype('int64', copy=False)

    return gmat_score_df


def gpa_requirements(df, school_ranking, avg_GPA):
    # to add the logic that:
    # if the school ranking is between 1-20 then the GPA requirements are 3.5 to 3.7
    # for ranking between 21-40 then requirement is 2.7 to 3.5
    # ranking beyond 40 then GPA requirement can be below 2.7 but always has to be greater than 2.0

    # reference:
    # https://www.investopedia.com/articles/personal-finance/010215/gpa-and-applying-mba-program.asp

    df['avg_GPA'] = [3.5 if x <=20 else (2.7 if x > 20 and x <= 40 else 2.0) for x in df['school_ranking']]

    return df


def decision_support(df):
    applicant_gmat_input = int(input(
        "Welcome! Please type your GMAT score (0 - 800)!\n"
    ))

    gmat_query = applicant_gmat_input
    df = df.query('average_GMAT_score <= %d' % gmat_query)

    print("Here is the list of schools you can consider based on your GMAT score!\n",  df)

    applicant_gpa_input = float(input(
        "Again! Please type your GPA (0.0-4.0)!\n"
    ))

    gpa_query = applicant_gpa_input
    df = df.query('avg_GPA <= %d' % gpa_query)

    print("Here is the list of schools you can consider based on your GMAT and GPA!\n", df)

    return df

if __name__ == "__main__":
    main()


