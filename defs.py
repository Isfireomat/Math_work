import random
import math
from PyQt5.QtGui import QColor
import queue
from copy import deepcopy
import json

def replace_common_keys(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key] = dict2[key]
    return dict1

def modify_masiv(masiv, n):    
    if n > 0: 
        for i in range(len(masiv)):
            masiv[i].extend([0] * n)
    elif n < 0:
        for i in range(len(masiv)): 
            masiv[i] = masiv[i][:n]
    return masiv

def grouped_on_dict(masiv,size,file_path):
    masiv=[str(i) for i in masiv]
    # if len(masiv)%size: masiv+=["" for _ in range(size-len(masiv)%size)]
    with open(file_path,'w') as f:
        json.dump({"Numbers":masiv},f,indent=4)

def abbreviation(masiv):
    new_masiv=[]
    carry=True
    for i in masiv:
        if carry:
            if type(i)!=list:
                new_masiv.append(i)
                if i['type']=='stroka':
                    carry=False
        else: 
            new_masiv.append(i)
    return new_masiv

def view_error(masiv,cz):
    for i in masiv:
        if not i in [0,1]:
            return True
    else:
        if sum(masiv)!=cz:
            return True
    return False

def isled(masiv,cz):
    errors=queue.LifoQueue()
    for i in masiv:
        for j in i:
            if not j in [0,1]:
                errors.put(True)
                break
        else:
            if sum(i)!=cz:
                errors.put(True)
            else: errors.put(False)
    return errors

def find_all_repet(masiv):
    repeat_masiv = queue.LifoQueue()
    repeat_masiv.put([0 for _ in range(len(masiv[0]))])
    for i in range(1,len(masiv)):
        repeat_podmasiv=[0 for _ in range(len(masiv[0]))]
        for j in range(len(masiv[i])):
            if masiv[i][j]==1 and masiv[i-1][j]==masiv[i][j]: 
                repeat_podmasiv[j]=1
        repeat_masiv.put(repeat_podmasiv)
    return repeat_masiv

def normal_generate(normal):
    return [normal-1,normal,normal+1]

def color_generat(count,size):
    colors=[]
    standart_colors=[QColor(105,165,145),QColor(117,105,140),QColor(122,147,121),QColor(185,136,163),QColor(137,167,124),QColor(155,121,157)]
    for i in range(math.ceil(count/size))  :
        for _ in range(size):
            colors.append(standart_colors[i%len(standart_colors)])
    return colors
    
def input_random(masiv,work_count):
    for i in range(len(masiv)):
        for j in random.sample(range(len(masiv[i])), work_count):
            masiv[i][j]=1
    
def generate(day_count,chiken_count):
    return [[0 for _ in range(chiken_count)] for _ in range(day_count)]

def calculate_cycles(day_count,cycle_days,start_cycle):
        cycles=0
        while cycles*start_cycle+cycle_days<day_count:
            cycles+=1
        return cycles+1

def sumator_end_to_start(masiv):
    for i in range(len(masiv))[::-1]:
        masiv[i]=sum(masiv[:i+1])
    return masiv

def repeat(m,pred_masiv,start_cycle):
    masiv_10=deepcopy(m)
    if pred_masiv: 
        masiv_10.insert(0,pred_masiv)
    masiv_10=masiv_10[::-1]
    repetitions_all=0
    repetitions_day=0
    for i in range(1,len(masiv_10)):
        support=False
        for j in range(len(masiv_10[i])):
            if masiv_10[i][j]==1 and masiv_10[i-1][j]==masiv_10[i][j]: 
                repetitions_all+=1
                support=True
        if support: repetitions_day+=1 
    return repetitions_day, repetitions_all,m[start_cycle-1]

def otstup(masiv,size_sum_masiv):
    masiv=deepcopy(masiv)
    masiv_otstup=[0 for _ in range(math.ceil(len(masiv[0]) / size_sum_masiv))]
    for x in range(len(masiv)):
        masiv[x] = [masiv[x][i:i + size_sum_masiv] for i in range(0, len(masiv[x]), size_sum_masiv)]    
    sumator=0
    for x in range(len(masiv[0])):
        if sum(masiv[0][x])==0:
            sumator=0
            for y in range(len(masiv)):
                if sum(masiv[y][x])!=0: break
                sumator-=1
        else: 
            sumator=0
            for y in range(len(masiv)):
                if sum(masiv[y][x])==0: break 
                sumator+=1    
        masiv_otstup[x]=sumator
    return masiv_otstup
