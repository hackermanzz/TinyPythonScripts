import wikipedia
from tkinter import *
from tkinter.messagebox import showinfo
search = input(' What are you searching for? \n>>')
reply = lambda search : wikipedia.summary(search)
print('This was what we found ' ,str(reply))