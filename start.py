"""
 This is the god file of aupas. We may need to refactor this at some point.
"""

import csv
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import Style
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
from pandastable import Table
import psycopg2
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure 


"""
	PENDING: Fonts differ depending on OS. Once we see how the native font looks on windows,
	then we'll make a decision. 
	BASE_FONT = ("Ubuntu",12)
"""



""" Database connection details"""
table_name = "card_transactions"
dbname = "cmsreplica"
port = "5432"
user = "tiffymuchaya"
pwd = "tiffymuchaya"
host = "localhost"

""" Varibles for widget colors"""
bg_color__btn = "#212121"
font_color__btn = "#fff"
highlight_bg_color__btn = "#212121"
active_font_color__btn = "#fff"
activebackground_color__btn = "#444"
BG_COLOR = '#999'
mycolor1 = '#FFF'
mycolor2 = '#212121'
mycolor3 = '#333333'
mycolor4 = '#ffffff'


class Aupas(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		icon = tk.PhotoImage("AUPAS",file='chev6.ico')
		self.tk.call('wm', 'iconphoto', self._w, icon)
		#tk.Tk.iconbitmap(self, default='chev6.ico')
		self.title("AUPAS")
		self.geometry("800x600")

		container = tk.Frame(self)
		container = ttk.Frame(self)
		

		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)
		container.configure()

		text = tk.Text(container)
		
		menubar = tk.Menu(container) 
		file = tk.Menu(menubar, tearoff = 0,background= "#333333", activebackground="#E95420", fg="#fff") 
		menubar.add_cascade(label ='File',background= "#333333", menu = file) 
		file.add_command(label ='      New file             ', command = None, accelerator="Ctrl+Q") 
		file.add_command(label ='      Open...', command = None) 
		file.add_command(label ='      Save', command = None) 
		file.add_separator() 
		file.add_command(label ='      Exit', command = quit) 
		tk.Tk.config(self, menu = menubar) 


		menubar.configure(bg=mycolor3, fg=mycolor4, activebackground=mycolor2, activeforeground=mycolor4
									,activeborderwidth=0, bd=0)


		self.frames = {}

		for F in (HomePage,PageOne,BaseGraph):
			
			frame = F(container,self)
			
			self.frames[F] = frame
			frame.grid(row=0,column=0, sticky="nsew")

			

			frame.configure(background = "#111")
			#frame.grid(row=0 ,column=0,sticky="nsew")

			self.show_frame(HomePage)

	def show_frame(self, cont):
		
		frame = self.frames[cont]
		frame.tkraise()

	def quit(container,event):
		print("Aupas is exiting ..... ")
		sys.exit(3)

def rs(params):
	print(params)

def popupmsg(str):
	print(str)  

"""
 The homepage is the first page we see when we launch the application
"""
class HomePage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		
		content = tk.Frame(self)

		
		self.filename = ImageTk.PhotoImage(Image.open("three.jpg"))
		background_label = tk.Label(content, image = self.filename)
		background_label.place(x=0, y=0, relwidth = 1, relheight=1) 

		
		upload_btn = tk.Button(content, cursor="hand1",width ="20",padx = 2, fg = font_color__btn,activeforeground = active_font_color__btn, highlightbackground = highlight_bg_color__btn , bg = bg_color__btn,activebackground = activebackground_color__btn, text="Upload", command = lambda: controller.show_frame(PageOne))


		analyze_btn = tk.Button(content, cursor="hand1",width ="20",padx = 2, fg = font_color__btn,activeforeground = active_font_color__btn, highlightbackground = highlight_bg_color__btn , bg = bg_color__btn,activebackground = activebackground_color__btn, text="Analyze", command = lambda: controller.show_frame(BaseGraph))

		
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0,weight=1)
		content.rowconfigure(0,weight=5)
		content.rowconfigure(1,weight=5)
		content.rowconfigure(2,weight=1)
		content.rowconfigure(3,weight=1)
		content.rowconfigure(4,weight=1)
		content.rowconfigure(5,weight=5)
		content.rowconfigure(6,weight=5)
		content.columnconfigure(0,weight=5)
		content.columnconfigure(1,weight=1)
		content.columnconfigure(2,weight=5)

		content.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.E,tk.W))

		upload_btn.grid(column=1,row=2,sticky=(tk.E,tk.W))
		analyze_btn.grid(column=1,row=3,sticky=(tk.E,tk.W))


