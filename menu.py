from objects import Ingredient, Pizza, Snack, Drink, Product, Size


class Ingredients:
    # МЯСО
    PEPPERONI = Ingredient(
        name='Пикантная пепперони', price=99,
        tokens={'пепперони'}
    )
    BEEF = Ingredient(
        name='Пряная говядина', price=99,
        tokens={'говядина', 'говядиной', 'говядины', 'мясо', 'мясом', 'мяса'}
    )
    HAM = Ingredient(
        name='Ветчина', price=69,
        tokens={'свинина', 'свининой', 'свинины', 'ветчина', 'ветчины', 'ветчиной', 'колбаса', 'колбасой', 'колбасы'}
    )
    CHICKEN = Ingredient(
        name='Нежный цыпленок', price=69,
        tokens={'цыпленок', 'цыпленком', 'цыпленка', 'курица', 'курицы', 'курицей', 'курицу',
                'индейка', 'индейки', 'индейкой', 'птица', 'птицей', 'птицы'}
    )
    BACON = Ingredient(
        name='Бекон', price=69,
        tokens={'бекон', 'беконом', 'бекона'}
    )

    # СЫРЫ
    MOZZARELLA = Ingredient(
        name='Моцарелла', price=69,
        tokens={'моцарелла', 'сыр', 'сыром', 'сыра'}
    )
    CHEDDAR = Ingredient(
        name='Сыры чеддер и пармезан', price=69,
        tokens={'чеддер', 'чеддером', 'чеддера', 'пармезан', 'пармезаном', 'пармезана'}
    )
    FETA = Ingredient(
        name='Кубики брынзы', price=69,
        tokens={'брынза', 'брынзой', 'брынзы', 'фета', 'фетой', 'феты'}
    )
    JALAPENO = Ingredient(
        name='Острый перец халапеньо', price=49,
        tokens={'острый', 'острая', 'острую', 'острого', 'халапеньо'}
    )

    # СПЕЦИИ
    HERB = Ingredient(
        name='Итальянские травы', price=29,
        tokens={'трава', 'травами', 'травы'}
    )
    ONION = Ingredient(
        name='Красный лук', price=49,
        tokens={'лук', 'лука', 'луком'}
    )

    # НАПОЛНЕНИЯ
    MUSHROOM = Ingredient(
        name='Шампиньоны', price=49,
        tokens={'гриб', 'грибы', 'грибов', 'шампиньон'}
    )
    PICKLE = Ingredient(
        name='Маринованные огурчики', price=49,
        tokens={'огурец', 'огурцом', 'огурцом', 'маринованный', 'маринованным', 'маринованного'}
    )
    TOMATO = Ingredient(
        name='Свежие томаты', price=49,
        tokens={'томат', 'томата', 'томатом', 'томатов', 'помидор', 'помидора', 'помидоров'}
    )
    PINEAPPLE = Ingredient(
        name='Сочный ананасы', price=49,
        tokens={'ананас', 'ананасами', 'ананасов', 'ананаса', 'ананасы'}
    )
    PEPPER = Ingredient(
        name='Сладкий перец', price=49,
        tokens={'перец', 'перцем', 'перца', 'перцев'}
    )
    SHRIMP = Ingredient(
        name='Креветки', price=179,
        tokens={'креветка', 'креветок', 'креветкой', 'морепродукт', 'морепродуктов', 'морепродуктами'}
    )

    # СОУСЫ
    TOMATO_SAUCE = Ingredient(
        name='Фирменный томатный соус', price=49,
        tokens={'томатный', 'соус', 'соуса', 'соус томатный', 'соус томат'}
    )
    BARBECUE_SAUCE = Ingredient(
        name='Фирменный соус барбекю', price=49,
        tokens={'соус барбекю', 'барбекю'}
    )
    ALFREDO_SAUCE = Ingredient(
        name='Фирменный соус альфредо', price=49,
        tokens={'соус альфредо', 'альфредо'}
    )
    CAESAR_SAUCE = Ingredient(
        name='Соус Цезарь', price=49,
        tokens={'соус цезарь', 'цезарь'}
    )


