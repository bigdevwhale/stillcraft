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
    "hoard": ("A camera for moments worth keeping: three a day, kept as pixel-art treasure.",
              "Камера для моментов, которые хочется сохранить: три в день, как пиксельные сокровища."),
}

CATS = [
    ("calm", ("Calm and worry", "Спокойствие и тревога"),
     ("Breathing, meditation, and a way through thoughts that won't let go.", "Дыхание, медитации и способ справиться с мыслями, которые не отпускают."),
     ["swisszen", "serene", "keeper", "kite", "spintop", "hushwood", "heartwood", "longwave"]),
    ("focus", ("Focus and the phone", "Фокус и телефон"),
     ("Fewer feeds, fewer distractions, fewer impulse buys, and help giving something up.", "Меньше лент, отвлечений и импульсивных покупок и помощь, чтобы от чего-то отказаться."),
     ["focusshield", "obol", "unhook", "vigil", "cellar", "sidea", "rewind"]),
    ("habits", ("Habits, goals and the body", "Привычки, цели и тело"),
     ("Routines, chores, goals, fasting, cold water and walks, in a way you'll keep up.", "Привычки, дела, цели, голодание, закаливание и прогулки — так, чтобы не бросить."),
     ["dayquest", "waypoint", "podium", "hearthspell", "ember", "temper", "fogwalk", "lipovka", "stringer", "errand"]),
    ("learn", ("Learning and reading", "Учёба и чтение"),
     ("Remember what you learn, read more, and keep trying new things.", "Запоминать выученное, читать больше и пробовать новое."),
     ["scriptor", "stele", "familiar", "sill"]),
    ("family", ("Family and friends", "Семья и близкие"),
     ("Time with your children and each other, bedtime stories, family photos, keeping in touch.", "Время с детьми и друг с другом, сказки на ночь, семейные фото, связь с близкими."),
     ["lantern", "campfire", "marbles", "tessera", "nighttrain", "party", "fridge", "ties", "notch", "silverbox"]),
    ("self", ("You and your life", "Вы и ваша жизнь"),
     ("Your time, your wins, who you want to be, letters to the future, moments worth keeping.", "Ваше время, ваши победы, каким вы хотите быть, письма в будущее и моменты, которые стоит сохранить."),
     ["anyway", "calavera", "dearme", "glow", "prism", "hoard", "theusual", "carriage"]),
]

TEXT = {
    # Home hero.
    "c.hero.eyebrow": ("Stillcraft · 47 free apps", "Stillcraft · 47 бесплатных приложений"),
    "c.hero.title": ("Small apps for <em>everyday life</em>.", "Маленькие приложения <em>для обычной жизни</em>."),
    "c.hero.lede": ("Calm down, focus, keep a habit, learn, spend more time with the people you love. 46 apps for Android and one for Windows: free, open source, no ads and no accounts, in English and Russian.",
                    "Успокоиться, сосредоточиться, не бросить привычку, учиться, больше времени проводить с близкими. 46 приложений для Android и одно для Windows: бесплатно, с открытым кодом, без рекламы и аккаунтов, на русском и английском."),
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
    "c.ap.title": ("47 apps, <em>grouped by what they help with.</em>", "47 приложений, <em>по задачам.</em>"),
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
    "fridge": "fridge refrigerator door couple couples partner relationship shopping list groceries chores whose turn notes sticky notes magnets worries confession envelope love wishes gifts household home sync wifi qr холодильник дверца пара отношения партнёр покупки список продуктов дела чья очередь записки стикеры магниты тревоги признание конверт любовь желания подарки быт дом синхронизация",
    "stringer": "stringer correspondent reporter newspaper paper district editor telegram assignment assignments task walk walks walking outdoors go outside every day street city photo photography photo walk street photography camera halftone newsprint caption sunday issue rubrics doors cats signs letters alphabet press card flash dusk внештатник корреспондент репортёр газета районная редактор телеграмма задание задания прогулка прогулки на улицу каждый день улица город фото фотография фотопрогулка уличная фотография камера растр подпись воскресный номер рубрики двери коты вывески буквы алфавит пресс-карта молния сумерки",
    "errand": "errand courier delivery shopping shopping list grocery groceries list shop shops supermarket store waybill order orders family household chat messenger share list rush weight bag string bag cold aisle shelf route budget receipt prices price tracker inflation cheaper game gamification tokens depot bicycle van rank badges simulator посыльный курьер доставка покупки список покупок продукты магазин супермаркет накладная заказ заказы семья домашние мессенджер чат молния вес авоська термобокс полки маршрут бюджет чек цены подорожало дешевле игра геймификация жетоны депо велосипед фургон звание знаки симулятор habits привычки",
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
        s = re.sub(r'<span class="eyebrow" data-i18n="hero.eyebrow">.*?</span>', '<span class="eyebrow" data-i18n="c.hero.eyebrow">%s</span>' % TEXT["c.hero.eyebrow"][0], s, count=1)
        s = re.sub(r'<h1 data-i18n="hero.title">.*?</h1>', '<h1 data-i18n="c.hero.title">%s</h1>' % TEXT["c.hero.title"][0], s, count=1)
        s = re.sub(r'<p class="lede" data-i18n="hero.lede">.*?</p>', '<p class="lede" data-i18n="c.hero.lede">%s</p>' % TEXT["c.hero.lede"][0], s, count=1)
        s = s.replace('<a class="btn btn-primary" href="#apps" data-i18n="hero.cta">See the apps</a>',
                      '<a class="btn btn-primary" href="#apps" data-i18n="c.hero.cta">%s</a>\n        <a class="btn btn-ghost" href="apps/" data-i18n="c.hero.all">%s</a>' % (TEXT["c.hero.cta"][0], TEXT["c.hero.all"][0]), 1)
        # The GitHub button stays in the nav; the hero keeps two clear choices.
        s = re.sub(r'\n        <a class="btn btn-ghost" href="https://github.com/bigdevwhale" target="_blank" rel="noopener">\s*<svg.*?</svg>\s*<span data-i18n="hero.source">Source on GitHub</span>\s*</a>', "", s, count=1, flags=re.S)
        # Thirty-odd moments are too many to scroll past: the first six, then a button.
        s = s.replace('<div class="moments">', '<div class="moments" data-fold="6">', 1)
        s = s.replace('<script src="assets/site.js', '<!-- catalog:ru -->\n<!-- /catalog:ru -->\n<script src="assets/site.js', 1)
    s = put(s, "home", home_catalog(A))
    s = put(s, "ru", ru_script(keys_all()))
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
        s = re.sub(r'<span class="eyebrow" data-i18n="ap.eyebrow">.*?</span>', '<span class="eyebrow" data-i18n="c.ap.eyebrow">%s</span>' % TEXT["c.ap.eyebrow"][0], s, count=1)
        s = re.sub(r'<h1 data-i18n="ap.title">.*?</h1>', '<h1 data-i18n="c.ap.title">%s</h1>' % TEXT["c.ap.title"][0], s, count=1)
        s = re.sub(r'<p class="lede" data-i18n="ap.lede">.*?</p>', '<p class="lede" data-i18n="c.ap.lede">%s</p>' % TEXT["c.ap.lede"][0], s, count=1)
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
