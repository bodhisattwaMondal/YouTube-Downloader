from pytube import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from threading import *

fileSize = 0


def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if urlENtry.get() == 'URL Here...':
       urlENtry.delete(0, "end") # delete all the text in the entry
       urlENtry.insert(0, '') # Insert blank for user input


def progress(stream = None, chunk = None, file_handle = None, bytes_remaining = None ):
    """
    This function gets called every sec to check the percentage progress of the download
    """
   # file_downloaded = (fileSize - bytes_remaining)                # I'm getting an error here 
   # per = (file_downloaded/fileSize)*100
   # dwnldBtn.config(text = "{:00.0f} % Downloaded".format(per))
    dwnldBtn.config(text = "Downloading..!!")


def startDwnld():
    """
    This function will download the YouTube video of the desired URL.
    """
    global fileSize
    try:
        url = urlENtry.get()
        dwnldBtn.config(text = 'Please Wait...')
        dwnldBtn.config(state = DISABLED)
        dwnldPath = askdirectory()
        if dwnldPath is None:
            return
        yt = YouTube(url, on_progress_callback=progress)  # This one 
        strm = yt.streams.filter(only_audio=True).first()
        fileSize = strm.filesize
        vTitle.config(text = f"[{fileSize/1024000:00.0f} MB] TITLE: {strm.title}")
        vTitle.pack(side = TOP, pady = 6, padx = 8, fill = X)
        strm.download(dwnldPath)
        urlENtry.delete(0, END)
        dwnldBtn.config(text = 'DOWNLOAD')
        dwnldBtn.config(state = NORMAL)
        showinfo("Download Finished", "Succesfully Downloaded !!")
        vTitle.pack_forget()
            
    except Exception as e :
        showerror("ERROR",e)
        urlENtry.delete(0, END)
        dwnldBtn.config(text = 'DOWNLOAD')
        dwnldBtn.config(state = NORMAL)
        vTitle.pack_forget()


def startDwnldThread():
    """
    This function will start the dwonload in a separate thread.
    """
    thread = Thread(target = startDwnld)
    thread.start()

# Driver Code

if __name__ == "__main__":

    # GUI Creation

    root = Tk()
    root.geometry("480x750")
    root.minsize(480,750)
    root.title("YouTube Audio Downloader")
    root.iconbitmap('icon.ico')
    root.config(bg = 'snow')

    # Creating the photo label
    img = PhotoImage(file = 'pic2.png')
    picLabel = Label(root, image = img,bg = "snow")
    picLabel.pack(side = TOP, pady = 15)

    # Creating the URL Entry widget
    urlENtry = Entry(root,font = "comicsansms 20", justify = CENTER, relief = RIDGE, borderwidth = 5, bg = 'LightCyan2')
    urlENtry.insert(0, "URL Here...")
    urlENtry.bind('<FocusIn>', on_entry_click)
    urlENtry.pack(pady = 8, padx = 15, ipady = 10, fill = X)


    # Creating the video title Label
    vTitle = Label(root, font = "comicsansms 10 bold ", bg = 'snow', fg = 'green yellow')

     
    # Creating watermark label
    watermarkLabel = Label(root, text = "by Bodhi", font = "comicsansms 12", fg = 'brown4', bg = 'snow' )
    watermarkLabel.pack(side = BOTTOM, anchor = SE, padx = 8, pady = 5)
    

    # Creating the download button
    dwnldBtn = Button(root, text = "DOWNLOAD", font = "cooper 22", fg = 'orangered', bg = 'snow', relief = RIDGE, command = startDwnldThread)
    dwnldBtn.pack(pady = 10, ipady = 10, ipadx = 8)
    root.mainloop()

   