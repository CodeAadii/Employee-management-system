from tkinter import *
import customtkinter
from requests import *
from sqlite3 import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt


# switch windows
def main():
	root.deiconify()
	add_window.withdraw()
	view_window.withdraw()
	update_window.withdraw()
	delete_window.withdraw()

def add():
	add_window.deiconify()
	root.withdraw()

def view():
	view_window.deiconify()
	root.withdraw()
	scr_view.delete(1.0 , END)
	con = None
	try : 
		con = connect("employee.db")
		cursor = con.cursor()
		sql = "select * from emp"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data : 
			info +=  " id: " +   str(d[0])   +   " name: " +    str(d[1])  +   " salary: " +  str(d[2]) +  "\n"
		scr_view.insert(INSERT , info)
	except Exception as e :
		con.rollback()
		showerror("Issue" , e) 
	finally : 
		if con is not None :
			con.close()

def update():
	update_window.deiconify()
	root.withdraw()

def delete():
	delete_window.deiconify()
	root.withdraw()


# Main window
root = customtkinter.CTk()
root.title("Employee management system")
root.iconbitmap("emp.ico")
customtkinter.set_appearance_mode("dark")
root.geometry("650x400")
f = 16
b_w = 200
b_h = 40

add_emp_button= customtkinter.CTkButton(root,text="Add Employee",font = (None,f), command=add, width=b_w, height=b_h)
add_emp_button.place(x=200, y=30)

view_emp_button= customtkinter.CTkButton(root,text="View Employee",font = (None,f), command=view, width=b_w, height=b_h)
view_emp_button.place(x=200, y=90)

update_emp_button= customtkinter.CTkButton(root,text="Update Employee",font = (None,f), command=update, width=b_w, height=b_h)
update_emp_button.place(x=200, y=150)

delete_emp_button= customtkinter.CTkButton(root,text="Delete Employee",font = (None,f), command=delete, width=b_w, height=b_h)
delete_emp_button.place(x=200, y=210)

def get_weather_data(city_name):
    try:
        api_key = "7b2659424c7686111ba0846bbc7066fc"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        res = get(url)
        data = res.json()
        temperature = data["main"]["temp"]
        lab_temp.configure(text=f"{temperature} °C")
    except Exception as e:
        lab_temp.configure(text="Error fetching data")

tempreture_label= customtkinter.CTkLabel(root,text="Tempreture: ",font = (None,f))
tempreture_label.place(x=200, y=350)

lab_temp = customtkinter.CTkLabel(root, text="",font = (None,f))
lab_temp.place(x=292, y=350)

location_label= customtkinter.CTkLabel(root,text="Location: ",font = (None,f))
location_label.place(x=200, y=325)

lab_loc = customtkinter.CTkLabel(root, text="",font = (None,f))
lab_loc.place(x=270, y=325)

wa = "https://ipinfo.io/223.189.24.150/json?token=9ad7ceff08a9a2"
res = get(wa)
data = res.json()
city_name = data["city"]
lab_loc.configure(text=city_name)

get_weather_data(city_name)


# Add window
add_window = customtkinter.CTkToplevel(root)
add_window.title("Add Employee")
add_window.iconbitmap("emp.ico")
add_window.geometry("650x400")

def save() : 
	con = None
	try : 
		con = connect("employee.db")
		cursor = con.cursor()  
		sql = "insert into emp values('%d' , '%s' , '%f')"
		eid = ent_id.get()
		eid = eid.strip()              
		if (eid == "") or (eid.strip()== "" ) : 
			showerror("Failed ","Id should not be empty")
			ent_id.delete(0 , END)
			ent_id.focus()
			return
		try : 
			id = int(eid) 
		except ValueError : 
			showerror("Failed " , "Id must be integer only")
			ent_id.delete(0 , END)
			ent_id.focus()
			return
		if id < 1 : 
			showerror("Failed " ,"Minimum id should be 1")
			ent_id.delete(0 , END)
			ent_id.focus()
			return
		name = ent_name.get()
		if (name == "") or (name.strip() == "") : 
			showerror("Failed " ,"Name should not be empty ")
			ent_name.delete(0 , END)
			ent_name.focus()
			return
		if (not name.isalpha()) :
			showerror("Failed " ,"Invalid name")
			ent_name.delete(0 , END)
			ent_name.focus()
			return
			
		esalary = (ent_salary.get())
		if (esalary == "" ) or (esalary.strip() == "") : 
			showerror("Failed " ,"Salary should not be empty")
			ent_salary.delete(0 , END)
			ent_salary.focus()
			return
		try : 
			salary = float(esalary)
		except : 
			showerror("Failed " ,"Invalid salary")
			ent_salary.delete(0 , END)
			ent_salary.focus()
			return
		cursor.execute(sql%(id,name,salary))
		con.commit()
		showinfo("Success" , "Records saved ")
		ent_id.delete(0 , END)
		ent_name.delete(0, END)
		ent_salary.delete(0 , END)
		ent_id.focus()
		return
		
	except Exception as e :
		con.rollback()
		showerror("Failed ", e)
		ent_id.delete(0 , END)
		ent_name.delete(0, END)
		ent_salary.delete(0 , END)
		ent_id.focus()
		return

	finally : 
		if con is not None :
			con.close()

