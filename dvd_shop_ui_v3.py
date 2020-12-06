from tkinter import *
from tkinter import ttk 
import mysql.connector
import utils
from functools import partial
import pyautogui
from tkinter.tix import *

config = utils.load_config('config.json')

try:
	mydb = mysql.connector.connect(
	  host=config["host"], 
	  user=config["user"],
	  password=config["passwd"],
	)

	mycursor = mydb.cursor()

	mycursor.execute("CREATE DATABASE {0}".format(config["database"]))

except mysql.connector.errors.DatabaseError:
	
	print("Connecting to the Database......")
	mydb = mysql.connector.connect(
		host = config["host"], 
		user = config["user"],
		passwd = config["passwd"],
		database = config["database"]
		)

	my_cursor = mydb.cursor()
	try:
		my_cursor.execute("""  
		CREATE TABLE dvds (Title VARCHAR(255) , Star_name VARCHAR(255) , YearOfRelease INTEGER(10) , Genre VARCHAR(255) , user_id INTEGER AUTO_INCREMENT PRIMARY KEY)
		""")  # need to execute only once
	except mysql.connector.errors.ProgrammingError:
		pass
mydb = mysql.connector.connect(
		host = config["host"], 
		user = config["user"],
		passwd = config["passwd"],
		database = config["database"]
		)

my_cursor = mydb.cursor()

def addDVD(data):  # data is a dictionary
	print("Adding Data to Database")
	global my_cursor,mydb
	info = []
	try:
		Title = data["Title"]
		info.append(Title)
	except KeyError:
		print("No key found ")
		info.append("_____")

	try:
		Star_name = data["Star_name"]
		info.append(Star_name)
	except KeyError:
		print("No key found ")
		info.append("_____")

	try:
		YearOfRelease = data["YearOfRelease"]
		info.append(YearOfRelease)
	except KeyError:
		print("No key found ")
		info.append()

	try:
		Genre = data["Genre"]
		info.append(Genre)
	except KeyError:
		print("No key found ")
		info.append("_____")

	
	command = "INSERT INTO dvds (Title,Star_name,YearOfRelease,Genre) VALUES (%s, %s, %s, %s)"
	my_cursor.execute(command,info)
	mydb.commit()
	print("Added Successfully...")



#addDVD({"Title" :"Civil War" ,"Star_name" : "RDJ" , "YearOfRelease" : 2016 , "Genre" : "Action"})  


def delete(name):
	global my_cursor,mydb
	command = "DELETE FROM dvds WHERE Title = %s"
			

	try:
		my_cursor.execute(command, (name,))
		mydb.commit()
		print("Deleted")
	except mysql.connector.errors.ProgrammingError:
		print("That DVD does not exist...")

#delete("Civil War")
# if field == "" and Genre != "NULL":
# 		command = "SELECT * FROM dvds WHERE Genre = {0}".format(Genre)
# 		try:
# 			my_cursor.execute(command)
# 			myres = my_cursor.fetchall()
# 			return myres


def search(field, Genre):
	global my_cursor,mydb
	if field == "" and Genre != "NULL":
		command = "SELECT * FROM dvds WHERE Genre = '{0}' ORDER BY YearOfRelease DESC ".format(Genre)
		# try:
		my_cursor.execute(command)
		myres = my_cursor.fetchall()
		if myres:
			return myres
		else:
			return ["NOT_FOUND_ANYTHING_IN_DB"]
		# except mysql.connector.errors.ProgrammingError:
			# print("Some exception..")

	if Genre != "NULL":
		# print("Genre found in input")
		iters = ["Title" , "Star_name" , "YearOfRelease"]
		error_mitigation_counter = 0
		for it in iters:
			if it != "YearOfRelease":
				command = "SELECT * FROM dvds WHERE {0} = '{1}' AND Genre = '{2}' ORDER BY YearOfRelease DESC ".format(it, field , Genre )
			else:
				command = "SELECT * FROM dvds WHERE {0} = {1} AND Genre = '{2}' ORDER BY YearOfRelease DESC ".format(it, field , Genre )
			try:
				my_cursor.execute(command)
				myres = my_cursor.fetchall()
				if myres:
					return myres
					break
				else:
					error_mitigation_counter += 1

			except:
				error_mitigation_counter += 1
		if error_mitigation_counter == 3:
			return ["NOT_FOUND_ANYTHING_IN_DB"]
			

	

	elif Genre == "NULL":
		iters = ["Title" , "Star_name" , "YearOfRelease"  ]
		error_mitigation_counter = 0
		for it in iters:
			if it != "YearOfRelease":
				command = "SELECT * FROM dvds WHERE {0} = '{1}' ORDER BY YearOfRelease DESC ".format(it, field)
			else:
				command = "SELECT * FROM dvds WHERE {0} = {1} ORDER BY YearOfRelease DESC ".format(it, field)
			try:
				#print(command)
				my_cursor.execute(command)
				myres = my_cursor.fetchall()
				if myres:
					return myres
					break
				else:
					error_mitigation_counter += 1

			except:
				error_mitigation_counter += 1
		if error_mitigation_counter == 3:

			return ["NOT_FOUND_ANYTHING_IN_DB"]


