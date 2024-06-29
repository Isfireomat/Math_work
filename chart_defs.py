import math

def get_analytics_list(masiv):
    return [i for i in masiv if type(i)==dict and i["type"]=="analitika"]

def get_before_days_sum_list(masiv):
    return [i["before_days_sum"] for i in masiv]

def get_before_days_list(masiv):
    l=[]
    for i in masiv: l.extend(i["before_days"])
    return l

def get_sum_columns_list(masiv):
    l=[]
    for i in masiv: l.extend(i["sum_columns"])
    return l

def get_average_number_list(masiv,days):
    l=[]
    for i in range(1,len(masiv)+1):
        m=masiv[0 if i+1-days<=0 else i-days:i]
        l.append(round(sum(m)/len(m)))
    return l        

def get_normal_plot(masiv,normal,days):
    average_number=get_average_number_list(masiv,days)
    x,y=[],[]
    for i,v in enumerate(average_number):
        if v!=normal:
            x.append(i+1)
            y.append(normal)
    return x,y

def get_points_significance_dict(masiv):
    d={}
    for i in masiv:
        if i in d:
            d[i]+=1
        else:
            d[i]=1
    return dict(sorted(d.items(), key=lambda item: (item[1], item[0]), reverse=True))
    # return dict(sorted(d.items(), key=lambda item: item[1]) 

def get_deviation_dict(masiv,normal):
    d={"less":0,"more":0,"deviation":0,"deviation_2":0}
    for i in masiv:
        if i>normal:
            d["more"]+=1
            d["deviation"]+=i-normal
        elif i<normal:
            d["less"]+=1
            d["deviation"]+=i-normal
    return d

def get_medium_nubmer(masiv):
    try:
        return sum(masiv)/len(masiv)
    except: return 0
def get_group_point(masiv,group):
    d={}
    for y in range(int(min(masiv)),int(max(masiv))-group+2):
        n=0
        for y2 in range(y,y+group):
            if y2 in masiv:
                n+=masiv.count(y2)            
        if n in d.keys(): d[n].append(f"{y}-{y+group-1}")
        else: d[n]=[f"{y}-{y+group-1}"]
    return max(d.keys()),d[max(d.keys())]

def pruning(masiv,comments,x):
    return masiv[-x:],comments[-x:]
    
def get_title(masiv,titles,params):
    new_titles=[]
    gap=params["start_cycle"]
    first_day=params["cycle_days"]-gap+1
    for i,v in enumerate(masiv):
        if v['before_days']:
            day=first_day+gap*i-1
            new_titles.extend(titles[day:day+len(v['before_days'])])
    return new_titles,[i+1 for i in range(len(masiv))]
        
        
        
if __name__=="__main__":
    print( get_average_number_list(masiv=[1,2,3,4,5,6,7,8,9,10],days=5) )