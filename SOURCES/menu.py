##############################
#                            #
#  PANTELIDIS NIKOS AM 2787  #
#                            #
##############################
import os
from loader import *
from pair_finder import *
import time
import pandas as pd
from plots import *


def print_presentation_commands():
    print('===================================\n')
    print('(a)   List ALL discovered rules                     [format: a]\n')
    print('(b)   List all rules containing a BAG of movies')
    print('      [format:    in their <ITEMSET|HYPOTHESIS|CONCLUSION>      \
    b,<i,h,c>,<comma-sep. movie IDs>]\n')
    print('(c)   COMPARE rules with <CONFIDENCE,LIFT>          [format: c]\n')
    print('(h)   Print the HISTOGRAM of <CONFIDENCE|LIFT>      [format: h]\n')
    print('(m)   Show details of a MOVIE                       [format: m,<movie ID>]\n')
    print('(r)   Show a particular RULE                        [format: r,<rule ID>]\n')
    print('(s)   SORT rules by increasing <CONFIDENCE|LIFT|INTEREST>')
    print('                                                    [format: s,<c,l,i>]')
    print('(v)   VISUALIZATION of association rules            [format: v,<draw_choice:')     
    print('      (sorted by lift)                              [c(ircular),r(andom),s(pring)]>,')
    print('                                                    <num of rules to show>]\n')
    print('(e)    EXIT                                         [format: e]\n')


def loading_menu():
    files_dict = {
        '1': 'Data\\ratings.csv',
        '2': 'Data\\ratings_100users.csv',
        '3': 'Data\\ratings_100user_shuffled.csv',
        }
    print_loading_options(files_dict)
    selected_option = input()
    
    print("Give a Min-Score(0,5):")
    min_score = float(input())
    while min_score > 5 or min_score < 0:
        print("Please give a number that is inside the given range (0,5):")
        min_score = input()
    
    return apply_option(selected_option, files_dict, min_score)
    


def print_loading_options(files_dict):
    print('==========LOADING OPTIONS==========\n')
    for i in files_dict.keys():
        print(f'({i})   {files_dict[i][5:]}\n')

    print('(This option is used in sampled apriori. It returns a stream of the ratings)\n')


def apply_option(loading_option, files_dict, min_score):
    if loading_option == '1' or loading_option == '2':
        return CreateMovieBaskets(files_dict[loading_option], min_score)

    elif loading_option == '3':
        return createRatingsStream(files_dict[loading_option], min_score)

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
            
            results = pd.DataFrame([rules.iloc[i] for i in range(len(rules)) if bag_of_movies <= set(rules.iloc[i][destination])]) 
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
            result = rules.loc[rules['rule ID'] == rule_id]
            print_df(result)
            
        elif command_type == "m":

            # Show details of a movie
            
            movie_id = int(opt_list[1])
            result = movies_df.loc[movies_df['movieId'] == movie_id]
            print(result)

        elif command_type == "h":
            # Print the histogram of <confidence|lift|interest>
            
            hist_lift_confidence(rules)

        elif command_type == "c":

            # Comparison of confidence vs lift
            
            compare_confidence_lift(rules)
        
        elif command_type == "v":
            
            # Visualization of association rules
            
            plot_option = opt_list[1]
            number_of_rules_to_draw = int(opt_list[2])

            draw_graph(rules.sort_values('lift'), number_of_rules_to_draw, plot_option)

        elif command_type == "e":
            
            # Exit
            
            return -1
        
        else:
            print("Wrong command input. Please try again.")
        
        print("Would you like to continue?")
        print('Press e to exit or anything else to continue:')
        user_selection = input()
        if user_selection == "e":
            return -1
        
        os.system('cls' if os.name == 'nt' else 'clear')


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