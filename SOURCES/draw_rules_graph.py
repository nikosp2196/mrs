import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
# INPUT: 
#   rules = dataframe with the (most important wrt lifts) rules to show...
#   number_of_rules = number of rules to show
#   draw_choice =   c for circular placement of nodes, 
#                   r for random placement of nodes, and 
#                   s for "spring" placement of nodes

def draw_graph(rules,number_of_rules,draw_choice):

    G = nx.DiGraph()

    color_map = []
    final_node_sizes = []

    color_iter = 0

    NumberOfRandomColors = 100
    edge_colors_iter = np.random.rand(NumberOfRandomColors)


    node_sizes = {}     # larger rule-nodes imply larger confidence
    node_colors = {}    # darker rule-nodes imply larger lift
    
    for index, row in rules.iterrows():

        color_of_rule = edge_colors_iter[color_iter]

        rule = row['rule']
        rule_id = row['rule ID']
        confidence = row['confidence']
        lift = row['lift']
        itemset = row['itemset']
        hypothesis=row['hypothesis']
        conclusion=row['conclusion']
        
        G.add_nodes_from(["R"+str(rule_id)])

        node_sizes.update({"R"+str(rule_id): float(confidence)})

        node_colors.update({"R"+str(rule_id): float(lift)})
        
        for item in hypothesis:
            G.add_edge(str(item), "R"+str(rule_id), color=color_of_rule)

        for item in conclusion:
            G.add_edge("R"+str(rule_id), str(item), color=color_of_rule)

        color_iter += 1 % NumberOfRandomColors

    print("\tNode size & color coding:")
    print("\t[Rule-Node Size] 4 : lift>7, 3 : lift>6, 2 : lift>5, 1 : default")
    print("\t[Rule-Node Color] purple : conf>0.9, blue : conf>0.75, cyan : conf>0.6, green  : default")
    print("\t[Movie-Node Size] 0.7")
    print("\t[Movie-Node Color] yellow")

    for node in G:

        if str(node).startswith("R"): # these are the rule-nodes...
                
            conf = node_sizes[str(node)]
            lift = node_colors[str(node)]
            
            # rule-node sizes encode lift...
            if lift > 7:
                final_node_sizes.append(1000*(1+4*conf))

            elif lift > 6:
                final_node_sizes.append(1000*(1+3*conf))

            elif lift > 5:
                final_node_sizes.append(1000*(1+2*conf))

            else: # lift > min_lift...
                final_node_sizes.append(1000*(1+conf))

            # rule-node colors encode confidence...
            if conf > 0.9:
                color_map.append('purple')

            elif conf > 0.75:
                color_map.append('blue')

            elif conf > 0.6:
                color_map.append('cyan')

            else: # lift > min_confidence...
                color_map.append('green')

        else: # these are the movie-nodes...
            color_map.append('yellow') 
            final_node_sizes.append(700)

    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]

    if draw_choice == 'c': #circular layout
        nx.draw_circular(G, edges=edges, node_size=final_node_sizes, node_color = color_map, edge_color=colors, font_size=10, with_labels=True)

    elif draw_choice == 'r': #random layout
        nx.draw_random(G, edges=edges, node_size=final_node_sizes, node_color = color_map, edge_color=colors, font_size=10, with_labels=True)

    else: #spring layout...
        pos = nx.spring_layout(G, k=16, scale=1)
        nx.draw(G, pos, edges=edges, node_size=final_node_sizes, node_color = color_map, edge_color=colors, font_size=10, with_labels=False)
        nx.draw_networkx_labels(G, pos)    

    plt.show()
