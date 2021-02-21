import math
import numpy as np
import csv
import random
import string

#Record consists fields: (1) Transaction ID (an integer), (2) Transaction sale amount (an integer), 
# (3) Customer name (string) and, (4) category of item.
class Record:
    def __init__(self,t_id,t_amount,cust_name,category):
        self.t_id=t_id
        self.t_amount=t_amount
        self.cust_name=cust_name
        self.category=category
    

#Bucket consists of a number of records, link to overflowing bucket and local depth, emptyspace.
class Bucket:
    def __init__(self,capacity):
        self.capacity=capacity
        self.count=0
        a=Record(-1,-1,'a',-1)
        x=[a for _ in range(capacity)]        
        self.record_arr=x
        self.overflow_bucket=None
        self.local_depth=0
        self.is_directory=False

    def fill_bucket(self,record):
        self.record_arr[self.count]=record



#Simulated Secondary memory with an array of very large size of Bucket datatype.
class Secondary_Memory:
    def __init__(self,record_buckets,directory_buckets):
        
        self.bucket_arr=record_buckets
        self.bucket_directory_arr=directory_buckets
        self.buckets_count=1
        self.bucket_directory_count=0
        self.filled_memory=0

    def add_bucket(self,bkt,bkt_count):
        if self.bucket_arr[bkt_count] is None:
            self.bucket_arr[bkt_count]=bkt
            self.buckets_count=self.buckets_count+1
        else:
            while self.bucket_arr[bkt_count] is None:
                bkt_count=bkt_count+1
            self.bucket_arr[bkt_count]=bkt
            self.buckets_count=self.buckets_count+1
        return bkt_count
    

    def overflow_bkt(self,record, prefix,bkt_link):
        count=self.buckets_count
        self.bucket_arr[count].record_arr[0]=record
        self.bucket_arr[count].count=self.bucket_arr[count].count+1
        self.bucket_arr[bkt_link].overflow_bucket=count
        self.buckets_count=self.buckets_count+1
    


    

#Directory_Entry consists of prefix , link to bucket    
class Directory_Entry:
    def __init__(self,prefix):
        self.prefix=prefix
        self.bucket_link=None

