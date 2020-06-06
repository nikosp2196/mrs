import os
from loader import *
from pair_finder import *

def print_presentation_commands():
    print('===================================\n')
    print('(a)   List ALL discovered rules                     [format: a]\n')
    print('(b)   List all rules containing a BAG of movies')
    print('      [format:    in their <ITEMSET|HYPOTHESIS|CONCLUSION>      \
    b,<i,h,c>,<comma-sep. movie IDs>]\n')
    print('(c)   COMPARE rules with <CONFIDENCE,LIFT>          [format: c]\n')
    print('(h)   Print the HISTOGRAM of <CONFIDENCE|LIFT >     [format: h,<c,l >]\n')
    print('(m)   Show details of a MOVIE                       [format: m,<movie ID>]\n')
    print('(r)   Show a particular RULE                        [format: r,<rule ID>]\n')
    print('(s)   SORT rules by increasing <CONFIDENCE|LIFT>\n')
    print('(v)   VISUALIZATION of association rules            [format: v,<draw_choice:')     
    print('      (sorted by lift)                              [c(ircular),r(andom),s(pring)]>,')
    print('                                                    <num of rules to show>]\n')
    print('(e)    EXIT                                         [format: e]\n')


def loading_menu():
    options = ['1', '2', '3']
    print_loading_options()
    selected_option = input()
    '''while selected_option not in options:
        print('Please pick one of the given options:')
        selected_option = input()'''
    
    print("Give a Min-Score(0,5):")
    min_score = float(input())
    while min_score > 5 or min_score < 0:
        print("Please give a number that is inside the given range (0,5):")
        min_score = input()
    
    return apply_option(selected_option, min_score)
    


def print_loading_options():
    print('==========LOADING OPTIONS==========\n')
    print('(1)   Load ratings.csv\n')
    print('(2)   Load ratings_100users.csv\n')
    print('(3)   Load ratings_100user_shuffled.csv')
    print('(This option is used in sampled apriori. It returns a stream of the ratings)\n')


def apply_option(loading_option, min_score):
    if loading_option == '1':
        ratings_path = "DATA\\ratings.csv"
        return CreateMovieBaskets(ratings_path, min_score)

    elif loading_option == '2':
        ratings_path = "DATA\\ratings_100users.csv"
        return CreateMovieBaskets(ratings_path, min_score)

    elif loading_option == '3':
        ratings_path = "DATA\\ratings_100users_shuffled.csv"
        return createRatingsStream(ratings_path, min_score)

    else:
        print("Somethong went wrong please try again.")
        return -1
    

def apriori_menu(item_baskets):
    print_apriori_options()
    options = input()
    return apply_apriori_options(options, item_baskets)

def print_apriori_options():
    print('=================APRIORI OPTIONS=================\n')
    print('(1)   Classic Apriori   #,MinFrequency,MaxLength\n')
    print('(2)   Sampled Apriori   #,MinFrequency,MaxLength,SampleSize\n')
    print('Example_1: 1,0.1,4  Example_2: 2,0.5,5,100 \n')


def apply_apriori_options(options, item_baskets):
    opt_list = options.split(",")
    algorithm = opt_list[0]
    min_frequency = float(opt_list[1])
    max_length = int(opt_list[2])

    if algorithm == '1':
        return myApriori(item_baskets, min_frequency, max_length)
    elif algorithm == '2':
        sample_size = int(opt_list[3])
        return sampledApriori(sample_size, item_baskets, min_frequency, max_length)
    else:
        print("Somethong went wrong please try again.")
        return -1





def presentation_menu(combos, movies_df):
    commands = ['a', 'b', 'c', 'h', 'm', 'r', 's', 'v', 'e']
    while True:
        os.system('clear')
        print_presentation_commands()
        selected_command = input()
        while selected_command not in commands:
            print("Please choose one of the above options:")
            selected_command = input()

        if selected_command == "exit":
            exit()


def execute_command(command, combos, movies_df):
    options_list = command.split(',')
    command_id = options_list[0]

    if command_id == 'a':
        


def menu():
    movies_path =  "DATA\\movies.csv"
    item_baskets = loading_menu()
    
    movies_df = ReadMovies(movies_path)
    
    combos = apriori_menu(item_baskets)
    
    presentation_menu(combos, movies_df)


menu()