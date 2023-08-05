from rapidfuzz import fuzz,process
import pandas as pd 

def deduplication(df,cols,threshold):
        df['Matches']=''
        final_list=[]
        count=0
        df['Combined']=''
        for i in range(0,len(cols)):
                df['Combined']=df[cols[i]]+'+'+df['Combined']
        for  i in df['Combined']:
                count=count+1
                found_list=[]
                countExactMatch=0


                for found, score, matchrow in process.extract(i, df['Combined'], scorer=fuzz.token_set_ratio):
                        found.rstrip('+')
                        if score >=threshold:
                            if bool(i==found)==True:
                                countExactMatch=countExactMatch+1
                                if countExactMatch>1:
                                    found_list.append(found.rstrip('+')+'---> score : '+str(score))
                                else:
                                   found_list.append('')


                            else:
                                found_list.append(found.rstrip('+')+'---> score : '+str(score))




                final_list.append(found_list)

        for i in range(0,len(df)):
                df.at[i,'Matches']=final_list[i]
          
        df['Combined']=df['Combined'].str.rstrip('+')
        return df 