def update(name,field): # field is a dictionary
	iters = ["Title" , "Star_name" , "YearOfRelease", "Genre"]
	global my_cursor,mydb

	if name == "":
		print("Name not found..")
		return ["COULD_NOT_PROCESS"]
	
			
			
	c1 = "SELECT * FROM dvds where Title = '{0}' ".format(name)
	my_cursor.execute(c1)
	data = my_cursor.fetchone()
	#print(data)
	if not data:
		return ["COULD_NOT_PROCESS"]

	titleToAdd = field["Title"] if field["Title"] != ""  else data[0]
	starToAdd = field["Star_name"] if field["Star_name"] != "" else data[1]
	YORtoAdd = field["YearOfRelease"] if field["YearOfRelease"] != "" else data[2]
	genreTOadd = field["Genre"] if field["Genre"] != "" else data[3]
	command = "UPDATE dvds SET Title = '{0}' , Star_name = '{1}' ,  YearOfRelease = {2} , Genre = '{3}' WHERE Title = '{4}'".format(titleToAdd , starToAdd , YORtoAdd , genreTOadd , name )
	my_cursor.execute(command)
	mydb.commit()
	return ["UPDATED_SUCCESSFULLY"]
		




#print(update("Be Water" , {"Title" : "Be Water" , "Star_name" : "" , "YearOfRelease" : 20900 , "Genre" : ""}))

	
# print(search("" , "Politics"))

mainWindow = Tk()

mainWindow.attributes('-fullscreen',True)
mainWindow.iconbitmap('DVDs.ico')
mylabel1 = Label(mainWindow,text=" Welcome to the DVD shop  "  , font=('Helvetica', 20, 'bold') , pady = 20)
mylabel1.grid(row= 0 , column =2)

def exit_app():
	pyautogui.hotkey('alt', 'F4')	

# Add Area Begins

addButton = Button(mainWindow, text = "Exit" ,  fg = "blue" , bg = "white" , width = 20  ,command = exit_app)
addButton.grid(row = 0, column = 4)

titleEntry = Entry(mainWindow, width = 50 , borderwidth = 5)
genreEntry = Entry(mainWindow, width = 50 , borderwidth = 5)
yearOfReleaseEntry = Entry(mainWindow, width = 50 , borderwidth = 5)
starNameEntry = Entry(mainWindow, width = 50 , borderwidth = 5)


titleEntry.grid(row = 1, column = 0)
genreEntry.grid(row = 1, column = 1)
yearOfReleaseEntry.grid(row = 1, column = 2)
starNameEntry.grid(row = 1, column = 3)

titleEntry.insert(0, "Title of the DVD")
genreEntry.insert(0, "Genre of the DVD")
yearOfReleaseEntry.insert(0, "Year of Release of the DVD")
starNameEntry.insert(0, "Star name  of the DVD")

titleEntry.configure(state=DISABLED)
genreEntry.configure(state=DISABLED)
yearOfReleaseEntry.configure(state=DISABLED)
starNameEntry.configure(state=DISABLED)


mylabel2 = Label(mainWindow,text="                                  "  , font=('Helvetica', 15))
mylabel2.grid(row= 2 , column =2)






