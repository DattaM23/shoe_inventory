from tabulate import tabulate

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost                #defines class of Shoe. Will be used to create Shoe objects when functions are called 
        self.quantity = quantity

    def get_cost(self):
        return self.cost
        
    def get_quantity(self):
        quantity = self.quantity[:-1]
        return quantity

    def __str__(self):          
        print(f'''                      
__________________________________________________________________

Shoe: {self.product}

Product ID: {self.code}
Country produced in: {self.country}
Product cost: {self.cost}
Quantity: {self.quantity}
__________________________________________________________________
''')

#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []
shoes_data = []
#==========Functions outside the class==============
def read_shoes_data():
    shoes_data.clear()                  #this function will be called at the start of every other function to get the most up to date data from the text file. 
    shoe_list.clear()                   #to avoid adding to the above lists and creating duplicates, will clear the list and then repopulate with the up to date data from text file. 
    try:
        with open('inventory.txt','r+') as a:
            for line in a:
                shoes_data.append(line)         #reads the file and adds it to the shoes_data list. This will then be split up to get individual aspects of the shoe.
        for shoe in shoes_data[1:]:
            shoe_split = shoe.split(',')
            new_shoe = Shoe(shoe_split[0], shoe_split[1], shoe_split[2], shoe_split[3], int(shoe_split[4]))
            shoe_list.append(new_shoe)      #once split, each aspect can be used as an argument for creating an object in the Shoe class. This object will be added to the shoe_list list. 
        a.close()
    except FileNotFoundError:
        print('\nFile is not found\n')      #try, exception used in case there is no file. 


def capture_shoes():
    shoe_country = input('Which country is this shoe is produced in?: ')
    shoe_code = input('What is the product code?: ')
    shoe_product = input('What is the name of the shoe?: ')
    while True:
        try:                #the last two inputs will need to be converted into integers later so needs to be a number to avoid errors. Therefore try, except used to get a number.
            shoe_cost = int(input('How much will this shoe cost?: '))
            break
        except Exception:
            print('\nInvalid input. Please enter a number.\n')
    while True:
        try:
            shoe_quantity = int(input('How many of these shoes do you want to add to the inventory: '))
            break
        except Exception:
            print('\nInvalid input. Please enter a number.\n')
    with open('inventory.txt','a+') as c:        #will open the inventory file and add this line to it in the same format as the others. Will open a new file if not present.
        c.write(f'\n{shoe_country},{shoe_code},{shoe_product},{shoe_cost},{shoe_quantity}')
    c.close()
    print(f'\n{shoe_product} has been added to the inventory!\n')


def view_all():
    read_shoes_data()
    shoe_table = []     #this function will iterate through shoe_list list which has been populated by the read_shoes_data function. 
    for n in shoe_list:   #will add an item into the list which will contain the details of each shoe. The list will then be made into a table to present on the screen
        shoe_table.append([n.country,n.code,n.product,n.cost,n.quantity])
    print(tabulate(shoe_table, headers = ['Country','Code','Product','Cost','Quantity']))

def re_stock():
    read_shoes_data()
    shoe_quantities = {}            #will create dictionary which will be populated with quantity of shoe as key and shoe name as the value
    for n in shoe_list:
        shoe_quantities[int(n.quantity)] = n.product        #min function used to find lowest key (quantity) and the corresponding value (shoe name)
    print(f'\nThe shoe that is the lowest in stock is: {shoe_quantities[min(shoe_quantities)]}. There are only {min(shoe_quantities)} in stock.\n')
    user_restock = 0        
    while user_restock != 1 and user_restock != 2:
        try:            #uses try, except function to ask if user wants to restock item. Invalid inputs will make the program ask the question again
            user_restock = int(input('Do you want to re-stock this item? Type 1 for yes or 2 for no: '))
            if user_restock != 1 and user_restock != 2:
                print('Invalid input. Please try again')
        except Exception:
            print('Invalid input. Please try again')
    should_continue = True
    while user_restock == 1 and should_continue == True:        #uses while loop and try,except to get a number for how many they want to add to the stock
        try:
            restock_number = int(input('\nHow many of these shoes would you like to add to stock?: '))
            new_stock_number = str(min(shoe_quantities) + restock_number)
            for n in range(len(shoes_data)):
                n_split = shoes_data[n].split(',')      #uses the shoes_data list which contain the details but not in object format. Changes the 4th index to the new stock after calculating it.
                if n_split[2] == shoe_quantities[min(shoe_quantities)]:
                    shoes_data[n] = f'{n_split[0]},{n_split[1]},{n_split[2]},{n_split[3]},{new_stock_number}\n'
            new_file_text = ''.join(shoes_data)
            with open('inventory.txt','w+') as b:  #will overwrite the inventory file with the new list containing the changed data 
                b.write(new_file_text)
            b.close()
            print('\nInventory has been updated with new stock!\n')
            should_continue = False
        except Exception:      
            print('\nInvalid input. Please try again')
    if user_restock == 2:
        pass
    

def search_shoe():
    read_shoes_data()
    shoe_codes = []         
    user_choice = input('Enter the code of the shoe you want: ').upper()
    for n in shoe_list:         #adds all the shoe codes to the local list - shoe_codes. This will be used to check if the code they enter actually belongs to a shoe. 
        shoe_codes.append(n.code)
        if n.code == user_choice:   #if code is in the list, then it will call the method from the Shoe class to print the data 
            n.__str__()
    if user_choice not in shoe_codes:
        print('\nThat code was not found.\n')


def value_per_item():
    read_shoes_data()
    shoe_table_2 = []
    for n in shoe_list:   #will iterate through list of shoe objects and calculate their stock value. Will add an item to the list containing shoe name and value
        total_value = float(n.cost) * float(n.quantity)
        shoe_table_2.append([n.product,total_value])
    print(tabulate(shoe_table_2, headers = ['Shoe','Stock value'])) #will print a table to represent the data onto the screen 

def highest_qty():
    read_shoes_data()
    shoe_quantities = {}    #will create dictionary which will be populated with quantity of shoe as key and shoe name as the value
    for n in shoe_list:     
        shoe_quantities[int(n.quantity)] = n.product
    print(f'''
The shoe that is the highest in stock is: {shoe_quantities[max(shoe_quantities)]}. There are {max(shoe_quantities)} in stock.
They are now on sale!
''')            #uses max function to print the highest key (quantity) in dictionary and then will also provide the value (shoe name)

#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
should_repeat = True
intro_message = '''
-----------WELCOME TO THE SHOE INVENTORY------------

MAIN MENU: 
a - Add a shoe to the inventory
b - View all shoes and their details 
c - View the lowest stock item +/- restock
d - View the details of one shoe using product code 
e - View the total stock value for each shoe
f - View the highest stock item and put it on sale
g - exit 

Please pick an option from the above list: 
'''
while should_repeat:
    user_input = input(intro_message).lower()
    if user_input == 'a':
        capture_shoes()
    elif user_input == 'b':
        view_all()
    elif user_input == 'c':         #main menu which will be looped through until exited. Functions called from above depending on choice. 
        re_stock()
    elif user_input == 'd':
        search_shoe()
    elif user_input == 'e':
        value_per_item()
    elif user_input == 'f':
        highest_qty()
    elif user_input == 'g':
        print('\nGoodbye!\n')
        should_repeat = False
    else:
        print('\nInvalid input. Try again.\n')
