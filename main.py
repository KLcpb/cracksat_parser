from bs4 import BeautifulSoup
import requests
import re
import genanki

url = 'https://www.cracksat.net/sat/reading/the_master_sat_word_list.html'
request = requests.get(url)
soup = BeautifulSoup(request.text,'html.parser')
teme = soup.find_all('li')
teme = filter(lambda x: x.text[:8]=="SAT Word",teme)
links = []
for r in teme:
    link = r.find('a',href=True)
    links.append(link['href'])
links = links[:-13]

dictionary = []

for l in links:
    request = requests.get(l)
    sp = BeautifulSoup(request.text,'html.parser')
    words = sp.find_all('p')
    for w in words:
        definition = w.text
        if definition == "* SAT is a registered trademark of the College Board, which was not involved in the production of, and does not endorse, this product.":
            continue
        else:
            word = definition.split()[0]
            definition = ''.join(re.split(r'(\s+)', definition)[3])
            dictionary.append([word,definition])
            # a = input(f'{word} (y/n)')
            # if a == 'y':



#---crating anki deck
model_id = 1602282319
model = genanki.Model(
    model_id,
    'Words From Cracksat',
    fields=[
        {'name': 'word'},
        {'name': 'definition'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{word}}',
            'afmt': '{{definition}}',
        },
    ])

deck_id = 2059400110
deck = genanki.Deck(deck_id, 'Words From Cracksat')

for word,definition in dictionary:
    note = genanki.Note(model=model, fields=[word, definition])
    deck.add_note(note)

genanki.Package(deck).write_to_file('cracksat_words.apkg')
print(f'generated {len(dictionary)} words')