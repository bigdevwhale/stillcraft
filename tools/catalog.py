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
    "hoard": ("A camera for moments worth keeping: three a day, kept as pixel-art treasure.",
              "Камера для моментов, которые хочется сохранить: три в день, как пиксельные сокровища."),
}

CATS = [
    ("calm", ("Calm and worry", "Спокойствие и тревога"),
     ("Breathing, meditation, and a way through thoughts that won't let go.", "Дыхание, медитации и способ справиться с мыслями, которые не отпускают."),
     ["swisszen", "serene", "keeper", "kite"]),
    ("focus", ("Focus and the phone", "Фокус и телефон"),
     ("Fewer feeds, fewer distractions, and help giving something up.", "Меньше лент и отвлечений и помощь, чтобы от чего-то отказаться."),
     ["focusshield", "obol", "unhook", "vigil", "sidea", "rewind"]),
    ("habits", ("Habits, goals and the body", "Привычки, цели и тело"),
     ("Routines, chores, goals, fasting, cold water and walks, in a way you'll keep up.", "Привычки, дела, цели, голодание, закаливание и прогулки — так, чтобы не бросить."),
     ["dayquest", "waypoint", "podium", "hearthspell", "ember", "temper", "fogwalk"]),
    ("learn", ("Learning and reading", "Учёба и чтение"),
     ("Remember what you learn, and read more.", "Запоминать выученное и читать больше."),
     ["scriptor", "stele", "familiar"]),
    ("family", ("Family and friends", "Семья и близкие"),
     ("Time with your children and each other, bedtime stories, family photos, keeping in touch.", "Время с детьми и друг с другом, сказки на ночь, семейные фото, связь с близкими."),
     ["lantern", "marbles", "tessera", "nighttrain", "party", "ties", "notch", "silverbox"]),
    ("self", ("You and your life", "Вы и ваша жизнь"),
     ("Your time, your wins, who you want to be, letters to the future, moments worth keeping.", "Ваше время, ваши победы, каким вы хотите быть, письма в будущее и моменты, которые стоит сохранить."),
     ["anyway", "calavera", "dearme", "glow", "prism", "hoard"]),
]

TEXT = {
    # Home hero.
    "c.hero.eyebrow": ("Stillcraft · 34 free apps", "Stillcraft · 34 бесплатных приложения"),
    "c.hero.title": ("Small apps for <em>everyday life</em>.", "Маленькие приложения <em>для обычной жизни</em>."),
    "c.hero.lede": ("Calm down, focus, keep a habit, learn, spend more time with the people you love. 33 apps for Android and one for Windows: free, open source, no ads and no accounts, in English and Russian.",
                    "Успокоиться, сосредоточиться, не бросить привычку, учиться, больше времени проводить с близкими. 33 приложения для Android и одно для Windows: бесплатно, с открытым кодом, без рекламы и аккаунтов, на русском и английском."),
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
    "c.ap.title": ("34 apps, <em>grouped by what they help with.</em>", "34 приложения, <em>по задачам.</em>"),
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