#Directory or bucket-hash-table
class Directory:
    def __init__(self):
        self.global_depth=0
        self.capacity=1024
        self.directories_arr=[]
        self.overflow=False
        self.count=0

    def add_entry_secondary_memory(self,entry):
        entry=Record(entry.prefix,entry.bucket_link,'x',1)
        count=Sec_memory.bucket_directory_count
        if count==0:
            capacity=Sec_memory.bucket_directory_arr[0].capacity
            enteries_count=Sec_memory.bucket_directory_arr[0].count    
            if enteries_count<capacity:
                Sec_memory.bucket_directory_arr[0].record_arr[enteries_count]=entry
                Sec_memory.bucket_directory_arr[0].count=Sec_memory.bucket_directory_arr[count-1].count+1
                self.count=self.count+1
            elif enteries_count==capacity:
                Sec_memory.bucket_directory_arr[1].record_arr[0]=entry
                Sec_memory.bucket_directory_arr[1].count=1
                Sec_memory.bucket_directory_count=Sec_memory.bucket_directory_count+1
                self.count=self.count+1    
        capacity=Sec_memory.bucket_directory_arr[count-1].capacity
        enteries_count=Sec_memory.bucket_directory_arr[count-1].count
        self.overflow=True
        if enteries_count<capacity:
            Sec_memory.bucket_directory_arr[count-1].record_arr[enteries_count]=entry
            Sec_memory.bucket_directory_arr[count-1].count=Sec_memory.bucket_directory_arr[count-1].count+1
            self.count=self.count+1
        elif enteries_count==capacity:
            print(count)
            Sec_memory.bucket_directory_arr[count].record_arr[0]=entry
            Sec_memory.bucket_directory_arr[count].count=1
            Sec_memory.bucket_directory_count=Sec_memory.bucket_directory_count+1
            self.count=self.count+1
        
    def add_entry(self,entry):
        if self.count<1024:
            self.directories_arr.append(entry)
            self.count=self.count+1
            
        else:
            self.add_entry_secondary_memory(entry)

    def find_dir_entry(self,prefix):
        #print("TTT",prefix)
        #print(self.count,self.directories_arr)
        overflow=self.overflow
        gd=self.global_depth
        count=self.count
        if overflow==False:
            for x in self.directories_arr:
                #print("LL",x.prefix)
                if x.prefix==prefix:
                    #print("YES")
                    return x.bucket_link
        else:
            for i in range(0,count):
                if i<1024:
                    if self.directories_arr[i].prefix==prefix:
                        return self.directories_arr[i].bucket_link
                
            cnt=Sec_memory.bucket_directory_count
            for i in range(0,cnt):
                cn=Sec_memory.bucket_directory_arr[i].count
                for j in range(0,cn):
                    xc=Sec_memory.bucket_directory_arr[i].record_arr[j]
                    pre=int_to_bin(int(xc.t_id))
                    pre=pre[-gd:]
                    if pre==prefix:
                        return int(xc.t_amount)

    def update_link(self,prefix,new_bkt_link):
        for x in self.directories_arr:
            if x.prefix==prefix:
                x.bucket_link=new_bkt_link
                return 1
        
    def split_directory(self):
        #print("O22O") 
        depth=self.global_depth
        count=self.count
        #print("SSSDDDD",count," ",depth)
        self.global_depth=depth+1
        ls=[]
        if count==0:
            
            pref='0'
            pref2='1'
            link=0
            entry1=Directory_Entry(pref)
            entry1.bucket_link=link
            entry2=Directory_Entry(pref2)
            entry2.bucket_link=link
            
            self.add_entry(entry1)
            self.add_entry(entry2)
            
        else:
            mnm=0
            
            for i in range(0,count):
                if i<1024:
                    ls.append(self.directories_arr[i])
                    mnm=mnm+1
            if self.overflow is True:
                    #print(depth," ",i-1024)
                cn1=Sec_memory.bucket_directory_count
                for i in range(0,cn1):
                    cnt2=Sec_memory.bucket_directory_arr[i].count
                    for j in range(0,cnt2):
                        xc=Sec_memory.bucket_directory_arr[i].record_arr[j]
                        pre=int_to_bin(int(xc.t_id))
                        pre=pre[-depth:]
                        link=int(xc.t_amount)
                        aaa=Directory_Entry(pre)
                        aaa.bucket_link=link
                        ls.append(aaa)
                        mnm=mnm+1
                    Sec_memory.bucket_directory_arr[i].count=0
                Sec_memory.bucket_directory_count=0
                
            self.directories_arr.clear()
            self.count=0
            for i in range(0,mnm):
                pref='0'+ls[i].prefix
                pref2='1'+ls[i].prefix
                link=ls[i].bucket_link
                entry1=Directory_Entry(pref)
                entry1.bucket_link=link
                entry2=Directory_Entry(pref2)
                entry2.bucket_link=link
                self.add_entry(entry1)
                self.add_entry(entry2)






def int_to_bin(num):
    x='{:032b}'.format(num)
    return x


def bin_to_int(num): 
    return int(num,2) 



#Updates the bucket_links in directory entries whose corresponding buckets have been splitted
def update_dir_after_bucketsplit(prefix_of_bucket,bkt_link):
    #print("prefix_update",prefix_of_bucket)
    if directory.overflow==False:
        for x in directory.directories_arr:
            if x.prefix==prefix_of_bucket:
                x.bucket_link=bkt_link
                #print("fdone")
                return 1
    else:        
        count=Sec_memory.bucket_directory_count 
        count_dir=directory.count
        for x in directory.directories_arr:
            if x.prefix==prefix_of_bucket:
                x.bucket_link=bkt_link
                #print("fdone")
                return 1
        for i in range(0,count):
            cn=Sec_memory.bucket_directory_arr[i].count
            for j in range(0,cn):
                if Sec_memory.bucket_directory_arr[i].record_arr[j].t_id==prefix_of_bucket:
                    Sec_memory.bucket_directory_arr[i].record_arr[j].t_amount=bkt_link
                    return 1
        