menu: set[Product] = {
    Pizza(name='Пепперони',
          tokens={'пепперони', 'пицца с пепперони', 'пицца с колбаса', 'пицца с колбасами', 'пицца с колбасой'},
          price={Size.S: 519, Size.M: 789, Size.L: 929},
          fix_ingredients={Ingredients.MOZZARELLA, Ingredients.TOMATO_SAUCE},
          remove_ingredients={Ingredients.PEPPERONI}),
    Pizza(name='Сырная',
          tokens={'сырная', 'пицца с сыр', 'пицца с сыром'},
          price={Size.S: 309, Size.M: 599, Size.L: 749},
          fix_ingredients={Ingredients.MOZZARELLA, Ingredients.CHEDDAR, Ingredients.ALFREDO_SAUCE}),
    Pizza(name='Двойной цыпленок',
          tokens={'пицца с курица', 'пицца с птица', 'куриная пицца', 'пицца с курицей', 'пицца с птицей'},
          price={Size.S: 479, Size.M: 709, Size.L: 829},
          fix_ingredients={Ingredients.MOZZARELLA, Ingredients.ALFREDO_SAUCE},
          remove_ingredients={Ingredients.CHICKEN}),
    Pizza(name='Мясная',
          tokens={'мясную', 'мясная пицца', 'мясную пиццу', 'пицца мясная', 'пицца с мясом', 'пицца с мясо',
                  'пицца с ветчиной', 'пицца с ветчина', 'пиццы с ветчиной'},
          price={Size.S: 599, Size.M: 889, Size.L: 1049},
          fix_ingredients={Ingredients.MOZZARELLA, Ingredients.TOMATO_SAUCE},
          remove_ingredients={Ingredients.CHICKEN, Ingredients.BEEF, Ingredients.HAM, Ingredients.PEPPERONI}),
    Pizza(name='Овощи и грибы',
          tokens={'овощная пицца', 'грибная пицца', 'пицца с овощами', 'пицца с овощ',
                  'пицца с грибами', 'пицца с гриб'},
          price={Size.S: 579, Size.M: 889, Size.L: 1029},
          fix_ingredients={Ingredients.MOZZARELLA, Ingredients.TOMATO_SAUCE},
          remove_ingredients={Ingredients.MUSHROOM, Ingredients.TOMATO, Ingredients.PEPPER, Ingredients.ONION,
                              Ingredients.FETA, Ingredients.HERB}),
    Pizza(name='Карбонара',
          tokens={'карбонара', 'пицца карбонара', 'карбонара пицца'},
          price={Size.S: 649, Size.M: 989, Size.L: 1099},
          fix_ingredients={Ingredients.MOZZARELLA, Ingredients.ALFREDO_SAUCE},
          remove_ingredients={Ingredients.BACON, Ingredients.CHEDDAR, Ingredients.TOMATO, Ingredients.ONION,
                              Ingredients.PEPPER, Ingredients.HERB}),
    Snack(name='Картофель из печи',
          tokens={'картошка', 'картофель', 'фри', 'картофель фри', 'картофеля', 'картофеля фри'},
          price={Size.M: 139, Size.L: 249},
          description='Запеченная в печи картошечка с пряными специями'),
    Snack(name='Куриные наггетсы', tokens={'наггетс', 'наггетсы', 'нагетс', 'нагетсы'},
          price={Size.M: 159, Size.L: 309},
          description='Нежное куриное мясо в хрустящей панировке'),
    Snack(name='Куриные крылья барбекю',
          tokens={'курица', 'крыло', 'крылья', 'крылья барбекю', 'крыло барбекю', 'куриные крылышки', 'крылышки',
                  'курица крыло', 'курица крылья'},
          price={Size.M: 279, Size.L: 539},
          description='Куриные крылышки со специями и ароматом копчения'),
    Snack(name='Салат Цезарь',
          tokens={'салат', 'цезарь', 'салат цезарь'},
          price=305,
          fix_ingredients={Ingredients.CHICKEN, Ingredients.HERB, Ingredients.TOMATO, Ingredients.CHEDDAR,
                           Ingredients.CAESAR_SAUCE}),
    Drink(name='Кофе Американо', tokens={'американо'},
          price=109),
    Drink(name='Кофе Капучино', tokens={'капучино'},
          price=169),
    Drink(name='Кофе Латте', tokens={'латте'},
          price=169),
    Drink(name='Какао', tokens={'какао', 'шоколад', 'шоколадом'},
          price=149),
    Drink(name='Кола', tokens={'кола', 'колы', 'колу', 'колой', 'газировка', 'газировкой', 'пепси'},
          price=145),
    Drink(name='Чай черный', tokens={'чай черный', 'черный', 'чай'},
          price=149),
    Drink(name='Чай зеленый', tokens={'чай зеленый', 'зеленый'},
          price=149),
    Drink(name='Апельсиновый сок', tokens={'апельсин', 'апельсинового', 'апельсиновый сок'},
          price=269),
    Drink(name='Яблочный сок', tokens={'сок', 'сока', 'яблочный сок', 'яблоко', 'яблочного'},
          price=269),
    Drink(name='Вишневый нектар', tokens={'вишневый сок', 'вишня'},
          price=269),
    Drink(name='Вода', tokens={'вода', 'воды', 'воду'},
          price=85),
}


if __name__ == '__main__':
    print(Ingredients.MOZZARELLA.name, ' 1 ', Ingredients.MOZZARELLA.price)
    for item in menu:
        print(item.food_type, item)
    print(dir(Ingredients))
