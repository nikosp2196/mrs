import os
from loader import *


def print_presentation_commands():
    print('===================================\n')
    print('(a)   List ALL discovered rules                     [format: a]\n')
    print('(b)   List all rules containing a BAG of movies')
    print('      [format:    in their <ITEMSET|HYPOTHESIS|CONCLUSION>      \
    b,<i,h,c>,<comma-sep. movie IDs>]\n')
    print('(c)   COMPARE rules with <CONFIDENCE,LIFT>           [format: c]\n')
    print('(h)   Print the HISTOGRAM of <CONFIDENCE|LIFT >      [format: h,<c,l >]\n')
    print('(m)   Show details of a MOVIE                       [format: m,<movie ID>]\n')
    print('(r)   Show a particular RULE                        [format: r,<rule ID>]\n')
    print('(s)   SORT rules by increasing <CONFIDENCE|LIFT>\n')
    print('(v)   VISUALIZATION of association rules            [format: v,<draw_choice:')     
    print('      (sorted by lift)                                     [c(ircular),r(andom),s(pring)]>,')
    print('                                                    <num of rules to show>]\n')
    print('(e)    EXIT                                           [format: e]\n')


def loading_menu():
    options = ['1', '2', '3']
    print_loading_options()
    selected_option = input()
    while selected_option not in options:
        print('Please pick one of the given options:')
        selected_option = input()
    
    print("Give a Min-Score(0,5):")
    min_score = input()
    while min_score > 5 or min_score < 0:
        print("Please give a number that is inside the given range (0,5):")
        min_score = input()
    
    apply_option(selected_option, min_score)
    


def print_loading_options():
    print('==========LOADING OPTIONS==========\n')
    print('(1)   Load ratings.csv\n')
    print('(2)   Load ratings_100users.csv\n')
    print('(3)   Load ratings_100user_shuffled.csv')
    print('(This option is used in sampled apriori. It returns a stream of the ratings)\n')


def apply_option(loading_option, min_score):
    if loading_option == '1':
        ratings_path = "DATA\\ratings.csv"
    elif loading_option == '2':
        ratings_path = "DATA\\ratings_100users.csv"
    else:
        ratings_path = "DATA\\ratings_100users_shuffled.csv"
    

def apriori_menu():


def presentation_menu():
    commands = ['a', 'b', 'c', 'h', 'm', 'r', 's', 'v', 'e']
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_presentation_commands()
        selected_command = input()
        while selected_command not in commands:
            print("Please choose one of the above options:")
            selected_command = input()

        if selected_command == "exit":
            exit()
        #execute_command()

menu()