emp_id_label= customtkinter.CTkLabel(add_window,text="Enter employee id: ",font = (None,f))
emp_id_label.place(x=160, y=30)

ent_id= customtkinter.CTkEntry(add_window,font = (None,f))
ent_id.place(x=340, y=30)

emp_name_label= customtkinter.CTkLabel(add_window,text="Enter employee name: ",font = (None,f))
emp_name_label.place(x=160, y=80)

ent_name= customtkinter.CTkEntry(add_window,font = (None,f))
ent_name.place(x=340, y=80)

emp_salary_label= customtkinter.CTkLabel(add_window,text="Enter employee salary: ",font = (None,f))
emp_salary_label.place(x=160, y=130)

ent_salary= customtkinter.CTkEntry(add_window,font = (None,f))
ent_salary.place(x=340, y=130)

submit_button= customtkinter.CTkButton(add_window,text="Submit",command=save,font = (None,f))
submit_button.place(x=240, y=200)

back_button= customtkinter.CTkButton(add_window,text="Back",command=main,font = (None,f))
back_button.place(x=240, y=240)

add_window.withdraw()


# View window
view_window = customtkinter.CTkToplevel(root)
view_window.title("View Employee")
view_window.iconbitmap("emp.ico")
view_window.geometry("650x400")

scr_view = ScrolledText(view_window, width = 45 , height = 11,font = (None,23))
scr_view.pack(pady = 20)

back_button= customtkinter.CTkButton(view_window,text="Back",command=main,font = (None,f))
back_button.place(x=240, y=357)

view_window.withdraw()


# Update window
update_window = customtkinter.CTkToplevel(root)
update_window.title("Update Employee")
update_window.iconbitmap("emp.ico")
update_window.geometry("650x400")

def fetch_employee_data_for_update():
    con = None
    try:
        con = connect("employee.db")
        cursor = con.cursor()
        id = uw_ent_id.get()
        if (id == "") or (id.strip() == ""):
            showerror("Failed", "Id should not be empty")
            uw_ent_id.delete(0, END)
            uw_ent_id.focus()
            return
        try:
            id = int(id)
        except:
            showerror("Failed", "Id must be an integer")
            uw_ent_id.delete(0, END)
            uw_ent_id.focus()
            return

        sql = "SELECT * FROM emp WHERE id = %d" % id
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            uw_ent_name.delete(0, END)
            uw_ent_name.insert(0, data[1])
            uw_ent_salary.delete(0, END)
            uw_ent_salary.insert(0, str(data[2]))
        else:
            showerror("Failed", "No employee found with the given ID")
            uw_ent_name.delete(0, END)
            uw_ent_salary.delete(0, END)
    except Exception as e:
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()