def solv_analitics(solv,m,normal,normal_radius):
    solv["column_sums"]=[sum(column) for column in zip(*m)]  
    solv["above_normal"]=sum([1 if i>normal and not i in normal_radius else 0 for i in solv["column_sums"]])
    solv["below_normal"]=sum([1 if i<normal and not i in normal_radius else 0 for i in solv["column_sums"]])
    solv["sum_even"]=sum([i if n%2==0 else 0 for n,i in enumerate(solv["column_sums"])])
    solv["sum_odd"]=sum([i if n%2!=0 else 0 for n,i in enumerate(solv["column_sums"])])
    solv["sum_above_normal"]=sum([i-normal if i>normal and not i in normal_radius else 0 for i in solv["column_sums"]])
    solv["sum_below_normal"]=sum([normal-i if i<normal and not i in normal_radius else 0 for i in solv["column_sums"]])
    return solv

def podsolver(m,end,normal_radius,day_count,cycle_days,start_cycle,size_sum_masiv,normal,befor_days,pred_masiv):
    solv={}
    start_process=cycle_days-befor_days  
    end_process=len(m)
    solv['sum_columns']=[sum(i+1 for i,v in enumerate(m[j]) if v) for j in range(start_process,end_process)]
    solv['repetitions_day'], solv['repetitions_all'],pred_masiv=repeat(m,pred_masiv,start_cycle)
    b_days=[sum([sum(list(zip(*m[:j]))[i]) for i,v in enumerate(m[j]) if v]) for j in range(start_process,end_process)] 
    # b_days_2=[sum([sum(list(zip(*m[:j]))[i]) for i,v in enumerate(m[j]) if v]) for j in range(start_process-1,end_process)] 
    solv["sumator_before_days"]=sumator_end_to_start(deepcopy(b_days))
    solv["before_days_sum"]=sum(b_days)   
    solv["before_days"]=b_days
    solv["after_day"]=end
    solv["column_sums"]=[sum(column) for column in zip(*m)]  
    solv["size_sum_masiv"] = [sum(solv["column_sums"][i:i + size_sum_masiv]) for i in range(0, len(solv["column_sums"]), size_sum_masiv)]
    solv["otstup_masiv"] = otstup(m[::-1],size_sum_masiv)
    solv=solv_analitics(solv,m,normal,normal_radius)
    if len(m)>=start_process: solv["prediction"]=[solv_analitics({},m[:j],normal,normal_radius) for j in range(start_process,end_process)]
    solv["raz_sum_normals"]=abs(solv["sum_above_normal"]-solv["sum_below_normal"])
    solv["type"]="analitika"
    return solv,pred_masiv

def solver(masiv,day_count,cycle_days,start_cycle,size_sum_masiv,normal,befor_days,work_count):
    normal_radius=normal_generate(normal) 
    solv_masiv=[]
    pred_masiv=None
    cycles=calculate_cycles(day_count,cycle_days,start_cycle)
    
    completed=False
    for cycle in range(cycles):
        begin=cycle*start_cycle
        end=cycle*start_cycle+cycle_days if cycle*start_cycle+cycle_days<=day_count else len(masiv)
        m=masiv[begin:end]
        solv,pred_masiv=podsolver(m,end,normal_radius,day_count,cycle_days,start_cycle,size_sum_masiv,normal,befor_days,pred_masiv)     
        solv_masiv.append(solv)
        if cycle==cycles-1:
            if (len(m)!=cycle_days or view_error(masiv[len(masiv)-1],work_count)) and len(m)>=cycle_days-start_cycle and completed:
                solv["after_day"]+=1
                solv_masiv.append({'dop_date':cycle_days-start_cycle,'type':'stroka',
                                'after_day':end-(len(m)-(cycle_days-start_cycle)),
                                'column_sums':[sum(column) for column in zip(*(m[:cycle_days-start_cycle]))]})
                #  before_days заменён на start_cycle 
            elif (completed or len(m)==cycle_days):  
                # solv,pred_masiv=podsolver(m[befor_days:],end,normal_radius,day_count,cycle_days,start_cycle,size_sum_masiv,normal,befor_days,pred_masiv)
                # solv['dop_date']=cycle_days-befor_days
                solv,pred_masiv=podsolver(m[start_cycle:],end,normal_radius,day_count,cycle_days,start_cycle,size_sum_masiv,normal,befor_days,pred_masiv)
                solv['dop_date']=cycle_days-start_cycle
                (cycle_days-start_cycle)
                solv_masiv.append(solv)    
        if cycle_days==len(m):
            completed=True
        else:
            completed=False
    j=0
    for i in range(len(solv_masiv)):
        if solv_masiv[i]["type"]=="analitika":
            j+=1
            solv_masiv[i]["number"]=j        
    print("+")
    return solv_masiv

def normolize_masiv(masiv,solv_masiv):
    for i in solv_masiv[::-1]:
        masiv.insert(i["after_day"],i)
    return masiv

def return_days(masiv):
    return sum([1 for i in masiv if isinstance(i,list)])

if __name__=="__main__":
    pass
    # for i in grouped_on_dict([1,2,3,4,5,6,7,8,9,10,11,12,13],3):(i)
    