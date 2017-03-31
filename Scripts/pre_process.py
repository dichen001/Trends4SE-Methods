import os, csv, collections
DIR = os.path.abspath(os.path.dirname(__file__))
input_csv = os.path.join(DIR, os.pardir, 'MT', 'MT-1.csv')
feature_csv = os.path.join(DIR, 'processed1.csv')

# ToDos
# DOI preprocess
# multi choice --> lead to multi chosen
# empty input --> 0



def stat(pair, a, total):
    diffAnswers = pair[a]
    aName = a.split('.')[1].capitalize()
    aSame, aChosen, aEmpty = aName + '_Same', aName + '_Chosen', aName + '_EmptyCount',
    cnt = collections.Counter(diffAnswers)
    pair[aEmpty] = cnt['{}'] + cnt['']
    if cnt.most_common(1)[0][1] > total/2.0:
        pair[aChosen]= 1
    else:
        pair[aChosen]= 0
    pair[aSame] = min(1, cnt.most_common(1)[0][1]/2.0)


def featuralize():
    with open(input_csv, 'rU') as csvIn:
        reader = csv.DictReader(csvIn)
        headers = reader.fieldnames
        with open(feature_csv, 'wb') as detailsOut:
            id = 'HITId'
            infos = ['AssignmentId',
                     'WorkerId',
                     'WorkTimeInSeconds']
            inputs = [
                     'Input.Id',
                     'Input.Venue',
                     'Input.Title',
                     'Input.Authors',
                     'Input.Cites',
                     'Input.Abstract',]
            answers = ['Answer.DOI',
                      'Answer.Methods?',
                      'Answer.Primary?',
                      'Answer.Quant?',
                      'Answer.Read?',
                      'Answer.Suggestion',
                      'Answer.citation',
                      'Answer.paper-link']
            answers_expanded = [v.split('.')[1].capitalize() for v in answers]
            answers_expanded = sorted([v+'_Same' for v in answers_expanded] + [v+'_Chosen' for v in answers_expanded] + [v+'_EmptyCount' for v in answers_expanded])
            writer1 = csv.DictWriter(detailsOut, fieldnames= [id] + infos + inputs + answers + answers_expanded)
            writer1.writeheader()

            first, count = True, 0
            for i, row in enumerate(reader):
                if first:
                    ####
                    priorHIT = row[id]
                    pair = {}
                    pair[id] = row[id]
                    for k in infos + answers:
                        if '|' in row[k]:
                            pair[k] = row[k].split('|')
                        else:
                            pair[k] = [row[k]]
                    for k in inputs:
                        pair[k] = row[k]
                    first = False
                    count += 1
                    #####
                else:
                    if row[id] == priorHIT:
                        for k in infos + answers:
                            if '|' in row[k]:
                                pair[k].extend(row[k].split('|'))
                            else:
                                pair[k] += [row[k]]
                        count += 1
                        'hi'
                    else:
                        for a in answers:
                            stat(pair, a, count)
                        'hi'
                        writer1.writerow(pair)

                        ####
                        priorHIT = row[id]
                        pair = {}
                        pair[id] = row[id]
                        for k in infos + answers:
                            if '|' in row[k]:
                                pair[k] = row[k].split('|')
                            else:
                                pair[k] = [row[k]]
                        for k in inputs:
                            pair[k] = row[k]
                        count = 1
                        ####

featuralize()
