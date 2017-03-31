import pandas, collections

d = collections.defaultdict(list)
with open("citemap_v8.csv", "r") as ins:
    for line in ins:
        line = line.split('$|$')
        for i, h in enumerate(['ID','Venue','Is_Conference','Year','Title','H2','H3','Ref_ID','Cites','Author_IDs','Authors','Abstract','DOI_URL']):
            d[h].append(line[i])

pandas.DataFrame.from_dict(d).to_csv('all_v8.csv')
