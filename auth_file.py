from asyncio import events
from cgitb import text
from distutils.command.config import config
import email
from msilib.schema import Error
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
from tkinter import messagebox  
from firebase_admin import db, storage, auth


win = tkinter.Tk()
# Set the geometry of the window
win.geometry("1000x500")
win.resizable(0, 0)
win.title("Local Search Engine")
win.eval('tk::PlaceWindow . center')
# Create a frame widget
# frame=Frame(win, width=700, height=500)
# frame.grid(row=0, column=0, sticky="NW")

Auth_Id = "1"

def openNewAuthWindow():
     
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(win)
    newWindow.resizable(0, 0)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Sign in")
 
    # sets the geometry of toplevel
    newWindow.geometry("405x370")
    
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
        global Auth_Id
        Email = str(email.get())
        Pass = str(password.get())
        Device_Name = str(device_name.get())
        Device_Pass = str(device_pass.get())

        if len(Email) != 0 and len(Pass) != 0 and len(Device_Name) != 0 and len(Device_Pass):
            try:
                auth.create_user(email = Email, password = Pass)
                Auth_Id = auth.get_user_by_email(email=Email).uid
                ref = db.reference("/users/" + Auth_Id)
                ref.set({
                    'email': Email,
                    'pass': Pass,
                    'device_name': Device_Name,
                    'device_pass': Device_Pass
                })

                email.config(text="")
                password.config(text="")
                device_name.config(text="")
                device_pass.config(text="")

                messagebox.showinfo("Done","Successfully signed in.")  

            except Exception as e:
                messagebox.showinfo("Error",e)          


    def open_login():
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(win)
        newWindow.resizable(0, 0)
    
        # sets the title of the
        # Toplevel widget
        newWindow.title("Login")
    
        # sets the geometry of toplevel
        newWindow.geometry("405x370")
        
        Label(newWindow, text="Email: ", font='Arial 10').place(x = 18, y = 65)

        email = Entry(newWindow, width=40)
        email.place(x=135, y=65)

        password = Entry(newWindow, width=40)
        password.place(x=135, y=105)
        Label(newWindow, text="Password: ", font='Arial 10').place(x = 18, y = 105)

        def do_login():
            global Auth_Id
            Email = str(email.get())
            Pass = str(password.get())
        
            if len(Email) != 0 and len(Pass) != 0 :
                try:
                
                    Auth_Id = auth.get_user_by_email(email=Email).uid
                  
                    email.config(text="")
                    password.config(text="")

                    ref = db.reference("/users/" + Auth_Id)
                    data = ref.get()
                    
                    if data != None:
                        if data.get('email') == Email and data.get('pass') == Pass:
                            messagebox.showinfo("Done","Successfully logged in.")
                        else:
                            Auth_Id = "1"
                            raise Error("Please check your email and password.")
                    else:
                        Auth_Id = "1"
                        raise Error("Account does not exists.")
                        
                except Exception as e:
                    messagebox.showinfo("Error",e)  

        def forgot_pass():
            newWindow = Toplevel(win)
            newWindow.resizable(0, 0)
        
            # sets the title of the
            # Toplevel widget
            newWindow.title("Forgot Password")
        
            # sets the geometry of toplevel
            newWindow.geometry("405x370")
            
            Label(newWindow, text="Email: ", font='Arial 10').place(x = 18, y = 65)

            email = Entry(newWindow, width=40)
            email.place(x=135, y=65)

            password = Entry(newWindow, width=40)
            password.place(x=135, y=105)
            Label(newWindow, text="Password: ", font='Arial 10').place(x = 18, y = 105)

            def change_pass():
                Email = str(email.get())
                Pass = str(password.get())
            
                if len(Email) != 0 and len(Pass) != 0:
                    try:
                        Id = auth.get_user_by_email(email=Email).uid
                        ref = db.reference("/users/" + Id)
                        data = ref.get()
                        if data != None:
                            db.reference("/users/" + Id + "/pass").set(Pass)

                            auth.delete_user(Id)
                            auth.create_user(email = Email, password = Pass)
                            
                            data = db.reference("/users/" + Id ).get()
                            db.reference("/users/" + auth.get_user_by_email(email=Email).uid).set(data)
                            ref.delete()


                            email.config(text = "")
                            password.config(text = "")
                            messagebox.showinfo("Done","Successfully updated password.")  

                        else:
                            raise Error("User does not exists.")

                    except Exception as e:
                        messagebox.showinfo("Error",e)  

            Button(newWindow, text ="Change Password", command = change_pass, width=50).place(x = 23, y = 260)

        Button(newWindow, text ="Login", command = do_login, width=50).place(x = 23, y = 260)

        Button(newWindow, text ="Forgot Password", command = forgot_pass, width=50).place(x = 23, y = 300)


    Button(newWindow, text ="Sign Up", command = do_auth, width=50).place(x = 23, y = 260)

    Button(newWindow, text ="Login", command = open_login, width=50).place(x = 23, y = 300)


openNewAuthWindow()

win.mainloop()