from tkinter import *
from tkinter import ttk,filedialog,messagebox
import os
import cv2
from PIL import Image,ImageTk

class Application:

    def __init__(self):
        self.FileURL = ""
        self.title = "Untitled"
        self.Height = 0
        self.Width = 0
        self.Ratio = 1
        self.Constant_value = 0.2
        self.Custom = False
        self.FullScreen = False
        self.Export_img = None
        pass

    def User_Interface(self,*args):
        self.root=Tk()
        self.root.title(self.title)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.root.state("zoomed")

        # style
        self.STYLE = ttk.Style()
        self.STYLE.theme_use("default")
        self.STYLE.configure("TButton",font=("arial",13,"bold"),background="yellow")

        # side panel
        self.SidePanel = Frame(self.root,borderwidth=0,relief=SOLID,bg="#00004d",padx=4,pady=4)
        
        # Import Image
        ttk.Button(self.SidePanel,cursor="hand2",text="Open",command=self.Import_Image_FUNC).grid(row=0,column=0,padx=2,pady=2,sticky="nswe")
        
        # Define Ratio
        ttk.Button(self.SidePanel,cursor="hand2",text="Custom\nDimensions",command=self.Custom_Window_FUNC).grid(row=1,column=0,padx=2,pady=2,sticky="nswe")

        # Save Image
        ttk.Button(self.SidePanel,cursor="hand2",text="Save",command=self.Export_Image_FUNC).grid(row=2,column=0,padx=2,pady=2,sticky="nswe")

        # Reset
        ttk.Button(self.SidePanel,cursor="hand2",text="Reset",command=self.Reset_FUNC).grid(row=3,column=0,padx=2,pady=2,sticky="nswe")

        # FullScreen
        ttk.Button(self.SidePanel,cursor="hand2",text="Full Screen",command=self.FullScreen_FUNC).grid(row=4,column=0,padx=2,pady=2,sticky="nswe")

        # Exit Button
        ttk.Button(self.SidePanel,cursor="hand2",text="Exit Button",command=self.root.destroy).grid(row=5,column=0,padx=2,pady=2,sticky="nswe")
        
        self.SidePanel.grid(row=0,column=1,padx=0,pady=0,sticky="nswe")

        # Main window
        self.MainWindow = Canvas(self.root,borderwidth=0,bg="#0000b3",highlightthickness=0)
        self.MainWindow.grid(row=0,column=0,padx=0,pady=0,sticky="nswe")

        # Footer Status
        self.StatusBar = Label(self.root,text="Welcome to Image Resizer",borderwidth=1,relief=SOLID,font=("arial",12),bg="#00004d",fg="yellow")
        self.StatusBar.grid(row=1,column=0,columnspan=2,padx=0,pady=0,sticky="nswe")

        self.MainWindow.bind("<ButtonPress-1>",self.Drag_Point)
        self.MainWindow.bind("<B1-Motion>",self.Drag_ToPoint)
        self.MainWindow.bind("<MouseWheel>",self.Change_Size_Scroll_FUNC)
        self.root.mainloop()
        pass

    def Drag_Point(self,e):
        self.MainWindow.scan_mark(e.x,e.y)
        pass

    def Drag_ToPoint(self,e):
        self.MainWindow.scan_dragto(e.x,e.y,gain=1)
        pass

    def Import_Image_FUNC(self,*args):
        fileurl = filedialog.askopenfilename(title="Open Image",filetypes=[("JPG","*.jpg"),("PNG","*.png"),("JPEG","*.jpeg")])
        if fileurl:
            self.FileURL = fileurl
            img = Image.open(self.FileURL)
            self.Export_img = img.copy()
            self.Height,self.Width = img.size

            self.MainWindow.delete(ALL)
            imgtk = ImageTk.PhotoImage(img)
            self.MainWindow.create_image((0,0),image=imgtk,anchor="nw")
            self.MainWindow.image=imgtk
            self.MainWindow.config(scrollregion=self.MainWindow.bbox(ALL))
            self.StatusBar.config(text=f"Height: {self.Height} Pixels\tWidth: {self.Width} Pixels") 
        pass

    def Change_Size_Scroll_FUNC(self,e):
        if self.FileURL:
            data = e.delta
            
            if data==120:
                img = cv2.imread(self.FileURL)
                img = cv2.resize(img,(0,0),fx=(self.Ratio+self.Constant_value),fy=(self.Ratio+self.Constant_value),interpolation=cv2.INTER_LANCZOS4)
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                img = Image.fromarray(img)
                self.Export_img = img.copy()
                self.Height,self.Width = img.size
                self.MainWindow.delete(ALL)
                imgtk = ImageTk.PhotoImage(img)
                self.MainWindow.create_image((0,0),image=imgtk,anchor="nw")
                self.MainWindow.image=imgtk
                self.MainWindow.config(scrollregion=self.MainWindow.bbox(ALL))

                self.Ratio+=self.Constant_value
                self.StatusBar.config(text=f"Height: {self.Height} Pixels\tWidth: {self.Width} Pixels")

            if data==-120:
                img = cv2.imread(self.FileURL)
                checker = self.Ratio-self.Constant_value
                if checker>0.1:
                    img = cv2.resize(img,(0,0),fx=checker,fy=checker,interpolation=cv2.INTER_LANCZOS4)
                    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                    img = Image.fromarray(img)
                    self.Export_img = img.copy()
                    self.Height,self.Width = img.size
                    self.MainWindow.delete(ALL)
                    imgtk = ImageTk.PhotoImage(img)
                    self.MainWindow.create_image((0,0),image=imgtk,anchor="nw")
                    self.MainWindow.image=imgtk
                    self.MainWindow.config(scrollregion=self.MainWindow.bbox(ALL))

                    self.Ratio-=self.Constant_value
                    self.StatusBar.config(text=f"Height: {self.Height} Pixels\tWidth: {self.Width} Pixels")
                else:
                    messagebox.showwarning("Warning","The Image cannot be Srinked more than this")
            
            if self.Custom:
                self.E1_Value.set(self.Height)
                self.E2_Value.set(self.Width)

    def Custom_Window_FUNC(self,*args):
        if self.FileURL:
            self.Custom_Window = Toplevel()
            self.Custom_Window.resizable(0,0)
            self.Custom_Window.wm_protocol("WM_DELETE_WINDOW",self.Close_Custom_FUNC)
            self.Custom = True
            # label frame
            L1 = LabelFrame(self.Custom_Window,text="Custom Dimentions",bg="#00004d",fg="yellow",font=("arial",20,"bold"))

            Label(L1,text="Height:",bg="#00004d",fg="yellow",font=("arial",17)).grid(row=0,column=0,padx=2,pady=2,sticky="nswe")
            Label(L1,text="Width:",bg="#00004d",fg="yellow",font=("arial",17)).grid(row=1,column=0,padx=2,pady=2,sticky="nswe")

            self.E1_Value = IntVar()
            self.E2_Value = IntVar()

            self.E1 = ttk.Entry(L1,font=("arial",17),textvariable=self.E1_Value)
            self.E1.grid(row=0,column=1,padx=2,pady=2,sticky="nswe")

            self.E2 = ttk.Entry(L1,font=("arial",17),textvariable=self.E2_Value)
            self.E2.grid(row=1,column=1,padx=2,pady=2,sticky="nswe")

            self.E1_Value.set(self.Height)
            self.E2_Value.set(self.Width)

            ttk.Button(L1,text="Change Dimensions",cursor="hand2",command=self.Change_Dimension_FUNC).grid(row=2,column=0,columnspan=2,sticky="nswe",padx=2,pady=2)
            L1.pack(fill=BOTH,expand=True)

            self.Custom_Window.grab_set()
            self.Custom_Window.focus()
    
    def Close_Custom_FUNC(self,*args):
        self.Custom = False
        self.Custom_Window.destroy()

    def Change_Dimension_FUNC(self,*args):
        h = self.E1_Value.get()
        w = self.E2_Value.get()
        if h>=100 and w>=100:
            img = cv2.imread(self.FileURL)
            img = cv2.resize(img,(h,w),interpolation=cv2.INTER_LANCZOS4)
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            img = Image.fromarray(img)
            self.Export_img = img.copy()
            self.Height,self.Width = img.size
            self.MainWindow.delete(ALL)
            imgtk = ImageTk.PhotoImage(img)
            self.MainWindow.create_image((0,0),image=imgtk,anchor="nw")
            self.MainWindow.image=imgtk
            self.MainWindow.config(scrollregion=self.MainWindow.bbox(ALL))

            self.Ratio+=self.Constant_value
            self.StatusBar.config(text=f"Height: {self.Height} Pixels\tWidth: {self.Width} Pixels")
        else:
            messagebox.showwarning("Warning","The Image cannot be shrinked more than 100X100")

    def FullScreen_FUNC(self,*args):
        if self.FullScreen==True:
            self.FullScreen=False
            self.root.wm_attributes("-fullscreen",False)
        elif self.FullScreen==False:
            self.FullScreen=True
            self.root.wm_attributes("-fullscreen",True)

    def Reset_FUNC(self,*args):
        if self.FileURL:
            ask = messagebox.askquestion("Reset","Do you really want to Reset")
            if ask=="yes":
                self.FileURL = ""
                self.title = "Untitled"
                self.Height = 0
                self.Width = 0
                self.Ratio = 1
                self.Constant_value = 0.2
                self.Custom = False
                self.FullScreen = False
                self.Export_img = None
                self.MainWindow.delete(ALL)
                self.MainWindow.config(scrollregion=self.MainWindow.bbox(ALL))
                self.StatusBar.config(text="Welcome to Image Resizer")

    def Export_Image_FUNC(self,*args):
        if self.Export_img:
            save_loc = filedialog.asksaveasfilename(title="Save File",defaultextension=".jpg",filetypes=[("JPG","*.jpg"),("PNG","*.png")])
            if save_loc:
                self.FileURL = save_loc
                self.Export_img.save(self.FileURL)
                messagebox.showinfo("Successful",f"{self.FileURL} have been Saved")
        pass
    pass

if __name__ == "__main__":
    App = Application()
    App.User_Interface()