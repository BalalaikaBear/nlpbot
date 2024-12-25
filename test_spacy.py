import spacy
from spacy.matcher import Matcher
from request_examples import examples

nlp = spacy.load('ru_core_news_sm')


# ПОИСК СОВПАДЕНИЙ
"""
matcher = Matcher(nlp.vocab)

pattern = [{"LEMMA": 'пицца'}, {"TEXT": 'с'}, {"LEMMA": 'ветчина'}]
matcher.add("Пицца с ветчиной", [pattern])

for sentence in examples:
    doc = nlp(sentence)

    print(doc.text, matcher(doc))
"""


for sentence in examples:
    doc = nlp(sentence)

    print(doc.text)
    for token in doc:
        print(token.text, token.pos_, token.dep_, token.lemma_, token.head.text, sep=" | ")
    print("")