def on_click1(event):
	titleEntry.configure(state=NORMAL)
	titleEntry.delete(0, END)
	titleEntry.unbind('<Button-1>', on_click_id1)

def on_click2(event):
	genreEntry.configure(state=NORMAL)
	genreEntry.delete(0, END)
	genreEntry.unbind('<Button-1>', on_click_id2)

def on_click3(event):
	yearOfReleaseEntry.configure(state=NORMAL)
	yearOfReleaseEntry.delete(0, END)
	yearOfReleaseEntry.unbind('<Button-1>', on_click_id3)

def on_click4(event):
	starNameEntry.configure(state=NORMAL)
	starNameEntry.delete(0, END)
	starNameEntry.unbind('<Button-1>', on_click_id4)


	

on_click_id1 = titleEntry.bind('<Button-1>', on_click1)
on_click_id2 = genreEntry.bind('<Button-1>', on_click2)
on_click_id3 = yearOfReleaseEntry.bind('<Button-1>', on_click3)
on_click_id4 = starNameEntry.bind('<Button-1>', on_click4)

# Add Area Ends

# Search Area starts

mylabel3 = Label(mainWindow,text=" Search Options  "  , font=('Helvetica', 18, 'bold') , pady = 30)
mylabel3.grid(row= 3 , column =2)

fieldSearch = Entry(mainWindow, width = 50 , borderwidth = 5)
genreSearch = Entry(mainWindow, width = 50 , borderwidth = 5)
fieldSearch.grid(row = 4, column = 0)
genreSearch.grid(row = 4, column = 1)
fieldSearch.insert(0, "Please enter Movie name or year or Artist to search.")
genreSearch.insert(0, "Please specify Genre (Optional)")
fieldSearch.configure(state=DISABLED)
genreSearch.configure(state=DISABLED)

def on_click5(event):
	fieldSearch.configure(state=NORMAL)
	fieldSearch.delete(0, END)
	fieldSearch.unbind('<Button-1>', on_click_id5)

def on_click6(event):
	genreSearch.configure(state=NORMAL)
	genreSearch.delete(0, END)
	genreSearch.unbind('<Button-1>', on_click_id6)

on_click_id5 = fieldSearch.bind('<Button-1>', on_click5)
on_click_id6 = genreSearch.bind('<Button-1>', on_click6)

# Search Area Ends

# Delete ARea Begins
mylabel4 = Label(mainWindow,text="Delete Options "  , font=('Helvetica', 18, 'bold') , pady = 30)
mylabel4.grid(row= 5 , column =2)

deleteSearch = Entry(mainWindow, width = 50 , borderwidth = 5)
deleteSearch.grid(row = 6, column = 0)
deleteSearch.insert(0, "Please enter Movie name to Delete")
deleteSearch.configure(state=DISABLED)

def on_click7(event):
	deleteSearch.configure(state=NORMAL)
	deleteSearch.delete(0, END)
	deleteSearch.unbind('<Button-1>', on_click_id7)



on_click_id7 = deleteSearch.bind('<Button-1>', on_click7)

# Delete ARea Ends

# Update Area Starts

upLabel = Label(mainWindow,text="Update your DVD Info..."  , font=('Helvetica', 20, 'bold') , pady = 20)
upLabel.grid(row= 7 , column =2)


titleUp = Entry(mainWindow, width = 50 , borderwidth = 5)
genreUp = Entry(mainWindow, width = 50 , borderwidth = 5)
yearOfReleaseUp = Entry(mainWindow, width = 50 , borderwidth = 5)
starNameUp = Entry(mainWindow, width = 50 , borderwidth = 5)


titleUp.grid(row = 8, column = 0)
genreUp.grid(row = 8, column = 1)
yearOfReleaseUp.grid(row = 8, column = 2)
starNameUp.grid(row = 8, column = 3)

titleUp.insert(0, "Title of the DVD")
genreUp.insert(0, "Genre of the DVD")
yearOfReleaseUp.insert(0, "Year of Release of the DVD")
starNameUp.insert(0, "Star name  of the DVD")

titleUp.configure(state=DISABLED)
genreUp.configure(state=DISABLED)
yearOfReleaseUp.configure(state=DISABLED)
starNameUp.configure(state=DISABLED)