def usave() : 
	con = None
	try  :
		con = connect("employee.db")
		cursor = con.cursor()
		sql = "update emp set name ='%s' , salary='%f' where id = '%d' "
		id = uw_ent_id.get()
		id = id.strip()    
		if (id == "") or (id.strip() == "" ) : 
			showerror("Failed " , "Id should not be empty")
			uw_ent_id.delete(0 , END)
			uw_ent_id.focus()
			return
		try : 
			id = int(id)
		except ValueError : 
			showerror("Failed" , "Id must be integer only")
			uw_ent_id.delete(0 , END)
			uw_ent_id.focus()
			return

		if (id < 1) : 
			showerror("Failed" , "Minimum id should be 1 ")
			uw_ent_id.delete(0 , END)
			uw_ent_id.focus()
			return

		name = uw_ent_name.get()
		if (name == "") or (name.strip() == "") : 
			showerror("Failed" , "Name should not be empty")
			uw_ent_name.delete(0 , END)
			uw_ent_name.focus()
			return

		if (not name.isalpha()) : 
			showerror("Failed" , "Invalid name")
			uw_ent_name.delete(0 , END)
			uw_ent_name.focus()
			return
		
		salary = uw_ent_salary.get()
		if (salary == "") or (salary.strip() == "") : 
			showerror("Failed" , "Salary should not be empty")
			uw_ent_salary.delete(0 , END)
			uw_ent_salary.focus()
			return
		try :
			salary = float(salary)
		except ValueError :
			showerror("Failed" , "Invalid salary" )
			uw_ent_salary.delete(0 , END)
			uw_ent_salary.focus()
			return
		cursor.execute(sql%(name,salary,id))
		if cursor.rowcount == 1 : 
			con.commit()
			showinfo("Success" , "Records updated")
			uw_ent_id.delete(0 , END)
			uw_ent_name.delete(0 , END)
			uw_ent_salary.delete(0 , END)
			uw_ent_id.focus()
			return
		else : 
			showerror("Failed" , "Record does not exists ")
			uw_ent_id.delete(0 , END)
			uw_ent_name.delete(0 , END)
			uw_ent_salary.delete(0 , END)
			uw_ent_id.focus()
			return

	except Exception as e : 
		con.rollback()
		showerror("Issue" , e )
		uw_ent_id.delete(0 , END)
		uw_ent_name.delete(0 , END)
		uw_ent_salary.delete(0 , END)
		uw_ent_id.focus()
		return
	
	finally  :
		if con is not None : 
			con.close()

emp_id_label= customtkinter.CTkLabel(update_window,text="Enter employee id: ",font = (None,f))
emp_id_label.place(x=160, y=30)

uw_ent_id= customtkinter.CTkEntry(update_window,font = (None,f))
uw_ent_id.place(x=340, y=30)

emp_name_label= customtkinter.CTkLabel(update_window,text="Enter employee name: ",font = (None,f))
emp_name_label.place(x=160, y=80)

uw_ent_name= customtkinter.CTkEntry(update_window,font = (None,f))
uw_ent_name.place(x=340, y=80)

emp_salary_label= customtkinter.CTkLabel(update_window,text="Enter employee salary: ",font = (None,f))
emp_salary_label.place(x=160, y=130)

uw_ent_salary= customtkinter.CTkEntry(update_window,font = (None,f))
uw_ent_salary.place(x=340, y=130)

fetch_button = customtkinter.CTkButton(update_window, text="Fetch Data", command=fetch_employee_data_for_update, font=(None, f))
fetch_button.place(x=240, y=190)

update_button= customtkinter.CTkButton(update_window,text="Update", command=usave,font = (None,f))
update_button.place(x=240, y=230)

back_button= customtkinter.CTkButton(update_window,text="Back",command=main,font = (None,f))
back_button.place(x=240, y=270)

update_window.withdraw()


# Delete window
delete_window = customtkinter.CTkToplevel(root)
delete_window.title("Delete Employee")
delete_window.iconbitmap("emp.ico")
delete_window.geometry("650x400")

def fetch_employee_data():
    con = None
    try:
        con = connect("employee.db")
        cursor = con.cursor()
        id = dw_ent_id.get()
        if (id == "") or (id.strip() == ""):
            showerror("Failed", "Id should not be empty")
            dw_ent_id.delete(0, END)
            dw_ent_id.focus()
            return
        try:
            id = int(id)
        except:
            showerror("Failed", "Id must be an integer")
            dw_ent_id.delete(0, END)
            dw_ent_id.focus()
            return

        sql = "SELECT * FROM emp WHERE id = %d" % id
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            dw_emp_id_label.configure(text="Employee ID: " + str(data[0]))
            dw_emp_name_label.configure(text="Employee Name: " + data[1])
            dw_emp_salary_label.configure(text="Employee Salary: " + str(data[2]))
        else:
            showerror("Failed", "No employee found with the given ID")
            dw_emp_id_label.configure(text="")
            dw_emp_name_label.configure(text="")
            dw_emp_salary_label.configure(text="")
    except Exception as e:
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()

