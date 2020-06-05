def generate_rules(MinConfidence, itemsets):
    rules = {}
    rule_id = 1

    for k in range(2, MaxCombo + 1):

        combo_size = k
        even_size = (combo_size % 2) == 0
        mid = math.ceil(combo_size / 2)


        final_hypothesis =  list(range(1, combo_size))
        current_hypothesis = list(range(combo_size-1))
        for combo in itemsets[k].keys():
            movie_set = sorted(list(combo))
            hypothesis = frozenset([movie_set[i] for i in current_hypothesis])
            conclusion = combo.difference(hypothesis)
            frequency = itemsets[k][combo]['frequency']
            confidence, lift, interest = get_scores(
                frequency,
                itemsets[k][hypothesis]['frequency'],
                itemsets[k][conclusion]['frequency']
                )
            

            for i in range(combo_size-2, 0, -1):






def get_scores(itemset_f, hypothesis_f, conclusion_f):
    confidence = get_confidence(itemset_f, hypothesis_f)
    lift = get_lift(confidence, conclusion_f)
    interest = get_interest(confidence, conclusion_f)

    return confidence, lift, interest
    
