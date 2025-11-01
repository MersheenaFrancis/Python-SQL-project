import  mysql.connector
from datetime import date,datetime
from tabulate import tabulate

mysql=mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Rowdy@26",
    database = "personal_expense_tracker"
)

# Add Income
def income(n):
    for i in range(0,n):
        D = int(input("Enter 1 for today's Date / 0 for giving date manually :"))
        if D == 1:
            user_date = date.today()
        else:
            user = input("Enter the date in '(yyyy-MM-DD)':")
            user_date = datetime.strptime(user,"%Y-%m-%d").date()
        source = input("Enter the  source of income :")
        amount = int(input("Enter the Amount of income :"))
        desc = input("Enter the description :")
        cursor = mysql.cursor()
        query = "Insert into income (date_on,category,amount,descriptions) values(%s,%s,%s,%s);"
        data = (user_date,source,amount,desc)
        cursor.execute(query,data)
        mysql.commit()
        print("\n")

# Add Expense
def expense(n):
    for i in range(0,n):
        D=int(input("Enter 1 for today's Date / 0 for giving date manually :"))
        if D==1:
            user_date = date.today()
        else:
            user = input("Enter the date in '(YYYY-MM-DD)':")
            user_date = datetime.strptime(user,"%Y-%m-%d").date()
        category = input("Enter the Category of the Expense you do :")
        amount = int(input("Enter the amount you spend :"))
        payment_mode = input("Enter the payment mode :")
        desc = input("Enter the description :")
        cursor = mysql.cursor()
        query = "insert into expenses (date_on,category,amount,payment_mode,descriptions)values(%s,%s,%s,%s,%s);"
        data = (user_date,category,amount,payment_mode,desc)
        cursor.execute(query,data)
        mysql.commit()
        print("\n")

# View Data
def view(tab):
    cursor = mysql.cursor()
    query = f"select * from {tab} ;"
    cursor.execute(query)
    result = cursor.fetchall()
    col = [i[0] for i in cursor.description]
    datas = tabulate(result,headers=col,tablefmt="fancy_grid")
    print(datas)

#Summary
def summary(tab):
    cursor = mysql.cursor()
    query = "select IFNULL(sum(amount),0)from income ;"
    cursor.execute(query)
    total_income = cursor.fetchone()[0]

    query = "select IFNULL(sum(amount),0)from expenses;"
    cursor.execute(query)
    total_expense = cursor.fetchone()[0]

    net_balance = total_income - total_expense

    # Over all Summary
    print(" "*50+"Total Income   :",total_income)
    print(" "*50+"Total Expense  :",total_expense)
    print(" "*50+"Net Balance    :",net_balance)

    print("\n")

    print(" "*40+"Category / month based total amount ")



    print("Category Based : \n")
    # Category Based total amount

    query = f"select category , sum(amount) total_amount from {tab} group by category;"
    cursor.execute(query)
    result = cursor.fetchall()
    col = [i[0] for i in cursor.description]
    data = tabulate(result,headers=col,tablefmt="fancy_grid")
    print(data)


    print("Month  based : \n")
    # Month Based total amount

    query = f"select DATE_FORMAT(date_on,'%M') as Month ,sum(amount) total_amount from {tab} group by month;"
    cursor.execute(query)
    result = cursor.fetchall()
    col = [i[0] for i in cursor.description]
    data = tabulate(result,headers=col,tablefmt="fancy_grid")
    print(data)


