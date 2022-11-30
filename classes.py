class User:

    def __init__(self, username, password, shippingInfo, card_number, card_exp, card_sec_pin, card_zip):
        self.username = username
        self.password = password
        self.shippingInfo = shippingInfo
        self.card_number = card_number
        self.card_exp = card_exp
        self.card_sec_pin = card_sec_pin
        self.card_zip = card_zip


class Cart:

    def __init__(self, id, username, itemType, size, quality, price):
        self.id = id
        self.username = username
        self.itemType = itemType
        self.price = price
        self.size = size
        self.quality = quality


class Inventory:

    def __init__(self, id, itemType, size, quality, price, quantity):
        self.id = id
        self.itemType = itemType
        self.size = size
        self.quality = quality
        self.price = price
        self.quantity = quantity


class TV:

    def __init__(self, id, size, pictureQuality, price, quantity):
        self.id = id
        self.size = size
        self.pictureQuality = pictureQuality
        self.price = price
        self.quantity = quantity


class Laptop:

    def __init__(self, id, size, pictureQuality, price, quantity):
        self.id = id
        self.size = size
        self.pictureQuality = pictureQuality
        self.price = price
        self.quantity = quantity
