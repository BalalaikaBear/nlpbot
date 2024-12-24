from menu import menu, Ingredients
from objects import Ingredient, Pizza, Snack, Drink, Product, Size, OrderItem, Order
from requests import requests as texts
from colorama import Fore

verbs: dict[str, set[str]] = {
    'order': {'заказать', 'заказ', 'купить'},
    'add': {'добавь'},
    'delete': {'убери', 'убрать', 'удали', 'удалить'},
    'change': {'вместо', 'взамен'}
}

lemmatized_words: dict[str, set[str]] = {
    'гриб': {'грибами', 'грибы', 'грибной', 'грибная'},
    'курица': {'куриные', 'курицей', 'курой', 'кура', 'куриная', 'курицу'},
    'крыло': {'крылья', 'крылышко', 'крылышки'},
    'ветчина': {'ветчиной', 'ветчины'},
    'пицца': {'пицц', 'пиццы', 'пиццу'}
}

sizes: dict[str, set[str]] = {
    'small': {'маленькая', 'малая', 'малый', 'мелкая', 'маленькую', 'маленькие'},
    'medium': {'средняя', 'средний', 'средние', 'обычная', 'обычные', 'стандартная', 'стандартные'},
    'big': {'большая', 'большие', 'большой', 'большую', 'огромная', 'огромный', 'огромную'}
}

quantity: dict[int, set[str]] = {
    1: {'1', 'один', 'одна', 'одну'},
    2: {'2', 'два', 'две', 'двух'},
    3: {'3', 'три'},
    4: {'4', 'четыре'},
    5: {'5', 'пять'},
    6: {'6', 'шесть'},
    7: {'7', 'семь'},
    8: {'8', 'восемь'},
    9: {'9', 'девять'},
    10: {'10', 'десять'}
}

punctuation: str = ".,!?:;"


def tokenise(text: str) -> list[str]:
    """Разделение текста на отдельные слова (токены)"""
    text = text.replace('+', 'и')  # замена '+' на 'и'
    words = text.lower().split()  # прописные символы и разделение текста на слова

    # убрать пунктуацию в конце слова
    for i, word in enumerate(words):
        if word[-1] in punctuation:
            words[i] = word[-1]

    # лемматизация слов
    for i, word in enumerate(words):
        for key, value_set in lemmatized_words.items():
            if word in value_set:
                words[i] = key

    return words


def left_attributes(tokens: list[str],
                    index: int,
                    attributes: dict | None = None) -> dict[str, int | Size | set[Ingredient] | None]:
    """Определение параметров блюда (размер, количество)"""

    if not attributes:
        attributes: dict = {'quantity': 1, 'size': None, 'add_ingredients': set(), 'remove_ingredients': set()}

    # смещение влево
    if index > 0:
        token = tokens[index - 1]

        # если слово является стаканом -> пропустить его
        if token in ['стакан', 'стакана', 'бутылку', 'бутылки', 'порция', 'порции', 'порцию', 'салатом', 'салата']:
            left_attributes(tokens, index - 1, attributes)

        # проверка слова на то, является ли он размером
        for key, value_set in sizes.items():
            if token in value_set:
                tokens[index - 1] = ''
                attributes['size'] = key
                left_attributes(tokens, index - 1, attributes)

        # проверка слова на то, является ли он количеством
        for key, value_set in quantity.items():
            if token in value_set:
                tokens[index - 1] = ''
                attributes['quantity'] = key
                left_attributes(tokens, index - 1, attributes)

    return attributes


def right_attributes(tokens: list[str],
                     index: int,
                     attributes: dict | None = None,
                     was_negative_token: bool = False) -> dict[str, int | Size | set[Ingredient] | None]:
    """Определение параметров блюда (ингредиенты)"""

    if not attributes:
        attributes: dict = {'quantity': 1, 'size': None, 'add_ingredients': set(), 'remove_ingredients': set()}

    # смещение вправо
    if index < len(tokens) - 1:
        token = tokens[index + 1]

        # если слово является предлогом -> пропустить его
        if token in ['с', 'и', 'где', 'больше', 'большим', 'количеством']:
            right_attributes(tokens, index + 1, attributes)

        # если слово == 'без' -> следующим словом ожидается ингредиент
        if token in ['без']:
            right_attributes(tokens, index + 1, attributes, was_negative_token=True)

        # проверка слова на то, является ли он ингредиентом
        for ingredients_attribute in dir(Ingredients):
            if ingredients_attribute[0:1].isupper():
                ingr_obj: Ingredient = getattr(Ingredients, ingredients_attribute)
                if token in ingr_obj.tokens:
                    tokens[index + 1] = ''
                    if was_negative_token:
                        attributes.get('remove_ingredients').add(ingr_obj)
                        right_attributes(tokens, index + 1, attributes)
                    else:
                        attributes.get('add_ingredients').add(ingr_obj)
                        right_attributes(tokens, index + 1, attributes)

    return attributes


def delete_left_attributes(tokens: list[str],
                           index: int,
                           deleted_ingredients: list | None = None) -> list[Ingredient]:
    """Определение удаляемых аттрибутов у объекта"""
    if deleted_ingredients is None:
        deleted_ingredients: list = []

    # смещение влево
    if index > 0:
        token = tokens[index - 1]

        # если слово 'из' или 'и' -> пропустить его
        if token in ['из', 'и']:
            delete_left_attributes(tokens, index - 1, deleted_ingredients)

        # проверка слова на то, является ли он ингредиентом
        for ingredients_attribute in dir(Ingredients):
            if ingredients_attribute[0:1].isupper():
                ingr_obj: Ingredient = getattr(Ingredients, ingredients_attribute)
                if token in ingr_obj.tokens:
                    tokens[index - 1] = ''
                    deleted_ingredients.append(ingr_obj)
                    delete_left_attributes(tokens, index - 1, deleted_ingredients)

    return deleted_ingredients

