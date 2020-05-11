tmp_list= [{"movieId":0, "lol": "re"},
    {"movieId":1, "lol": "re"},
    {"movieId":2, "lol": "re"},
    {"movieId":3, "lol": "re"},
    {"movieId":4, "lol": "re"}
]

ub = [
    [0,1,2],
    [1,2,3],
    [0,1,3],
    [1,3,4]
]

df = pd.DataFrame(tmp_list)
print(df.head())

tm = TriangularMatrixOfPairsCounters(df, ub)
for i in tm:
    print(i)