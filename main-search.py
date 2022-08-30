from asyncio import events
from cgitb import text
import email
from tkinter import *
import tkinter
import glob
import re
import string
import threading
import pickle
import os
import string
from ctypes import windll
import time
import webbrowser
import firebase
from firebase_admin import db, storage, auth



def current_milli_time():
    return round(time.time() * 1000)

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


win = tkinter.Tk()
# Set the geometry of the window
win.geometry("1000x500")
win.resizable(0, 0)
win.title("Local Search Engine")
win.eval('tk::PlaceWindow . center')
# Create a frame widget
# frame=Frame(win, width=700, height=500)
# frame.grid(row=0, column=0, sticky="NW")

tokens_dict_main = {}
all_files_main = {}
lnth_token = 0
name_address = []



def openNewAuthWindow():
     
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(win)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Sign up")
 
    # sets the geometry of toplevel
    newWindow.geometry("500x400")
    
    Label(newWindow, text="Email: ", font='Arial 10').place(x = 18, y = 65)

    email = Entry(newWindow, width=40)
    email.place(x=135, y=65)

    password = Entry(newWindow, width=40)
    password.place(x=135, y=105)
    Label(newWindow, text="Password: ", font='Arial 10').place(x = 18, y = 105)

    device_name = Entry(newWindow, width=40)
    device_name.place(x=135, y=145)
    Label(newWindow, text="Device Name: ", font='Arial 10').place(x = 18, y = 145)

    device_pass = Entry(newWindow, width=40)
    device_pass.place(x=135, y=185)
    Label(newWindow, text="Device Password: ", font='Arial 10').place(x = 18, y = 185)

    def do_auth():
        pass

    Button(newWindow, text ="Hello", command = do_auth, width=30).place(x = 18, y = 300)

openNewAuthWindow()


listbox = Listbox(win, width=35, height=20)  
listbox.place(x=770, y=100)


# Create a label widget
label=Label(win, text="Local Search Engine by Rahul Kantwa", font='Arial 17 bold')
label.place(relx=0.5, rely=0.05, anchor=CENTER)

stage = Entry(win, width=8)
stage.place(x=800, y=65)
stage.insert(0, "Stage")

stage = Entry(win, width=8)
stage.place(x=800, y=65)

query = Entry(win, width=80)
query.place(x=20, y=65)

cnt_result = Entry(win, width=5)
cnt_result.place(x=530, y=65)