def on_click8(event):
	titleUp.configure(state=NORMAL)
	titleUp.delete(0, END)
	titleUp.unbind('<Button-1>', on_click_id8)

def on_click9(event):
	genreUp.configure(state=NORMAL)
	genreUp.delete(0, END)
	genreUp.unbind('<Button-1>', on_click_id9)

def on_click10(event):
	yearOfReleaseUp.configure(state=NORMAL)
	yearOfReleaseUp.delete(0, END)
	yearOfReleaseUp.unbind('<Button-1>', on_click_id10)

def on_click11(event):
	starNameUp.configure(state=NORMAL)
	starNameUp.delete(0, END)
	starNameUp.unbind('<Button-1>', on_click_id11)


on_click_id8 = titleUp.bind('<Button-1>', on_click8)
on_click_id9 = genreUp.bind('<Button-1>', on_click9)
on_click_id10 = yearOfReleaseUp.bind('<Button-1>', on_click10)
on_click_id11 = starNameUp.bind('<Button-1>', on_click11)

# Update Area Ends


def add_dvd_details():
	data = {"Title" : "random","Star_name" : "NOT_ADDED"  , "YearOfRelease" : 0  , "Genre" : "NOT_ADDED" }
	Title = titleEntry.get()
	Star_name = starNameEntry.get()
	YearOfRelease = yearOfReleaseEntry.get()
	Genre = genreEntry.get()

	# print(YearOfRelease == "Year of Release of the DVD")
	if Title == "" or Title == None or Title == "Title of the DVD" :
		newWindow = Toplevel(mainWindow)
		newWindow.iconbitmap('DVDs.ico')

		newWindow.geometry("600x200")
		newWindow.title("Uploading Failed")
		label1 = Label(newWindow,text="Please enter a Valid Movie Name "  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)
		titleEntry.delete(0, END)
		titleEntry.insert(0, "Title of the DVD")
		titleEntry.configure(state=DISABLED)
		on_click_id1 = titleEntry.bind('<Button-1>', on_click1)

	else:
		data["Title"] = Title

		if Star_name != "" and  Star_name != "Star name  of the DVD":
			data["Star_name"] = Star_name

		if YearOfRelease != "" and  YearOfRelease != "Year of Release of the DVD":
			data["YearOfRelease"] = int(YearOfRelease)

		if Genre != "" and  Genre != "Genre of the DVD":
			data["Genre"] = Genre

		print(data)
		addDVD(data)
		newWindow = Toplevel(mainWindow)
		newWindow.iconbitmap('DVDs.ico')
		newWindow.geometry("500x500")
		newWindow.title("Upload successful")
		label1 = Label(newWindow,text="Added Successfully"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)
		

		titleEntry.delete(0, END)
		titleEntry.insert(0, "Title of the DVD")

		genreEntry.delete(0, END)
		genreEntry.insert(0, "Genre of the DVD")

		yearOfReleaseEntry.delete(0, END)
		yearOfReleaseEntry.insert(0, "Year of Release of the DVD")

		starNameEntry.delete(0, END)
		starNameEntry.insert(0, "Star name  of the DVD")

		titleEntry.configure(state=DISABLED)
		genreEntry.configure(state=DISABLED)
		yearOfReleaseEntry.configure(state=DISABLED)
		starNameEntry.configure(state=DISABLED)

		on_click_id1 = titleEntry.bind('<Button-1>', on_click1)
		on_click_id2 = genreEntry.bind('<Button-1>', on_click2)
		on_click_id3 = yearOfReleaseEntry.bind('<Button-1>', on_click3)
		on_click_id4 = starNameEntry.bind('<Button-1>', on_click4)


		

	

addButton = Button(mainWindow, text = "Add DVD" ,  fg = "blue" , bg = "white" , width = 50 , command = add_dvd_details)  # state = DISABLED , padx = 50 , pady = 50
addButton.grid(row = 1, column = 4)

