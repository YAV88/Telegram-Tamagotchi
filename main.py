import telebot
import random
import threading
import time
import schedule

bot = telebot.TeleBot('6392030549:AAGqdEZplS0NUNf7AWgh2-CuDy4UTbqzlyI')

class Tamagotchi:
    def __init__(self, name, hunger_rate, playfulness_rate, description):
        self.name = name
        self.hunger_rate = hunger_rate
        self.playfulness_rate = playfulness_rate
        self.state = 100
        self.description = description

    def decrease_state(self):
        self.state -= self.hunger_rate

    def play(self):
        self.state += self.playfulness_rate

class Dog(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, hunger_rate=3, playfulness_rate=7)

class Cat(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, hunger_rate=5, playfulness_rate=5)

class Bird(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, hunger_rate=2, playfulness_rate=8)

class Fish(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, hunger_rate=6, playfulness_rate=3)

class Rabbit(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, hunger_rate=4, playfulness_rate=6)

tamagotchis = {}

# Словарь с описаниями животных
animal_descriptions = {
    'Dog': 'Собака — ваш верный друг и компаньон. Она любит играть и бегать на улице.',
    'Cat': 'Кошка — независимое и загадочное создание. Она обожает спать и играть с мячиками.',
    'Bird': 'Птица — красивый и мелодичный певец. Она обожает музыку и свежие ягоды.',
    'Fish': 'Рыбка — нежное создание, плавающее в воде. Она любит спокойствие и красивые аквариумы.',
    'Rabbit': 'Кролик — быстрый и лукавый зверек. Он любит морковку и прыгать по лугам.'
}

def send_tamagotchi_state():
    for user_id, tamagotchi in list(tamagotchis.items()):
        bot.send_message(user_id, f"Текущее состояние тамагочи {tamagotchi.name}: {tamagotchi.state}")

# Запускаем периодическую задачу для отправки состояния тамагочи каждую минуту
schedule.every(1).minutes.do(send_tamagotchi_state)

# Функция для запуска бота и периодической задачи
def run_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

def create_random_tamagotchi():
    animal_type = random.choice(list(animal_descriptions.keys()))
    name = random.choice(['Buddy', 'Fluffy', 'Tweetie', 'Nemo', 'Thumper'])
    description = animal_descriptions[animal_type]
    hunger_rate = random.randint(3, 7)
    playfulness_rate = random.randint(5, 10)
    return Tamagotchi(name, hunger_rate, playfulness_rate, description)


def decrease_tamagotchis_state():
    while True:
        for user_id, tamagotchi in list(tamagotchis.items()):
            tamagotchi.decrease_state()
            if tamagotchi.state <= 0:
                del tamagotchis[user_id]
        time.sleep(60)  # Уменьшать состояние каждую минуту

# Запускаем поток для уменьшения состояния тамагочи
threading.Thread(target=decrease_tamagotchis_state, daemon=True).start()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in tamagotchis:
        tamagotchi = create_random_tamagotchi()
        tamagotchis[user_id] = tamagotchi
        bot.reply_to(message, f"Привет! Вы получили питомца {tamagotchi.description} по имени {tamagotchi.name}. Оберегайте его!")
    else:
        bot.reply_to(message, "Вы уже начали игру. Используйте /feed, чтобы покормить тамагочи, или /check, чтобы проверить его состояние.")

@bot.message_handler(commands=['feed'])
def handle_feed(message):
    user_id = message.from_user.id
    tamagotchi = tamagotchis.get(user_id)
    if tamagotchi:
        tamagotchi.play()
        bot.reply_to(message, f"Питомец {tamagotchi.name} покормлен! Текущее состояние: {tamagotchi.state}")
    else:
        bot.reply_to(message, "У вас нет тамагочи. Используйте /start, чтобы начать игру.")

@bot.message_handler(commands=['check'])
def handle_check(message):
    user_id = message.from_user.id
    tamagotchi = tamagotchis.get(user_id)
    if tamagotchi:
        bot.reply_to(message, f"Текущее состояние {tamagotchi.name}: {tamagotchi.state}")
    else:
        bot.reply_to(message, "У вас нет тамагочи. Используйте /start, чтобы начать игру.")

@bot.message_handler(commands=['reset'])
def handle_reset(message):
    user_id = message.from_user.id
    if user_id in tamagotchis:
        del tamagotchis[user_id]
        bot.reply_to(message, "Вы успешно сбросили своего тамагочи. Используйте /start, чтобы начать игру заново.")
    else:
        bot.reply_to(message, "У вас нет тамагочи. Используйте /start, чтобы начать новую игру.")

bot.polling()