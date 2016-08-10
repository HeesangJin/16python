__author__ = 'jinheesang'
from tkinter import *

#===== DATA
user_db = []
message = {'clear': "",'add_ok': "성공적으로 추가하였습니다", "del_ok":"성공적으로 삭제하였습니다",\
           "load_ok": "성공적으로 파일을 읽었습니다", "save_ok": "성공적으로 저장하였습니다",\
           "edit_ok": "성공적으로 수정되었습니다"}

#===== DATA VALIDATE
def find_in(i, value): #0:index , 1:name, 2:grade
    for user_data in user_db:
        if str(user_data[i]) == value.strip():
            return True
            break
    return False

def is_empty(string): #0:index , 1:name, 2:grade
    if not string:
        return True
    return False

def is_digit(str):
    try:
        tmp = float(str)
        return True
    except ValueError:
        return False

#===== HELPER
def show_txt():
    output_txt.delete(0.0,END)
    for user_data in user_db:
        string = "{0:^5} {1:<20} {2:<10}\n".format(user_data[0],user_data[1],user_data[2])
        output_txt.insert(END,string)

def show_alert(text):
    output_alert.delete(0.0,END)
    output_alert.insert(END,text)

def add_db(data):
    global user_db
    user_db.append(data)



#===== BUTTON FUNCTION ======
def add_data():
    name = entry_name.get()
    grade = entry_grade.get()
    if find_in(1,name):
        show_alert("[추가 실패]동일한 이름이 이미 존재합니다")
        return
    elif is_empty(name) or is_empty(grade):
        show_alert("[추가 실패]입력하지 않은 항목이 있습니다")
        return
    elif not is_digit(grade):
        show_alert("[추가 실패]점수를 올바르게 입력해주세요")
        return

    user_data = [len(user_db)+1, name.strip(), grade.strip()] #make user data
    add_db(user_data)
    entry_name.delete(0,END)
    entry_grade.delete(0,END)
    show_txt()
    show_alert(message['add_ok'])

def delete_data():
    idx = entry_idx.get()
    if not find_in(0,idx):
        show_alert("[삭제 실패]존재하지 않는 번호입니다")
        return
    for user_data in user_db:
        if str(user_data[0]) == idx:
            user_db.remove(user_data)
            show_alert(message['del_ok'])
            break
    show_txt()
    entry_idx.delete(0,END)
    show_alert(message['del_ok'])

def sort_db(i,option=False):
    global user_db
    if i!=2:
        user_db= sorted(user_db, key=lambda data: data[i])
    else:
        user_db= sorted(user_db, key=lambda data: int(data[i]), reverse=option)
    show_txt()
    show_alert(message['clear'])

def file_save():
    file_name = entry_fsave.get()
    if is_empty(file_name):
        show_alert("[저장 실패]파일 이름을 입력해주세요")
        return
    elif not user_db:
        show_alert("[저장 실패]저장할 내용이 없습니다")
        return
    f = open(file_name, 'w')
    for user_data in user_db:
        string = "{0} {1} {2}\n".format(user_data[0],user_data[1],user_data[2])
        f.write(string)
    f.close
    show_alert(message['save_ok'])
    output_alert.insert(END," (파일 이름:"+file_name+")")
    entry_fsave.delete(0,END)

def file_load():
    global user_db
    file_name = entry_fload.get()
    if is_empty(file_name):
        show_alert("[읽기 실패]파일 이름을 입력해주세요")
        return
    user_db=[]
    try:
        f = open(file_name, 'r')
    except IOError:
        show_alert("[읽기 실패]파일이 존재 하지 않습니다")
        return

    while True:
        user_data = f.readline()
        if not user_data: break
        user_db.append(user_data.split())

    f.close
    show_txt()
    show_alert(message['load_ok'])
    output_alert.insert(END," (파일 이름:"+file_name+")")
    entry_fload.delete(0,END)

