from dataclasses import dataclass
from enum import StrEnum


class FoodType(StrEnum):
    """Вид еды"""
    PIZZA = 'пицца'
    SNACK = 'закуска'
    DRINK = 'напиток'


class Size(StrEnum):
    """Размер блюда"""
    S = 'small'
    M = 'medium'
    L = 'big'


@dataclass
class Ingredient:
    """Класс использованных ингредиентов в блюде"""
    name: str
    tokens: set[str]
    price: int
    description: str | None = None

    def __repr__(self) -> str:
        return f'<Ингредиент ({self.name})>'

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name.lower())


@dataclass
class Product:
    """Стандартный класс для товаров ресторана"""
    name: str
    tokens: set[str]
    price: int | dict[str, int]
    food_type: FoodType
    description: str = None
    fix_ingredients: set[Ingredient] = None
    remove_ingredients: set[Ingredient] = None

    def __repr__(self) -> str:
        return f'<{self.food_type.value.capitalize()} ({self.name})>'

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name.lower())


class Pizza(Product):
    def __init__(self, **kwargs) -> None:
        super().__init__(food_type=FoodType.PIZZA, **kwargs)


class Snack(Product):
    def __init__(self, **kwargs) -> None:
        super().__init__(food_type=FoodType.SNACK, **kwargs)


class Drink(Product):
    def __init__(self, **kwargs) -> None:
        super().__init__(food_type=FoodType.DRINK, **kwargs)


@dataclass
class OrderItem:
    """Параметры заказанного блюда"""
    dish: Product
    quantity: int = 1
    size: str | None = None
    add_ingredients: set[Ingredient] | None = None
    remove_ingredients: set[Ingredient] | None = None

    def __repr__(self) -> str:
        size = f', size.{self.size}' if self.size else ""
        add = ', add: ' + str(self.add_ingredients)[1:-2] if self.add_ingredients else ""
        remove = ', remove: ' + str(self.remove_ingredients)[1:-2] if self.remove_ingredients else ""

        return '<%s %s шт.%s%s%s>' % (self.dish.name, self.quantity, size, add, remove)

    def __contains__(self, item: Product | Ingredient) -> bool:
        if isinstance(item, Product):
            return item == self.dish
        elif isinstance(item, Ingredient):
            return item in self.dish.fix_ingredients


