
from tkinter import ttk
import time
import tkinter as tk
from tkinter import*
from tkinter import messagebox

def main():
    win = Tk()
    app = LoginPage(win)
    win.mainloop()

class LoginPage:

    def __init__(self,win):
        self.win = win
        self.win.geometry("1500x1500+0+0")
        self.win.title("Hotel Management System by clinton mogoi")
        self.title_label = Label(self.win, text="BURUDANI ADRESS MANAGEMENT SYSTEM ", font=('Arial', 35, 'bold'),fg='yellow',background="purple",borderwidth=15, relief=RIDGE)
        self.title_label.pack(side=TOP, fill=X)
        self.main_frame=Frame(self.win, background="black", borderwidth=6, relief=GROOVE)
        self.main_frame.place(x =1, y=90, width=1500, height=600)
        self.login_lbl=Label(self.main_frame, text="Login", bd=6, relief=GROOVE, anchor=CENTER, bg="lightgrey", font=('sans - serif',25, 'bold'))
        self.login_lbl.pack(side=TOP, fill=X)
        self.entry_frame=LabelFrame(self.main_frame, text="Enter Details", bd=6, relief=GROOVE, bg="lightgrey", font=('sans - serif',18))
        self.entry_frame.pack(fill=BOTH, expand=TRUE)
        self.entus_lbl=Label(self.entry_frame, text="Enter Username: ", font=("sans-serif", 15))
        self.entus_lbl.grid(row= 0, column=0,padx=2,pady=2)

        username = StringVar()
        password = StringVar()

        self.entus_ent = Entry(self.entry_frame, font=('sans-serif',15),bd=6, bg="aqua",textvariable=username,show="")
        self.entus_ent.grid(row=0,column=1,padx=2, pady=2)

        self.entpass_lbl = Label(self.entry_frame, text="Enter Password: ", bg="lightgrey", font=("sans- serif", 15))
        self.entpass_lbl.grid(row=1,column=0,padx=2, pady=2)

        self.entpass_ent = Entry(self.entry_frame, font=('sans-serif', 15), bd=6, bg="aqua",textvariable=password,show="*")
        self.entpass_ent.grid(row = 1, column= 1, padx=2, pady=2)

        def check_login():

            if username.get() == "clinton" and password.get() == "1234":
                self.progress_window = Toplevel(self.win)
                self.progress_window.title("Logging In...")
                self.progress_window.geometry("300x100")
                self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=200,mode="determinate")
                self.progress_bar.pack(pady=20)

                import threading

                def simulate_login_progress():
                    for i in range(101):
                        self.progress_bar['value'] = i
                        self.progress_window.update_idletasks()
                        time.sleep(0.01)
                    self.progress_window.destroy()
                    self.newwindow = Toplevel(self.win)
                    self.app = Window2(self.newwindow)

                login_thread = threading.Thread(target=simulate_login_progress)
                login_thread.start()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

        def reset():
            username.set("")
            password.set("")

        self.button_frame=LabelFrame(self.entry_frame, text="Options", font=("Arial", 15), bg="lightgrey", bd=7, relief=GROOVE)
        self.button_frame.place(x=20, y=188, width=500,height=100)

        self.login_btn=Button(self.button_frame, text="Login", font=("Arial", 15),bg="blue", bd= 5, width=15,command=check_login)
        self.login_btn.grid(row=0, column=0, padx=20, pady=2)

        self.reset_btn=Button(self.button_frame, text="Reset", font=("Arial", 15), bd =5, bg="red", width = 15,command=reset)
        self.reset_btn.grid(row=0, column=2, padx=20, pady=2)