def OpenFile(event):
    try:
        cs = int(listboxsearch.curselection()[0])
        if cs%2 == 0:
            webbrowser.open_new_tab(name_address[cs//2][1])
    except:
        pass

listboxsearch = Listbox(win, width=104, height=20)  
listboxsearch.place(x=20, y=100)
listboxsearch.bind('<Double-1>', OpenFile)

label_results = Label(win, text="", font='Arial 10')
label_results.place(x = 18, y = 430)

total_results = Label(win, text="Loading...", font='Arial 10')
total_results.place(x = 768, y = 430)


def getTokens():
    global lnth_token
    global tokens_dict_main

    if len(tokens_dict_main.keys()) == 0:
        try:
            with open(r'C:/Local Search/token_dictionary.pkl', 'rb') as f:
                tokens_dict_main = pickle.load(f)
                lnth_token += len(tokens_dict_main.keys())
        except:
            pass

threading.Thread(target = getTokens).start()

def getFiles():
    global all_files_main
    if len(all_files_main.keys()) == 0:
        try:
            with open(r'C:/Local Search/files_dictionary.pkl', 'rb') as f:
                all_files_main = pickle.load(f)
                total_results.config(text="Total files: "+str(round(len(all_files_main.keys())/10**3))+"K")
        except:
            total_results.config(text="")
            pass

threading.Thread(target = getFiles).start()

def main_search_logic(Name):
    last_dict = {}
    cnt_dict = {}
    Name = list(set(getGoodData([Name])[0].split(" ")))
                
    for i in Name:
        lst = tokens_dict_main.get(i)
        if lst != None:
            for j in lst:
                if j[0] in last_dict:
                    last_dict[j[0]] += j[1]
                    cnt_dict[j[0]] += 1
                else:
                    last_dict[j[0]] = j[1]
                    cnt_dict[j[0]] = 1
    last_lst = []
    for i in last_dict:
        last_lst.append([i, cnt_dict[i], last_dict[i]])
        
    last_lst.sort(key=lambda x : (x[1], x[2]), reverse = True)

    return last_lst

def Search(event):
    global name_address
    name_address.clear()
    starttime=current_milli_time()
    results = [0]

    def getFiles(Name, Count):

        listboxsearch.delete(0, END)
        listboxsearch.insert(0, "Searching...")
        
        last_lst = main_search_logic(Name)

        results[0] += len(last_lst)

        
        cnt = 0
        for i in last_lst[0:Count]:
            s = all_files_main.get(i[0])
            if s != None:
                if cnt == 0:
                    listboxsearch.delete(END)

                print(s)
                name = s.split("\\")[-1]
                name_address.append([name, s])
                listboxsearch.insert(cnt, " "+str(cnt//2 + 1) +".  "+name)
                listboxsearch.insert(cnt+1, "")
                cnt += 2

        if cnt == 0:
            listboxsearch.delete(END)

        if cnt == 0 and lnth_token == 0:
            listboxsearch.insert(0, "Please Fetch Files or Try Again After Some Time.")
        elif cnt == 0 and lnth_token != 0:
            listboxsearch.insert(0, "No result found.")

    Count = 20
    try:
        Count = int(cnt_result.get())
    except:
        pass

    getFiles(str(query.get()), Count)

    label_results.config(text= str(results[0]) + " results " + str((current_milli_time() - starttime))+ " ms")
    listboxsearch.see(0)


win.bind('<Return>', Search)



def getGoodData(Files):
    pun = string.punctuation

    documents_clean = []
    for d in Files:
        # Lowercase the document
        document_test = d.lower()
        # Remove punctuations
        document_test = re.sub(r'[%s]' % re.escape(pun), ' ', document_test)

        r_d = ""
        for i in document_test.split():
            s = i.strip()
            if len(s) != 0:
                r_d += s+" "
        document_test = r_d.strip()

        words_new = document_test.split()
        
        if len(words_new) == 0:
            words_new  = ["#"]

        documents_clean.append(" ".join(list(set(words_new))))

    return documents_clean

def proces():

    global tokens_dict_main
    global all_files_main

    Stage = 8
    try:
        Stage = int(stage.get())
    except:
        pass

    
    listbox.delete(0,END)
    listbox.insert(0,"Fetching...")
    listbox.see(tkinter.END)

    files = []
    cnt = [1]
    file_cnt = [0]
    def getFiles(Name):
        
        address = Name
        round_cnt = 1
        r_f_lnth = -1
        while r_f_lnth != 0 and round_cnt <= Stage:
            r_files = glob.glob(address)
            r_f_lnth = len(r_files)

            files.extend(r_files)
            address += "/*"

            
            listbox.delete(END)
            listbox.insert(cnt[0], "File: "+ address.split("/")[0]+"/ Stage: " + str(round_cnt) + " Total Files: "+ str(r_f_lnth)) 
            listbox.insert(cnt[0]+1,"Fetching...")
            listbox.see(tkinter.END)

            round_cnt += 1 
            cnt[0] += 2
            file_cnt[0] += r_f_lnth

            total_results.config(text="Total files: "+str(round(file_cnt[0]/10**3))+"K")

    

    for i in get_drives():
        getFiles(i+":")

    
    listbox.delete(END)
    listbox.insert(cnt[0]+1,"Indexing...")
    listbox.see(tkinter.END)

    main_file_names = []
    for i in files:
        main_file_names.append(i.split("\\")[-1])

    documents_clean = getGoodData(main_file_names)

    tokens_dict = {}
    for i in range(len(documents_clean)):
        split_lst = documents_clean[i].strip().split(" ")
        lnth = len(split_lst)

        for j in split_lst:
            if j in tokens_dict:
                tokens_dict[j].append([i, round(split_lst.count(j)/lnth, 4)])
            else:
                tokens_dict[j] = [[i, round(split_lst.count(j)/lnth, 4)]]

    tokens_dict_main = tokens_dict

    
    listbox.delete(END)
    listbox.insert(cnt[0]+2,"Storing...")
    listbox.see(tkinter.END)

    try:
        path = os.path.join("c:/", "Local Search")
        if not os.path.isfile(path):
            os.mkdir(path)
    except:
        pass

    try:
        with open(r'C:/Local Search/token_dictionary.pkl', 'wb') as f:
            pickle.dump(tokens_dict, f)
    except:
        pass

    files_dict = {}
    file_cnt = 0
    for i in files:
        files_dict[file_cnt] = i
        file_cnt += 1

    all_files_main = files_dict
    

    try:
        with open(r'C:/Local Search/files_dictionary.pkl', 'wb') as f:
            pickle.dump(files_dict, f)
    except:
        pass

    
    listbox.delete(END)
    listbox.insert(cnt[0]+3,"Done")
    listbox.see(tkinter.END)

def getData():
    threading.Thread(target = proces).start()

def getSearch():
    threading.Thread(target = Search(events)).start()

B=Button(win, text ="Fetch Files",command = getData).place(x=880, y=60)
SearchBtn=Button(win, text ="Search",command = getSearch).place(x=600, y=60)


def get_Firebase():
    #Firbase Data
    def listener(event):
        last_lst = main_search_logic(event.data['data'])
        Count = event.data['cnt']

        ref = db.reference("/results")

        ref.delete()

        cnt = 0
        for i in last_lst[0:Count]:
            s = all_files_main.get(i[0])
            if s != None:
                data = {
                        'name':s.split("\\")[-1],
                        'address': i[0],
                        'cnt': cnt
                        }

                cnt += 1

                ref.push().set(data)
        
    db.reference("/query/1").listen(listener)

    def listener2(event):
        if event.data != None :
            s = all_files_main.get(event.data['address'])
            fileName = event.data['name']
            print(fileName, s)

            if s != None:
                bucket = storage.bucket()
                blob = bucket.blob(fileName)
                
                ref = db.reference("/update/1")
                ref.set({
                    'data': 'uploading'
                })

                blob.upload_from_filename(s)
                # Opt : if you want to make public access from the URL
                blob.make_public()

                ref.set({
                    'data': 'uploaded'
                })
                
            
    
    db.reference("/upload_file/1").listen(listener2)

threading.Thread(target = get_Firebase).start()


win.mainloop()