# function  to split buckets, first it copies the records from the bucket then empties the bucket and create other bucket and then fill the records again in two buckets
def split_bucket(bkt_link,record,prefix):
    
    local_depth=Sec_memory.bucket_arr[bkt_link].local_depth
    
    
    Sec_memory.bucket_arr[bkt_link].local_depth=local_depth+1
    
    local_depth=Sec_memory.bucket_arr[bkt_link].local_depth
    bin_value=int_to_bin(record.t_id)
    
    prefix_of_bucket=bin_value[-local_depth:]
    
    
    global_depth=directory.global_depth
    
    cnt=Sec_memory.bucket_arr[bkt_link].count
    
    #print("RRR",global_depth,local_depth,prefix_of_bucket)
    buffer=[]
    #copying data from bucket to buffer
    
    for i in range(0,cnt):

        buffer.append(Sec_memory.bucket_arr[bkt_link].record_arr[i])
    #print("QQQ",buffer)
    #emptying the target bucket before splitting it
    for i in range(0,cnt):
        Sec_memory.bucket_arr[bkt_link].record_arr[i]=None
        Sec_memory.bucket_arr[bkt_link].count=0
    
    buckets_count=Sec_memory.buckets_count
    Sec_memory.bucket_arr[buckets_count].local_depth=Sec_memory.bucket_arr[bkt_link].local_depth
    Sec_memory.buckets_count=Sec_memory.buckets_count+1
    update_dir_after_bucketsplit(prefix_of_bucket,bkt_link)
    update_dir_after_bucketsplit(prefix_of_bucket,buckets_count)
    #print("KKKKK")
    for x in buffer:
        #print("JJ",x.t_id)
        insert_record(x)
    
    return 1


######################## INSERT RECORD FUNCTION ######################################################

def insert_record(record):
    num=directory.global_depth
    bin_value=int_to_bin(record.t_id)
    prefix=bin_value[-num:]
    #print("Prefix ",prefix," tid ",record.t_id)
    #print("FF",record.t_id," global_depth ",num)


    #Go into this if incase directory have entries
    if directory.global_depth>0:
        #print("YY")
        #retrieve the bucket link or address using prefix value
        bkt_link=directory.find_dir_entry(prefix)   #Target bucket
        #print(prefix,"PPP",bkt_link)
        #print(directory.directories_arr[0].prefix)
        #if the bucket has space for adding more, just add record and increase record counter of bucket
        if bkt_link==None:
            return 1
        if Sec_memory.bucket_arr[bkt_link].count<Sec_memory.bucket_arr[bkt_link].capacity:            
            #p#rint("GG")
            count=Sec_memory.bucket_arr[bkt_link].count
            Sec_memory.bucket_arr[bkt_link].record_arr[Sec_memory.bucket_arr[bkt_link].count]=record                                    
            Sec_memory.bucket_arr[bkt_link].count=Sec_memory.bucket_arr[bkt_link].count+1
            return 1
        #if the bucket directed from directory is already full
        else:
            
            #if the bucket does not have an overflowing bucket
            if Sec_memory.bucket_arr[bkt_link].overflow_bucket==None:
                #print("UU",Sec_memory.bucket_arr[bkt_link].local_depth," ",directory.global_depth)
                #if local_depth is same as global_depth then directory needs to be split once
                if directory.global_depth==Sec_memory.bucket_arr[bkt_link].local_depth:
                    directory.split_directory()#//////
                    num=directory.global_depth
                    #print("global depth- ",num)
                    bin_value=int_to_bin(record.t_id)
                    prefix=bin_value[-num:]
                    split_bucket(bkt_link,record,prefix)
                    #print(prefix," ",record.t_id)
                    bkt_link=directory.find_dir_entry(prefix)
                    if bkt_link==None:
                        return 1
                    #print("%%%%",Sec_memory.bucket_arr[bkt_link].record_arr[0].t_id," ",Sec_memory.bucket_arr[bkt_link].record_arr[1].t_id," ",Sec_memory.bucket_arr[bkt_link].record_arr[2].t_id)
                    #if after directory expansion the bucket being addressed asper directory is having space for new record
                    if Sec_memory.bucket_arr[bkt_link].count<Sec_memory.bucket_arr[bkt_link].capacity:
                        #print("IIO")
                        count=Sec_memory.bucket_arr[bkt_link].count
                        Sec_memory.bucket_arr[bkt_link].record_arr[Sec_memory.bucket_arr[bkt_link].count]=record                        
                        Sec_memory.bucket_arr[bkt_link].count=Sec_memory.bucket_arr[bkt_link].count+1
                        return 1
                    #if even after directory expansion bucket is full
                    else:
                        #an overflow bucket is added
                        #print("OOI")
                        Sec_memory.overflow_bkt(record,prefix,bkt_link)
                        return 1
                #bucket split possible as global_depth is more than local_depth
                elif directory.global_depth>Sec_memory.bucket_arr[bkt_link].local_depth:
                    #print("SS")
                    split_bucket(bkt_link,record,prefix)
                    insert_record(record)
                    return 1
            else:
                done=True
                while done:
                    bkt_link=Sec_memory.bucket_arr[bkt_link].overflow_bucket
                    if Sec_memory.bucket_arr[bkt_link].count<Sec_memory.bucket_arr[bkt_link].capacity:
                        count=Sec_memory.bucket_arr[bkt_link].count
                        Sec_memory.bucket_arr[bkt_link].record_arr[Sec_memory.bucket_arr[bkt_link].count]=record                        
                        Sec_memory.bucket_arr[bkt_link].count=Sec_memory.bucket_arr[bkt_link].count+1
                        done=False
                        return 1
                    elif Sec_memory.bucket_arr[bkt_link].count==Sec_memory.bucket_arr[bkt_link].capacity and Sec_memory.bucket_arr[bkt_link].overflow_bucket is None:
                        ind=Sec_memory.buckets_count                     
                        Sec_memory.bucket_arr[ind].record_arr[0]=record
                        Sec_memory.bucket_arr[ind].count=1+Sec_memory.bucket_arr[ind].count
                        Sec_memory.bucket_arr[bkt_link].overflow_bucket=ind
                        Sec_memory.buckets_count=Sec_memory.buckets_count+1
                        done=False
                        return 1