def search_details():
	fieldData,genreData = fieldSearch.get() , genreSearch.get()
	result = "hjksd7wq5e836eiohdsannsanxo892282181wj#hh@hl8wy982@jho8"
	#print(fieldData,genreData)
	if fieldData == "Please enter Movie name or year or Artist to search.":
		fieldData = ""
	if genreData != "" and genreData != "Please specify Genre (Optional)":
		result = search(fieldData,genreData)
		
	else:
		genreData = "NULL"
		# print("Running condition 3")
		result = search(fieldData,genreData)
		# print(result ==["NOT_FOUND_ANYTHING_IN_DB"])

	fieldSearch.delete(0, END)
	fieldSearch.insert(0, "Please enter Movie name or year or Artist to search.")

	genreSearch.delete(0, END)
	genreSearch.insert(0, "Please specify Genre (Optional)")

	fieldSearch.configure(state=DISABLED)
	genreSearch.configure(state=DISABLED)
	
	on_click_id5 = fieldSearch.bind('<Button-1>', on_click5)
	on_click_id6 = genreSearch.bind('<Button-1>', on_click6)	

	if result != ["NOT_FOUND_ANYTHING_IN_DB"] :
		newWindow = Toplevel(mainWindow)
		newWindow.geometry("1800x1000")
		newWindow.iconbitmap('DVDs.ico')
		newWindow.title("Search Results")

		main_frame = Frame(newWindow)
		main_frame.pack(fill = BOTH , expand = 1)

		my_canvas = Canvas(main_frame)
		my_canvas.pack(side=LEFT , fill = BOTH , expand = 1)

		my_scrollbar = ttk.Scrollbar(main_frame , orient = VERTICAL , command = my_canvas.yview)
		my_scrollbar.pack(side = RIGHT , fill = Y)


		my_canvas.configure(yscrollcommand= my_scrollbar.set)
		my_canvas.bind('<Configure>' , lambda e : my_canvas.configure(scrollregion = my_canvas.bbox("all")))

		second_frame = Frame(my_canvas)
		my_canvas.create_window((0,0) , window = second_frame , anchor = "nw")

		label1 = Label(second_frame,text="Title"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)
		label2 = Label(second_frame,text="Star Name"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label2.grid(row= 0 , column =1)
		label3 = Label(second_frame,text="Year of Release"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label3.grid(row= 0 , column =2)
		label4 = Label(second_frame,text="Genre"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label4.grid(row= 0 , column =3)

		for i in range(len(result)):
			for j in range(4):
				l = Label(second_frame,text=str(result[i][j]) , font=('Helvetica', 14) , borderwidth = 15)
				l.grid(row = i+1, column = j)
	
	else:
		
		newWindow = Toplevel(mainWindow)
		newWindow.iconbitmap('DVDs.ico')
		newWindow.geometry("800x200")
		newWindow.title("Search Results")
		label1 = Label(newWindow,text="No Results Found. Please Try Again"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)

	print(result)


searchButton = Button(mainWindow, text = "Search" ,  fg = "blue" , bg = "white" , width = 50 , command = search_details)  # state = DISABLED , padx = 50 , pady = 50
searchButton.grid(row = 4, column = 2)

def delete_complete(name):
	delete(name)
	newWindow = Toplevel(mainWindow)
	newWindow.iconbitmap('DVDs.ico')
	newWindow.geometry("500x500")
	newWindow.title("Search Results")
	label1 = Label(newWindow,text="Deleted Successfully"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
	label1.grid(row= 0 , column =0)

def delete_details():
	deleteData = deleteSearch.get()
	result = "hjksd7wq5e836eiohdsannsanxo892282181wj#hh@hl8wy982@jho8"
	#print(fieldData,genreData)
	if deleteData == "Please enter Movie name to Delete" or deleteData == "":
		deleteData = "NULL"
		# newWindow = Toplevel(mainWindow)
		# newWindow.geometry("500x500")
		# newWindow.title("Search Results")
		# label1 = Label(newWindow,text="No Results Found. Please Try Again"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		# label1.grid(row= 0 , column =0)

	
	else:
		genreData = "NULL"
		result = search(deleteData,genreData)

	deleteSearch.delete(0, END)
	deleteSearch.insert(0, "Please enter Movie name to Delete")



	deleteSearch.configure(state=DISABLED)
	
	on_click_id7 = deleteSearch.bind('<Button-1>', on_click7)

	if result != ["NOT_FOUND_ANYTHING_IN_DB"] and deleteData != "NULL" :
		newWindow = Toplevel(mainWindow)
		newWindow.geometry("1800x1000")
		newWindow.title("Search Results")

		


		label1 = Label(newWindow,text="Title"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)
		label2 = Label(newWindow,text="Star Name"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label2.grid(row= 0 , column =1)
		label3 = Label(newWindow,text="Year of Release"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label3.grid(row= 0 , column =2)
		label4 = Label(newWindow,text="Genre"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label4.grid(row= 0 , column =3)

		for i in range(len(result)):
			for j in range(4):
				
				l = Label(newWindow,text=str(result[i][j]) , font=('Helvetica', 14) , borderwidth = 15)
				l.grid(row = i+1, column = j)

		label5 = Label(newWindow,text="Are You sure you want to delete??"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label5.grid(row= 2 , column =3)

		delete = Button(newWindow, text = "Delete Finally" ,  fg = "blue" , bg = "white" , width = 50 , command = partial(delete_complete,result[0][0]))  # state = DISABLED , padx = 50 , pady = 50
		delete.grid(row = 2, column = 4)





	
	else:
		
		newWindow = Toplevel(mainWindow)
		newWindow.iconbitmap('DVDs.ico')
		newWindow.geometry("800x200")
		newWindow.title("Search Results")
		label1 = Label(newWindow,text="No Results Found. Please Try Again"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)

	print(result)




deleteButton = Button(mainWindow, text = "Delete" ,  fg = "blue" , bg = "white" , width = 50 , command = delete_details)  # state = DISABLED , padx = 50 , pady = 50
deleteButton.grid(row = 6, column = 1)



def updateInfo():
	TitleData = titleUp.get()
	GenreData = genreUp.get()
	YearOfReleaseData = yearOfReleaseUp.get()
	StarNameData = starNameUp.get()

	if TitleData == "Title of the DVD":
		TitleData = ""
	if GenreData == "Genre of the DVD":
		GenreData = ""
	if YearOfReleaseData == "Year of Release of the DVD":
		YearOfReleaseData = ""
	if StarNameData == "Star name  of the DVD":
		StarNameData = ""
	d = dict(zip(["Title" , "Star_name" , "YearOfRelease", "Genre"], [TitleData,StarNameData,YearOfReleaseData,GenreData]))
	result = update(TitleData , d)
	# print(d)
	# print(result)
	if result != ['UPDATED_SUCCESSFULLY']:
		newWindow = Toplevel(mainWindow)
		newWindow.iconbitmap('DVDs.ico')
		newWindow.geometry("800x200")
		newWindow.title("Search Results")
		label1 = Label(newWindow,text="Could not Process the request. Try again!!"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)

	elif result == ['UPDATED_SUCCESSFULLY'] :
		newWindow = Toplevel(mainWindow)
		newWindow.iconbitmap('DVDs.ico')
		newWindow.geometry("500x200")
		newWindow.title("Search Results")
		label1 = Label(newWindow,text="Updated Successfully!!"  , font=('Helvetica', 18, 'bold') , borderwidth = 15)
		label1.grid(row= 0 , column =0)


		titleUp.delete(0, END)
		titleUp.insert(0, "Title of the DVD")

		genreUp.delete(0, END)
		genreUp.insert(0, "Genre of the DVD")

		yearOfReleaseUp.delete(0, END)
		yearOfReleaseUp.insert(0, "Year of Release of the DVD")

		starNameUp.delete(0, END)
		starNameUp.insert(0, "Star name  of the DVD")

		titleUp.configure(state=DISABLED)
		genreUp.configure(state=DISABLED)
		yearOfReleaseUp.configure(state=DISABLED)
		starNameUp.configure(state=DISABLED)

		on_click_id8 = titleUp.bind('<Button-1>', on_click8)
		on_click_id9 = genreUp.bind('<Button-1>', on_click9)
		on_click_id10 = yearOfReleaseUp.bind('<Button-1>', on_click10)
		on_click_id11 = starNameUp.bind('<Button-1>', on_click11)
deleteButton = Button(mainWindow, text = "Update" ,  fg = "blue" , bg = "white" , width = 50 , command = updateInfo)  # state = DISABLED , padx = 50 , pady = 50
deleteButton.grid(row = 8, column = 4)

mainWindow.mainloop()
