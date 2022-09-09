from tkinter import *
from tkinter.font import *
from Database import Database
import os
from subprocess import call
from tkinter import messagebox
import re

# region Building Screen & Database
root = Tk()
root.title('Menu')
padx = 2
pady = 2
my_font = Font(family='calibri', size=17)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')
root.state('zoomed')
root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=3)
root.grid_rowconfigure(0, weight=1)
db = None
if os.path.isfile('restaurant.db') == False:
    db = Database('restaurant.db')
    db.insert(1, 'چلو گوشت', 110000, True)
    db.insert(2, 'چلو مرغ', 70000, True)
    db.insert(3, 'کباب کوبیده', 85000, True)
    db.insert(4, 'فسنجون', 65000, True)
    db.insert(5, 'باقالی پلو با گردن', 120000, True)
    db.insert(6, 'جوجه کباب', 75000, True)
    db.insert(7, 'قورمه سبزی', 60000, True)
    db.insert(8, 'نوشابه قوطی', 7000, False)
    db.insert(9, 'نوشابه خانواده', 15000, False)
    db.insert(10, 'دوغ', 6000, False)
    db.insert(11, 'آب معدنی', 5000, False)
else:
    db = Database('restaurant.db')


# endregion

# region Reciept frame
def load_reciepts(reciept_id):
    list_box.delete(0, END)
    reciepts = db.get_recieptLoad(reciept_id)
    for reciept in reciepts:
        list_box.insert(0, '%s   -   %s     %s      %s' % (reciept[0], reciept[2], reciept[3], reciept[4]))


reciept_frame = LabelFrame(root, text='صورتحساب', bg='blue', font=my_font, padx=padx, pady=pady)
reciept_frame.grid(row=0, column=0, sticky='nsew', pady=pady, padx=padx)

reciept_frame.grid_rowconfigure(1, weight=1)
reciept_frame.grid_columnconfigure(0, weight=1)

entry_order_num = Entry(reciept_frame, width=10, font=my_font, justify='center')
entry_order_num.grid(row=0, column=0, padx=padx, pady=pady)


def entry_pressKey(key):
    try:
        reciept_id = int(entry_order_num.get())
        load_reciepts(reciept_id)
    except:
        list_box.delete(0, END)


entry_order_num.bind('<KeyRelease>', entry_pressKey)
max_reciept_num = db.get_max_reciept()
if max_reciept_num[0][0] == None:
    max_reciept_num = 0
else:
    max_reciept_num = int(max_reciept_num[0][0])
max_reciept_num += 1
entry_order_num.insert(0, max_reciept_num)

list_box = Listbox(reciept_frame, font=my_font)
list_box.grid(row=1, column=0, sticky='nsew', padx=padx, pady=pady)
list_box.configure(justify=RIGHT)

listbox_bottuns_frame = LabelFrame(reciept_frame)
listbox_bottuns_frame.grid(row=2, column=0, sticky='nsew', padx=padx, pady=pady)


# ==== buttons ====

def delete_reciept_item():
    reciept_id = int(entry_order_num.get())
    menu_item = list_box.get(ACTIVE)
    menu_item_name = menu_item.split('   -')[0]
    result = db.get_menuName_item(menu_item_name)
    menu_item_id = int(result[0][0])
    db.delete_rexiept(reciept_id, menu_item_id)
    load_reciepts(reciept_id)


button_delete = Button(listbox_bottuns_frame, text='حذف', font=my_font, command=lambda: delete_reciept_item())
button_delete.grid(row=0, column=0, sticky='nsew')


def new_reciept():
    list_box.delete(0, END)
    max_reciept_num = db.get_max_reciept()
    if max_reciept_num[0][0] == 0:
        max_reciept_num = 0
    else:
        max_reciept_num = int(max_reciept_num[0][0])
    max_reciept_num += 1
    entry_order_num.delete(0, END)
    entry_order_num.insert(0, max_reciept_num)


button_new = Button(listbox_bottuns_frame, text='فاکتور جدید', font=my_font, command=new_reciept)
button_new.grid(row=0, column=1, sticky='nsew')


def increase_item():
    reciept_id = int(entry_order_num.get())
    menu_item = list_box.get(ACTIVE)
    menu_item_name = menu_item.split('   -')[0]
    result = db.get_menuName_item(menu_item_name)
    menu_item_id = int(result[0][0])
    db.increase_count(reciept_id, menu_item_id)
    load_reciepts(reciept_id)


button_add = Button(listbox_bottuns_frame, text='+', font=my_font, command=increase_item)