class Order:
    def __init__(self) -> None:
        self.items: dict[str, OrderItem | list[OrderItem]] = {}

    def add(self, order: OrderItem) -> None:
        """Добавление блюда в заказ"""
        # если блюдо с таким название уже есть...
        if order.dish.name in self.items:
            order_items: OrderItem | list[OrderItem] = self.items.get(order.dish.name)
            # и уже было заказано несколько идентичных блюд
            if isinstance(order_items, list):
                changed = False
                for order_item in order_items:
                    order_item: OrderItem
                    # и оно идентично по ингредиентам и размеру -> увеличить его на 1
                    if (order_item.size == order.size
                            and order_item.add_ingredients == order.add_ingredients
                            and order_item.remove_ingredients == order.remove_ingredients):
                        order_item.quantity += 1
                        changed = True
                        break
                # добавить его в заказ
                if not changed:
                    self.items[order.dish.name].append(order)
            # и уже было заказано одно такое блюдо
            elif isinstance(order_items, OrderItem):
                # и оно идентично по ингредиентам и размеру -> увеличить его на 1
                if (order_items.size == order.size
                        and order_items.add_ingredients == order.add_ingredients
                        and order_items.remove_ingredients == order.remove_ingredients):
                    order_items.quantity += 1
                # добавить его в заказ
                else:
                    self.items[order.dish.name] = [order_items, order]
        else:
            self.items[order.dish.name] = order

    def remove_ingredient(self, ingredients: list[Ingredient], product: Product) -> bool:
        """Удаляет ингредиент из блюда"""
        is_product_changed: bool = False

        # если блюдо с таким название уже есть...
        if product.name in self.items:
            order_items: OrderItem | list[OrderItem] = self.items.get(product.name)
            # и уже было заказано несколько идентичных блюд
            if isinstance(order_items, list):
                for order_item in order_items:
                    order_item: OrderItem
                    for ingredient in ingredients:
                        # если ингредиент является добавленным -> убрать его из множества
                        if ingredient in order_item.add_ingredients:
                            order_item.add_ingredients.remove(ingredient)
                            is_product_changed = True
                        # если ингредиент не был добавлен вручную и он присутствует в блюде -> добавить его в список на удаление
                        elif ingredient in order_item.dish.remove_ingredients:
                            order_item.remove_ingredients.add(ingredient)
                            is_product_changed = True
                        else:
                            continue
            # и уже было заказано одно такое блюдо
            elif isinstance(order_items, OrderItem):
                for ingredient in ingredients:
                    # если ингредиент является добавленным -> убрать его из множества
                    if ingredient in order_items.add_ingredients:
                        order_items.add_ingredients.remove(ingredient)
                        is_product_changed = True
                    # если ингредиент не был добавлен вручную и он присутствует в блюде -> добавить его в список на удаление
                    elif ingredient in order_items.dish.remove_ingredients:
                        order_items.remove_ingredients.add(ingredient)
                        is_product_changed = True
                    else:
                        continue

        return is_product_changed

    def remove_product(self, product: Product) -> bool:
        """Удаляет блюдо из заказа"""
        is_product_deleted: bool = False

        # если блюдо с таким название уже есть...
        if product.name in self.items:
            order_items: OrderItem | list[OrderItem] = self.items.get(product.name)
            # и уже было заказано несколько идентичных блюд
            if isinstance(order_items, list):
                order_items = order_items[:-2]  # удалить последнее добавленное блюдо
                is_product_deleted = True
            elif isinstance(order_items, OrderItem):
                self.items.pop(product.name)  # удалить блюдо
                is_product_deleted = True

        return is_product_deleted

    def read(self) -> list:
        """Возвращает заказ в формате списка"""
        order: list = []
        for value in self.items.values():
            if isinstance(value, list):
                for i in value:
                    order.append(i)
            else:
                order.append(value)
        return order

    def has_something(self) -> bool:
        """Было ли что-то заказано?"""
        return bool(self.items)

    def reset(self) -> None:
        """Сброс заказа"""
        self.items = {}

    def to_text(self) -> str:
        """Преобразование заказа в читаемый текст для бота"""

        answer: str = ''
        i: int = 1
        for values in self.items.values():
            # несколько одинаковых блюд
            if isinstance(values, list):
                for value in values:
                    value: OrderItem

                    # блюдо
                    if value.quantity > 1:
                        answer += f'{str(i)}. *{value.dish.name}* {value.quantity} шт.'
                    else:
                        answer += f'{str(i)}. *{value.dish.name}*'

                    # ингредиенты
                    if value.add_ingredients:
                        for ingredient in value.add_ingredients:
                            answer += f'\n- Добавлен ингредиент: {ingredient.name}'
                    if value.remove_ingredients:
                        for ingredient in value.remove_ingredients:
                            answer += f'\n- Без ингредиента: {ingredient.name}'

                    answer += '\n'
                    i += 1

            # одно блюдо
            elif isinstance(values, OrderItem):
                # блюдо
                if values.quantity > 1:
                    answer += f'{str(i)}. *{values.dish.name}* {values.quantity} шт.'
                else:
                    answer += f'{str(i)}. *{values.dish.name}*'

                # ингредиенты
                if values.add_ingredients:
                    for ingredient in values.add_ingredients:
                        answer += f'\n- Добавлен ингредиент: {ingredient.name}'
                if values.remove_ingredients:
                    for ingredient in values.remove_ingredients:
                        answer += f'\n- Без ингредиента: {ingredient.name}'

                answer += '\n'
                i += 1

        return answer

    def __repr__(self) -> str:
        return str(self.items)
