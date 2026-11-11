"""The catalogue on the home page and on /apps: every app grouped by what it helps with, one plain line each.

Run by build_app_pages.py (or alone: python tools/catalog.py). It rewrites only what sits between the
<!-- catalog:... --> markers, so it can run again and again. English goes into the HTML; Russian goes into a
window.PAGE_RU script, which site.js already reads.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# What each app is for, said plainly: the line that tells a stranger whether it's for them.
PLAIN = {
    "swisszen": ("Breathing exercises, a mindfulness bell, short practices and a one-line journal.",
                 "Дыхательные упражнения, колокольчик осознанности, короткие практики и дневник в одну строку."),
    "serene": ("Guided meditations, visualisations and affirmations, read aloud and working offline.",
               "Медитации, визуализации и аффирмации с озвучкой, без интернета."),
    "keeper": ("For anxious and intrusive thoughts: notice them, let them pass, check what came true.",
               "Для тревожных и навязчивых мыслей: заметить, отпустить, проверить, что сбылось."),
    "kite": ("Come back to the present during the day: a few soft tugs ask where your mind has wandered.",
             "Возвращаться в настоящее посреди дня: несколько тихих рывков спрашивают, куда унесло мысли."),
    "sidea": ("Love music again: one album a week, a whole side at a time, on a turntable or a tape deck.",
               "Снова полюбить музыку: один альбом в неделю, сторона целиком — на вертушке или в кассетной деке."),
    "party": ("Dates as quests: the two of you are a party of heroes, the phone is the game master.",
              "Свидания как квесты: вы двое — отряд героев, а телефон — мастер игры."),
    "spintop": ("Learn lucid dreaming: dream signs, reality checks by day, a ritual at night, and a top that keeps count.",
                "Научиться осознанным снам: знаки сна, проверки реальности днём, ритуал на ночь и волчок, который ведёт счёт."),
    "hushwood": ("A cosy pixel-art meditation tracker: sit still and shy animals come out.",
                 "Уютный пиксельный трекер медитации: замри — и выйдут пугливые звери."),
    "heartwood": ("Befriend a real tree: every visit is a ring, and the friendship grows only when you go and stand beside it.",
                  "Подружиться с настоящим деревом: каждая встреча — кольцо, и дружба растёт, только когда вы приходите к нему."),
    "longwave": ("Fall asleep faster: sleep sounds, and spoken programmes that quiet the mind, with a timer.",
                 "Засыпать быстрее: звуки для сна и говорящие передачи, которые успокаивают ум, с таймером."),
    "rewind": ("Love films again: your watchlist as a nineties video rental store, two tapes at a time, with due dates.",
               "Снова полюбить кино: список «посмотреть потом» как видеопрокат девяностых, две кассеты на руках и срок возврата."),
    "focusshield": ("A focus timer for Windows that blocks distracting sites and apps until the session ends.",
                    "Таймер фокуса для Windows: блокирует отвлекающие сайты и приложения до конца сессии."),
    "obol": ("Less scrolling: time in Reels, Shorts and TikTok has to be earned with useful apps.",
             "Меньше ленты: время в Reels, Shorts и TikTok нужно заработать полезными приложениями."),
    "unhook": ("Quit a habit: counts the days, the money saved, and helps you ride out a craving.",
               "Бросить привычку: считает дни и сэкономленные деньги, помогает переждать тягу."),
    "vigil": ("Give something up for a while (sugar, the phone in the morning) and keep the vow.",
              "Отказаться от чего-то на время (сахар, телефон по утрам) и сдержать обет."),
    "dayquest": ("Habits and to-dos as a role-playing game: your pixel hero levels up when you do them.",
                 "Привычки и дела как ролевая игра: пиксельный герой растёт, когда вы их делаете."),
    "waypoint": ("Set goals and reach them with 17 proven methods: OKR, WOOP, the 12-week year and more.",
                 "Ставить цели и доходить до них: 17 методов, от OKR и WOOP до «12 недель»."),
    "podium": ("Time everyday tasks and race your own best time, with splits and medals.",
               "Засекать обычные дела и обгонять собственный рекорд — с отсечками и медалями."),
    "hearthspell": ("Household chores as a cosy pixel game: each room is a floor of a wizard's tower.",
                    "Домашние дела как уютная пиксельная игра: каждая комната — этаж башни волшебника."),
    "ember": ("An intermittent fasting timer with the body's stages along the way.",
              "Таймер интервального голодания с этапами, через которые проходит тело."),
    "temper": ("Cold showers, contrast showers and the sauna: a timer, a plan and your progress.",
               "Холодный и контрастный душ, баня: таймер, план и ваш прогресс."),
    "fogwalk": ("Get out for walks: the map of your city is covered in fog until you walk through it.",
                "Чтобы чаще гулять: карта города скрыта туманом, пока вы по ней не пройдёте."),
    "scriptor": ("Remember what you study: write it in your own words, review it before you forget.",
                 "Запоминать, что изучаете: записать своими словами и повторить, пока не забыли."),
    "stele": ("Memorise words, terms, dates and quotes with spaced repetition. Imports Anki decks.",
              "Запоминать слова, термины, даты и цитаты интервальными повторениями. Импорт колод Anki."),
    "familiar": ("A reading tracker with a pixel pet that grows on the pages you read.",
                 "Трекер чтения с пиксельным питомцем, который растёт от прочитанных страниц."),
    "lipovka": ("A pedometer where your steps carry the village post: letters and stories of a small village that go on for years.",
                "Шагомер, в котором шаги разносят деревенскую почту: письма и истории маленькой деревни, которые длятся годами."),
    "stringer": ("Get out every day and see your street again: a small paper's editor wires one thing to photograph, and Sunday's issue collects the week.",
                 "Выходить каждый день и снова видеть свою улицу: редактор маленькой газеты телеграфирует, что снять, а воскресный номер собирает неделю."),
    "ranger": ("A running journal with a fantasy twist: every run is a patrol, and weather, moon, terrain and pulse decide which creatures you meet.",
               "Беговой дневник со сказкой: каждая пробежка — дозор, а кого вы встретите, решают погода, луна, местность и пульс."),
    "apothecary": ("The fridge and the medicine box as a potion shop: every product is a bottle that dims before its date, and every meal is a potion.",
                   "Сроки годности продуктов и лекарств в виде лавки зелий. Свежие продукты светятся, а из приготовленной еды получаются зелья."),
    "fieldscan": ("An anomaly scanner for your city: creatures live in real places, and each comes out to someone who solves its riddle and does its rite. Beta.",
                  "Прибор, который ищет аномалии в городе. Существа показываются тем, кто разгадал загадку и выполнил обряд. Бета."),
    "postround": ("Be the postman of your own neighbourhood: real house numbers, mail handed over only at the door, letters you carry between houses.",
                  "Почтальон своего района: настоящие номера домов, письмо вручается только у двери, а переписку соседей вы носите сами."),
    "opposite": ("An advent calendar across the yard: a window lights after the real sunset for each day's small deed, and ten neighbours are suspects.",
                 "Адвент-календарь в окнах дома напротив: каждый вечер после заката загорается новое окно, а за ним — комната, соседи и загадка."),
    "yourmove": ("Chess by post with seven correspondents: every letter brings a move and a little of their life.",
                 "Шахматы по переписке с семью собеседниками. В каждом письме ход и немного их жизни."),
    "rustle": ("A little creature that lives inside the phone: turn the phone face down, and it goes out exploring and brings back finds.",
               "Зверёк, который живёт в телефоне: переверните телефон экраном вниз, и он уйдёт гулять и вернётся с находками."),
    "cabinet": ("A museum for an odd collection: halls, cabinets, a card for every thing, and a photo check: do I already have it?",
                "Музей для необычной коллекции: залы, шкафы, карточка на каждую вещь и проверка по фото, есть ли такая у вас."),
    "hob": ("Keeps track of things at home, so nothing gets lost and nothing piles up for nothing.",
            "Чтобы дома ничего не терялось и не копилось зря."),
    "threshold": ("An alarm after which the morning starts at once: each day its own app, video, playlist or radio.",
                  "Будильник, который утром сам открывает новости, музыку, радио или фильм – на каждый день своё."),
    "charms": ("A child photographs the deeds they've done, the pictures turn into golden engravings, and a week of them brews a real reward.",
                "Ребёнок фотографирует сделанные дела, и они становятся золотыми страницами гримуара. За неделю набирается на настоящую награду."),
    "matryoshka": ("A present opened layer by layer: the gift sits in the smallest figure, and every figure around it has its own lock.",
                   "Подарок, спрятанный в матрёшку: открывать её придётся фигурку за фигуркой, и у каждой свой замок."),
    "gossamer": ("Catch passing thoughts in two seconds and see which ones you keep coming back to.",
                 "Записывать мысли на лету и замечать, к каким из них вы возвращаетесь снова и снова."),
    "greenstreet": ("A cozy farming game on the real map of your district: beds by the roads you walk and neighbours with stories.",
                    "Уютная ферма на карте вашего района: грядки вдоль привычных дорог и соседи, у каждого из которых своя история."),
    "overwinter": ("A wellbeing diary kept like a polar station: energy is the wind, mood is the cloud, pain is the rain.",
                   "Дневник самочувствия в виде полярной станции: силы — это ветер, настроение — облачность, а боль — осадки."),
    "fridge": ("A fridge door for two: the shopping list, whose turn, notes and worries, shared between your two phones at home.",
               "Дверца холодильника на двоих: покупки, чья очередь, записки и тревоги — общие на двух телефонах дома."),
    "campfire": ("A talk by the fire with the people close to you: sparks bring questions, and the word of the day stays in the ash.",
                 "Разговор у костра с близкими: искры приносят вопросы, а слово дня остаётся в пепле."),
    "lantern": ("Make up bedtime stories with your child from randomly dealt heroes, places and troubles.",
                "Придумывать с ребёнком сказки на ночь из случайных героев, мест и бед."),
    "nighttrain": ("A date night for couples: hundreds of questions to see each other from a new side.",
                   "Свидание для пары: сотни вопросов, чтобы увидеть друг друга с новой стороны."),
    "tessera": ("The same questions to a child, yourself or a grandparent, year after year, on film or in words.",
                "Одни и те же вопросы ребёнку, себе или бабушке год за годом — на видео или словами."),
    "marbles": ("For parents: spend more evenings with your kids, and see what the phone takes.",
                "Для родителей: больше вечеров с детьми — и честно видно, сколько забирает телефон."),
    "ties": ("Reminds you to call and write to the people who matter, before you drift apart.",
             "Напоминает звонить и писать близким, пока вы не отдалились."),
    "notch": ("A weekly photo of each child on a door frame, so you can watch them grow.",
              "Фото каждого ребёнка раз в неделю на дверном косяке — видно, как они растут."),
    "silverbox": ("A family camera that works like film: 24 frames, prints developed the next day.",
                  "Семейная камера как плёнка: 24 кадра, снимки проявляются на следующий день."),
    "anyway": ("See how many Saturdays you have left, and stop putting off what matters.",
               "Увидеть, сколько осталось суббот, и перестать откладывать главное."),
    "calavera": ("Make peace with growing old and with death, gently, in the spirit of the Day of the Dead.",
                 "Мягко примириться со старением и смертью — в духе мексиканского Дня мёртвых."),
    "dearme": ("Write letters to your future self; they stay sealed until the day you choose.",
               "Письма себе в будущее, запечатанные до выбранного дня."),
    "glow": ("Write down your wins, big and small, and get praised for them. Kinder to yourself.",
             "Записывать свои победы, большие и маленькие, и получать за них похвалу."),
    "prism": ("Choose who you want to be in each part of life: partner, parent, colleague, friend.",
              "Выбрать, каким быть в каждой сфере жизни: партнёром, родителем, коллегой, другом."),
    "theusual": ("A diary of the cafés you keep coming back to: each gets a page and a sugar packet, and every cup leaves a coffee stain on the page.",
                 "Дневник кофеен, куда ты возвращаешься: у каждой своя страница и сахарный пакетик, а каждая чашка оставляет на странице кофейный след."),
    "sill": ("Try new things again: sow a seed from a catalogue of new things, water it each time you go back, and when it blooms it's yours.",
             "Снова пробовать новое: посади семя из каталога нового, поливай каждый раз, когда возвращаешься, — расцвело, значит твоё."),
    "cellar": ("Fewer impulse buys: every wish ages as a bottle in a cellar; open what you still want, pour the rest into your dream.",
               "Меньше импульсивных покупок: каждое желание выдерживается бутылкой в погребе; открой то, что всё ещё хочется, остальное вылей в мечту."),
    "carriage": ("A diary, index cards, telegrams and letters on a typewriter: nothing can be erased, so you write slower and more honestly.",
                 "Дневник, карточки, телеграммы и письма на пишущей машинке: стереть ничего нельзя, поэтому пишешь медленнее и честнее."),
    "errand": ("Shopping as a courier sim: the household orders, each shop learns its shelves, and every delivered waybill pays in brass tokens.",
               "Покупки как симулятор курьера: домашние заказывают, магазины запоминают полки, а каждая доставленная накладная платит латунными жетонами."),
    "windup": ("A little movement all day long: nine pixel-art tin toys, each wound for two hours by a minute or three of squats, balance or breathing.",
               "Понемногу, но весь день: девять пиксельных жестяных игрушек, каждую на два часа заводит пара минут приседаний, баланса или дыхания."),
    "archipelago": ("Make friends and keep them for years: everyone you meet is an island, and every hour together builds the bridge.",
                    "Заводить друзей и не терять их годами: каждый новый человек — остров, а каждый час вместе строит мост."),
    "shapito": ("Step out of your comfort zone a little every day: your fears become circus acts, and the bill offers three small real-life numbers a day.",
                "Выходить из зоны комфорта понемногу каждый день: страхи становятся цирковыми номерами, а афиша предлагает три небольших настоящих номера в день."),
    "biohacker": ("Over a thousand evidence-graded protocols for sleep, movement, food, stress and mood, each tried on you for 14 days before it enters your firmware.",
                  "Больше тысячи протоколов с оценкой доказательности — сон, движение, еда, стресс, настроение; каждый 14 дней испытывается на тебе, прежде чем попасть в прошивку."),
    "lodger": ("A slow, quiet haunting on your own photos: someone already lives in your flat, and after two weeks of marks, notes and radio static you help them leave.",
               "Тихая, медленная жуть на твоих собственных фото: в квартире уже кто-то живёт, и через две недели следов, записок и радиошума ты помогаешь ему уйти."),
    "capsule": ("A small present every day from your past self: fill a capsule machine with little joys, outings and notes, forget them, and turn the crank for one a day.",
                "Маленький подарок каждый день от себя прошлого: заправь автомат с капсулами мелочами, опытом и записками, забудь — и крути ручку раз в день."),
    "papertrail": ("A budget kept like a detective's case file: spending is evidence, categories are suspects, and patterns open cases you close with a verdict.",
                   "Бюджет как дело сыщика: траты — улики, категории — подозреваемые, а почерк в уликах открывает дела, которые вы закрываете вердиктом."),
    "pilgrim": ("A pilgrim's pass: sit ten minutes without the phone at a church, a mosque, a spring or an old tree, and get a stamp inked by the sun and the weather.",
                "Книжка паломника: посидите десять минут без телефона у храма, мечети, родника или старого дерева — и получите печать, которую раскрасили солнце и погода."),
    "horae": ("A book of hours for your own practices: hours by the sun, a bell for each, and what you keep written into an illuminated manuscript.",
              "Часослов для своих практик: часы по солнцу, колокол на каждый, а соблюдённое вписывается в иллюминированную рукопись."),
    "lot": ("Be drawn one of the 117 billion people who ever lived and read their life: the open doors, the shut ones, and what was left behind.",
            "Вытянуть жребий из 117 миллиардов когда-либо живших людей и прочитать свою жизнь: какие двери были открыты, какие закрыты и что осталось после."),
    "counterweight": ("Put a worry on a brass balance as a stone, and weights with arguments go on the other pan until it tips.",
                      "Положить тревогу камнем на латунные весы, а на другую чашу — гирьки с доводами, пока не перевесит."),
    "underbed": ("Feed a pet under your bed with fear: horror films and books, a little news. It guards your own fears at night.",
                 "Кормить страхом питомца под кроватью: ужастики, книги ужасов, немного новостей. Твои страхи он сторожит по ночам."),
    "curator": ("Sort your phone's gallery like a museum storeroom: a crate a month, one gesture per photo, and the space you free builds the museum.",
                "Разбор галереи как работа хранителя музея: по ящику на месяц, по жесту на фото, а освобождённое место достраивает музей."),
    "softlanding": ("A calorie counter where every day is a balloon flight: land in your norm and you reach the next village and its recipe.",
                    "Счётчик калорий, где каждый день — полёт на воздушном шаре: попал в свою норму — долетел до следующей деревни, а там дают рецепт."),
    "nooklings": ("Catch the cosy moments of your day into glowing jars; six little lodgers of a pixel room eat them.",
                  "Собирай уютные минуты дня в банки — ими кормятся шестеро жильцов пиксельной комнаты."),
    "undermat": ("A week in someone's flat abroad: notes in every corner on what to cook, watch, hear and read.",
                 "Неделя в чужой квартире за границей: записки во всех углах — что приготовить, посмотреть, послушать и почитать."),
    "farwalker": ("A pedometer that walks you round the real world: every border a stamp, every km a coin for a train or a ship.",
                  "Шагомер-кругосветка: твои шаги ведут путника по настоящей карте мира. За каждую границу в паспорте появляется штамп, за каждый километр — монета на поезд или корабль."),
    "aloft": ("A training log where five elemental spirits keep your floating island in the sky.",
              "Дневник тренировок, в котором пять духов стихий держат в небе твой летучий остров."),
    "reelkin": ("Films and series raise a small pet in a projectionist's booth, and every film seats a spectator in your hall.",
                "Дневник фильмов и сериалов с питомцем, который живёт в будке киномеханика и растёт с каждым просмотром."),
    "pumpling": ("Log your workouts, and a team of pets trains with you and grows on rest days.",
                "Записывайте тренировки, а команда питомцев тренируется с вами и растёт в дни отдыха."),
    "kitchenwitch": ("A recipe book where every moon you cook something you've never made.",
                "Книга рецептов, где раз в луну вы готовите что-то совсем новое."),
    "keyling": ("Note how much you wrote, and the residents of your keyboard eat your words.",
                "Отмечайте, сколько написали, – и ваши слова съедят жители клавиатуры."),
    "songling": ("A pet that grows from the music you play in any player.",
                 "Питомец растёт от музыки, которую вы слушаете в любом плеере."),
    "mimic": ("Video games, board games and tabletop RPGs on one pixel shelf, with a mimic that eats what you finish.",
              "Видеоигры, настолки и НРИ на одной пиксельной полке и мимик, который ест пройденное."),
    "insidejob": ("Your limiting beliefs are a bank that keeps what you forbade yourself: put a crew together and take it back.",
                  "Убеждения, которые мешают жить, — банк с тем, что ты себе запретил: собери команду и забери своё."),
    "silverlining": ("Draw tarot with no bad cards: an auntie finds the good in every card and gives you an omen to watch for today.",
                     "Гадать на таро без плохих карт: тётушка в каждой найдёт хорошее и даст примету на сегодня."),
    "unwritten": ("Keep a bookshop of books that don't exist: a customer a day, and you write the title, first line and blurb.",
                  "Книжная лавка, где продаются несуществующие книги: каждый день приходит покупатель, и ты придумываешь ему книгу."),
    "dyer": ("Eat thirty different plants a week and each one paints a fairy-tale kingdom back to colour. No calories, no bans.",
             "Тридцать разных растений за неделю: каждое возвращает краски сказочному королевству. Без калорий и запретов."),
    "rootlings": ("Catch the spirits of your real houseplants: real sun on the sill, a finger in the soil instead of a calendar, cuttings that hatch, real pests.",
                  "Ухаживать за настоящими комнатными растениями вместе с их пиксельными духами: свет по настоящему солнцу, полив по проверке пальцем, черенки и бои с вредителями."),
    "honours": ("Get enamel badges for the small deeds of your day, with an order, a stamp and a fanfare. Nothing to plan and no streaks.",
                "Получать эмалевые значки за маленькие дела дня, с приказом, печатью и фанфарами. Ничего не нужно планировать, и никаких серий."),
    "tsukumo": ("The things of your hobbies wake into little spirits with practice and keep growing for years in a pixel-art Japanese house.",
                "Вещи ваших хобби от занятий оживают и годами растут маленькими духами в пиксельном японском доме."),
    "hoard": ("A camera for moments worth keeping: three a day, kept as pixel-art treasure.",
              "Камера для моментов, которые хочется сохранить: три в день, как пиксельные сокровища."),
}

CATS = [
    ("calm", ("Calm and worry", "Спокойствие и тревога"),
     ("Breathing, meditation, and a way through thoughts that won't let go.", "Дыхание, медитации и способ справиться с мыслями, которые не отпускают."),
     ["swisszen", "serene", "counterweight", "keeper", "kite", "spintop", "hushwood", "heartwood", "pilgrim", "horae", "longwave"]),
    ("focus", ("Focus and the phone", "Фокус и телефон"),
     ("Fewer feeds, fewer distractions, fewer impulse buys, and help giving something up.", "Меньше лент, отвлечений и импульсивных покупок и помощь, чтобы от чего-то отказаться."),
     ["focusshield", "obol", "unhook", "vigil", "cellar", "papertrail", "sidea", "rewind", "mimic", "reelkin", "songling", "rustle"]),
    ("habits", ("Habits, goals and the body", "Привычки, цели и тело"),
     ("Routines, chores, goals, fasting, cold water and walks, in a way you'll keep up.", "Привычки, дела, цели, голодание, закаливание и прогулки — так, чтобы не бросить."),
     ["dayquest", "waypoint", "podium", "hearthspell", "ember", "temper", "fogwalk", "lipovka", "stringer", "errand", "windup", "biohacker", "rootlings", "dyer", "aloft", "farwalker", "greenstreet", "softlanding", "curator", "overwinter", "ranger", "apothecary", "fieldscan", "postround", "opposite", "threshold", "pumpling"]),
    ("learn", ("Learning and reading", "Учёба и чтение"),
     ("Remember what you learn, read more, and keep trying new things.", "Запоминать выученное, читать больше и пробовать новое."),
     ["scriptor", "stele", "familiar", "sill", "tsukumo", "undermat", "yourmove", "keyling", "kitchenwitch"]),
    ("family", ("Family and friends", "Семья и близкие"),
     ("Time with your children and each other, bedtime stories, family photos, keeping in touch.", "Время с детьми и друг с другом, сказки на ночь, семейные фото, связь с близкими."),
     ["lantern", "campfire", "marbles", "tessera", "nighttrain", "party", "archipelago", "fridge", "matryoshka", "charms", "ties", "notch", "silverbox"]),
    ("self", ("You and your life", "Вы и ваша жизнь"),
     ("Your time, your wins, who you want to be, letters to the future, moments worth keeping.", "Ваше время, ваши победы, каким вы хотите быть, письма в будущее и моменты, которые стоит сохранить."),
     ["anyway", "calavera", "dearme", "glow", "prism", "shapito", "lodger", "capsule", "lot", "honours", "underbed", "unwritten", "silverlining", "insidejob", "hoard", "theusual", "carriage", "gossamer", "nooklings", "cabinet", "hob"]),
]

TEXT = {
    # Home hero.
    "c.hero.eyebrow": ("Stillcraft · 93 free apps", "Stillcraft · 93 бесплатных приложения"),
    "c.hero.title": ("Small apps for <em>everyday life</em>.", "Маленькие приложения <em>для обычной жизни</em>."),
    "c.hero.lede": ("Calm down, focus, keep a habit, learn, spend more time with the people you love. 92 apps for Android and one for Windows: free, open source, no ads and no accounts, in English and Russian.",
                    "Успокоиться, сосредоточиться, не бросить привычку, учиться, больше времени проводить с близкими. 92 приложения для Android и одно для Windows: бесплатно, с открытым кодом, без рекламы и аккаунтов, на русском и английском."),
    "c.hero.cta": ("Find an app", "Найти приложение"),
    "c.hero.all": ("All apps with screenshots", "Все приложения со скриншотами"),
    # Home catalogue.
    "c.eyebrow": ("Find an app", "Найти приложение"),
    "c.title": ("What would you like help with?", "С чем помочь?"),
    "c.lede": ("Six groups, one line about each app. Tap one for screenshots and the download.", "Шесть групп, по строчке о каждом приложении. Нажмите на любое — там скриншоты и скачивание."),
    "c.more": ("Screenshots of every app", "Скриншоты всех приложений"),
    "c.moreMoments": ("More moments", "Ещё ситуации"),
    # Apps page.
    "c.ap.eyebrow": ("All Stillcraft apps", "Все приложения Stillcraft"),
    "c.ap.title": ("93 apps, <em>grouped by what they help with.</em>", "93 приложения, <em>по задачам.</em>"),
    "c.ap.lede": ("Pick a group or search. Every app is free, works without an account and keeps your data on the device.",
                  "Выберите группу или найдите поиском. Все приложения бесплатные, работают без аккаунта и хранят данные на устройстве."),
    "c.all": ("All", "Все"),
    "c.search": ("Search: sleep, habit, kids, anxiety…", "Поиск: сон, привычка, дети, тревога…"),
    "c.none": ("Nothing found. Try another word, or pick a group.", "Ничего не нашлось. Попробуйте другое слово или выберите группу."),
}

# Extra words a person might search for, in both languages, that the plain line doesn't say.
WORDS = {
    "swisszen": "breath meditation mindfulness wim hof дыхание медитация осознанность",
    "serene": "meditation sleep relax affirmation медитация сон расслабление аффирмации",
    "keeper": "anxiety worry ocd intrusive тревога беспокойство окр навязчивые мысли",
    "kite": "mindfulness present moment here now wandering mind grounding senses reminder notification осознанность настоящее здесь и сейчас блуждающие мысли заземление чувства напоминание",
    "sidea": "music album vinyl record turntable cassette tape spotify listening streaming музыка альбом винил пластинка проигрыватель кассета плёнка слушать стриминг",
    "party": "date couple quest quests fantasy rpg dnd d20 dice adventure game knights heraldry coat of arms partner relationship свидание пара квест квесты фэнтези ролевая игра кость приключение рыцари герб отношения отряд",
    "spintop": "lucid dream dreams dreaming sleep dream journal diary reality check mild wbtb inception totem spinning top nightmare осознанный сон сны сновидения дневник снов проверка реальности сон волчок начало кошмар",
    "hushwood": "meditation meditate mindfulness sitting stillness breathing breathwork box breathing 4-7-8 yoga timer tracker pixel art cozy cosy forest animals nature sounds rain birds tingsha guardian медитация осознанность тишина дыхание йога таймер трекер пиксель лес звери природа звуки птицы хранитель",
    "heartwood": "heartwood tree trees befriend friend friendship nature outdoors walk walks park forest oak birch linden maple hug tree hugging rings tree rings cross-section age girth species key field guide herbarium leaves pressed leaf bark rubbing frottage timelapse hollow note to future self grove mycelium seasons map qr forester notebook сердцевина дерево деревья подружиться друг дружба природа на улице прогулка прогулки парк лес дуб берёза липа клён обнять объятие кольца годовые кольца спил возраст обхват порода определитель гербарий листья лист кора фроттаж таймлапс дупло записка себе в будущее роща грибница времена года карта лесник блокнот",
    "longwave": "sleep insomnia fall asleep bedtime night white noise brown noise rain sounds sea waves train nature sounds sleep timer radio valve tube vintage shipping forecast body scan cognitive shuffle 4-7-8 breathing counting relaxation qsl сон бессонница уснуть заснуть засыпание ночь белый шум коричневый шум дождь море волны поезд звуки природы таймер сна радио приёмник ламповый морская сводка сканирование тела дыхание счёт расслабление",
    "sill": "new things try something new novelty curiosity hobby hobbies new experiences comfort zone bucket list learn new skills explore food cuisine music art crafts pottery language people courage plants garden windowsill seeds pots watering bloom herbarium gift friend новое попробовать что-то новое новизна любопытство хобби увлечения новый опыт зона комфорта список желаний научиться навыки кухня еда музыка искусство ремёсла язык люди смелость растения сад подоконник семена горшки полив цветение гербарий подарок друг",
    "rewind": "watchlist movies films cinema series tv shows books comics manga albums video rental vhs tape kinopoisk imdb letterboxd goodreads список посмотреть потом фильмы кино сериалы книги комиксы манга альбомы видеопрокат кассета кинопоиск",
    "focusshield": "focus pomodoro windows block work фокус помодоро работа блокировка",
    "obol": "social media scrolling tiktok screen time соцсети лента экранное время",
    "unhook": "quit smoking alcohol addiction бросить курить алкоголь зависимость",
    "vigil": "abstinence fast vow sugar отказ пост обет сахар",
    "dayquest": "habit rpg game todo habitica привычки игра задачи",
    "waypoint": "goals plan okr цели план",
    "podium": "timer speed routine таймер скорость рутина",
    "hearthspell": "cleaning chores home уборка дом дела",
    "ember": "fasting diet weight голодание диета вес",
    "temper": "cold shower sauna ice закаливание холод душ баня",
    "fogwalk": "walk steps city map прогулка шаги город карта",
    "scriptor": "study memory notes spaced repetition учёба память конспект",
    "stele": "language words anki flashcards язык слова карточки",
    "familiar": "books reading pet книги чтение питомец",
    "lipovka": "lipovka post postman pedometer step counter steps walking walk walks letters mail village cozy pixel game stories telegram stamps map weather почта в липовке почтальон шагомер шаги ходьба прогулки письма деревня уютная пиксельная игра истории телеграммы марки карта погода",
    "ranger": "ranger running run runner run tracker running journal running diary running log jogging jog marathon half marathon 5k 10k trail running strava garmin samsung health mi fitness zepp polar coros health connect gpx tcx fit import gps tracker heart rate heart rate zones pulse trimp training load fitness fatigue recovery rest resting heart rate hrv steps step counter pedometer shoes mileage personal records pace gamification game rpg fantasy bestiary creatures monsters ranks outpost map fog of war openstreetmap weather moon full moon sunrise rain fog campaigns challenges music playlist dog следопыт бег пробежки пробежка бегун трекер бега беговой дневник дневник пробежек джоггинг марафон полумарафон трейл страва гармин пульс пульсовые зоны нагрузка тренировки закалка усталость восстановление отдых пульс покоя вариабельность шаги шагомер кроссовки пробег рекорды темп игра геймификация фэнтези сказка бестиарий существа чудовища звания застава карта погода луна полнолуние рассвет дождь туман походы челленджи музыка собака",
    "apothecary": "apothecary зельевар expiry date expiration best before use by shelf life food waste fridge refrigerator freezer pantry cupboard groceries leftovers meal prep kitchen inventory food tracker medicine cabinet medicine box first aid kit medicines pills vitamins supplements course opened after opening potion potions brew cauldron recipes alchemy witch magic cosy cozy game gamification guild срок годности просрочка просроченные продукты холодильник морозилка шкаф запасы продукты остатки еда выбрасывать еду пищевые отходы аптечка лекарства таблетки витамины курс вскрыто после вскрытия зелья зелье котёл рецепты алхимия лавка уютное игра гильдия",
    "fieldscan": "fieldscan сканер scanner anomaly anomalies creatures monsters cryptids bestiary collection trail camera trail cam night ir infrared riddles rites location based game gps walking walks urban exploration city mystery openstreetmap bridges fountains stairs bus stops compass torch morse sing note fog full moon beta аномалии аномалия сканер существа монстры бестиарий коллекция фотоловушка ночная съёмка загадки обряды игра по геолокации gps прогулки город городские легенды тайна мосты фонтаны лестницы остановки компас фонарик морзе спеть ноту туман полнолуние бета",
    "postround": "postround poste restante postman post office mail letters postcards parcels telegrams newspaper delivery round neighbourhood district real map openstreetmap house numbers addresses residents neighbours correspondence pen pals stories walking walks gps location based game steps pedometer health connect stamps pixel art cozy до востребования почтальон почта письма открытки посылки телеграммы газета разносить участок район настоящая карта номера домов адреса жильцы соседи переписка истории прогулки ходьба игра по геолокации gps шаги шагомер марки пиксель уютная",
    "opposite": "opposite the house opposite advent calendar december christmas new year winter countdown 24 windows sunset dusk daily deed small task kindness rooms neighbours residents mystery detective deduction whodunit secret santa clues notebook suspects tree ornaments presents gifts surprise candles cozy дом напротив адвент календарь адвент-календарь декабрь новый год рождество зима 24 окна закат дело дня огонёк доброе дело комнаты соседи жильцы загадка детектив тайный дед дед мороз улики блокнот подозреваемые ёлка елка игрушки подарки сюрприз свечи уютный",
    "yourmove": "yourmove your move chess by post correspondence chess letters pen pal penpal mail post stamps stamp album engine opponent bot characters story lighthouse teacher slow chess cozy board pieces knight bishop queen king endgame opening kitchen board analysis presents gifts rating titles ваш ход шахматы по переписке переписка письма почта марки альбом марок движок соперник собеседники маяк учительница кружок доска фигуры конь слон ферзь король эндшпиль дебют кухонная доска анализ подарки разряд разряды уютные шахматы",
    "rustle": "rustle virtual pet tamagotchi pet creature critter cozy game pixel art focus timer focus phone face down put the phone down screen time digital wellbeing outings explore finds loot collect crafting workshop furniture clothes dress up kitchen cooking battery charging stove camera window weather sleep night widget achievements streak requests boko шуршик виртуальный питомец тамагочи питомец зверёк уютная игра пиксель пиксельная графика фокус таймер отложить телефон экраном вниз экранное время цифровой детокс вылазки прогулки находки коллекция мастерская мебель одежда одёжка кухня готовка батарея зарядка печка камера окно погода сон ночь виджет достижения серия просьбы",
    "cabinet": "cabinet of curiosities collection collector collecting catalog catalogue inventory museum halls shelves cabinets records vinyl books coins numismatics banknotes cans bottles figurines toys magnets fridge magnets stamps postcards model cars hobby flea market swap duplicates wish list series do i have it duplicate check photo search image recognition similar background removal cut out exhibition visitors arrivals book backup pdf csv кабинет редкостей коллекция коллекционер коллекционирование каталог учёт опись музей залы полки шкафы пластинки винил книги монеты нумизматика банкноты банки бутылки фигурки игрушки магниты марки открытки модели машин хобби барахолка обмен дубли дубликаты список желаний серии есть ли у меня поиск по фото распознавание похожие убрать фон выставка посетители книга поступлений резервная копия",
    "hob": "hob house spirit domovoi home inventory household things stuff junk clutter declutter clear out organizer organiser storage where is it find lost things rooms shelves boxes numbered boxes labels pantry garage dacha shed attic lend lent borrowed borrow reminder kids children clothes hand-me-downs grow into sizes growth height shoe size season christmas decorations tent backup csv домовой учёт вещей дом вещи хлам барахло разбор порядок хранение где лежит найти потерял комнаты полки антресоль коробки кладовка гараж дача сарай чердак одолжить одолжил взял напоминание дети детская одежда на вырост размеры рост размер ноги сезон ёлочные игрушки палатка резервная копия",
    "threshold": "threshold portal alarm alarm clock wake up wake-up morning routine morning ritual weekday schedule open app launch app youtube spotify yandex music kinopoisk radio internet radio stream playlist news exercise workout snooze gentle alarm lock screen finds worlds journal holidays vacation порог портал будильник проснуться подъём утро утренний ритуал расписание по дням недели открыть приложение запуск приложения ютуб спотифай яндекс музыка кинопоиск радио интернет-радио плейлист новости зарядка отложить мягкий будильник экран блокировки находки миры журнал праздники отпуск",
    "charms": "charms grimoire kids children child chores chore chart routine tracker habit tracker reward chart rewards morning routine bedtime routine teeth homework tidy room school bag reminders without nagging parents mentor magic spells potions cauldron engraving photo camera creatures bestiary owl cat fox gamification чары гримуар дети ребёнок дела обязанности распорядок режим трекер привычек награды поощрения утро вечер отбой зубы уроки уборка портфель без напоминаний родители наставник магия волшебство заклинания зелья котёл гравюра фото камера существа бестиарий сова кот лиса геймификация",
    "matryoshka": "matryoshka nesting doll russian doll gift gifts present birthday surprise wrapping unwrap quest treasure hunt riddle puzzle code word place location time capsule gesture locks layers encryption shared gift group gift friends family voice note photo note reply матрёшка подарок подарки день рождения сюрприз вручение квест загадка кодовое слово место время жест замки слои шифрование общий подарок вместе друзья семья голос фото записка отклик",
    "gossamer": "gossamer thought catcher thoughts ideas idea capture quick capture inbox notes note taking zettelkasten mind map web spider threads links connections second brain voice notes widget dew wind forgetting cocoon butterfly insight journal паутинка ловец мыслей мысли идеи идея заметки записать быстро входящие связи нити паутина паук карта мыслей второй мозг голос виджет роса ветер кокон бабочка озарение дневник",
    "greenstreet": "green street greenstreet beta farming game farm cozy game stardew pixel art garden gardening beds seeds plants harvest walking walk gps location based real map openstreetmap district neighbours neighbors stories hens eggs cooking recipes fishing fair market finds foraging mushrooms зелёная улица зеленая улица бета ферма фермерская игра уютная игра пиксельная грядки семена огород сад урожай прогулки ходьба gps настоящая карта район соседи истории куры яйца кухня рецепты рыбалка ярмарка рынок находки грибы",
    "overwinter": "overwinter wellbeing diary health diary symptom tracker symptoms mood tracker mood energy fatigue pain headache migraine sleep tracker sleep journal barometer pressure weather sensitivity meteosensitive patterns triggers coffee doctor report pdf polar station arctic weather station beaufort cloud cyclone forecast зимовка дневник самочувствия самочувствие дневник здоровья симптомы трекер настроения настроение силы усталость боль головная боль мигрень сон давление барометр метеозависимость метеочувствительность погода закономерности триггеры кофе врач отчёт pdf полярная станция арктика метеостанция бофорт облачность циклон прогноз",
    "fridge": "fridge refrigerator door couple couples partner relationship shopping list groceries chores whose turn notes sticky notes magnets worries confession envelope love wishes gifts household home sync wifi qr холодильник дверца пара отношения партнёр покупки список продуктов дела чья очередь записки стикеры магниты тревоги признание конверт любовь желания подарки быт дом синхронизация",
    "stringer": "stringer correspondent reporter newspaper paper district editor telegram assignment assignments task walk walks walking outdoors go outside every day street city photo photography photo walk street photography camera halftone newsprint caption sunday issue rubrics doors cats signs letters alphabet press card flash dusk внештатник корреспондент репортёр газета районная редактор телеграмма задание задания прогулка прогулки на улицу каждый день улица город фото фотография фотопрогулка уличная фотография камера растр подпись воскресный номер рубрики двери коты вывески буквы алфавит пресс-карта молния сумерки",
    "errand": "errand courier delivery shopping shopping list grocery groceries list shop shops supermarket store waybill order orders family household chat messenger share list rush weight bag string bag cold aisle shelf route budget receipt prices price tracker inflation cheaper game gamification tokens depot bicycle van rank badges simulator посыльный курьер доставка покупки список покупок продукты магазин супермаркет накладная заказ заказы семья домашние мессенджер чат молния вес авоська термобокс полки маршрут бюджет чек цены подорожало дешевле игра геймификация жетоны депо велосипед фургон звание знаки симулятор habits привычки",
    "windup": "windup wind-up wind up tin toys toy shelf exercise snacks exercise snack movement move all day micro workout workout fitness bodyweight no equipment desk office stretch mobility balance squats push-ups plank breathing posture kettle music box melody tune drum pins score records alloys brass copper silver gold fair weekend fair skier hare diver miner clown sailor reminder habits gamification pixel art завод заводные игрушки жестяные полка разминка разминки движение весь день упражнения фитнес без инвентаря за столом офис растяжка баланс приседания отжимания планка дыхание осанка чайник шкатулка мелодия барабан штифты партитура пластинки латунь медь серебро золото ярмарка выходные лыжник заяц водолаз шахтёр клоун морячок напоминание привычки геймификация пиксель-арт habits привычки",
    "archipelago": "archipelago islands island bridges bridge sea chart map friends friendship make friends new people meet people meeting strangers social anxiety shy introvert courage small talk conversation invite invitation loneliness lonely community club hobby group keep in touch follow up second time reminder hall 50 hours 200 hours close friend acquaintance lighthouse party gathering introduce mutual friends years anniversary journal мостки архипелаг острова мосты карта друзья дружба знакомства новые люди познакомиться незнакомцы стеснительность интроверт смелость разговор пригласить одиночество клуб общение второй раз поддерживать связь маяк вечеринка годовщина журнал",
    "shapito": "shapito big top circus comfort zone step out courage brave fear fears anxiety social anxiety shy shyness exposure exposure therapy challenge challenges daily challenge dare self improvement growth confidence public speaking phone calls saying no boundaries conflict asking for help vulnerability feelings unknown change decisions new places alone mistakes perfectionism imperfection beginner sharing work praise money charging being seen body image sport discomfort drum roll applause lion tamer ringmaster clown juggler magician strongman tightrope trapeze pixel art game шапито цирк зона комфорта выйти из зоны комфорта смелость страх страхи тревога социальная тревожность стеснительность застенчивость экспозиция вызов челлендж саморазвитие рост уверенность публичные выступления звонки сказать нет границы конфликты просить помощи уязвимость чувства неизвестность перемены решения новые места одному ошибки перфекционизм новичок показать творчество похвала деньги быть замеченным тело спорт дискомфорт барабанная дробь аплодисменты укротитель конферансье клоун жонглёр фокусник силач канатоходец гимнаст пиксель игра",
    "papertrail": "paper trail budget budgeting money finance personal finance expense expenses expense tracker spending spend tracker money tracker envelope budget daily budget allowance payday salary bills rent subscriptions subscription tracker cancel subscriptions savings goals save money impulse buys bank notifications cash detective noir mystery case cases clue clues suspect suspects mugshot police verdict gamification бюджет деньги финансы личные финансы расходы трата траты учёт расходов трекер расходов конверты дневной бюджет аванс зарплата счета аренда подписки отменить подписки накопления цели копить импульсивные покупки уведомления банка наличные детектив нуар сыщик дело дела улика улики подозреваемый подозреваемые вердикт висяк",
    "pilgrim": "pilgrim pilgrimage pilgrim's pass credential camino santiago passport stamps stamp collection places of power sacred places holy places church churches cathedral chapel mosque synagogue temple monastery shrine spring springs holy spring old tree trees stone stones hill viewpoint peak walk walks wander explore exploration city walks travel trips mindfulness meditation silence quiet stillness solitude digital detox phone free screen time without phone ten minutes sit sitting outdoors nature openstreetmap map rumour notes journal подорожная паломник паломничество паломничество книжка паломника печати печать коллекция места силы святые места храм храмы церковь собор часовня мечеть синагога дацан монастырь родник родники источник старое дерево дерево камень холм смотровая вершина прогулка прогулки бродить исследовать путешествия осознанность медитация тишина покой уединение цифровой детокс без телефона экранное время десять минут посидеть природа карта слух записки дневник",
    "horae": "horae book of hours hours canonical hours liturgy of the hours monastery monk benedictine rule of life prayer prayers psalms bell bells singing bowl meditation mindfulness breathing breathwork box breathing 4-7-8 metta loving kindness beads rosary mala tasbih lestovka jesus prayer hesychasm zen zazen stoic stoicism seneca marcus aurelius examen ignatius reading lectio divina gratitude journal silence candle ritual rituals spiritual practice spirituality esoteric sun sunrise sunset illuminated manuscript medieval calligraphy часослов часы книга часов канонические часы богослужение монастырь монах устав молитва молитвы псалмы колокол колокола поющая чаша медитация осознанность дыхание дыхательные практики метта чётки четки лестовка мала тасбих розарий иисусова молитва исихазм дзен дзадзэн стоики стоицизм сенека марк аврелий экзамен лектио чтение благодарность дневник молчание тишина свеча ритуал ритуалы духовные практики духовность эзотерика солнце восход закат рукопись средневековье буквица",
    "lot": "lot lots draw a lot fate life simulator life sim bitlife 1 in 8 billion one in eight billion 117 billion everyone who ever lived history world history historical life peasant serf slave medieval middle ages ancient stone age early modern demography population birth lottery inequality privilege chance odds probability statistics census parish register genealogy family tree ancestors ancestry heirloom inheritance great-grandchildren dynasty epitaph choices doors witness gratitude perspective reflection memento mori black death mongols socrates ibn battuta жребий судьба симулятор жизни один из восьми миллиардов 117 миллиардов все жившие история всемирная история историческая жизнь крестьянин крепостной раб средневековье древний мир каменный век новое время демография население лотерея рождения неравенство привилегии шанс шансы вероятность статистика перепись метрическая книга генеалогия родословная предки наследство реликвия правнуки род эпитафия выбор двери свидетель благодарность взгляд со стороны размышление чёрная смерть монголы сократ ибн баттута",
    "counterweight": "counterweight counter weight противовес противовеса anxiety anxious worry worries worrying fear fears overthinking rumination catastrophizing catastrophising cbt stoic stoicism seneca reassurance optimism optimist positive arguments facts balance scale scales weights brass stone pebble panic 3am sleepless тревога тревоги тревожность беспокойство страх страхи накручивание катастрофизация кпт стоики сенека оптимизм оптимист доводы аргументы факты весы гирьки гиря камень на душе галька паника бессонница деньги увольнение смерть здоровье отношения",
    "underbed": "underbed under bed bogey bogeyman boogeyman monster under the bed pet virtual pet tamagotchi creature ghost zombie vampire werewolf doll kikimora horror horror movies horror films horror books scary scared fear fears anxiety news doomscrolling night light nightlight night watch goosebumps jump scare film night popcorn graveyard grave epitaph gothic folk horror j-horror halloween full moon бука букa подкроватник чудище под кроватью питомец тамагочи призрак зомби вампир оборотень кукла кикимора ужасы ужастики фильмы ужасов книги ужасов страх страхи тревога новости думскроллинг ночник дозор мурашки кино попкорн погост кладбище могилка эпитафия готика фолк хэллоуин полнолуние",
    "curator": "curator gallery photos photo cleaner clean up gallery delete photos duplicates duplicate photos blurred screenshots storage free space phone memory swipe sort albums museum storeroom crates exhibits act of write-off wings куратор запасник галерея фото фотографии почистить галерею удалить фото дубли дубликаты смазанные скриншоты память место на телефоне свайп разобрать альбомы музей ящики экспонаты акт списания крылья",
    "softlanding": "soft landing calories calorie counter kcal diet nutrition food diary meal tracker weight loss lose weight keep weight protein macros barcode scanner qr label photo open food facts recipes dishes portions plates balloon flight villages route hangar logbook мягкая посадка калории счётчик калорий ккал диета питание дневник питания похудеть вес белки бжу штрихкод сканер честный знак этикетка рецепты блюда порции тарелка воздушный шар полёт деревни маршрут ангар журнал",
    "nooklings": "nooklings cosy cozy cosiness hygge comfort moments small joys noticing jar jars pantry catch sound recording rain kettle tea lamp light photo quiet silence walk steps pedometer weather snow lodgers pets pet cat dormouse moth bullfinch hedgehog raccoon pixel room stove dreams gifts jam diary mood ютята уют уютный уютные моменты маленькие радости замечать банка банки кладовка поймать звук запись дождь чайник чай лампа свет снимок тишина прогулка шаги шагомер погода снег жильцы питомцы питомец кот соня моль снегирь ёжик енотик пиксельная комната печка сны подарки варенье дневник настроение",
    "undermat": "under the mat undermat culture countries abroad travel from home host flat apartment week notes recipes cooking films movies music records books reading holidays traditions languages words naples kyoto oaxaca bergen seoul lyon tbilisi kolkata salvador lisbon galway istanbul ключ под ковриком культура страны заграница путешествие из дома хозяин квартира неделя записки рецепты кухня фильмы кино музыка пластинки книги чтение праздники традиции языки слова неаполь киото оахака берген сеул лион тбилиси калькутта салвадор лиссабон голуэй стамбул",
    "farwalker": "farwalker round the world around the world pedometer step counter steps walking walk travel journey world map atlas countries borders passport stamps trains ships sea voyage cape ends of the earth weather local time natural earth кругосветка вокруг света кругосветное путешествие шагомер шаги ходьба прогулки путешествие карта мира атлас страны границы паспорт штампы поезд корабль море мыс края земли погода местное время",
    "aloft": "aloft floating island sky island training log workout log fitness sports exercise running walking cycling swimming weights strength gym yoga stretching boxing hiit intervals training load srpe rpe overtraining rest day injury recovery elements spirits sylph golem undine dryad salamander voyage laputa avalon weather guests pixel art летучий остров остров в небе журнал тренировок тренировки фитнес спорт бег ходьба велосипед плавание силовая зал йога растяжка бокс интервалы нагрузка перетренированность отдых травма восстановление стихии духи сильф голем ундина дриада саламандра путешествие лапута буян авалон погода гости пиксель-арт",
    "reelkin": "reelkin film diary movie diary watchlist films movies tv series shows letterboxd tracker cinema projector booth projectionist virtual pet tamagotchi ticket stubs popcorn rating genres noir horror animation comedy post-credits scene season ticket cliffhanger awards pixel art бобина дневник кино фильмы кино сериалы трекер вотчлист кинотеатр проектор будка киномеханик питомец тамагочи корешки билеты попкорн оценки жанры нуар хоррор мультфильмы комедии сцена после титров абонемент клифхэнгер премия пиксель-арт",
    "pumpling": "pumpling workout log workout tracker gym training strength training weightlifting lifting fitness exercise sets reps weight bodyweight calisthenics home workout cardio running run walking plank routines programs program beginner progress records personal record pr stats statistics muscles body measurements weight loss virtual pet pets tamagotchi gamification pixel art share cards тренировки дневник тренировок трекер зал фитнес силовые штанга гантели подходы повторы вес свой вес воркаут дома кардио бег ходьба планка программы новичок прогресс рекорды статистика мышцы замеры похудение питомец питомцы тамагочи геймификация пиксель открытки habits привычки",
    "kitchenwitch": "kitchenwitch kitchen witch кухонная ведьма recipes recipe book cookbook cooking cook dinner new dishes meal ideas what to cook leftovers pantry spices herbs moon phases moon calendar wheel of the year sabbats witchcraft witchy cottagecore grimoire book of shadows sigils cooking timer рецепты книга рецептов кулинарная книга готовка кулинария ужин новые блюда что приготовить остатки кладовая специи травы фазы луны лунный календарь колесо года шабаш ведьма колдовство гримуар книга теней сигилы таймер learning and reading учёба и чтение",
    "keyling": "keyling клавишка writing tracker word count word counter writer novel book manuscript nanowrimo thesis stories chapters editing sprints writing sprint streak year goal author pet virtual pet tamagotchi pixel art keyboard mechanical keyboard keycaps switches typos письмо писатель писательство роман книга рукопись счётчик слов слова знаки авторский лист главы правка редактура спринт серия цель на год питомец тамагочи пиксель-арт клавиатура механическая клавиатура колпачки опечатки learning and reading учёба и чтение",
    "songling": "songling music pet music tracker scrobbler last.fm listening stats statistics spotify yandex music youtube music vk albums singles songs artists vinyl records cassette tapes playlist genres goals new albums discover virtual pet tamagotchi pixel art den posters lyrebird bestiary eggs listening history wrapped музыка питомец трекер музыки скробблер статистика прослушиваний спотифай яндекс музыка ютуб музыка вк альбомы синглы песни артисты группы винил пластинки кассеты плейлист жанры цели новые альбомы тамагочи пиксель-арт логово постеры бестиарий яйца история прослушиваний итоги года",
    "mimic": "mimic chest game shelf game collection backlog pile of shame games video games board games tabletop rpg ttrpg steam backloggd boardgamegeek bgg howlongtobeat covers rating reviews sessions screenshots genres pixel art мимик сундук полка игр коллекция игр бэклог куча позора игры видеоигры настолки настольные игры нри ролевые игры стим обложки оценки отзывы сессии скриншоты жанры пиксель-арт",
    "insidejob": "inside job heist bank robbery crew safe vault safecracker blueprint limiting beliefs beliefs core beliefs inner critic cbt cognitive behavioral therapy cognitive behavioural therapy cognitive distortions thinking traps mind reading catastrophizing should statements all or nothing evidence socratic questions behavioral experiments exposure self help mental health self esteem confidence permission rest asking for help perfectionism people pleasing дело века ограбление банк нельзя команда сейф ячейка медвежатник чертёж убеждения ограничивающие убеждения глубинные убеждения внутренний критик кпт когнитивно-поведенческая терапия когнитивные искажения ловушки мышления чтение мыслей катастрофизация долженствование всё или ничего доказательства сократические вопросы поведенческие эксперименты самопомощь психология самооценка уверенность разрешение отдых просить о помощи перфекционизм угодничество",
    "silverlining": "silver lining tarot tarot cards rider waite rider-waite 1909 pamela colman smith fortune telling fortune teller reading spread card of the day omen omens signs luck lucky good luck positive positive thinking optimism gratitude noticing good things hope comfort auntie grandma kitchen tea candle death tower happy predictions good news journal what came true к добру таро карты таро райдер уэйт гадание гадалка расклад карта дня примета приметы знак удача везение счастье позитив оптимизм благодарность замечать хорошее надежда утешение тётушка бабушка кухня чай свеча смерть башня хорошие предсказания сбылось шкатулка святки купала",
    "unwritten": "unwritten bookshop book shop bookstore second-hand books library books that don't exist imaginary books fake books writing creative writing writing prompts prompts story ideas fiction first line opening line blurb back cover title pen name epigraph table of contents zine print booklet cover design book covers pulp samizdat paperback critics reviews library card stamps oulipo six-word story lipogram imprint publisher cozy rain window weather лавка книжная лавка букинист библиотека ненаписанное ненаписанные книги книги которых нет выдуманные книги писать письмо творческое письмо писательство идеи для текста сюжет первая фраза аннотация обложка название псевдоним эпиграф оглавление зин печать книжка обложки бульварное самиздат критики рецензии формуляр штамп улипо рассказ в шесть слов липограмма издательство уют дождь окно погода",
    "dyer": "dyer dye dyehouse paint watercolour watercolor kingdom fairy tale gloom colour color plants plant diversity 30 plants thirty plants eat the rainbow rainbow vegetables fruit berries greens grains legumes nuts seeds herbs spices fermented kefir sauerkraut gut health microbiome fibre fiber healthy eating nutrition diet food tracker meal plate no calories picky eater new taste eight tries mindful eating slow eating quiet meal shelf jars recipes natural dyes onion skins red cabbage красильня краска акварель королевство сказка хмарь цвет растения разнообразие 30 растений тридцать растений радуга овощи фрукты ягоды зелень крупы бобовые орехи семена травы пряности квашеное кефир квашеная капуста микрофлора кишечник клетчатка здоровое питание питание еда тарелка без калорий нелюбимые овощи восемь проб осознанное питание тихая трапеза полка банки рецепты натуральные красители луковая шелуха",
    "rootlings": "rootlings rootling plants houseplants house plants indoor plants plant care plant care app plant journal plant diary watering watering reminder when to water soil moisture finger test windowsill sill window light light meter sun compass weather clouds winter rest dormancy radiators dry air humidity cactus succulents monstera spider plant ficus orchid pothos cuttings propagation rooting cuttings in water pests spider mites scale thrips mealybugs fungus gnats aphids whitefly root rot sunburn powdery mildew springtails plant doctor treatment pokemon pokédex pokedex catch them all gotta catch em all game boy pixel art pixel retro evolution creatures spirits collection dex herbarium gamification корешки растения комнатные растения цветы уход за растениями дневник растений полив напоминание о поливе когда поливать влажность земли подоконник окно свет солнце компас погода облака зимовка покой батареи сухой воздух кактус суккуленты монстера хлорофитум фикус орхидея черенки размножение укоренение вредители паутинный клещ щитовка трипсы мучнистый червец сциариды мошки тля белокрылка корневая гниль ожог мучнистая роса ногохвостки лечение покемон покедекс поймай их всех геймбой пиксель-арт ретро эволюция духи коллекция декс гербарий геймификация habits привычки habits, goals and the body привычки, цели и тело",
    "honours": "small honours honours honors badge badges pin badges enamel pins enamel badge pins medal medals order orders award awards decoration decorations soviet ussr vintage znachok pennant felt pennant fanfare ceremony stamp rubber stamp chancellery typewriter small deeds small wins little wins tiny wins everyday wins chores household cleaning wins journal done list done diary achievements achievement tracker gamification self praise self esteem kindness to yourself no streaks no habits evening review hard day bad day survived the day idleness rest collection workshop pixel art award sheet certificate friends значкист значки значок эмалевые значки медаль медали орден ордена награда награды наградной лист вымпел ссср советский фанфары печать приказ канцелярия малые дела маленькие победы подвиги подвиг бытовые дела уборка достижения похвала самооценка без серий тяжёлый день пережитый день безделье коллекция мастерская пиксель грамота друзья",
    "capsule": "capsule capsules gachapon gashapon capsule toy vending machine gumball machine crank coin present presents gift gifts surprise surprises treat treats self care self-care small joys little joys past self future self note to self notes kindness to yourself reward rewards hiding place hiding places treasure hunt riddle hard day bad day comfort mood weather rain snow sun weekend friday figures figurines collection shelf album memories forget sealed time capsule capsule machine daily ritual капсула капсулы гачапон автомат с капсулами игрушки из автомата ручка монетка подарок подарки сюрприз сюрпризы радость маленькие радости забота о себе себе прошлому себе будущему записка записки награда тайник тайники загадка тяжёлый день плохой день утешение настроение погода дождь снег солнце выходные пятница фигурки коллекция полка альбом воспоминания забыть запечатать капсула времени ритуал",
    "lodger": "lodger ghost ghosts haunting haunted haunted house horror cozy horror spooky creepy scary halloween mystery detective story clues investigation lodger tenant photos photo camera rooms flat apartment home house marks footprints shadow radio static notes letters cork board red thread unfinished business house spirit poltergeist candle lantern full moon домовой призрак привидение дух жилец квартира дом комнаты фото фотографии страшно жуть уютная жуть ужасы хоррор хэллоуин мистика тайна загадка детектив улики следы тень радио эфир записки письма доска красная нить незаконченное дело полнолуние свеча фонарь лоджер",
    "biohacker": "biohacker biohacking bio hacker biohacks longevity healthy life health wellbeing wellness protocols protocol evidence evidence-based science research studies self experiment self-experiment n=1 quantified self tracking tracker mood tracker sleep sleep hygiene light circadian rhythm movement exercise strength walking food nutrition diet water hydration cold shower hardening prevention check-up screening focus learning productivity stress breathing breath calm meditation mood happiness meaning gratitude people friends nature habits habit tracker trial trials lab gauges readings energy firmware mods upgrade version patch notes myths broken mods combos parcel cards rarity legendary blueprint cyanotype биохакер биохакинг долголетие здоровье здоровый образ жизни зож протоколы доказательность доказательная медицина наука исследования эксперимент на себе самоэксперимент n=1 трекер настроения сон гигиена сна свет циркадный ритм движение спорт сила ходьба еда питание диета вода холодный душ закаливание профилактика обследование чекап скрининг фокус обучение продуктивность стресс дыхание спокойствие медитация настроение счастье смысл благодарность люди друзья природа привычки испытание лаборатория показания энергия прошивка моды апгрейд версия патчноуты мифы сломанные моды комбо посылка карточки редкость легендарная чертёж синька habits привычки",
    "tsukumo": "tsukumo tsukumogami hobby hobbies hobby tracker practice practice log practise music guitar piano drawing painting watercolour knitting crochet embroidery sewing origami baking sourdough tea coffee cooking language japanese calligraphy writing reading chess go puzzles programming yoga running climbing dance garden bonsai pottery models woodcarving spirits pixel art japanese house candles kami game gamification years no guilt цукумо цукумогами хобби увлечения трекер хобби практика занятия музыка гитара фортепиано рисование акварель вязание вышивка шитьё оригами выпечка закваска чай кофе готовка язык японский каллиграфия писательство чтение шахматы го головоломки программирование йога бег скалолазание танцы огород бонсай гончарство модели резьба духи пиксель японский дом свечи ками игра геймификация годы без чувства вины",
    "carriage": "carriage typewriter typing type diary journal journaling notes writing write honest slow no backspace no delete index cards card drawer recipes lists telegram telegrams letter letters carbon copy ribbon red ribbon bell margin correction fluid typo strike out stamps folders drawer lock archive index underline paper yellowing wastebasket year ago counter office portable electric machine bluetooth keyboard pdf каретка пишущая машинка машинка печатать дневник записи заметки писать честно медленно без стирания карточки картотека рецепты списки телеграмма телеграммы письмо письма копирка копия лента красная лента звоночек край штрих опечатка забить иксами штампы папки ящик архив указатель подчёркивание бумага желтеет корзина год назад счётчик конторская походная электрическая клавиатура",
    "cellar": "cellar wine bottle impulse buying impulse buys shopping spending money save saving savings budget wishlist wish list want buy purchase delay wait 30 day rule marketplace sale black friday 11.11 dream barrel погреб вино бутылка импульсивные покупки шопинг траты деньги экономия копить бюджет вишлист желания хочу купить подождать распродажа скидки чёрная пятница мечта бочка",
    "campfire": "campfire fire talk conversation questions couple couples parent child kids family friends evening ritual together journal word recording костёр огонь разговор вопросы пара семья дети друзья вечер ритуал вместе дневник запись",
    "lantern": "kids children bedtime story fairy tale sleep дети ребёнок сказка сон на ночь",
    "marbles": "kids children parents screen time дети родители",
    "nighttrain": "couple date questions relationship partner love conversation пара свидание вопросы отношения партнёр любовь разговор",
    "tessera": "interview questions child children kids grandparents family video diary memories growing up birthday интервью вопросы ребёнок дети бабушка семья видео дневник память взросление день рождения",
    "ties": "friends family call contacts друзья семья звонить",
    "notch": "kids children growth photo дети рост фото",
    "silverbox": "photo film camera family фото плёнка камера семья",
    "anyway": "death time life memento mori смерть время жизнь",
    "calavera": "death ageing old смерть старение",
    "dearme": "letter future diary письмо будущее дневник",
    "glow": "praise self esteem wins похвала самооценка победы",
    "prism": "roles values identity роли ценности",
    "theusual": "the usual cafe café cafes coffee coffee shop barista diary journal notebook places favourite regular visits map friends кофейня кофейни кафе кофе бариста дневник блокнот места любимые визиты карта друзья как обычно",
    "hoard": "photo moments memories фото моменты воспоминания",
}


def esc(s):
    return html.escape(s, quote=True)


def apps():
    import importlib.util
    spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "tools", "build_app_pages.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {a["slug"]: a for a in m.APPS}


def ru_script(keys):
    ru = {k: v[1] for k, v in keys.items()}
    return '<script>window.PAGE_RU = Object.assign(window.PAGE_RU || {}, %s);</script>' % json.dumps(ru, ensure_ascii=False)


def keys_all():
    keys = dict(TEXT)
    for slug, pair in PLAIN.items():
        keys["pl." + slug] = pair
    for key, title, blurb, _ in CATS:
        keys["cat." + key] = title
        keys["cat." + key + ".d"] = blurb
    return keys


def put(s, name, body):
    """Replace the block between <!-- catalog:name --> and <!-- /catalog:name -->."""
    a, b = "<!-- catalog:%s -->" % name, "<!-- /catalog:%s -->" % name
    i, j = s.index(a), s.index(b)
    return s[: i + len(a)] + "\n" + body + "\n" + s[j:]


def platform(app):
    return "Windows" if "Windows" in app["plat_badge"] else "Android"


def home_catalog(A):
    nav = "\n".join('          <a href="#c-%s" data-i18n="cat.%s">%s</a>' % (k, k, t[0]) for k, t, _, _ in CATS)
    out = ['      <nav class="cat-nav" aria-label="Groups">\n%s\n      </nav>' % nav]
    for key, title, blurb, slugs in CATS:
        minis = []
        for s in slugs:
            a = A[s]
            minis.append(
                '          <a class="mini" href="apps/{s}/">\n'
                '            <img src="assets/{icon}" alt="" width="48" height="48" loading="lazy">\n'
                '            <span class="mini-text"><span class="mini-name">{name}<small>{plat}</small></span>'
                '<span class="mini-what" data-i18n="pl.{s}">{what}</span></span>\n'
                '          </a>'.format(s=s, icon=a["icon"], name=esc(a["name"]), plat=platform(a), what=esc(PLAIN[s][0])))
        out.append(
            '      <section class="cat" id="c-{k}">\n'
            '        <div class="cat-head"><h3 data-i18n="cat.{k}">{t}</h3><p data-i18n="cat.{k}.d">{d}</p></div>\n'
            '        <div class="mini-grid">\n{m}\n        </div>\n'
            '      </section>'.format(k=key, t=esc(title[0]), d=esc(blurb[0]), m="\n".join(minis)))
    out.append('      <p class="cat-more"><a class="btn btn-ghost" href="apps/" data-i18n="c.more">%s</a></p>' % TEXT["c.more"][0])
    return "\n".join(out)


def refresh(s, keys):
    """The English texts that sit in the page itself (Russian comes from PAGE_RU): rewritten on every build, so counts never go stale."""
    for k in keys:
        s = re.sub(r'(data-i18n="%s">).*?(</(?:span|h1|p)>)' % re.escape(k), lambda m: m.group(1) + TEXT[k][0] + m.group(2), s, count=1, flags=re.S)
    return s


def build_home(A):
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    # First run: the long column of app panels becomes the catalogue.
    if "<!-- catalog:home -->" not in s:
        i = s.index('<div class="shelf">')
        j = s.index('<div class="next">', i)
        s = s[:i] + '<div class="shelf">\n<!-- catalog:home -->\n<!-- /catalog:home -->\n        ' + s[j:]
        s = s.replace('<span class="eyebrow" data-i18n="apps.eyebrow">', '<span class="eyebrow" data-i18n="c.eyebrow">', 1)
        s = re.sub(r'<h2 data-i18n="apps.title">.*?</h2>', '<h2 data-i18n="c.title">%s</h2>\n        <p data-i18n="c.lede">%s</p>' % (TEXT["c.title"][0], TEXT["c.lede"][0]), s, count=1)
        s = re.sub(r'<span class="eyebrow" data-i18n="(?:c\.)?hero.eyebrow">.*?</span>', '<span class="eyebrow" data-i18n="c.hero.eyebrow">%s</span>' % TEXT["c.hero.eyebrow"][0], s, count=1)
        s = re.sub(r'<h1 data-i18n="(?:c\.)?hero.title">.*?</h1>', '<h1 data-i18n="c.hero.title">%s</h1>' % TEXT["c.hero.title"][0], s, count=1)
        s = re.sub(r'<p class="lede" data-i18n="(?:c\.)?hero.lede">.*?</p>', '<p class="lede" data-i18n="c.hero.lede">%s</p>' % TEXT["c.hero.lede"][0], s, count=1)
        s = s.replace('<a class="btn btn-primary" href="#apps" data-i18n="hero.cta">See the apps</a>',
                      '<a class="btn btn-primary" href="#apps" data-i18n="c.hero.cta">%s</a>\n        <a class="btn btn-ghost" href="apps/" data-i18n="c.hero.all">%s</a>' % (TEXT["c.hero.cta"][0], TEXT["c.hero.all"][0]), 1)
        # The GitHub button stays in the nav; the hero keeps two clear choices.
        s = re.sub(r'\n        <a class="btn btn-ghost" href="https://github.com/bigdevwhale" target="_blank" rel="noopener">\s*<svg.*?</svg>\s*<span data-i18n="hero.source">Source on GitHub</span>\s*</a>', "", s, count=1, flags=re.S)
        # Thirty-odd moments are too many to scroll past: the first six, then a button.
        s = s.replace('<div class="moments">', '<div class="moments" data-fold="6">', 1)
        s = s.replace('<script src="assets/site.js', '<!-- catalog:ru -->\n<!-- /catalog:ru -->\n<script src="assets/site.js', 1)
    s = put(s, "home", home_catalog(A))
    s = put(s, "ru", ru_script(keys_all()))
    s = refresh(s, ['c.hero.eyebrow', 'c.hero.title', 'c.hero.lede'])
    open(p, "w", encoding="utf-8", newline="\n").write(s)


def build_apps(A):
    p = os.path.join(ROOT, "apps", "index.html")
    s = open(p, encoding="utf-8").read()
    cards = {m.group(1): m.group(0) for m in re.finditer(r'<a class="card" id="([a-z]+)".*?</a>\n(?=\s*(?:<a class="card"|</div>|<!--))', s, re.S)}
    missing = [x for x in A if x not in cards]
    assert not missing, missing
    if "<!-- catalog:apps -->" not in s:
        i = s.index('<div class="lineup">')
        j = s.index('<div class="next"', i)
        s = s[:i] + '<!-- catalog:apps -->\n<!-- /catalog:apps -->\n\n      ' + s[j:]
        # The section heading moves into the hero; the name chips become the filter.
        s = re.sub(r'\s*<div class="section-head">\s*<span class="eyebrow" data-i18n="ap.lineup">.*?</div>', "", s, count=1, flags=re.S)
        s = re.sub(r'<span class="eyebrow" data-i18n="(?:c\.)?ap.eyebrow">.*?</span>', '<span class="eyebrow" data-i18n="c.ap.eyebrow">%s</span>' % TEXT["c.ap.eyebrow"][0], s, count=1)
        s = re.sub(r'<h1 data-i18n="(?:c\.)?ap.title">.*?</h1>', '<h1 data-i18n="c.ap.title">%s</h1>' % TEXT["c.ap.title"][0], s, count=1)
        s = re.sub(r'<p class="lede" data-i18n="(?:c\.)?ap.lede">.*?</p>', '<p class="lede" data-i18n="c.ap.lede">%s</p>' % TEXT["c.ap.lede"][0], s, count=1)
        s = re.sub(r'\s*<div class="cta-row">\s*<a class="btn btn-primary" href="https://github.com/bigdevwhale".*?</div>', "", s, count=1, flags=re.S)
        s = re.sub(r'\s*<p class="meta" data-i18n="ap.meta">.*?</p>', "", s, count=1, flags=re.S)
        s = re.sub(r'<div class="quick">.*?</div>', '<!-- catalog:filter -->\n<!-- /catalog:filter -->', s, count=1, flags=re.S)
        s = s.replace('<script src="../assets/site.js', '<!-- catalog:ru -->\n<!-- /catalog:ru -->\n<script src="../assets/site.js', 1)
    chips = ['        <button type="button" class="on" data-f="all"><span data-i18n="c.all">All</span> <small>%d</small></button>' % len(A)]
    for key, title, _, slugs in CATS:
        chips.append('        <button type="button" data-f="%s"><span data-i18n="cat.%s">%s</span> <small>%d</small></button>' % (key, key, esc(title[0]), len(slugs)))
    filt = ('    <div class="filter" role="search">\n'
            '      <div class="filter-chips">\n%s\n      </div>\n'
            '      <input type="search" id="app-search" autocomplete="off" aria-label="Search apps" placeholder="%s" data-ph-ru="%s">\n'
            '    </div>' % ("\n".join(chips), esc(TEXT["c.search"][0]), esc(TEXT["c.search"][1])))
    groups = []
    for key, title, blurb, slugs in CATS:
        items = []
        for slug in slugs:
            c = cards[slug].rstrip("\n")
            # One plain line about what it's for, instead of the poster tagline.
            c = re.sub(r'<p class="card-tagline" data-i18n="[^"]+">.*?</p>', '<p class="card-tagline" data-i18n="pl.%s">%s</p>' % (slug, esc(PLAIN[slug][0])), c, count=1, flags=re.S)
            q = " ".join([A[slug]["name"], PLAIN[slug][0], PLAIN[slug][1], WORDS.get(slug, ""), title[0], title[1]]).lower()
            c = re.sub(r'^<a class="card" id="%s"(?: data-q="[^"]*")?' % slug, '<a class="card" id="%s" data-q="%s"' % (slug, esc(q)), c)
            items.append("        " + c.strip())
        groups.append(
            '      <section class="cat" id="c-{k}" data-cat="{k}">\n'
            '        <div class="cat-head"><h2 data-i18n="cat.{k}">{t}</h2><p data-i18n="cat.{k}.d">{d}</p></div>\n'
            '        <div class="lineup">\n{c}\n        </div>\n'
            '      </section>'.format(k=key, t=esc(title[0]), d=esc(blurb[0]), c="\n".join(items)))
    groups.append('      <p class="cat-none" id="cat-none" hidden data-i18n="c.none">%s</p>' % TEXT["c.none"][0])
    s = put(s, "filter", filt)
    s = put(s, "apps", "\n".join(groups))
    s = put(s, "ru", ru_script(keys_all()))
    s = refresh(s, ['c.ap.eyebrow', 'c.ap.title', 'c.ap.lede'])
    open(p, "w", encoding="utf-8", newline="\n").write(s)


def build():
    A = apps()
    assert set(PLAIN) == set(A), set(A) ^ set(PLAIN)
    assert sorted(x for _, _, _, l in CATS for x in l) == sorted(A)
    build_home(A)
    build_apps(A)
    print("catalog:", len(A), "apps in", len(CATS), "groups")


if __name__ == "__main__":
    build()