#################################### if Global depth is 0    ##########################################################3
    else:
        if Sec_memory.bucket_arr[0].count<Sec_memory.bucket_arr[0].capacity:            
            cn=Sec_memory.bucket_arr[0].count
            Sec_memory.bucket_arr[0].record_arr[cn]=record            
            Sec_memory.bucket_arr[0].count=Sec_memory.bucket_arr[0].count+1      
            
        else:
            directory.split_directory()#//////
            num=directory.global_depth            
            
            #print("Coming",num)
            bin_value=int_to_bin(record.t_id)
            prefix=bin_value[-num:]
            split_bucket(0,record,prefix)
            bkt_link=directory.find_dir_entry(prefix)
            #print(prefix)
            #print(directory.directories_arr[bkt_link].prefix)
            #if after directory expansion the bucket being addressed asper directory is having space for new record
            if Sec_memory.bucket_arr[bkt_link].count<Sec_memory.bucket_arr[bkt_link].capacity:
                #print("$$$RR")
                count=Sec_memory.bucket_arr[bkt_link].count
                Sec_memory.bucket_arr[bkt_link].record_arr[Sec_memory.bucket_arr[bkt_link].count]=record
                Sec_memory.bucket_arr[bkt_link].count=Sec_memory.bucket_arr[bkt_link].count+1
                return 1
            
            #if even after directory expansion bucket is full
            else:
                #print("JJJJWWW")
                #an overflow bucket is added
                Sec_memory.bucket_arr[2].record_arr[0]=record
                Sec_memory.bucket_arr[2].count=1+Sec_memory.bucket_arr[2].count
                Sec_memory.buckets_count=3
                Sec_memory.bucket_arr[bkt_link].overflow_bucket=2
                
                return 1


