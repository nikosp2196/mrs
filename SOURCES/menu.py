import os
from loader import *
from pair_finder import *
import time
import pandas as pd

def print_presentation_commands():
    print('===================================\n')
    print('(a)   List ALL discovered rules                     [format: a]\n')
    print('(b)   List all rules containing a BAG of movies')
    print('      [format:    in their <ITEMSET|HYPOTHESIS|CONCLUSION>      \
    b,<i,h,c>,<comma-sep. movie IDs>]\n')
    print('(c)   COMPARE rules with <CONFIDENCE,LIFT>          [format: c]\n')
    print('(h)   Print the HISTOGRAM of <CONFIDENCE|LIFT>     [format: h,<c,l>]\n')
    print('(m)   Show details of a MOVIE                       [format: m,<movie ID>]\n')
    print('(r)   Show a particular RULE                        [format: r,<rule ID>]\n')
    print('(s)   SORT rules by increasing <CONFIDENCE|LIFT|INTEREST>\n')
    print('                                                    [format: s,<c,l,i>]')
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
    print('(1)   Classic Apriori   #,MinFrequency,MaxLength,MinConfidence,MinLift,MaxLift\n')
    print('(2)   Sampled Apriori   #,MinFrequency,MaxLength,MinConfidence,MinLift,MaxLift,SampleSize\n')
    print('MinFrequency,MinConfidence,MinLift,MaxLift -------> (0,1)')
    print('You can disable MinLift,MaxLift by giving -1 as input')
    print('Example_1: 1,0.1,4,0.5,-1,-1  Example_2: 2,0.5,5,0.5,0.2,-1,100 \n')


def apply_apriori_options(options, item_baskets):
    opt_list = options.split(",")
    algorithm = opt_list[0]
    min_frequency = float(opt_list[1])
    max_length = int(opt_list[2])
    min_confidence = float(opt_list[3])
    min_lift = float(opt_list[4])
    max_lift = float(opt_list[5])

    start_time = time.time()
    if algorithm == '1':
        print("=============== Apriori Execution ===============")
        itemsets = myApriori(item_baskets, min_frequency, max_length)
    elif algorithm == '2':
        print("=========== Sampled Apriori Execution ===========")
        sample_size = int(opt_list[6])
        print("Sample Size: ", sample_size)
        itemsets = sampledApriori(sample_size, item_baskets, min_frequency, max_length)
    else:
        print("Somethong went wrong please try again.")
        return -1
    
    print("Min Frequency: ", min_frequency)
    print("Max Length: ", max_length)
    print("Min Confidence: ", min_confidence)
    print("Min Lift: ", min_lift)
    print("Max Lift: ", max_lift)

    rules = generate_all_rules(itemsets, min_confidence, min_lift, max_lift)
    exec_time = time.time() - start_time
    print("Generated", len(rules),"rules in", exec_time, "seconds")
    
    return rules



def presentation_menu(rules, movies_df):
    commands = ['a', 'b', 'c', 'h', 'm', 'r', 's', 'v', 'e']
    while True:
        
        print_presentation_commands()
        user_input = input()
        while user_input[0] not in commands:
            print("Please choose one of the above options:")
            user_input = input()
        opt_list = user_input.split(",")
        command_type = opt_list[0]


        if  command_type == "a":

            # List all discovered rules

            pd.options.display.width=None
            pd.options.display.max_columns = None
            pd.options.display.max_rows = None
            print_df(rules)

        elif command_type == "b":

            # List all rules containing a bag of movies

            bag_of_movies = set([int(i) for i in opt_list[2:]])
            
            if opt_list[1] == 'i':
                destination = 'itemset'
            elif opt_list[1] == 'h':
                destination = 'hypothesis'
            elif opt_list[1] == 'c':
                destination = 'conclusion'
            else:
                print("Sth went wrong. Try again.")
            
            results = pd.DataFrame([rules.iloc[i] for i in range(len(rules)) if bag_of_movies <= set(rules.iloc[i]['itemset'])]) 
            print_df(results)
            
        elif command_type == "s":
           
            # Sort rules by increasing <confidence|lift|interest>
           
            if opt_list[1] == 'c':
                column = 'confidence'
            elif opt_list[1] == 'l':
                column = 'lift'
            elif opt_list[1] == 'i':
                column = 'interest'
            else:
                print("Sth went wrong. Try again.")

            results = rules.sort_values(column)
            print_df(results)
        
        elif command_type == "r":

            # Show a particular rule
            
            rule_id = int(opt_list[1])
            result = rules.loc[rules['rule_id'] == rule_id]
            print(result)
            
        elif command_type == "m":

            # Show details of a movie
            
            movie_id = int(opt_list[1])
            result = movies_df.loc[movies_df['movieId'] == movie_id]
            print(result)

        elif command_type == "h":
            # Print the histogram of <confidence|lift|interest>
            print(command_type)
        elif command_type == "c":
            # Comparison of confidence vs lift
            print(command_type)
        elif command_type == "v":
            # Visualization of association rules
            print(command_type)
        elif command_type == "e":
            # Exit
            return -1
        else:
            print("Wrong command input. Please try again.")
        
        print("Would you like to continue?")
        print('Press y to continue or anything else to exit: ')
        user_selection = input()
        if user_selection != "y":
            return -1
        
        os.system('cls')


def print_df(input_df):
    pd.options.display.width=None
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None 
    print(input_df)         


def menu():
    movies_path =  "DATA\\movies.csv"
    item_baskets = loading_menu()
    
    movies_df = ReadMovies(movies_path)
    
    rules = apriori_menu(item_baskets)
    
    presentation_menu(rules, movies_df)


menu()