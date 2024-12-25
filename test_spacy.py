import spacy
from spacy.language import Language
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span

import nltk
from nltk.tokenize import word_tokenize

from colorama import Fore

from objects import FoodType
from menu import menu
from request_examples import examples

nlp = spacy.load('ru_core_news_sm')

# nltk.download()

# ПОИСК СОВПАДЕНИЙ
"""
matcher = Matcher(nlp.vocab)

pattern = [{"LEMMA": 'пицца'}, {"TEXT": 'с'}, {"LEMMA": 'ветчина'}]
matcher.add("Пицца с ветчиной", [pattern])

for sentence in examples:
    doc = nlp(sentence)

    print(doc.text, matcher(doc))
"""

# ВЫВОД ТОКЕНОВ | ЧАСТЬ РЕЧИ | LABEL ЗАВИСИМОСТИ | ЛЕММА | К КАКОМУ СЛОВУ ОТНОСИТСЯ |
"""
for sentence in examples:
    doc = nlp(sentence)

    print(doc.text)
    for token in doc:
        print(token.text, token.pos_, token.dep_, token.lemma_, token.head.text, sep=" | ")
    print("")
"""

# СОЗДАНИЕ СВОЕГО TIMELINE ПО ПОИСКУ ЕДЫ, ПРИ ВЫЗОВЕ DOC
"""
pizzas: list[list[str]] = [list(pizza.tokens) for pizza in menu if pizza.food_type == FoodType.PIZZA]
snacks: list[list[str]] = [list(snack.tokens) for snack in menu if snack.food_type == FoodType.SNACK]
drinks: list[list[str]] = [list(drink.tokens) for drink in menu if drink.food_type == FoodType.DRINK]

pizza_names, snack_names, drink_names = [], [], []
lists = [pizza_names, snack_names, drink_names]
food_types = [pizzas, snacks, drinks]

for i, list_ in enumerate(lists):
    for tokens in food_types[i]:
        for name in tokens:
            list_.append(name)
    print(list_)

pizza_patterns = list(nlp.pipe(pizza_names))
snack_patterns = list(nlp.pipe(snack_names))
drink_patterns = list(nlp.pipe(drink_names))

matcher = PhraseMatcher(nlp.vocab)
for pattern, name in [(pizza_patterns, 'PIZZA'),
                      (snack_patterns, 'SNACK'),
                      (drink_patterns, 'DRINK')]:
    matcher.add(name, pattern)


# собственный компонент при создании документа
@Language.component("add_menu")
def add_menu_component(doc):
    # добавление совпадений в документ
    matches = matcher(doc)
    # создание срезов токенов для каждого совпадения с указанным label
    spans = []
    spans.extend([Span(doc, start, end, label='PIZZA') for match_id, start, end in matches])
    spans.extend([Span(doc, start, end, label='SNACK') for match_id, start, end in matches])
    spans.extend([Span(doc, start, end, label='DRINK') for match_id, start, end in matches])
    print(spans)
    doc.ents = spans
    return doc


nlp.add_pipe("add_menu", after="ner")

for sentence in examples:
    doc = nlp(sentence)
    print([(ent.text, ent.label_) for ent in doc.ents])
"""

# ПОИСК СОВПАДЕНИЙ ИЗ ИМЕЮЩЕГОСЯ МЕНЮ
# преобразование меню в формат [{'LOWER': 'TOKEN'}, ...]
pizzas: list[tuple[str, list[str]]] = [(pizza.name, list(pizza.tokens)) for pizza in menu if
                                       pizza.food_type == FoodType.PIZZA]
snacks: list[tuple[str, list[str]]] = [(snack.name, list(snack.tokens)) for snack in menu if
                                       snack.food_type == FoodType.SNACK]
drinks: list[tuple[str, list[str]]] = [(drink.name, list(drink.tokens)) for drink in menu if
                                       drink.food_type == FoodType.DRINK]

pizza_names, snack_names, drink_names = [], [], []
lists = [pizza_names, snack_names, drink_names]
food_types = [pizzas, snacks, drinks]

for i, list_ in enumerate(lists):
    for food_name, tokens in food_types[i]:
        for tokens_name in tokens:
            list_.append((food_name, [{'LOWER': token} for token in word_tokenize(tokens_name)]))

# добавление токенов в matcher
matcher = Matcher(nlp.vocab)
for list_ in [pizza_names, snack_names, drink_names]:
    for name, pattern in list_:
        matcher.add(name, [pattern])

# поиск совпадений и вывод их в командную строку
for sentence in examples:
    doc = nlp(sentence)
    print(doc.text)
    for match in matcher(doc):
        print(f'{Fore.GREEN} - match: {nlp.vocab.strings[match[0]]} {Fore.RESET}')
