#!/usr/bin/env python3

"""
Given an author identified by his/her BAI, this Python3 script counts the number of
citations and the number of citations excluding self cites in the Inspirehep database
(https://inspirehep.net/) for each author's paper.

Additionally, it allows saving a snapshot for later detection of new/removed papers and
change in the number of citations of individual papers

Built on & inspired by https://github.com/efranzin/python
"""

AUTHOR             = 'P.Motloch.2'
MAX_NUM_PAPERS     = 1000       #Number of papers requested from INSPIRE-HEP
SHORT_TITLE_LENGTH = 50         #Shorten long paper titles
NEED_WRITE_CONFIRM = True       #Whether to ask user for permission to save to disk
FILENAME           = 'old_biblio.npy'

# Import the modules to open and reading URLs and the JSON encoder
import urllib.request, json

# Open the INSPIRE-HEP profile
inspirehep_profile = 'https://inspirehep.net/api/literature?sort=mostrecent&size=' + \
                        str(MAX_NUM_PAPERS) + '&q=a%20' + AUTHOR

# Load the data
data     = json.loads(urllib.request.urlopen(inspirehep_profile).read())
num_hits = data['hits']['total']

# Data type to store paper id, beginning of the title, number of citations and number of
# citations without self-citations
import numpy as np
bibliography_dtype = np.dtype([
                        ('id',          np.int64),
                        ('title',       np.unicode_, SHORT_TITLE_LENGTH),
                        ('cits',        np.int64),
                        ('cits_noself', np.int64),
                    ])

# Fill in information about author's papers from the website response
biblio = np.zeros(num_hits, dtype = bibliography_dtype)

for i in range(num_hits):
    biblio[i]['id']          = data['hits']['hits'][i]['id']
    biblio[i]['title']       = data['hits']['hits'][i]['metadata']['titles'][0]['title']
    biblio[i]['cits']        = data['hits']['hits'][i]['metadata']['citation_count']
    biblio[i]['cits_noself'] = data['hits']['hits'][i]['metadata']['citation_count_without_self_citations']

# Print the total number of citations and the total number of citations excluding self cites
print(
        '\nTotal number of citations: ', 
        sum(biblio['cits']), 
        '; Excluding self cites: ', 
        sum(biblio['cits_noself']), 
        '\n',
        sep=''
    )

# Function to save current snapshot of the author's citations
def save_snapshot():
    """
    Saves a current snapshot of the bibliography. 
    If NEED_WRITE_CONFIRM is True, asks the user for permission first.
    """

    if NEED_WRITE_CONFIRM:
        rewrite = input('\nDo you want to save a snapshot [y/n]? ')
        if rewrite != 'y':
            print('Not saved.')
            return

    np.save(FILENAME, biblio)
    print('Saved.')
    return

#If snapshot does not exist, create it (potentially confirming with the user) and exit
from os.path import exists
if not exists(FILENAME):
    save_snapshot()
    exit()

#Load snapshot
old_biblio = np.load(FILENAME)

#Get a set of paper IDs that were added/removed/stayed
new_paper_ids = set(    biblio['id'])
old_paper_ids = set(old_biblio['id'])

added_paper_ids   = new_paper_ids.difference(old_paper_ids)
removed_paper_ids = old_paper_ids.difference(new_paper_ids)
stayed_paper_ids  = new_paper_ids.intersection(old_paper_ids)

#Keep track of whether we had any changes
changes_present = False

#Print information about papers that were added or removed
for i in removed_paper_ids:
    changes_present = True

    idx       = np.argmax(old_biblio['id'] == i)
    title     = old_biblio[idx]['title'] 
    num_cites = old_biblio[idx]['cits']

    if num_cites == 1:
        print('Removed paper: "' + title + '" with ' +  str(num_cites) + ' citation')
    else:
        print('Removed paper: "' + title + '" with ' +  str(num_cites) + ' citations')

for i in added_paper_ids:
    changes_present = True

    idx       = np.argmax(biblio['id'] == i)
    title     = biblio[idx]['title'] 
    num_cites = biblio[idx]['cits']

    if num_cites == 1:
        print('Added paper: "' + title + '" with ' +  str(num_cites) + ' citation')
    else:
        print('Added paper: "' + title + '" with ' +  str(num_cites) + ' citations')

#For papers no added or removed, check if number of citations has changed
for i in stayed_paper_ids:

    idx_old       = np.argmax(old_biblio['id'] == i)
    idx_new       = np.argmax(    biblio['id'] == i)
    title         = biblio[idx_new]['title'] 
    num_new_cites = biblio[idx_new]['cits'] - old_biblio[idx_old]['cits']

    if num_new_cites != 0:
        changes_present = True

        if   num_new_cites == 1:
            print('1 new citation: "' + title + '"')
        elif num_new_cites == -1:
            print('1 citation removed: "' + title + '"')
        elif num_new_cites  > 1:
            print(str(num_new_cites) + ' new citations: "' + title + '"')
        elif num_new_cites  < -1:
            print(str(abs(num_new_cites)) + ' citations removed: "' + title + '"')

#Save current snapshot if anything changed (potentially confirming with the user)
if changes_present:
    save_snapshot()