""" 
 This is the upload page where we do all the dirty work
"""
class PageOne(ttk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self,parent)

		content = tk.Frame(self)
		content.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.E,tk.W)) 

		self.columnconfigure(0, weight =1)
		self.rowconfigure(0, weight =1)


		content.configure(bg = "#111")

		content.rowconfigure(0,weight=4)
		content.rowconfigure(1,weight=1)
		content.rowconfigure(2,weight=10)
		content.rowconfigure(3,weight=1)
		content.rowconfigure(4,weight=2)
		content.rowconfigure(5,weight=1)
		
		
		
		
		
		content.columnconfigure(0,weight=1)
		content.columnconfigure(1,weight=1)
		content.columnconfigure(2,weight=1)
		content.columnconfigure(3,weight=1)
		content.columnconfigure(4,weight=10)
		content.columnconfigure(5,weight=3)
		
		
		"""
		 This fat method does almost all the work in uploads.
		 We start with a blank canvas and we then continously build up widgets as needed
		 When an upload is done, this method unpacks the preview and we revert back to the blank canvas  
		"""			

		

		def pick_data():
			self.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
			label = tk.Label(self, text=self.filename)
			df = pd.read_csv(self.filename)
			pd.set_option('max_info_columns',20)
			
			upload__meta = "Source: {csv_name}\ntype: csv\nrows: {csv_row_nums}\ncolumns: {csv_column_nums}\n".format(csv_name = os.path.basename(self.filename) ,csv_row_nums = df.shape[0],csv_column_nums = df.shape[1])
			csv_type= tk.Label(content, text = upload__meta, anchor="w", bg="#111", justify = "left", fg="#fff")
			csv_type.grid(column = 1, row = 2, rowspan = 1, columnspan = 2, sticky="new")

			"""We use a newline here and its ugly but its the price we'll pay to make targets prettier"""
			target__meta = "\n\nTarget =======\nType: Database\nName: cmsreplica".format()
			target__meta_label= tk.Label(content, text = target__meta, anchor="w", bg="#111", justify = "left", fg="#fff")
			target__meta_label.grid(column = 1, row = 3, rowspan = 1, columnspan = 2, sticky="new")         
			

			upload_data_btn = tk.Button(content, command =lambda: pg_load_table(self.filename, table_name, dbname, host, port,user,pwd), cursor="hand1",width ="20",padx = 2, fg = font_color__btn,activeforeground = active_font_color__btn, highlightbackground = highlight_bg_color__btn , bg = bg_color__btn,activebackground = activebackground_color__btn, text="Upload Data") 
			upload_data_btn.grid(row = 3, column = 4, rowspan = 1, columnspan = 1, sticky="w",)
			

			preview_data_label = tk.Label(content,text = "Preview Data", width="20", bg = bg_color__btn, fg = font_color__btn)
			preview_data_label.grid(row  = 1, column = 4, columnspan = 4, sticky="w",)

			preview_data_frame = tk.Frame(content, bg="#c0c0c0", relief="sunken")
			preview_data_frame.grid(column=4, row = 2, sticky="nsew")

			pt = Table(preview_data_frame, dataframe = df,showtoolbar=True, showstatusbar=True )
			pt.importCSV(self.filename) 
			pt.show()
			
			
		select_data_btn = tk.Button(content, cursor="hand1",width ="20", fg = font_color__btn,activeforeground = active_font_color__btn, highlightbackground = highlight_bg_color__btn , bg = bg_color__btn,activebackground = activebackground_color__btn, text="Select Data", command = pick_data) 
		select_data_btn.grid(row = 1, column = 1, rowspan = 1, columnspan = 3, sticky="w")

		"""
		 This method does the copying to the database.
		 It is called by the upload button.
		 PENDING: There are errors that need to be handled and unpacking widgets that need to be done. 
		"""
		def pg_load_table(file_path, table_name, dbname, host, port, user, pwd):
			try:
				conn = psycopg2.connect(dbname=dbname, host=host, port=port,\
				user=user, password=pwd)
				print("Connecting to Database")
				cur = conn.cursor()

				f = open(file_path, "r")
				""" Remove the method when we have more csv files"""
				cur.execute("Truncate {} Cascade;".format(table_name))
				print("Truncated {}".format(table_name))
				#Load table from the file with header
				cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(table_name), f)
				cur.execute("commit;")
				print("Loaded data into {}".format(table_name))
				conn.close()
				

				messagebox.showinfo("Sweet Alert", "Copying is Complete")
				print("DB connection closed.")

			
			except Exception as e:
				print("Error: {}".format(str(e)))
				
		def unpack_preview_and_revert_to_blank_canvas():
			preview_data_frame.grid_forget()
			upload_data_btn.grid_forget()
			csv_type.grid_forget()
			target__meta_label.grid_forget()

class BaseGraph(ttk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		content = tk.Frame(self)
		content.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.E,tk.W)) 

		self.columnconfigure(0, weight =1)
		self.rowconfigure(0, weight =1)

		content.configure(bg = "#111")

		content.rowconfigure(0,weight=2)
		content.rowconfigure(1,weight=10)
		content.rowconfigure(2,weight=2)
		
		content.columnconfigure(0,weight=4)
		content.columnconfigure(1,weight=8)
		content.columnconfigure(2,weight=4)
		
		f = Figure(figsize=(5,5),dpi=100)
		a = f.add_subplot(111)
		a.plot([12,3,56,7,8,9,8],[1,2,3,4,5,6,7])

		graph_frame = ttk.Frame(content)
		graph_frame.grid(row = 1, column = 1, sticky="nsew")

		canvas = FigureCanvasTkAgg(f,graph_frame)
		canvas.show()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		toolbar = NavigationToolbar2TkAgg(canvas, graph_frame)
		toolbar.update()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)




"""
 Execute the nifty program
"""  

app = Aupas()


app.mainloop()