#Search
def search(tab):
    choice = int(input("1) date_on , 2) category 3)amount 4)payment_mode : "))
    col_name = {1:"date_on",2:"category",3:"amount",4:"payment_mode"}
    search = col_name[choice]
    cursor= mysql.cursor()
    if choice == 1:
        value = input("Enter the Date to be find in format (YYYY-MM-DD) :")
        query = f"select * from {tab} where {search} = '{value}';"
    elif choice == 2:
        value = input("Enter the Category to be searched :")
        query = f"select * from {tab} where {search} = '{value}';"
    elif choice == 3:
        opt = int(input("1)greater than 2)lesser than 3)between 4)equal :"))
        match opt:
            case 1:
                value = int(input("Enter the value to be searched :"))
                query = f"select * from {tab} where {search} > {value};"
            case 2:
                value = int(input("Enter the value to be searched :"))
                query = f"select * from {tab} where {search} < {value}"
            case 3 :
                value1,value2 = map(int , input("Enter the values  in range (start and end) :").split())
                query = f"select * from {tab} where {search} between {value1} and {value2};"
            case _:
                value = int(input("Enter the value to be searched  :"))
                query = f"select * from {tab} where {search} = {value};"
    elif choice == 4:
        if n == 1:
            print(f"{search} column is not present in {tab}")
        else:
            value = input("Enter the value to be searched :")
            query = f"select * from {tab} where {search} = '{value}';"

    else:
        print("Invalid Choice")
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        colums = [i[0] for i in cursor.description]
        data = tabulate(result,headers=colums,tablefmt="fancy_grid")
        print(data)
    except Exception as e:
        print(f"No such column present in {tab}")

#Update Records
def update(tab):
    col_dict = {1:"date_on",2:"category",3:"amount",4:"payment_mode"}
    n = int(input("Enter the column to update : 1)date / 2)category 3)amount 4)payment_mode :"))
    cursor = mysql.cursor()
    try:
       col_name = col_dict[n]
       if choice == 1 and n == 4:
           print(f"No such column in {tab} ")
       else:
           id = int(input("Enter the id :"))
           if n==1:
               new_value = input("Enter value in (YYYY-MM-DD)format :")
               date_on =datetime.strptime(new_value,"%Y-%m-%d").date()
               query = f"update {tab} set {col_name} = '{date_on}' where id = {id}"
           elif n==3:
               new_value = int(input("Enter the value :"))
               query = f"update {tab} set {col_name} = {new_value} where id = {id};"
           else:
               new_value = input("Enter the new value : ")
               query = f"update {tab} set {col_name} = '{new_value}' where id = {id};"
           cursor.execute(query)
           mysql.commit()
    except Exception  as e:
        print(f"Not updated")
    else:
        print("Successfully updated")

#Delete Records
def delete(tab):
    cursor = mysql.cursor()
    id = int(input("Enter the id :"))

    try:
        query = f"delete from {tab} where id = '{id}';"
        cursor.execute(query)
        mysql.commit()
    except  Exception   :
        print(f"No such column present in {tab}")
    else:
        print("Successfully Deleted")

#Main Program

n=1
while True:
    print(" "*50+"Personal Expense Tracker💸💰")
    print(" "*55+"Choose Your Plan ")
    print(" 1)Add Income \n 2) Add Expense \n 3) View All Records \n 4) view Summary \n 5) Search Records \n 6) Update Record \n 7) Delete Record \n 8) Exit  ")
    choice = int(input("Enter your choice : "))
    n = int(input("Enter the type of data to view (1)income / (2)expenses):"))
    dicts = {1: "income", 2: "expenses"}
    tab = dicts[n]
    match choice:
        case 1:
            print("Add Income ")
            n = int(input("Enter no of incomes : "))
            income(n)
            pass
        case 2:
            print("Add Expense ")
            n=int(input("Enter no of expenses :"))
            expense(n)
        case 3:
            print("View All Records")
            view(tab)
        case 4:
            print("View Summary")
            summary(tab)
        case 5:
            print("Search Records")
            search(tab)
        case 6:
            print("Update Records")
            update(tab)
        case 7:
            print("Delete Records")
            delete(tab)
        case 8:
            exit()
        case _:
            print("You have entered the invalid Option")


    n =int(input("Press 1 to Continue or 0 to Exit :"))
    print("\n")
    if n==0:
        break
    else:
        print(" "*40+"User using again the personal Expense Tracker ")