def Print_func():
    count=directory.count
    print('\n')
    print("PRINTING ALL BUCKETS CORRESPONDING TO DIRECTORY TABLE")
    print('\n')
    print("W",count,"     Global_Depth = ",directory.global_depth)

    for i in range(0,count):
        print("$")
        if i <1024:
            print("-----------------------------------------------------------------------------")
            print("Directory-entry-prefix ",directory.directories_arr[i].prefix,"=>")
            print("Bucket-index= ",directory.directories_arr[i].bucket_link," Bucket-local_depth= ",Sec_memory.bucket_arr[directory.directories_arr[i].bucket_link].local_depth)
            cnt=Sec_memory.bucket_arr[directory.directories_arr[i].bucket_link].count
            overflow=Sec_memory.bucket_arr[directory.directories_arr[i].bucket_link].overflow_bucket

            #print(cnt,"cnt")
            #print("cap",Sec_memory.bucket_arr[directory.directories_arr[i].bucket_link].capacity)
            for j in range(0,cnt):
                xc=Sec_memory.bucket_arr[directory.directories_arr[i].bucket_link].record_arr[j]                
                print("Record=   ",int_to_bin(int(xc.t_id)),"  T_id = ",xc.t_id," T_amout = ",xc.t_amount," T_name = ",xc.cust_name)
            if overflow is not None:
                print("Bucket-index= ",overflow," Bucket-local_depth ",Sec_memory.bucket_arr[overflow].local_depth)
                while overflow is not None:
                    cnt=Sec_memory.bucket_arr[overflow].count
                    for j in range(0,cnt):
                        xc=Sec_memory.bucket_arr[overflow].record_arr[j]                
                        print("Record=   ",int_to_bin(xc.t_id),"  T_id = ",xc.t_id," T_amout = ",xc.t_amount," T_name = ",xc.cust_name)
                    overflow=Sec_memory.bucket_arr[overflow].overflow_bucket
        
        else:
            index=i-1024
            count=Sec_memory.bucket_directory_count

            cn=Sec_memory.bucket_directory_arr[index].count
            for j in range(0,cn):

                xc=Sec_memory.bucket_directory_arr[index].record_arr[j]                
                bkt_link1=xc.t_amount
                pref=xc.t_id
                print("-----------------------------------------------------------------------------")
                print("Directory-entry-prefix ",pref,"=>")
                print("Bucket-index= ",bkt_link1," Bucket-local_depth= ",Sec_memory.bucket_arr[bkt_link1].local_depth)
                cnt1=Sec_memory.bucket_arr[bkt_link1].count
                for k in range(0,cnt1):
                    xa=Sec_memory.bucket_arr[bkt_link1].record_arr[k]                
                    print("Record=   ",int_to_bin(int(xa.t_id)),"  T_id = ",xa.t_id," T_amout = ",xa.t_amount," T_name = ",xa.cust_name)
                


    if count==0:
        print("No entry in Directory table !!!!!!!!!!!!!!!!!")
        print("Bucket-index = 0  local-depth of bucket= ",Sec_memory.bucket_arr[0].local_depth)
        cnt=Sec_memory.bucket_arr[0].count
        for j in range(0,cnt):
            xc=Sec_memory.bucket_arr[0].record_arr[j]                
            print("Record=   ",int_to_bin(int(xc.t_id)),"  T_id = ",xc.t_id," T_amout = ",xc.t_amount," T_name = ",xc.cust_name)
        

            print("-----------------------------------------------------------------------------")


def print_buckets():
    count=Sec_memory.buckets_count
    print('\n')
    print("PRINTING ALL Buckets")
    print('\n')
    for i in range(0,count):
        print("####################################################################################")
        print("Bucket-index= ",i,"   Bucket-local_depth= ",Sec_memory.bucket_arr[i].local_depth)
        cnt=Sec_memory.bucket_arr[i].count
        for j in range(0,cnt):
            xc=Sec_memory.bucket_arr[i].record_arr[j]                
            print("Record=   ",int_to_bin(int(xc.t_id)),"  T_id = ",xc.t_id," T_amout = ",xc.t_amount," T_name = ",xc.cust_name)
    

def add_record():
    print("Enter transaction ID ")
    t_id=int(input())
    print("Enter transaction sale amount ")
    t_amount=int(input())
    print("Enter Customer Name ")
    cust_name=input()
    print("Enter Category ")
    category=int(input())
    insert_record(Record(t_id,t_amount,cust_name,category))
    print("Record added !!")

def search_record():
    print("Enter transaction ID to search record: ")
    t_id=int(input())
    gd=directory.global_depth
    pref=int_to_bin(t_id)
    pref=pref[-gd:]
    bkt_link=directory.find_dir_entry(pref)
    if bkt_link==None:
        
        a1=Sec_memory.bucket_arr[0].count
        for h in range(0,a1):
            if Sec_memory.bucket_arr[0].record_arr[h].t_id==t_id:
                xc=Sec_memory.bucket_arr[0].record_arr[h]
                print("Found    Bucket-index= 0"," Transaction ID= ",xc.t_id," Transaction sale amount= ",xc.t_amount,"Customer Name= ",xc.cust_name," Category= ",xc.category)    
                return 1
        print("Not found !!")
        return 1
    count=Sec_memory.bucket_arr[bkt_link].count
    for i in range(0,count):
        if Sec_memory.bucket_arr[bkt_link].record_arr[i].t_id==t_id:
            xc=Sec_memory.bucket_arr[bkt_link].record_arr[i]
            print("Found    Bucket-index= ",bkt_link," Transaction ID= ",xc.t_id," Transaction sale amount= ",xc.t_amount,"Customer Name= ",xc.cust_name," Category= ",xc.category)
            return 1
    overflow=Sec_memory.bucket_arr[bkt_link].overflow_bucket
    while overflow is not None:
        if Sec_memory.bucket_arr[overflow].record_arr[i].t_id==t_id:
            xc=Sec_memory.bucket_arr[overflow].record_arr[i]
            print("Found    Bucket-index= ",bkt_link," Transaction ID= ",xc.t_id," Transaction sale amount= ",xc.t_amount,"Customer Name= ",xc.cust_name," Category= ",xc.category)
            return 1
        overflow=Sec_memory.bucket_arr[overflow].overflow_bucket
    print("NOT FOUND")
    return 1