class Window2:
    
    def __init__(self,win):
        self.win=win
        self.win.geometry("1500x670+0+0")
        self.win.title("Hotel Management System by mogoi")
        self.title_label=Label(self.win, text="HOTEL MANAGEMENT SYSTEM", font=('Arial', 35, "bold"), bg="lightgrey", bd=8, relief=RIDGE)
        self.title_label.pack(side=TOP, fill=X)
        self.win.resizable(0,0)

        calc_var = StringVar()
        cust_nm = StringVar()
        total_list = []
        self.grid_total = 0

        self.customer_name_label = Label(self.win, text="Customer Name:", font=('Arial', 15), fg="blue")
        self.customer_name_label.place(x=5, y=65,)

        self.customer_name_entry = Entry(self.win, bd=5,width=16, font=('Arial', 15))
        self.customer_name_entry.place(x=160, y=65)

        self.entry_frame=LabelFrame(self.win, text= "Cold Drinks",fg='blue', font=('Arial',15), bd=7, relief=GROOVE)
        self.entry_frame.place(x= 5, y=110, width= 400,height= 400)

        self.soda=Label(self.entry_frame, text="soda ", font=("Arial", 15),fg='magenta')
        self.soda.grid(row= 0, column =0, padx =2, pady=2)

        self.soda_ent=Entry(self.entry_frame, bd= 5,bg='aqua', font=('Arial', 15))
        self.soda_ent.grid(row=0, column= 1, padx=2, pady= 2)

        self.water_lbl = tk.Label(self.entry_frame, text="water", font=('Arial', 15),fg='magenta')
        self.water_lbl.grid(row=1, column=0, padx=2, pady=2)

        self.water_ent=Entry(self.entry_frame, bd=5, bg='aqua',font=('Arial', 15))
        self.water_ent.grid(row= 1, column=1, padx= 2, pady =2)

        self.juice=Label(self.entry_frame, text ="juice ", font=('Arial', 15),fg='magenta')
        self.juice.grid(row=2, column=0, padx=2, pady = 2)

        self.juice_ent=Entry(self.entry_frame, bd = 5,bg='aqua', font=('Arial', 15))
        self.juice_ent.grid(row=2, column=1, padx=2, pady=2)

        self.wine=Label(self.entry_frame, text="wine ", font=('Arial', 15), fg='magenta')
        self.wine.grid(row=3, column=0, padx=2, pady=2)

        self.wine_ent=Entry(self.entry_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.wine_ent.grid(row=3,column=1,padx=2,pady=2)

        self.hot_drinks_frame = LabelFrame(self.win, text="Hot Drinks",fg='blue', background="lightgrey", font=('Arial', 20), bd=7, relief=GROOVE)
        self.hot_drinks_frame.place(x=5, y=300, width=400, height=430)

        self.coffee = Label(self.hot_drinks_frame,text="Coffee", font=("Arial", 15), width=9,fg='magenta')
        self.coffee.grid(row=0, column=0, padx=2, pady=2,sticky=W)

        self.coffee_ent = Entry(self.hot_drinks_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.coffee_ent.grid(row=0, column=1, padx=2, pady=2,sticky=W)

        self.milk_label = Label(self.hot_drinks_frame,text="Milk", font=("Arial", 15), width=9,fg='magenta')
        self.milk_label.grid(row=1, column=0, padx=2, pady=2,sticky=W)

        self.milk_ent = Entry(self.hot_drinks_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.milk_ent.grid(row=1, column=1, padx=2, pady=2)

        self.black_tea_label = Label(self.hot_drinks_frame, text="Black Tea", font=("Arial", 15), width=9,fg='magenta')
        self.black_tea_label.grid(row=2, column=0, padx=2, pady=2,sticky=W)

        self.black_tea_ent = Entry(self.hot_drinks_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.black_tea_ent.grid(row=2, column=1, padx=2, pady=2)

        self.entry_frame=LabelFrame(self.win, text= "Foods", background="lightgrey", font=('Arial', 20),fg='blue', bd=7, relief=GROOVE)
        self.entry_frame.place(x= 400, y=110, width= 400,height= 400)

        self.matooke = Label(self.entry_frame, text="matooke ", font=("Arial", 15), width=9,fg='magenta')
        self.matooke.grid(row=0, column=0, padx=2, pady=2)

        self.matooke_ent=Entry(self.entry_frame, bd= 5,bg='aqua', font=('Arial', 15))
        self.matooke_ent.grid(row=0, column= 1, padx=2, pady= 2)

        self.rice=Label(self.entry_frame, text= "rice", font=('Arial', 15), width=9, fg='magenta')
        self.rice.grid(row=1, column =0, padx= 2, pady= 2,sticky=W)

        self.rice_ent=Entry(self.entry_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.rice_ent.grid(row= 1, column=1, padx= 2, pady =2)

        self.posho=Label(self.entry_frame, text ="posho ", font=('Arial', 15), width=9,fg='magenta')
        self.posho.grid(row=2, column=0, padx=2, pady = 2,sticky=W)

        self.posho_ent=Entry(self.entry_frame, bd = 5,bg='aqua', font=('Arial', 15))
        self.posho_ent.grid(row=2, column=1, padx=2, pady=2)

        self.hot_drinks_frame = LabelFrame(self.win, text="Sauce", background="lightgrey", font=('Arial', 20),fg='blue', bd=7, relief=GROOVE)
        self.hot_drinks_frame.place(x=400, y=300, width=400, height=430)

        self.meat = Label(self.hot_drinks_frame, text="meat", font=("Arial", 15), width=9,fg='magenta')
        self.meat.grid(row=0, column=0, padx=2, pady=2,sticky=W)

        self.meat_ent = Entry(self.hot_drinks_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.meat_ent.grid(row=0, column=1, padx=2, pady=2)

        self.beans = Label(self.hot_drinks_frame, text="beans", font=("Arial", 15), width=9,fg='magenta')
        self.beans.grid(row=1, column=0, padx=2, pady=2,sticky=W)

        self.beans_ent = Entry(self.hot_drinks_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.beans_ent.grid(row=1, column=1, padx=2, pady=2,sticky=W,columnspan=3)

        self.vegetables = Label(self.hot_drinks_frame, text="vegetables", font=("Arial", 15), width=9,fg='magenta')
        self.vegetables.grid(row=2, column=0, padx=2, pady=2)

        self.vegetables_ent = Entry(self.hot_drinks_frame, bd=5,bg='aqua', font=('Arial', 15))
        self.vegetables_ent.grid(row=2, column=1, padx=2, pady=2)

        soda = StringVar()
        water = StringVar()
        juice = StringVar()
        wine = StringVar()
        coffee = StringVar()
        milk = StringVar()
        blacktea = StringVar()
        matooke = StringVar()
        rice = StringVar()
        posho = StringVar()
        meat = StringVar()
        beans = StringVar()
        vegetables = StringVar()
        cust_nm = StringVar()

        def default_bill():
            self.bill_txt.insert(END, "Burudani club")
            self.bill_txt.insert(END, "\nJujacitycmall,Thika Road")
            self.bill_txt.insert(END, "\nContact:0796939191")
            self.bill_txt.insert(END, "\n=======================")

        def genbill():
            cust_nm.set(self.customer_name_entry.get())
            self.bill_txt.insert(END, f"\nCustomer Name: {cust_nm.get()}")
            self.total_btn.config(state="normal")

        def reset():
            soda.set("")
            water.set("")
            juice.set("")
            wine.set("")
            coffee.set("")
            milk.set("")
            blacktea.set("")
            matooke.set("")
            rice.set("")
            posho.set("")
            meat.set("")
            beans.set("")
            vegetables.set("")

            total_list.clear()
            self.grid_total = 0

            self.tax_btn.config(state="disabled")
            self.total_btn.config(state="disabled")

            self.bill_txt.delete(1.0, END)
            default_bill()

        def total():
            self.grid_total = 0
            total_list.clear()
            self.bill_txt.delete(1.0, END)
            default_bill()

            items_selected = False

            try:
                soda_qty = int(self.soda_ent.get().strip()) if self.soda_ent.get().strip() else 0
                water_qty = int(self.water_ent.get().strip()) if self.water_ent.get().strip() else 0
                juice_qty = int(self.juice_ent.get().strip()) if self.juice_ent.get().strip() else 0
                wine_qty = int(self.wine_ent.get().strip()) if self.wine_ent.get().strip() else 0
                coffee_qty = int(self.coffee_ent.get().strip()) if self.coffee_ent.get().strip() else 0
                rice_qty = int(self.rice_ent.get().strip()) if self.rice_ent.get().strip() else 0
                posho_qty = int(self.posho_ent.get().strip()) if self.posho_ent.get().strip() else 0
                meat_qty = int(self.meat_ent.get().strip()) if self.meat_ent.get().strip() else 0
                beans_qty = int(self.beans_ent.get().strip()) if self.beans_ent.get().strip() else 0
                vegetables_qty = int(self.vegetables_ent.get().strip()) if self.vegetables_ent.get().strip() else 0


                item_prices = {
                    "Soda": 60,
                    "Water": 50,
                    "Juice": 40,
                    "Wine": 200,
                    "Coffee": 30,
                    "Rice": 80,
                    "Posho": 60,
                    "Meat": 200,
                    "Beans": 35,
                    "Vegetables": 45
                }


                item_quantities = {
                    "Soda": soda_qty,
                    "Water": water_qty,
                    "Juice": juice_qty,
                    "Wine": wine_qty,
                    "Coffee": coffee_qty,
                    "Rice": rice_qty,
                    "Posho": posho_qty,
                    "Meat": meat_qty,
                    "Beans": beans_qty,
                    "Vegetables": vegetables_qty
                }


                for item, qty in item_quantities.items():
                    if qty > 0:
                        cost = qty * item_prices[item]
                        total_list.append(cost)
                        self.bill_txt.insert(END, f"\n{item}: kes{cost}\n")
                        items_selected = True


                total = sum(total_list)
                tax = total * 0.02
                grand_total = total + tax

                if items_selected:
                    self.bill_txt.insert(END, "\n================================")
                    self.bill_txt.insert(END, f"\nSubtotal: ksh{total}")
                    self.bill_txt.insert(END, f"\nTax:ksh {tax:.2f}")
                    self.bill_txt.insert(END, f"\nGrand Total:ksh {grand_total:.2f}")
                    self.bill_txt.insert(END, "\n================================")


                    self.tax_btn_entry.delete(0, END)
                    self.tax_btn_entry.insert(0, f"ksh{tax:.2f}")
                    self.total_btn_entry.delete(0, END)
                    self.total_btn_entry.insert(0, f"ksh{grand_total:.2f}")

                else:
                    self.bill_txt.insert(END, "\nNo items selected.")
                    self.tax_btn_entry.delete(0, END)
                    self.total_btn_entry.delete(0, END)

            except ValueError as e:
                print(f"Error: {e}")

        def qExit():
            win.destroy()

        self.calc_frame = LabelFrame(self.win, text="calculator", font=("Arial", 14), background="lightgrey", bd=8,  relief=GROOVE)
        self.calc_frame.place(x=1040, y=110, width=280, height=400)

        self.num_ent = Entry(self.calc_frame, bd=4, background="lightgrey", textvariable=calc_var, font=("Arial", 15),width=20, justify=LEFT)
        self.num_ent.grid(row=0, column=0, columnspan=4)

        self.display = tk.Entry(self.calc_frame, bd=4, background="yellow", textvariable=calc_var,font=("Arial", 15), width=20, justify=tk.LEFT)
        self.display.grid(row=0, column=0, columnspan=4)

        def press_btn(event):
            text = event.widget.cget("text")
            if text == "=":
                if calc_var.get().isdigit():
                    value = int(calc_var.get())
                else:
                    try:
                        value = eval(self.num_ent.get())
                    except:
                        print("error")
                calc_var.set(value)
                self.num_ent.update()
            elif text == "C":
                calc_var.set("")
                self.num_ent.delete(0, END)
            else:
                calc_var.set(calc_var.get() + text)
                self.num_ent.update()

        self.btn7 = Button(self.calc_frame, bg="lightgrey", text="7", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn7.grid(row=1, column=0)
        self.btn7.bind("<Button-1>", press_btn)
        self.btn8 = Button(self.calc_frame, bg="lightgrey", text="8", bd=15, width=2, height=1, font=("Arial", 15))
        self.btn8.grid(row=1, column=1)
        self.btn8.bind("<Button-1>", press_btn)
        self.btn9 = Button(self.calc_frame, bg="lightgrey", text="9", bd=15, width=2, height=1, font=("Arial", 15))
        self.btn9.grid(row=1, column=2)
        self.btn9.bind("<Button-1>", press_btn)
        self.btnadd = Button(self.calc_frame, bg="lightgrey", text="+", bd=15, width=2, height=1, font=('Arial', 15))
        self.btnadd.grid(row=1, column=3)
        self.btnadd.bind("<Button-1>", press_btn)
        self.btn4 = Button(self.calc_frame, bg="lightgrey", text="4", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn4.grid(row=2, column=0)
        self.btn4.bind("<Button-1>", press_btn)
        self.btn5 = Button(self.calc_frame, bg="lightgrey", text="5", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn5.grid(row=2, column=1)
        self.btn5.bind("<Button-1>", press_btn)
        self.btn6 = Button(self.calc_frame, bg="lightgrey", text="6", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn6.grid(row=2, column=2)
        self.btn6.bind("<Button-1>", press_btn)
        self.btnsubs = Button(self.calc_frame, bg="lightgrey", text="-", bd=15, width=2, height=1, font=('Arial', 15))
        self.btnsubs.grid(row=2, column=3)
        self.btnsubs.bind("<Button-1>", press_btn)
        self.btn1 = Button(self.calc_frame, bg="lightgrey", text="1", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn1.grid(row=3, column=0)
        self.btn1.bind("<Button-1>", press_btn)
        self.btn2 = Button(self.calc_frame, bg="lightgrey", text="2", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn2.grid(row=3, column=1)
        self.btn2.bind("<Button-1>", press_btn)
        self.btn3 = Button(self.calc_frame, bg="lightgrey", text="3", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn3.grid(row=3, column=2)
        self.btn3.bind("<Button-1>", press_btn)
        self.btnmult = Button(self.calc_frame, bg="lightgrey", text="*", bd=15, width=2, height=1, font=('Arial', 15))
        self.btnmult.grid(row=3, column=3)
        self.btnmult.bind("<Button-1>", press_btn)
        self.btn0 = Button(self.calc_frame, bg="lightgrey", text="0", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn0.grid(row=4, column=0)
        self.btn0.bind("<Button-1>", press_btn)
        self.btnpoint = Button(self.calc_frame, bg="lightgrey", text=".", bd=15, width=2, height=1, font=('Arial', 15))
        self.btnpoint.grid(row=4, column=1)
        self.btnpoint.bind("<Button-1>", press_btn)
        self.btn_clear = Button(self.calc_frame, bg="lightgrey", text="C", bd=15, width=2, height=1, font=('Arial', 15))
        self.btn_clear.grid(row=4, column=2)
        self.btn_clear.bind("<Button-1>", press_btn)
        self.btndiv = Button(self.calc_frame, bg="lightgrey", text="/", bd=15, width=2, height=1, font=('Arial', 15))
        self.btndiv.grid(row=4, column=3)
        self.btndiv.bind("<Button-1>", press_btn)
        self.btnequals = Button(self.calc_frame, bg="lightgrey", text="=", bd=15, width=2, height=1, font=('Arial', 15))
        self.btnequals.grid(row=5, column=0, columnspan=4, sticky="nsew")
        self.btnequals.bind("<Button-1>", press_btn)

        self.bill_frame = LabelFrame(self.win, text="Receipt", font=("Arial", 18), background="lightgrey", bd=8,     relief=GROOVE)
        self.bill_frame.place(x=800, y=90, width=240, height=400)
        self.y_scroll = Scrollbar(self.bill_frame, orient="vertical")
        self.bill_txt = Text(self.bill_frame, bg="white", yscrollcommand=self.y_scroll.set)
        self.y_scroll.config(command=self.bill_txt.yview)
        self.y_scroll.pack(side=RIGHT, fill=Y)
        self.bill_txt.pack(fill=BOTH, expand=TRUE)

        default_bill()

        self.tax_btn =Button(self.win, text="Tax", font=("Arial", 13), fg="purple", bd=1, relief=GROOVE)
        self.tax_btn.place(x=800, y=500, width=120, height=30)
        self.tax_btn_entry = Entry(self.win, bd=5,bg='aqua', font=('Arial', 15))
        self.tax_btn_entry.place(x=900, y=500, width=350, height=30)
        self.total_btn = Button(self.win, text="Total", font=("Arial", 15), background="purple", bd=1, relief=GROOVE,command=total)
        self.total_btn.place(x=800, y=535, width=120, height=30)
        self.total_btn_entry = Entry(self.win, bd=5,bg='aqua', font=('Arial', 15))
        self.total_btn_entry.place(x=900, y=535, width=350, height=30)
        self.printreceipt_btn = Button(self.win, text="Print receipt", font=("Arial", 15), background="purple",  bd=1, relief=GROOVE,command=genbill)
        self.printreceipt_btn.place(x=800, y=575, width=120, height=30)
        self.reset_btn = Button(self.win, text="Reset", font=("Arial", 15), background="purple", bd=1, relief=GROOVE,command=reset)
        self.reset_btn.place(x=920, y=575, width=90, height=30)
        self.exit_btn = Button(self.win, text="Exit", font=("Arial", 15), background="purple", bd=1, relief=GROOVE,command=qExit)
        self.exit_btn.place(x=1000, y=575, width=90, height=30,)

if __name__== "__main__":
    main()