def dsave():
    con = None
    try:
        con = connect("employee.db")
        cursor = con.cursor()
        id = dw_ent_id.get()
        if (id == "") or (id.strip() == ""):
            showerror("Failed", "Id should not be empty")
            dw_ent_id.delete(0, END)
            dw_ent_id.focus()
            return
        try:
            id = int(id)
        except:
            showerror("Failed", "Id must be an integer")
            dw_ent_id.delete(0, END)
            dw_ent_id.focus()
            return

        sql = "DELETE FROM emp WHERE id = %d" % id
        cursor.execute(sql)
        if cursor.rowcount == 1:
            con.commit()
            showinfo("Success", "Record deleted")
            dw_emp_id_label.configure(text="")
            dw_emp_name_label.configure(text="")
            dw_emp_salary_label.configure(text="")
            dw_ent_id.delete(0, END)
            dw_ent_id.focus()
        else:
            showerror("Failed", "Record does not exist")
            dw_ent_id.delete(0, END)
            dw_ent_id.focus()
    except Exception as e:
        con.rollback()
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()

emp_id_label= customtkinter.CTkLabel(delete_window,text="Enter employee id: ",font = (None,f))
emp_id_label.place(x=160, y=30)

dw_ent_id= customtkinter.CTkEntry(delete_window,font = (None,f))
dw_ent_id.place(x=340, y=30)

fetch_button = customtkinter.CTkButton(delete_window, text="Fetch Data", command=fetch_employee_data, font=(None, f))
fetch_button.place(x=240, y=80)

dw_emp_id_label = customtkinter.CTkLabel(delete_window, text="", font=(None, f))
dw_emp_id_label.place(x=220, y=110)

dw_emp_name_label = customtkinter.CTkLabel(delete_window, text="", font=(None, f))
dw_emp_name_label.place(x=220, y=140)

dw_emp_salary_label = customtkinter.CTkLabel(delete_window, text="", font=(None, f))
dw_emp_salary_label.place(x=220, y=170)

delete_button= customtkinter.CTkButton(delete_window,text="Delete",command=dsave,font = (None,f))
delete_button.place(x=240, y=200)

back_button= customtkinter.CTkButton(delete_window,text="Back",command=main,font = (None,f))
back_button.place(x=240, y=240)

delete_window.withdraw()

def chart():
	con = None
	try:
		con = connect("employee.db")
		cursor = con.cursor()
		sql = '''SELECT name, salary FROM emp ORDER BY salary DESC LIMIT 5'''
		cursor.execute(sql)
		data = cursor.fetchall()
		name = []
		salary = []
		for i in data:
			name.append(i[0])
			salary.append(i[1])
		plt.figure(figsize=(8,6))
		c = ['black', 'black', 'black', 'black' , 'black' ]
		plt.rcParams.update({'text.color': "black", 'axes.labelcolor': "black"})
		ax = plt.axes()
		ax.set_facecolor("lightblue")
		
		
		plt.bar(name, salary ,  color= c)
		plt.xlabel("Names of Employee" , fontsize = 15)
		plt.ylabel("Salary of Employee", fontsize = 15)
		plt.title("Top 5 Highest Salaried Employee", fontsize = 15)
		plt.grid()
		plt.show()
	except Exception as e:
        	showerror("issue ", e)
	        con.rollback()
	finally:
		if con is not None:
			con.close()

charts_emp_button= customtkinter.CTkButton(root,text="Charts",font = (None,f),command=chart, width=b_w, height=b_h)
charts_emp_button.place(x=200, y=270)


# Close windows
def on_closing():
	if askyesno('Exit','Do you want to exit?'):
	    root.destroy()

delete_window.protocol('WM_DELETE_WINDOW', on_closing)
update_window.protocol('WM_DELETE_WINDOW', on_closing)
view_window.protocol('WM_DELETE_WINDOW', on_closing)
add_window.protocol('WM_DELETE_WINDOW', on_closing)
root.protocol('WM_DELETE_WINDOW', on_closing)


root.mainloop()