def createRandomSortedList(num, start = 1, end = 100): 
    arr = [] 
    tmp = random.randint(start, end) 
    for x in range(num): 
        while tmp in arr: 
            tmp = random.randint(start, end) 
        arr.append(tmp) 
    arr.sort() 
    return arr 


# printing lowercase
def generate_data():
    print("Enter number of records you want to generate ")
    n=int(input())
    print("Enter name for output file (without extension)")
    name=input()
    writer = csv.writer(open(name+'.csv', 'w'))
    x=["transaction_id","transaction_amount","customer_name","category"]
    writer.writerow(x)
    lsa=createRandomSortedList(n,1,50000)
    for a in lsa:
        b=random.randint(1,500000)
        letters = string.ascii_lowercase
        c= ''.join(random.choice(letters) for i in range(3))
        d=random.randint(1,1500)
        sd=[a,b,c,d]
        writer.writerow(sd)
    print("File "+name+".csv created successfully !!")




def add_records_csv():
    print("Enter name of csv file with extension:")
    name=input()
    try:
        reader = csv.reader(open(name, 'r'))
    except:
        print("Ooops No such file Exist !!!")
        print('\n')
        add_records_csv()
    i=0
    for row in reader:
        if i>0:
            xc=Record(int(row[0]),int(row[1]),row[2],int(row[3]))
            insert_record(xc)
        else:
            i=i+1
    print("Successfully all records are added !!!")
    
def print_overflown_directories():
    gd=directory.global_depth
    sfg=0
    if directory.overflow==False:
        print("No directory entry overflow")
    else:
        count=Sec_memory.bucket_directory_count
        for i in range(0,count):
            cnt=Sec_memory.bucket_directory_arr[i].count
            for j in range(0,cnt):
                xc=Sec_memory.bucket_directory_arr[i].record_arr[j]
                pref=int_to_bin(int(xc.t_id))
                pref=pref[-gd:]
                print("Directory entry prefix= ",pref," ")
                sfg=sfg+1
    print("Global_Depth Of Directory is ",gd)
    x=math.pow(2,gd)
    x=x-1024
    print("Number of directory enteries overflow is ", x)

def Menu():
    print("****************************WELCOME TO MENU ***************")
    print("ENTER 1 TO SEARCH A RECORD: ")
    print("ENTER 2 TO ADD A RECORD: ")
    print("ENTER 3 TO ADD RECORDS FROM A CSV FILE: ")
    print("ENTER 4 TO PRINT ALL BUCKETS IN SECONDARY MEMORY: ")
    print("ENTER 5 TO PRINT BUCKETS CORRESPONDING TO EACH DIRECTORY TABLE ENTRY: ")
    print("ENTER 6 TO GENERATE SYNTHETIC RECORDS CSV FILE ")
    print("ENTER 7 TO PRINT All THE DIRECTORY ENTERIES OVERFLOWN TO SECONDARY MEMORY ")
    print("ENTER 8 TO EXIT ")
    a=int(input())
    if a==1:
        search_record()
        Menu()
    if a==2:
        add_record()
        Menu()
    if a==3:
        add_records_csv()
        Menu()
    if a==4:
        print_buckets()
        Menu()
    if a==5:
        Print_func()
        Menu()
    if a==6:
        generate_data()
        Menu()
    if a==7:
        print_overflown_directories()
        Menu()
    if a==8:
        exit
    else:
        print("Enter correct choice X!!!X ")
        Menu()

print("*********** WELCOME TO JAGDEEP`s DATA MANAGER ********************")
print("Enter capacity of buckets containing records: ")
c11=int(input())
print("Enter capacity of buckets used for overflowing directory enteries: ")
c22=int(input())





Bucket1=Bucket(c11)
Bucket2=Bucket(c22)
Bucket2.is_directory=True
# B1_arr=[Bucket1]*999999
# B2_arr=[Bucket2]*999999
B1_arr = [Bucket(3) for _ in range(999999)]
B2_arr = [Bucket(3) for _ in range(999999)]
Sec_memory=Secondary_Memory(B1_arr,B2_arr)
directory=Directory()
Menu()