def read_order(tokens: list[str], order: Order | None = None) -> tuple[Order, str]:
    """Определение заказа, и выдача комментария по этому поводу"""
    if order is None:
        order: Order = Order()

    # УДАЛЕНИЕ БЛЮДА/ИНГРЕДИЕНТА ИЗ ЗАКАЗА -------------------------------------------------------------------------- *
    for verb in verbs['delete']:
        for i in range(len(tokens)):
            if verb in tokens[i]:

                is_succeeded: bool = False  # блюдо/ингредиент был удален?
                deleted_obj: list = []

                # поиск блюд в тексте
                for product in menu:

                    # поиск блюд из трёх слов
                    for i in range(len(tokens) - 2):
                        three_tokens = " ".join(tokens[i:i + 3])
                        if three_tokens in product.tokens:
                            tokens[i], tokens[i + 1], tokens[i + 2] = '', '', ''
                            deleted_ingredients: list = delete_left_attributes(tokens, i)

                            # удаление ингредиентов из заказа
                            if deleted_ingredients:
                                is_succeeded = order.remove_ingredient(deleted_ingredients, product)
                                deleted_obj.extend(deleted_ingredients) if is_succeeded else None
                            # удаление блюда из заказа
                            else:
                                is_succeeded = order.remove_product(product)
                                deleted_obj.append(product) if is_succeeded else None

                    # поиск блюд из двух слов
                    for i in range(len(tokens) - 1):
                        two_tokens = " ".join(tokens[i:i + 2])
                        if two_tokens in product.tokens:
                            tokens[i], tokens[i + 1] = '', ''
                            deleted_ingredients: list = delete_left_attributes(tokens, i)

                            # удаление ингредиентов из заказа
                            if deleted_ingredients:
                                is_succeeded = order.remove_ingredient(deleted_ingredients, product)
                                deleted_obj.extend(deleted_ingredients) if is_succeeded else None
                            # удаление блюда из заказа
                            else:
                                is_succeeded = order.remove_product(product)
                                deleted_obj.append(product) if is_succeeded else None

                    # поиск блюд из одного слова
                    for i, token in enumerate(tokens):
                        if token in product.tokens:
                            tokens[i] = ''
                            deleted_ingredients: list = delete_left_attributes(tokens, i)

                            # удаление ингредиентов из заказа
                            if deleted_ingredients:
                                is_succeeded = order.remove_ingredient(deleted_ingredients, product)
                                deleted_obj.extend(deleted_ingredients) if is_succeeded else None
                            # удаление блюда из заказа
                            else:
                                is_succeeded = order.remove_product(product)
                                deleted_obj.append(product) if is_succeeded else None

                answer = f'{deleted_obj} убраны из заказа' if deleted_obj else 'Вы не могли бы повторить?'
                return order, answer

    # ДОБАВЛЕНИЕ БЛЮДА В ЗАКАЗ -------------------------------------------------------------------------------------- *
    for product in menu:

        # поиск блюд из трёх слов
        for i in range(len(tokens) - 2):
            three_tokens = " ".join(tokens[i:i + 3])
            if three_tokens in product.tokens:
                # добавление в заказ
                tokens[i], tokens[i + 1], tokens[i + 2] = '', '', ''
                attributes: dict = left_attributes(tokens, i)
                attributes: dict = right_attributes(tokens, i + 2, attributes)
                order.add(OrderItem(product, **attributes))

        # поиск блюд из двух слов
        for i in range(len(tokens) - 1):
            two_tokens = " ".join(tokens[i:i + 2])
            if two_tokens in product.tokens:
                # добавление в заказ
                tokens[i], tokens[i + 1] = '', ''
                attributes: dict = left_attributes(tokens, i)
                attributes: dict = right_attributes(tokens, i + 1, attributes)
                order.add(OrderItem(product, **attributes))

        # поиск блюд из одного слова
        for i, token in enumerate(tokens):
            if token in product.tokens:
                # добавление в заказ
                tokens[i] = ''
                attributes: dict = left_attributes(tokens, i)
                attributes: dict = right_attributes(tokens, i, attributes)
                order.add(OrderItem(product, **attributes))

    answer = 'Блюда добавлены' if order.has_something() else 'Вы не могли бы повторить заказ?'
    return order, answer


if __name__ == '__main__':
    for i, sentence in enumerate(texts):
        tokens: list[str] = tokenise(sentence)
        order, answer = read_order(tokens)
        tokens: list[str] = tokenise('Убери салат цезарь и колу')
        order, answer = read_order(tokens, order)
        tokens: list[str] = tokenise('Убери грибы из пиццы с ветчиной')
        order, answer = read_order(tokens, order)
        print(f'{Fore.RESET + str(i) + ': ' + sentence}:',
              f'{Fore.BLUE + '     Токены: ' + str(tokens)}',
              f'{Fore.GREEN + '     Заказ: ' + str(order.read())}',
              f'{Fore.RED + '     Ответ: ' + answer}', sep='\n')