def decrease_item():
    reciept_id = int(entry_order_num.get())
    menu_item = list_box.get(ACTIVE)
    menu_item_name = menu_item.split('   -')[0]
    result = db.get_menuName_item(menu_item_name)
    menu_item_id = int(result[0][0])
    db.decrease_count(reciept_id, menu_item_id)
    load_reciepts(reciept_id)


button_add.grid(row=0, column=2, sticky='nsew')

button_minus = Button(listbox_bottuns_frame, text='-', font=my_font,command=decrease_item)
button_minus.grid(row=0, column=3, sticky='nsew')

listbox_bottuns_frame.grid_columnconfigure(0, weight=1)
listbox_bottuns_frame.grid_columnconfigure(1, weight=1)
listbox_bottuns_frame.grid_columnconfigure(2, weight=1)
listbox_bottuns_frame.grid_columnconfigure(3, weight=1)
# endregion

# region Menu frame
menu_frame = LabelFrame(root, text='منو نوشیدنی و غذا', bg='green', font=my_font, padx=padx, pady=pady)
menu_frame.grid(row=0, column=1, sticky='nsew', padx=padx, pady=pady)
menu_frame.grid_columnconfigure(0, weight=1)
menu_frame.grid_columnconfigure(1, weight=1)
menu_frame.grid_rowconfigure(0, weight=1)
# ==== drink frame ===========================================
drink_frame = LabelFrame(menu_frame, text='نوشیدنی', font=my_font)
drink_frame.grid(row=0, column=0, sticky='nsew', padx=padx, pady=pady)
drink_frame.grid_columnconfigure(0, weight=1)
drink_frame.grid_rowconfigure(0, weight=1)
listbox_drink = Listbox(drink_frame, font=my_font, exportselection=False)
listbox_drink.grid(sticky='nsew', padx=padx, pady=pady)
listbox_drink.configure(justify=RIGHT)
drinks = db.get_menu_items(False)
for drink in drinks:
    listbox_drink.insert(END, drink[1])


def add_drink(event):
    drink_item = db.get_menuName_item(listbox_drink.get(ACTIVE))
    menu_id = drink_item[0][0]
    price = drink_item[0][2]
    reciept_id = int(entry_order_num.get())
    result = db.get_reciept_by_recieptid_muneid(reciept_id, menu_id)
    if len(result) == 0:
        db.reciept_insert(reciept_id, menu_id, 1, price)
    else:
        db.increase_count(reciept_id, menu_id)

    load_reciepts(reciept_id)


listbox_drink.bind('<Double-Button>', add_drink)
# ==== food frame =============================================
food_frame = LabelFrame(menu_frame, text='غذا', font=my_font)
food_frame.grid(row=0, column=1, sticky='nsew', padx=padx, pady=pady)
food_frame.grid_columnconfigure(0, weight=1)
food_frame.grid_rowconfigure(0, weight=1)
listbox_food = Listbox(food_frame, font=my_font, exportselection=False)
listbox_food.grid(sticky='nsew', padx=padx, pady=pady)
listbox_food.configure(justify=RIGHT)
foods = db.get_menu_items(True)
for food in foods:
    listbox_food.insert(END, food[1])


def add_food(event):
    food_item = db.get_menuName_item(listbox_food.get(ACTIVE))
    menu_id = food_item[0][0]
    price = food_item[0][2]
    reciept_id = int(entry_order_num.get())
    result = db.get_reciept_by_recieptid_muneid(reciept_id, menu_id)
    if len(result) == 0:
        db.reciept_insert(reciept_id, menu_id, 1, price)
    else:
        db.increase_count(reciept_id, menu_id)

    load_reciepts(reciept_id)


listbox_food.bind('<Double-Button>', add_food)

# endregion

# region Buttons frame
buttons_frame = LabelFrame(root, background='white', font=my_font, padx=padx, pady=pady)
buttons_frame.grid(row=1, column=1, padx=padx, pady=pady)


def exit_prog():
    message = messagebox.askquestion('خروج', 'آیا میخواهید خارج شوید؟', icon='warning')
    if message == 'yes':
        root.destroy()


bottun_exis = Button(buttons_frame, text='خروج', font=my_font, command=exit_prog)


def open_calc():
    call(['calc.exe'])


bottun_cal = Button(buttons_frame, text='محاسبه', font=my_font, command=open_calc)


def open_web():
    import webbrowser
    webbrowser.open('https://queenofvictory.com')


bottun_web = Button(buttons_frame, text='سایت ما', font=my_font, command=open_web)

bottun_exis.grid(row=0, column=0)
bottun_cal.grid(row=0, column=1)
bottun_web.grid(row=0, column=2)
# endregion
root.protocol('WM_DELETE_WINDOW', exit_prog)
root.mainloop()