def update_data(i):
    entry = entry_edit_grade if i==2 else entry_edit_name # 2:grade or 1:name
    entry_idx = entry_edit_grade_idx if i==2 else entry_edit_name_idx # 2:grade or 1:name

    for user_data in user_db:
        if user_data[0] == entry_idx.get():
            user_data[i] = entry.get()
            show_alert(message['edit_ok'])
            break
    show_txt()
    entry.delete(0,END)
    entry_idx.delete(0,END)
#===== //BUTTON FUNCTION ======

#================= UI =================


window =Tk()
window.title("My Coding Club Glossary")

#===== ADD DATA
Label(window, text="이름: ").grid(row=0, column=0, sticky=W)
entry_name = Entry(window, width=20, bg="light green")
entry_name.grid(row=0, column=2, sticky=W)

Label(window, text="점수: ").grid(row=0, column=3, sticky=W)
entry_grade = Entry(window, width=7, bg="light green")
entry_grade.grid(row=0, column=4, sticky=W)

button1 = Button(window, text="추가", width=5,command=add_data).grid(row=0, column=5)


#===== DELETE DATA
Label(window, text="번호: ").grid(row=1, column=3, sticky=W)
entry_idx = Entry(window, width=5, bg="light green")
entry_idx.grid(row=1, column=4, sticky=W)
button1 = Button(window, text="삭제", width=5,command=delete_data).grid(row=1, column=5)


#===== FILE SAVE & LOAD
Label(window, text="파일이름: ").grid(row=4, column=3, sticky=W)
entry_fsave = Entry(window, width=20, bg="light blue")
entry_fsave.grid(row=4, column=4, sticky=W)
button1 = Button(window, text="저장", width=5,command=file_save).grid(row=4, column=5)

Label(window, text="파일이름: ").grid(row=5, column=3, sticky=W)
entry_fload = Entry(window, width=20, bg="light blue")
entry_fload.grid(row=5, column=4, sticky=W)
button1 = Button(window, text="열기", width=5,command=file_load).grid(row=5, column=5,sticky=W)

#=====Sort
button1 = Button(window, text="번호순", width=5,command= lambda: sort_db(0) ).grid(row=6, column=2,sticky=W)
button1 = Button(window, text="이름순", width=5,command= lambda: sort_db(1) ).grid(row=6, column=3,sticky=W)
button1 = Button(window, text="점수내림차순", width=15,command= lambda: sort_db(2,True) ).grid(row=6, column=4,sticky=W)
button1 = Button(window, text="점수오름차순", width=15,command= lambda: sort_db(2,False) ).grid(row=6, column=5,sticky=W)

#=====EDIT(NAME)
Label(window, text="번호: ").grid(row=2, column=0, sticky=W)
entry_edit_name_idx = Entry(window, width=5, bg="gray")
entry_edit_name_idx.grid(row=2, column=2, sticky=W)

Label(window, text="이름: ").grid(row=2, column=3, sticky=W)
entry_edit_name = Entry(window, width=20, bg="gray")
entry_edit_name.grid(row=2, column=4, sticky=W)

button1 = Button(window, text="수정", width=5,command= lambda: update_data(1)).grid(row=2, column=5)

#=====EDIT(GRADE)
Label(window, text="번호: ").grid(row=3, column=0, sticky=W)
entry_edit_grade_idx = Entry(window, width=5, bg="gray")
entry_edit_grade_idx.grid(row=3, column=2, sticky=W)

Label(window, text="점수: ").grid(row=3, column=3, sticky=W)
entry_edit_grade = Entry(window, width=7, bg="gray")
entry_edit_grade.grid(row=3, column=4, sticky=W)

button1 = Button(window, text="수정", width=5,command= lambda: update_data(2)).grid(row=3, column=5)


#===== TEXT AREA
output_txt = Text(window, width=75, height=10, wrap=WORD, background="light yellow")
output_txt.grid(row=7,column=0,columnspan=6)
output_alert = Text(window, width=75, height=1, wrap=WORD, background="light pink")
output_alert.grid(row=8,column=0,columnspan=6)
#================= //UI =================





window.mainloop()