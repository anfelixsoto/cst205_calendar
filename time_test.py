from datetime import datetime

def convert_date(date):
    n_date = []
    for i in range(len(date) - 1):
        if(len(date[i]) == 1):
            n_date.append('0' + date[i])
        else:
            n_date.append(date[i])
    
    if(len(date[2]) == 2):
        n_date.append('20' + date[2])
    else:
        n_date.append(date[2])
    
    return(n_date[2] + '-' + n_date[0] + '-' + n_date[1])

def convert_24(str1):
    # Checking if last two elements of time 
    # is AM and first two elements are 12 
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
          
    # remove the AM     
    elif str1[-2:] == "AM": 
        return str1[:-2] 
      
    # Checking if last two elements of time 
    # is PM and first two elements are 12    
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
          
    else: 
          
        # add 12 to hours and remove PM 
        return str(int(str1[:2]) + 12) + str1[2:7] 

def convert(date, time):
    n_date = []
    temp = ''

    for i in range(len(date)):
        if date[i] != '/' and date[i] != '-':
            temp += date[i]
            if(i == len(date) - 1):
                n_date.append(temp)
                temp = ''
        else:
            n_date.append(temp)
            temp = ''
    
    n_d = convert_date(n_date)
    print(len(time))
    n_t = convert_24(time)

    return(n_d + 'T' + n_t + 'Z')

due_date = input('Enter date: ')
due_time = input('Enter time: ')

new_format = convert(due_date, due_time)
print(new_format)