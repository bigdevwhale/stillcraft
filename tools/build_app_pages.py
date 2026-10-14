"""Generates apps/<slug>/index.html for every app in APPS.

Run from the repo root:  python tools/build_app_pages.py
Each text is an (English, Russian) pair; English goes into the HTML, Russian into window.PAGE_RU.
"""
import glob
import hashlib
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "../../assets/"

APPS = [
    {
        "slug": "anyway",
        "name": "Anyway",
        "panel": "app--anyway",
        "gallery": "g-anyway",
        "icon": "anyway-icon.png",
        "visual": "en-now.png", "visual_ru": "ru-now.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/anyway",
        "download": "https://github.com/bigdevwhale/anyway/releases/latest/download/anyway.apk",
        "version": "v0.2.2",
        "tagline": ("How many Saturdays you have left, and what you'll do with them.",
                    "Сколько суббот у тебя осталось, и что ты с ними сделаешь."),
        "badge": ("Memento mori · Early release", "Memento mori · Ранняя версия"),
        "status": ("early", "Early release", "Ранняя версия"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("We're all gonna die anyway. <em>So go do the thing.</em>",
                  "Все мы когда-нибудь умрём. <em>Так что иди и сделай это.</em>"),
        "desc": ("A small, slightly dark, surprisingly warm app about living now. It's the old Stoic idea of memento mori, minus the skulls.",
                 "Маленькое, немного мрачное и неожиданно тёплое приложение о том, чтобы жить сейчас. Старая стоическая идея memento mori, только без черепов."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · No internet permission · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Без доступа к интернету · English и Русский"),
        "features": [
            (("Saturdays left", "Сколько суббот осталось"),
             ("A huge number counted from your birthday and an optimism level you choose. About 4,000 if you're lucky.",
              "Огромное число, посчитанное от даты рождения и уровня оптимизма, который ты выбираешь сам. Около 4 000, если повезёт.")),
            (("The ANYWAY button", "Кнопка ANYWAY"),
             ("Scared to send the message, quit the job, dance badly? Press it. Then go.",
              "Страшно написать, уволиться, потанцевать плохо? Нажми. И иди.")),
            (("The Worry Filter", "Фильтр тревог"),
             ("Will it matter in 5 years? In 100? When the Sun becomes a red giant? If it doesn't survive, it spins and floats away.",
              "Будет ли это важно через 5 лет? Через 100? Когда Солнце станет красным гигантом? Если нет — тревога закручивается и улетает.")),
            (("Before it's too late", "Пока не поздно"),
             ("Not a bucket list. Things you'd regret not doing. Each one counts its waiting days and turns orange after a week.",
              "Не список желаний, а то, о чём пожалеешь, если не сделаешь. Каждый пункт считает дни ожидания и через неделю становится оранжевым.")),
            (("You're still alive", "Ты всё ещё жив"),
             ("Once a day, at a random moment between 10:00 and 21:00, a notification reminds you and asks what you'll do about it.",
              "Раз в день, в случайный момент между 10:00 и 21:00, уведомление напоминает об этом и спрашивает, что ты будешь делать.")),
            (("A line from the Stoics", "Строка от стоиков"),
             ("A question of the day and a quote from Marcus Aurelius, Seneca, Epicurus or Ecclesiastes.",
              "Вопрос дня и цитата Марка Аврелия, Сенеки, Эпикура или Екклесиаста.")),
        ],
        "shots": [
            ("en-onboarding.png", "ru-onboarding.png", ("Setup", "Настройка"), ("Birthday and optimism level. That's all it asks.", "Дата рождения и уровень оптимизма. Больше ничего.")),
            ("en-now.png", "ru-now.png", ("Now", "Сейчас"), ("Saturdays left and the question of the day.", "Сколько суббот осталось и вопрос дня.")),
            ("en-anyway.png", None, ("ANYWAY", "ANYWAY"), ("The button for the thing you're scared to do.", "Кнопка для того, что страшно сделать.")),
            ("en-worry.png", None, ("Worry Filter", "Фильтр тревог"), ("Three questions, from 5 years to the red giant.", "Три вопроса: от 5 лет до красного гиганта.")),
            ("en-worry-done.png", None, ("Released", "Отпущено"), ("A worry that didn't survive the filter.", "Тревога, которая не прошла фильтр.")),
            ("en-before.png", "ru-before.png", ("Before it's too late", "Пока не поздно"), ("Waiting items turn orange after a week.", "Пункты, ждущие больше недели, становятся оранжевыми.")),
        ],
        "extra": None,
        "facts": [
            (("Version", "Версия"), ("v0.2.2", "v0.2.2")),
            (("File", "Файл"), ("anyway.apk", "anyway.apk")),
            (("Requires", "Нужно"), ("Android 8.0 or newer", "Android 8.0 или новее")),
            (("Permissions", "Разрешения"), ("Notifications only. No internet.", "Только уведомления. Без интернета.")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Enter your birthday. Go do the thing.", "Введи дату рождения. Иди и сделай это."),
        ],
        "note": None,
        "build_req": ("JDK 17+ and the Android SDK (API 36).", "JDK 17+ и Android SDK (API 36)."),
        "build": "git clone https://github.com/bigdevwhale/anyway.git\ncd anyway\n./gradlew assembleDebug   <c># app/build/outputs/apk/debug/</c>\n./gradlew installDebug    <c># to a connected phone</c>",
        "faq": [
            (("How is the number counted?", "Как считается число?"),
             ("From your birthday and an optimism level, the life expectancy you pick. Saturdays are just weeks you can feel.",
              "От даты рождения и уровня оптимизма — ожидаемой продолжительности жизни, которую ты выбираешь. Субботы — это просто недели, которые можно почувствовать.")),
            (("Is it gloomy?", "Это не слишком мрачно?"),
             ("A little dark, mostly warm. It doesn't track streaks or nag you about goals. It's the friend who read a lot of Seneca and just wants you to text them back.",
              "Немного мрачно, но в основном тепло. Тут нет серий и напоминаний о целях. Это друг, который много читал Сенеку и просто хочет, чтобы ты ему ответил.")),
            (("What does it know about me?", "Что оно обо мне знает?"),
             ("Your birthday, your worries and your list, all stored on the phone. The app has no internet permission, so none of it can leave.",
              "Дату рождения, тревоги и список, и всё это хранится на телефоне. У приложения нет доступа к интернету, так что ничего не может уйти наружу.")),
        ],
    },
    {
        "slug": "swisszen",
        "name": "SwissZen",
        "panel": "app--swisszen",
        "gallery": "g-swisszen",
        "icon": "swisszen-logo.svg",
        "visual": "sz-home.png", "visual_ru": "sz-home.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/SwissZen",
        "download": "https://github.com/bigdevwhale/SwissZen/releases/latest/download/SwissZen.apk",
        "version": "v1.0.1",
        "tagline": ("The mindfulness multi-tool: breathing, Wim Hof, a bell, practices and a journal.",
                    "Мультитул осознанности: дыхание, Вим Хоф, колокол, практики, дневник."),
        "badge": ("Mindfulness multi-tool · Stable", "Мультитул осознанности · Стабильная"),
        "status": ("ok", "Stable", "Стабильная"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Open the knife. <em>A minute is enough.</em>", "Открой нож. <em>Минуты достаточно.</em>"),
        "desc": ("Most mindfulness apps want a commitment. SwissZen is a pocket knife: unfold the one tool that fits the moment, use it, fold it back.",
                 "Большинство приложений для медитации требуют обязательств. SwissZen — карманный нож: раскрой один инструмент под момент, используй и сложи обратно."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · MIT licensed · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Лицензия MIT · English и Русский"),
        "features": [
            (("Guided breathing", "Дыхание с подсказкой"),
             ("A calm sphere grows on the inhale and settles on the exhale. Box 4‑4‑4‑4, Calm 4‑7‑8, Coherent 5‑5, for 2, 5 or 10 minutes.",
              "Спокойная сфера растёт на вдохе и опускается на выдохе. Квадрат 4‑4‑4‑4, Спокойствие 4‑7‑8, Когерентное 5‑5, на 2, 5 или 10 минут.")),
            (("Wim Hof rounds", "Раунды Вима Хофа"),
             ("Power breaths, an open-ended hold on empty lungs with a stopwatch, a 15‑second recovery breath. Four levels.",
              "Силовые вдохи, задержка на выдохе с секундомером без ограничения, восстановительный вдох на 15 секунд. Четыре уровня.")),
            (("Mindfulness bell", "Колокол осознанности"),
             ("Rings with the app closed: at random every 15–90 minutes, at a fixed interval or at set times, with quiet hours.",
              "Звонит при закрытом приложении: случайно раз в 15–90 минут, через равные интервалы или в заданное время, с тихими часами.")),
            (("Micro-practices", "Микропрактики"),
             ("5‑4‑3‑2‑1 grounding, body scan, notice three things, start-of-day pause, gratitude minute.",
              "Заземление 5‑4‑3‑2‑1, сканирование тела, три детали, пауза в начале дня, минута благодарности.")),
            (("Meditations", "Медитации"),
             ("Five timed sits of 5–20 minutes: breath anchor, loving-kindness, mountain, walking, sleep wind-down.",
              "Пять медитаций на 5–20 минут: якорь дыхания, доброта, гора, ходьба, подготовка ко сну.")),
            (("One-line journal", "Дневник в одну строку"),
             ("One line a day against a rotating prompt, a week view, and an Echo: a line you wrote weeks ago, brought back.",
              "Одна строка в день по сменяющейся подсказке, вид недели и «Эхо» — строка, которую ты написал несколько недель назад.")),
        ],
        "shots": [
            ("sz-home.png", "sz-home.ru.png", ("Home", "Главная"), ("Tools fan out of the knife handle.", "Инструменты раскрываются из рукоятки ножа.")),
            ("sz-breathe.png", "sz-breathe.ru.png", ("Breathe", "Дыхание"), ("Pick a Wim Hof level.", "Выбор уровня Вима Хофа.")),
            ("sz-wimhof.png", "sz-wimhof.ru.png", ("Wim Hof session", "Сессия Вима Хофа"), ("Breath 2 of 35. Let go.", "Вдох 2 из 35. Отпусти.")),
            ("sz-practices.png", "sz-practices.ru.png", ("Practices", "Практики"), ("Short pauses and longer sits.", "Короткие паузы и долгие медитации.")),
            ("sz-bell.png", "sz-bell.ru.png", ("Bell", "Колокол"), ("Set times and quiet hours.", "Время звонков и тихие часы.")),
        ],
        "extra": {
            "title": ("Wim Hof levels", "Уровни Вима Хофа"),
            "head": [("Level", "Уровень"), ("Rounds", "Раунды"), ("Breaths / round", "Вдохов за раунд"), ("Pace in / out", "Темп вдох / выдох"), ("Hold targets", "Цели задержки")],
            "rows": [
                [("Beginner", "Новичок"), ("3", "3"), ("30", "30"), ("2.0 s / 1.6 s", "2,0 с / 1,6 с"), ("0:30 → 1:00 → 1:30", "0:30 → 1:00 → 1:30")],
                [("Medium", "Средний"), ("3", "3"), ("30–35", "30–35"), ("1.6 s / 1.3 s", "1,6 с / 1,3 с"), ("1:00 → 1:30 → 1:30–2:00", "1:00 → 1:30 → 1:30–2:00")],
                [("Advanced", "Продвинутый"), ("4", "4"), ("35–40", "35–40"), ("1.4 s / 1.0 s", "1,4 с / 1,0 с"), ("1:00 → 1:30 → 2:00 → 2:30", "1:00 → 1:30 → 2:00 → 2:30")],
                [("Expert", "Эксперт"), ("4–5", "4–5"), ("40–50", "40–50"), ("1.1 s / 0.8 s", "1,1 с / 0,8 с"), ("1:30 → 2:00 → 2:30 → 3:00+", "1:30 → 2:00 → 2:30 → 3:00+")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.1", "v1.0.1")),
            (("File", "Файл"), ("SwissZen.apk", "SwissZen.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer", "Android 8.0 (API 26) или новее")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефоне."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Turn on the bell if you want the app to find you during the day.", "Включи колокол, если хочешь, чтобы приложение само находило тебя днём."),
        ],
        "note": ("Always do breathing exercises sitting or lying down. Never in or near water, never while driving. If you have a heart condition or epilepsy, are pregnant or unsure, talk to a doctor first.",
                 "Дыхательные упражнения делай только сидя или лёжа. Никогда в воде или рядом с ней и никогда за рулём. Если у тебя проблемы с сердцем, эпилепсия, беременность или есть сомнения — сначала посоветуйся с врачом."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/SwissZen.git\ncd SwissZen\n./gradlew testDebugUnitTest   <c># unit tests</c>\n./gradlew assembleDebug       <c># debug APK</c>\n./gradlew installDebug        <c># to a connected phone</c>",
        "faq": [
            (("Does the bell ring when the app is closed?", "Колокол звонит при закрытом приложении?"),
             ("Yes. It uses Android alarms, survives reboots and time changes, and needs no exact-alarm permission. Tap “I paused” on the notification to note what you noticed.",
              "Да. Он работает через системные будильники Android, переживает перезагрузку и смену времени и не требует разрешения на точные будильники. Нажми «Я остановился» в уведомлении, чтобы записать, что заметил.")),
            (("Where does the breathing sound come from?", "Откуда звук дыхания?"),
             ("It's synthesised on the phone: white noise through a sweeping filter, so it always matches the tempo of your level.",
              "Он синтезируется прямо на телефоне: белый шум через плавающий фильтр, поэтому всегда совпадает с темпом твоего уровня.")),
            (("Is anything collected?", "Собираются ли какие-то данные?"),
             ("No accounts, no network, no analytics. The journal, bell history and session log stay on the device.",
              "Ни аккаунтов, ни сети, ни аналитики. Дневник, история колокола и журнал сессий остаются на устройстве.")),
        ],
    },
    {
        "slug": "focusshield",
        "name": "FocusShield",
        "panel": "app--focus",
        "gallery": "g-focus",
        "icon": "focusshield-icon.svg",
        "visual": "fs-timer.gif", "visual_ru": None, "visual_wide": True,
        "repo": "https://github.com/bigdevwhale/focus-shield",
        "download": "https://github.com/bigdevwhale/focus-shield/releases/latest/download/FocusShield.exe",
        "version": "v1.2.1",
        "tagline": ("A strict focus timer that actually blocks distractions.", "Строгий таймер фокуса, который правда блокирует отвлечения."),
        "badge": ("Focus timer for Windows · Stable", "Таймер фокуса для Windows · Стабильная"),
        "status": ("ok", "Stable", "Стабильная"),
        "file_badge": ("Installer ready", "Установщик готов"),
        "plat_badge": "Windows 10 / 11",
        "title": ("Block the noise. <em>Keep yourself honest.</em>", "Отсеки шум. <em>Будь честен с собой.</em>"),
        "desc": ("Most focus apps are a timer with good intentions. FocusShield is built on friction: once a session starts, the distracted path gets slow and deliberate.",
                 "Большинство приложений для фокуса — таймер с добрыми намерениями. FocusShield построен на трении: когда сессия идёт, путь к отвлечению становится медленным и осознанным."),
        "cta": ("Download for Windows", "Скачать для Windows"),
        "plat": ("Windows 10 / 11 · Free · 100% local · English &amp; Русский",
                 "Windows 10 / 11 · Бесплатно · 100% локально · English и Русский"),
        "features": [
            (("A timer always in view", "Таймер всегда на виду"),
             ("A compact floating timer on top of every window: progress ring, time left, your intention and one-click controls.",
              "Компактный таймер поверх всех окон: кольцо прогресса, оставшееся время, твоё намерение и управление в один клик.")),
            (("Intention and check-in", "Намерение и итог"),
             ("Every session starts with what exactly will be done and ends with one question: did you make it?",
              "Каждая сессия начинается с того, что именно будет сделано, и заканчивается одним вопросом: получилось?")),
            (("Websites stop resolving", "Сайты перестают открываться"),
             ("Domains on your list go nowhere, system-wide. DNS-over-HTTPS servers are blocked too.",
              "Домены из списка перестают открываться во всей системе. Серверы DNS-over-HTTPS тоже блокируются.")),
            (("Tab guard", "Защита вкладок"),
             ("Closes a YouTube tab by its title, even through a proxy or VPN. A search for “how to block youtube” is left alone.",
              "Закрывает вкладку YouTube по заголовку, даже через прокси или VPN. Поиск «как заблокировать youtube» не трогает.")),
            (("Apps and folders", "Приложения и папки"),
             ("Chosen apps close during focus and chosen folders can't be opened. System folders are refused on purpose.",
              "Выбранные приложения закрываются, выбранные папки не открываются. Системные папки заблокировать нельзя — специально.")),
            (("Focus apps", "Рабочие приложения"),
             ("Pick the apps you work in. Wander off and they come back to the front.",
              "Выбери, в чём работаешь. Отвлёкся — они сами вернутся на передний план.")),
            (("Breaks that restore", "Перерывы, которые восстанавливают"),
             ("4‑7‑8 breathing with an animated circle, the 20‑20‑20 eye rule, a stretch and a glass of water.",
              "Дыхание 4‑7‑8 с анимированным кругом, правило 20‑20‑20 для глаз, разминка и стакан воды.")),
            (("A sprout that grows", "Росток, который растёт"),
             ("An optional mascot grows a leaf with each pomodoro, sweats in the last minute and blooms on the long break.",
              "Необязательный маскот отращивает лист с каждым помидоро, потеет в последнюю минуту и расцветает на длинном перерыве.")),
            (("Check-ins and stats", "Снимки и статистика"),
             ("Optional webcam and screen captures during focus, stored by day. Minutes, streaks and every intention with its outcome.",
              "Необязательные снимки с камеры и экрана во время фокуса, по дням. Минуты, серии и каждое намерение с итогом.")),
        ],
        "shots": [
            ("fs-start.png", None, ("New session", "Новая сессия"), ("Duration and what exactly will be done.", "Длительность и что именно будет сделано.")),
            ("fs-checkin.png", None, ("Check-in", "Итог"), ("Did you make it?", "Получилось?")),
            ("fs-break.gif", None, ("Break", "Перерыв"), ("4‑7‑8 breathing with the circle.", "Дыхание 4‑7‑8 по кругу.")),
            ("fs-mascot.png", None, ("The sprout", "Росток"), ("From napping seedling to bloom.", "От спящего ростка до цветка.")),
            ("fs-stats.png", None, ("Statistics", "Статистика"), ("Minutes, streaks, a 7-day chart.", "Минуты, серии, график за 7 дней.")),
            ("fs-photos.png", None, ("Photos by day", "Снимки по дням"), ("Optional captures, kept locally.", "Необязательные снимки, хранятся локально.")),
        ],
        "extra": {
            "title": ("Blocking that holds up", "Блокировка, которая держит"),
            "head": [("Layer", "Слой"), ("What it does", "Что делает"), ("Through proxy / VPN", "Через прокси / VPN")],
            "rows": [
                [("Websites", "Сайты"), ("Domains resolve to 0.0.0.0 via the hosts file; DNS-over-HTTPS servers are blocked", "Домены ведут в 0.0.0.0 через файл hosts; серверы DNS-over-HTTPS заблокированы"), ("No", "Нет")],
                [("Tab guard", "Защита вкладок"), ("Closes a tab whose title contains a keyword, YouTube by default", "Закрывает вкладку, в заголовке которой есть ключевое слово, по умолчанию YouTube"), ("Yes", "Да")],
                [("Apps", "Приложения"), ("Processes on your list are closed during focus", "Процессы из списка закрываются во время фокуса"), ("Yes", "Да")],
                [("Folders", "Папки"), ("An NTFS deny-read rule: every program gets “access denied”", "Правило NTFS на запрет чтения: любая программа получает «доступ запрещён»"), ("Yes", "Да")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.2.1", "v1.2.1")),
            (("File", "Файл"), ("FocusShield.exe + .sha256", "FocusShield.exe + .sha256")),
            (("Requires", "Нужно"), ("Windows 10 or 11, administrator rights", "Windows 10 или 11, права администратора")),
            (("Data", "Данные"), ("%LOCALAPPDATA%\\focus-shield", "%LOCALAPPDATA%\\focus-shield")),
        ],
        "steps": [
            ("Download FocusShield.exe. It's one file, no Python needed.", "Скачай FocusShield.exe. Это один файл, Python не нужен."),
            ("Run it and accept the administrator prompt.", "Запусти и подтверди запрос прав администратора."),
            ("It adds itself to startup and lives in the tray. Press ▶ on the timer to start.", "Он добавится в автозагрузку и будет жить в трее. Нажми ▶ на таймере, чтобы начать."),
        ],
        "note": ("The exe isn't code-signed, so Windows may say “Windows protected your PC”. Click More info → Run anyway. Every release is built from source by GitHub Actions and ships with a .sha256 checksum.",
                 "Exe не подписан, поэтому Windows может показать «Система Windows защитила ваш компьютер». Нажми «Подробнее» → «Выполнить в любом случае». Каждый релиз собирается из исходников в GitHub Actions и идёт с контрольной суммой .sha256."),
        "build_req": ("Python 3.10+ from python.org, with tkinter.", "Python 3.10+ с python.org, с tkinter."),
        "build": "git clone https://github.com/bigdevwhale/focus-shield.git\ncd focus-shield\npython install.py   <c># run from source, with autostart</c>\npython build.py     <c># or build dist\\FocusShield.exe</c>",
        "faq": [
            (("I use a proxy or VPN and YouTube still opens", "У меня прокси или VPN, и YouTube всё равно открывается"),
             ("With a proxy, domain names are resolved by the proxy and the hosts file is never asked. That's what the tab guard is for: it works on window titles. Keep it on in Settings → Tab guard.",
              "С прокси имена доменов разрешает сам прокси, и файл hosts не используется. Для этого и есть защита вкладок: она работает по заголовкам окон. Не выключай её в «Настройки → Защита вкладок».")),
            (("Something stayed blocked. How do I unblock it?", "Что-то осталось заблокированным. Как снять?"),
             ("Run <code>FocusShield.exe --unblock</code>, or remove everything with <code>FocusShield.exe --uninstall</code>. Your original hosts file is backed up as hosts.focus-shield.bak.",
              "Запусти <code>FocusShield.exe --unblock</code> или удали всё через <code>FocusShield.exe --uninstall</code>. Исходный файл hosts сохранён рядом как hosts.focus-shield.bak.")),
            (("Can I cheat?", "Можно схитрить?"),
             ("Of course. Anyone with an admin terminal can kill a process. FocusShield is friction, not armor, and friction is usually all it takes.",
              "Конечно. Кто угодно с терминалом администратора может убить процесс. FocusShield — это трение, а не броня, и обычно трения достаточно.")),
            (("Is anything sent anywhere?", "Что-то отправляется в сеть?"),
             ("No. There are no network calls in the code. Captures are deleted after the retention period you set, 14 days by default.",
              "Нет. В коде нет сетевых запросов. Снимки удаляются по истечении срока хранения, по умолчанию через 14 дней.")),
        ],
    },
    {
        "slug": "ties",
        "name": "Ties",
        "panel": "app--ties",
        "gallery": "g-ties",
        "icon": "ties-logo.svg",
        "visual": "ti-home.png", "visual_ru": "ti-home.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/ties",
        "download": "https://github.com/bigdevwhale/ties/releases/latest/download/Ties.apk",
        "version": "v1.0.0",
        "tagline": ("Don't drift apart from the people who matter.", "Не теряй тех, кто тебе дорог."),
        "badge": ("Keeping in touch · New", "Связь с близкими · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Don't drift apart from <em>the people who matter.</em>", "Не теряй тех, <em>кто тебе дорог.</em>"),
        "desc": ("Friendships rarely end in a fight. They fade quietly: university, a new job, a move, and suddenly a year passes without a call. Ties keeps the people who matter in sight.",
                 "Дружба редко заканчивается ссорой. Она тихо угасает: учёба, новая работа, переезд, и вдруг проходит год без звонка. Ties держит дорогих людей на виду."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · No internet permission · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Без доступа к интернету · English и Русский"),
        "features": [
            (("Your people", "Твои люди"),
             ("Add someone by hand or from contacts: family, friends, childhood friends, work and study. Pick a rhythm, from every week to every six months.",
              "Добавь человека вручную или из контактов: семья, друзья, друзья детства, работа и учёба. Выбери ритм: от раза в неделю до раза в полгода.")),
            (("A ring that cools down", "Кольцо, которое остывает"),
             ("Each avatar's ring empties as a contact comes due: green, then amber, then coral. The list is sorted into Time to reach out, Coming up and All good.",
              "Кольцо вокруг аватара пустеет, когда подходит время связаться: зелёное, потом янтарное, потом коралловое. Список делится на «Пора связаться», «Скоро» и «Всё хорошо».")),
            (("One tap to reach out", "Связаться в одно касание"),
             ("Call, or write via SMS, Telegram or WhatsApp. After a call from the app, Ties asks “Did you reach them?”, so logging takes one tap.",
              "Позвони или напиши в SMS, Telegram или WhatsApp. После звонка из приложения Ties спросит «Удалось поговорить?», и отметить разговор можно одним касанием.")),
            (("What to talk about", "О чём поговорить"),
             ("The first message is the hardest. Every card has a gentle opener, plus notes worth remembering for next time.",
              "Труднее всего первое сообщение. На каждой карточке есть мягкая подсказка для начала разговора и заметки о том, что важно помнить.")),
            (("Birthdays", "Дни рождения"),
             ("Upcoming birthdays sit on top of the list, and a notification comes on the day.",
              "Ближайшие дни рождения видны вверху списка, а в сам день приходит уведомление.")),
            (("One calm reminder a day", "Одно спокойное напоминание в день"),
             ("Only when someone is due or has a birthday, at the time you choose. People who stay overdue come back every 3 days, not daily.",
              "Только если кому-то пора позвонить или у кого-то день рождения, в выбранное тобой время. О тех, кто ждёт дольше, Ties напомнит раз в 3 дня, а не каждый день.")),
        ],
        "shots": [
            ("ti-home.png", "ti-home.ru.png", ("Home", "Главная"), ("Who's waiting, who's coming up, who's fine.", "Кто ждёт, кто скоро, у кого всё хорошо.")),
            ("ti-person.png", "ti-person.ru.png", ("A person", "Человек"), ("Call, write, an opener and what to remember.", "Позвонить, написать, подсказка и что важно помнить.")),
            ("ti-log.png", "ti-log.ru.png", ("We talked", "Связались"), ("How, when and a note.", "Как, когда и заметка.")),
            ("ti-edit.png", "ti-edit.ru.png", ("Add someone", "Добавить"), ("Who they are and how often you'd like to talk.", "Кто это и как часто хочешь общаться.")),
            ("ti-settings.png", "ti-settings.ru.png", ("Settings", "Настройки"), ("One reminder a day, at your time.", "Одно напоминание в день, в твоё время.")),
        ],
        "extra": None,
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Ties.apk", "Ties.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer", "Android 8.0 (API 26) или новее")),
            (("Permissions", "Разрешения"), ("Notifications and start after reboot. No internet.", "Уведомления и запуск после перезагрузки. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Add three people you'd hate to lose touch with.", "Добавь троих, с кем не хочешь терять связь."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Ties and set battery usage to No restrictions, or reminders may not arrive. Settings → Reminders not arriving? opens the right screen.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Ties автозапуск и сними ограничения батареи, иначе напоминания могут не приходить. «Настройки → Напоминания не приходят?» откроет нужный экран."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/ties.git\ncd ties\n./gradlew testDebugUnitTest   <c># unit tests</c>\n./gradlew assembleDebug       <c># debug APK</c>\n./gradlew installDebug        <c># to a connected phone</c>",
        "faq": [
            (("Does it read my contacts or call log?", "Оно читает мои контакты или журнал звонков?"),
             ("No. Picking a contact grants access to that one entry only, not your whole address book. Ties never reads the call log. You can also add people by hand.",
              "Нет. Когда ты выбираешь контакт, Ties получает доступ только к этой записи, а не ко всей адресной книге. Журнал звонков оно не читает. Людей можно добавить и вручную.")),
            (("Will it nag me?", "Оно не будет надоедать?"),
             ("One reminder a day at most, at the time you choose, and only when someone is due or has a birthday. If someone stays overdue, they come back every 3 days, not daily.",
              "Не больше одного напоминания в день, в выбранное тобой время, и только если кому-то пора позвонить или у кого-то день рождения. Если человек ждёт дольше, напоминание повторится через 3 дня, а не каждый день.")),
            (("Is anything sent anywhere?", "Что-то отправляется в сеть?"),
             ("No. No accounts, no servers, no analytics, and the app has no internet permission. Your people, notes and history live in a local database on the phone. Calls and messages open in your phone, SMS, Telegram or WhatsApp app.",
              "Нет. Ни аккаунтов, ни серверов, ни аналитики, и у приложения нет доступа к интернету. Люди, заметки и история хранятся в локальной базе на телефоне. Звонки и сообщения открываются в телефоне, SMS, Telegram или WhatsApp.")),
        ],
    },
    {
        "slug": "unhook",
        "name": "Unhook",
        "panel": "app--unhook",
        "gallery": "g-unhook",
        "icon": "unhook-logo.svg",
        "visual": "un-home.png", "visual_ru": "un-home.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/unhook",
        "download": "https://github.com/bigdevwhale/unhook/releases/latest/download/Unhook.apk",
        "version": "v1.0.0",
        "tagline": ("Quit a habit, one day at a time.", "Бросай привычку день за днём."),
        "badge": ("Quitting a habit · New", "Отказ от привычки · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Quitting isn't one big decision. <em>It's a small one, made again every day.</em>",
                  "Бросить — это не одно большое решение. <em>Это маленькое, которое принимаешь каждый день.</em>"),
        "desc": ("Unhook counts every clean minute and turns it into money saved and time won back, celebrates each milestone and helps you ride out a craving. A slip doesn't erase your progress. Everything paid quit trackers lock behind premium is free here, with no ads and no account.",
                 "Unhook считает каждую минуту без срыва и превращает её в сэкономленные деньги и возвращённое время, отмечает каждую веху и помогает переждать тягу. Срыв не стирает прогресс. Всё, что платные трекеры прячут за премиумом, здесь бесплатно, без рекламы и без аккаунта."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · No internet permission · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Без доступа к интернету · English и Русский"),
        "features": [
            (("A live counter", "Живой счётчик"),
             ("Days, hours, minutes and seconds since the last time, with a ring that fills toward the next goal. Track as many habits as you like.",
              "Дни, часы, минуты и секунды с последнего раза и кольцо, которое заполняется к следующей цели. Привычек можно вести сколько угодно.")),
            (("Goals that climb on their own", "Цели растут сами"),
             ("1 day → 3 days → 1 week → 2 weeks → 1 month → 3 → 6 months → 1 → 2 → 5 years. Nothing to pick: the next rung is always the goal.",
              "1 день → 3 дня → 1 неделя → 2 недели → 1 месяц → 3 → 6 месяцев → 1 → 2 → 5 лет. Выбирать ничего не нужно: цель — всегда следующая ступень.")),
            (("SOS for cravings", "SOS при тяге"),
             ("I have a craving opens paced breathing (in 4 · hold 4 · out 6) next to your own reasons. When the wave passes, one tap logs the win.",
              "Кнопка «Меня тянет» открывает дыхание в ритме (вдох 4 · задержка 4 · выдох 6) рядом с твоими причинами. Когда волна пройдёт, победа записывается одним касанием.")),
            (("Savings and rewards", "Копилка и награды"),
             ("Money not spent, time won back and times avoided, with a projection for a month, a year and five years. Add things you want and buy them from the savings.",
              "Сэкономленные деньги, возвращённое время и сколько раз удалось удержаться, плюс прогноз на месяц, год и пять лет. Добавь то, что хочется купить, и купи из копилки.")),
            (("Motivation", "Мотивация"),
             ("Your reasons to quit, a recovery timeline for smoking, alcohol, sugar or a general one that ticks off as time passes, and a quote of the day.",
              "Твои причины бросить, шкала восстановления для курения, алкоголя, сахара или общая, которая отмечается со временем, и цитата дня.")),
            (("Statistics", "Статистика"),
             ("Best, average, shortest and longest streaks, resets, cravings beaten and a chart of every streak.",
              "Лучшая, средняя, самая короткая и самая длинная серии, число сбросов, побеждённая тяга и график всех серий.")),
            (("Ten trophies", "Десять трофеев"),
             ("Shields from bronze to emerald, each with the date it was earned or the date it will be.",
              "Щиты от бронзы до изумруда, у каждого дата получения или дата, когда он будет получен.")),
            (("Calendar and diary", "Календарь и дневник"),
             ("Clean days in green, slips in red. Notes with a mood, cravings beaten and slips with their trigger, in one timeline. A slip logged by mistake can be undone.",
              "Чистые дни зелёные, срывы красные. Заметки с настроением, побеждённая тяга и срывы с причиной — в одной ленте. Срыв, отмеченный по ошибке, можно отменить.")),
            (("Milestones and a widget", "Вехи и виджет"),
             ("A short notification when you reach a new trophy, and a home-screen widget with clean days for up to three habits.",
              "Короткое уведомление о новом трофее и виджет на рабочем столе с чистыми днями для трёх привычек.")),
            (("Any habit", "Любая привычка"),
             ("16 ready-made habits, from smoking and alcohol to social media and nail biting, or your own with an icon you choose.",
              "16 готовых привычек, от курения и алкоголя до соцсетей и привычки грызть ногти, или своя с выбранной иконкой.")),
            (("Backup that stays yours", "Резервная копия у тебя"),
             ("Export everything to a JSON file and restore it on a new phone. No account, no cloud.",
              "Сохрани всё в JSON-файл и восстанови на новом телефоне. Без аккаунта и облака.")),
            (("Light and dark", "Светлая и тёмная"),
             ("Follows the system theme or set by hand, in English or Russian.",
              "Тема как в системе или на выбор, на английском или русском.")),
        ],
        "shots": [
            ("un-home.png", "un-home.ru.png", ("Home", "Главная"), ("Every habit, counting live.", "Все привычки, счётчик идёт.")),
            ("un-overview.png", "un-overview.ru.png", ("A habit", "Привычка"), ("The ring, the next goal and the calendar.", "Кольцо, следующая цель и календарь.")),
            ("un-sos.png", "un-sos.ru.png", ("Ride the wave", "Переждать волну"), ("Breathe with the circle until it passes.", "Дыши вместе с кругом, пока тяга не пройдёт.")),
            ("un-savings.png", "un-savings.ru.png", ("Savings", "Копилка"), ("Money kept and what it could buy.", "Сэкономленное и на что его потратить.")),
            ("un-trophies.png", "un-trophies.ru.png", ("Trophies", "Трофеи"), ("Ten shields, bronze to emerald.", "Десять щитов, от бронзы до изумруда.")),
            ("un-motivation.png", "un-motivation.ru.png", ("Motivation", "Мотивация"), ("Your reasons and what you win back.", "Твои причины и что ты возвращаешь себе.")),
        ],
        "extra": {
            "title": ("The goal ladder", "Лестница целей"),
            "head": [("Rung", "Ступень"), ("Goal", "Цель"), ("Trophy", "Трофей")],
            "rows": [
                [("1", "1"), ("1 day", "1 день"), ("Bronze", "Бронза")],
                [("2", "2"), ("3 days", "3 дня"), ("Bronze", "Бронза")],
                [("3", "3"), ("1 week", "1 неделя"), ("Bronze", "Бронза")],
                [("4", "4"), ("2 weeks", "2 недели"), ("Silver", "Серебро")],
                [("5", "5"), ("1 month", "1 месяц"), ("Silver", "Серебро")],
                [("6", "6"), ("3 months", "3 месяца"), ("Gold", "Золото")],
                [("7", "7"), ("6 months", "6 месяцев"), ("Gold", "Золото")],
                [("8", "8"), ("1 year", "1 год"), ("Emerald", "Изумруд")],
                [("9", "9"), ("2 years", "2 года"), ("Emerald", "Изумруд")],
                [("10", "10"), ("5 years", "5 лет"), ("Emerald", "Изумруд")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Unhook.apk", "Unhook.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer", "Android 8.0 (API 26) или новее")),
            (("Permissions", "Разрешения"), ("Notifications and start after reboot. No internet.", "Уведомления и запуск после перезагрузки. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Pick the habit, set the date of the last time and what it used to cost you.", "Выбери привычку, укажи, когда был последний раз и сколько она тебе стоила."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Unhook and set battery usage to No restrictions, or trophy notifications may arrive late. Settings → Notifications arrive late? opens the right screen.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Unhook автозапуск и сними ограничения батареи, иначе уведомления о трофеях могут опаздывать. «Настройки → Уведомления опаздывают?» откроет нужный экран."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/unhook.git\ncd unhook\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug          <c># to a connected phone</c>\n./gradlew installDebug -Pdemo   <c># demo build with made-up habits</c>",
        "faq": [
            (("What happens if I slip?", "Что будет, если я сорвусь?"),
             ("The counter starts again, but your best streak, trophies and history stay. A slip logged by mistake can be undone from the diary.",
              "Счётчик начнётся заново, но лучшая серия, трофеи и история останутся. Срыв, отмеченный по ошибке, можно отменить в дневнике.")),
            (("Is there a premium version?", "Есть ли премиум-версия?"),
             ("No. Every feature is unlocked for everyone, with no ads, no trial and no subscription.",
              "Нет. Все функции открыты для всех, без рекламы, пробного периода и подписки.")),
            (("Is anything sent anywhere?", "Что-то отправляется в сеть?"),
             ("No. No accounts, no servers, no analytics, and the app has no internet permission. Habits, diary and history live in a local database on the phone. Settings → Backup saves them to a file you keep.",
              "Нет. Ни аккаунтов, ни серверов, ни аналитики, и у приложения нет доступа к интернету. Привычки, дневник и история хранятся в локальной базе на телефоне. «Настройки → Резервная копия» сохранит их в файл, который останется у тебя.")),
            (("Is the recovery timeline medical advice?", "Шкала восстановления — это медицинский совет?"),
             ("No. It's general information to keep you going, not a substitute for a doctor.",
              "Нет. Это общая информация для поддержки, а не замена врачу.")),
        ],
    },
    {
        "slug": "dayquest",
        "name": "Dayquest",
        "panel": "app--dayquest",
        "gallery": "g-dayquest",
        "icon": "dayquest-logo.svg",
        "visual": "dq-tasks.png", "visual_ru": "dq-tasks.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/dayquest",
        "download": "https://github.com/bigdevwhale/dayquest/releases/latest/download/Dayquest.apk",
        "version": "v1.1.0",
        "tagline": ("Turn your days into a quest.", "Преврати дни в приключение."),
        "badge": ("Habit RPG · New", "RPG для привычек · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Habits stick when something small depends on them. <em>Turn your days into a quest.</em>",
                  "Привычки держатся, когда от них зависит что-то маленькое. <em>Преврати дни в приключение.</em>"),
        "desc": ("Your habits, dailies and to-dos power a pixel hero. Finish things and it levels up, finds pets, furnishes a home and beats bosses; skip your dailies and it gets hurt. Like Habitica, with richer pixel art, kinder mornings and content built to last for years. Free, no ads, no account.",
                 "Привычки, ежедневные задачи и дела двигают пиксельного героя. Делаешь — он растёт в уровнях, находит питомцев, обставляет дом и побеждает боссов; пропускаешь — ему достаётся. Как Habitica, но с более красивым пиксель-артом, мягким утром и контентом на годы. Бесплатно, без рекламы и аккаунта."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · No internet permission · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Без доступа к интернету · English и Русский"),
        "features": [
            (("Habits, dailies, to-dos", "Привычки, ежедневные и дела"),
             ("+ / − habits, dailies on chosen weekdays or every N days, to-dos with due dates and checklists that open right in the list. Neglected tasks turn red and pay more.",
              "Привычки с кнопками + / −, ежедневные по дням недели или раз в N дней, дела со сроками и чек-листами прямо в списке. Заброшенные задачи краснеют и приносят больше золота и опыта.")),
            (("A living pixel scene", "Живая пиксельная сцена"),
             ("Hero, pet and boss under a dithered sky that follows the real clock: dawn, sunset, stars and fireflies. Six places to unlock.",
              "Герой, питомец и босс под небом, которое живёт по реальным часам: рассвет, закат, звёзды и светлячки. Шесть мест, которые предстоит открыть.")),
            (("Boss fights", "Бои с боссами"),
             ("Finished tasks hit the boss, sometimes critically; missed dailies let it hit back. Numbers, sparks and coins fly across the scene.",
              "Сделанные задачи бьют босса, иногда критом; пропуски дают ему ударить в ответ. По сцене летят цифры, искры и монеты.")),
            (("88 pets", "88 питомцев"),
             ("8 species × 11 hatching potions. Pick an egg and a potion in one card, see who hatches, feed them their favourite food.",
              "8 видов × 11 инкубационных зелий. Яйцо и зелье выбираются в одной карточке, сразу видно, кто вылупится. Любимая еда растит питомца быстрее.")),
            (("Gear you can see", "Снаряжение на герое"),
             ("Every sword, robe, hat and shield changes your stats and your sprite. The shop lets you try it on before buying.",
              "Каждый меч, мантия, шляпа и щит меняют и характеристики, и спрайт. В лавке можно примерить перед покупкой.")),
            (("Real seasons", "Настоящие сезоны"),
             ("Blossom, summer, falling leaves and snow in every scene, with a seasonal potion, hat and boss. A switch for the southern hemisphere.",
              "Цветение, лето, листопад и снег во всех сценах, а с ними сезонное зелье, шляпа и босс. Есть переключатель для южного полушария.")),
            (("The endless forge", "Бесконечная кузница"),
             ("From level 20, a new tier of gear every 5 levels: rare, epic, legendary. It never runs out.",
              "С 20 уровня каждые 5 уровней — новый ранг снаряжения: редкое, эпическое, легендарное. Не кончается.")),
            (("Bosses that come back", "Боссы возвращаются"),
             ("Beaten bosses return as Elite, Ancient and Mythic, recoloured and tougher. A new boss of the week arrives every Monday.",
              "Побеждённые боссы возвращаются элитными, древними и мифическими — в новых цветах и сильнее. Каждый понедельник приходит новый босс недели.")),
            (("A home to furnish", "Свой дом"),
             ("27 pieces of furniture, wallpapers and floors. The fireplace glows at night and the window shows the real sky.",
              "27 предметов мебели, обои и полы. Ночью светится камин, в окне настоящее небо.")),
            (("Achievements that need time", "Достижения за время"),
             ("47 of them, from a 7-day streak to five years together, plus a yearly chronicle of what you got done.",
              "47 достижений — от серии в 7 дней до пяти лет вместе, плюс ежегодная летопись сделанного.")),
            (("Kind mornings, exact undo", "Мягкое утро и точная отмена"),
             ("Tick off yesterday's dailies before the day closes, move the day start for late nights, rest at the inn when ill, and undo any tap.",
              "Отметь вчерашние задачи до закрытия дня, сдвинь начало дня, если ложишься поздно, отдохни в таверне, когда болеешь, и отмени любое нажатие.")),
            (("A gentle start", "Мягкий старт"),
             ("A short illustrated guide before you create your hero, and a one-time tip on each screen the first time you open it.",
              "Короткий гайд с картинками до создания героя и одна подсказка на каждом экране при первом заходе.")),
            (("Your hero moves with you", "Герой переезжает с тобой"),
             ("No account: send yourself a file or a one-line code and import it on the new phone.",
              "Без аккаунта: отправь себе файл или однострочный код и импортируй его на новом телефоне.")),
        ],
        "shots": [
            ("dq-tasks.png", "dq-tasks.ru.png", ("Tasks", "Задачи"), ("The board under a living scene.", "Доска задач под живой сценой.")),
            ("dq-quests.png", "dq-quests.ru.png", ("Quests", "Квесты"), ("An elite rematch and the boss of the week.", "Элитный реванш и босс недели.")),
            ("dq-stable.png", "dq-stable.ru.png", ("Stable", "Питомцы"), ("Egg plus potion: see who hatches.", "Яйцо и зелье: сразу видно, кто вылупится.")),
            ("dq-shop.png", "dq-shop.ru.png", ("Shop", "Лавка"), ("Seasonal hats and gear you try on.", "Сезонные шляпы и примерка снаряжения.")),
            ("dq-home.png", "dq-home.ru.png", ("Home", "Дом"), ("A room to furnish with your gold.", "Комната, которую обставляешь на заработанное золото.")),
            ("dq-hero.png", "dq-hero.ru.png", ("Achievements", "Достижения"), ("Medals that take real time.", "Медали, на которые уходит реальное время.")),
        ],
        "extra": {
            "title": ("Built for years", "Рассчитано на годы"),
            "head": [("What", "Что"), ("How often", "Как часто"), ("What it brings", "Что даёт")],
            "rows": [
                [("Boss of the week", "Босс недели"), ("Every Monday", "Каждый понедельник"), ("Rare potions and eggs", "Редкие зелья и яйца")],
                [("Seasonal boss", "Сезонный босс"), ("Once a season", "Раз в сезон"), ("The season's potion", "Зелье сезона")],
                [("Seasonal hat", "Сезонная шляпа"), ("Sold only in its season", "Только в свой сезон"), ("Four to collect", "Собери все четыре")],
                [("Forge tier", "Ранг кузницы"), ("Every 5 levels from 20", "Каждые 5 уровней, начиная с 20-го"), ("Rare → epic → legendary gear", "Редкое → эпическое → легендарное")],
                [("Boss rematch", "Реванш с боссом"), ("After every win", "После каждой победы"), ("Elite, Ancient, Mythic", "Элитный, древний, мифический")],
                [("Achievements", "Достижения"), ("Up to 5 years", "До 5 лет"), ("47 medals and gold", "47 медалей и золото")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.1.0", "v1.1.0")),
            (("File", "Файл"), ("Dayquest.apk", "Dayquest.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer", "Android 8.0 (API 26) или новее")),
            (("Permissions", "Разрешения"), ("Notifications and start after reboot. No internet.", "Уведомления и запуск после перезагрузки. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Create your hero and pick a few starter tasks. Or choose I already have a hero to bring progress from another phone.", "Создай героя и выбери несколько стартовых задач. Или выбери «У меня уже есть герой», чтобы перенести прогресс с другого телефона."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Dayquest and set battery usage to No restrictions, or reminders may arrive late. Settings → Reminders don't arrive? opens the right screen.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Dayquest автозапуск и сними ограничения батареи, иначе напоминания могут приходить с опозданием. «Настройки → Не приходят напоминания?» откроет нужный экран."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/dayquest.git\ncd dayquest\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug          <c># to a connected phone</c>\n./gradlew installDebug -Pdemo   <c># demo build with a mid-game hero</c>",
        "faq": [
            (("Is it really free?", "Это правда бесплатно?"),
             ("Yes. Every feature is unlocked, with no ads, no gems to buy and no subscription.",
              "Да. Всё открыто, без рекламы, покупных кристаллов и подписки.")),
            (("How do I move my hero to a new phone?", "Как перенести героя на новый телефон?"),
             ("Settings → Move your progress: send a file or copy a one-line code, then on the new phone choose I already have a hero and import it.",
              "«Настройки → Перенос прогресса»: отправь файл или скопируй однострочный код, а на новом телефоне выбери «У меня уже есть герой» и импортируй его.")),
            (("Won't I run out of things to unlock?", "Не кончится ли контент?"),
             ("No. Seasons follow the calendar, the forge adds a tier every 5 levels, bosses return in stronger ranks and a new boss arrives every week.",
              "Нет. Сезоны идут по календарю, кузница добавляет ранг каждые 5 уровней, боссы возвращаются сильнее, а каждую неделю приходит новый.")),
            (("Is anything sent anywhere?", "Что-то отправляется в сеть?"),
             ("No. No accounts, no servers, no analytics, and the app has no internet permission. Everything lives in a local database on the phone.",
              "Нет. Ни аккаунтов, ни серверов, ни аналитики, и у приложения нет доступа к интернету. Всё хранится в локальной базе на телефоне.")),
        ],
    },
    {
        "slug": "serene",
        "name": "Serene",
        "panel": "app--serene",
        "gallery": "g-serene",
        "icon": "serene-logo.svg",
        "visual": "se-today.png", "visual_ru": "se-today.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/serene",
        "download": "https://github.com/bigdevwhale/serene/releases/latest/download/Serene.apk",
        "version": "v1.0.0",
        "tagline": ("A quiet place for your mind.", "Тихое место для ума."),
        "badge": ("Meditation · New", "Медитация · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Calm is a skill that grows from a few minutes a day. <em>A quiet place for your mind.</em>",
                  "Спокойствие — это навык, который растёт от нескольких минут в день. <em>Тихое место для ума.</em>"),
        "desc": ("Serene brings guided meditations, guided visualizations and affirmations into one calm app, for inner calm and harmony. Every session is read by a gentle voice recorded ahead of time and built into the app, so it all works offline. Free, with no ads, no premium and no account.",
                 "Serene собирает медитации, визуализации и аффирмации в одном спокойном приложении — для внутреннего покоя и гармонии. Каждую практику читает мягкий голос, записанный заранее и встроенный в приложение, поэтому всё работает без интернета. Бесплатно, без рекламы, премиума и аккаунта."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · No internet permission · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Без доступа к интернету · English и Русский"),
        "features": [
            (("Ten guided meditations", "Десять медитаций с голосом"),
             ("Calm in 3 minutes, breath awareness, body scan, loving-kindness, letting go, inner harmony, gratitude, morning intention, self-compassion and a sleep wind-down.",
              "Спокойствие за 3 минуты, наблюдение за дыханием, сканирование тела, любящая доброта, отпустить мысли, внутренняя гармония, благодарность, утреннее намерение, сострадание к себе и расслабление перед сном.")),
            (("Ten guided visualizations", "Десять визуализаций"),
             ("A safe place, a forest walk, the ocean shore, a mountain lake, healing light, meeting your future self, releasing worries, an inner garden, a goal achieved and a starry sky.",
              "Безопасное место, прогулка по лесу, берег океана, горное озеро, исцеляющий свет, встреча с собой из будущего, отпустить тревоги, внутренний сад, цель достигнута и звёздное небо.")),
            (("A calm voice, offline", "Спокойный голос без интернета"),
             ("Every session is read by a natural neural voice, recorded ahead of time and shipped inside the app. You can switch to your phone's own voice in Settings.",
              "Каждую практику читает естественный нейросетевой голос, записанный заранее и встроенный в приложение. В настройках можно переключиться на голос телефона.")),
            (("240 affirmations", "240 аффирмаций"),
             ("Twelve themes, from calm, self-love and confidence to sleep, courage and good morning. An affirmation of the day, favourites, your own lines and a daily mix read aloud with room to repeat.",
              "Двенадцать тем — от спокойствия, любви к себе и уверенности до сна, смелости и доброго утра. Аффирмация дня, избранное, свои фразы и микс дня вслух с паузой, чтобы повторить.")),
            (("A vision board", "Доска визуализаций"),
             ("Add what you want to bring into your life: a photo, how it looks and feels, and a line to say to yourself. Visualize my board turns it into your own guided session.",
              "Добавь то, что хочешь привести в свою жизнь: фото, как это выглядит и ощущается, и фразу для себя. «Визуализировать доску» превратит всё это в твою личную практику.")),
            (("Your own voice", "Твой собственный голос"),
             ("For your own affirmations and visions, record yourself in the app or upload an audio file. Or let the phone read your words.",
              "Для своих аффирмаций и визуализаций можно записать себя прямо в приложении или загрузить аудиофайл. Или пусть твои слова прочтёт телефон.")),
            (("Breathing", "Дыхание"),
             ("Calming 4-6, box, 4-7-8, coherent, the physiological sigh and equal breathing, with a glowing orb, soft tones and a light vibration.",
              "Успокаивающее 4-6, квадратное, 4-7-8, резонансное, физиологический вздох и ровное дыхание — со светящейся сферой, мягкими тонами и лёгкой вибрацией.")),
            (("Silent meditation", "Медитация в тишине"),
             ("A timer from 3 to 60 minutes with any background sound and a bell at the interval you choose.",
              "Таймер от 3 до 60 минут с любым фоном и колоколом через заданные интервалы.")),
            (("17 soundscapes", "17 фоновых звуков"),
             ("Real recordings of rain, thunderstorm, ocean, stream, wind, forest birds, a fireplace, a café, a train and more, reshuffled endlessly so they never audibly loop. Plus soft generative music, a warm tone and deep noise. The sound dips while the voice speaks.",
              "Настоящие записи дождя, грозы, океана, ручья, ветра, леса с птицами, камина, кафе, поезда и других — бесконечно перемешанные, чтобы не звучать по кругу. Плюс генеративная мягкая музыка, тёплый тон и глубокий шум. Пока говорит голос, фон становится тише.")),
            (("Journal and balance", "Дневник и баланс"),
             ("Mood check-ins, three good things, notes, a two-week mood chart, a practice calendar, your streak and minutes. The wheel of balance rates body, mind, relationships, work, rest and joy.",
              "Отметки настроения, три хороших вещи, заметки, график настроения за две недели, календарь практик, серия и минуты. Колесо баланса оценивает тело, ум, отношения, дело, отдых и радость.")),
            (("Gentle reminders and a widget", "Мягкие напоминания и виджет"),
             ("A morning affirmation and an evening wind-down at the time you pick, and a home-screen widget with the affirmation of the day.",
              "Утренняя аффирмация и вечернее приглашение расслабиться в выбранное время, а также виджет с аффирмацией дня на рабочем столе.")),
            (("Yours, in two languages", "Твоё, на двух языках"),
             ("Back up to a JSON file (photos stay on the phone), light and dark themes, and English and Russian written natively, not machine-translated.",
              "Резервная копия в JSON-файл (фото остаются на телефоне), светлая и тёмная темы, английский и русский, написанные вручную, без машинного перевода.")),
        ],
        "shots": [
            ("se-today.png", "se-today.ru.png", ("Today", "Сегодня"), ("The affirmation of the day and your practice.", "Аффирмация дня и твоя практика.")),
            ("se-practice.png", "se-practice.ru.png", ("Practice", "Практики"), ("Meditate, visualize, breathe.", "Медитации, визуализации, дыхание.")),
            ("se-player.png", "se-player.ru.png", ("A guided session", "Практика с голосом"), ("A calm voice over a slow, living scene.", "Спокойный голос и медленная живая сцена.")),
            ("se-breathe.png", "se-breathe.ru.png", ("Breathe", "Дыхание"), ("A glowing orb to breathe with.", "Светящаяся сфера, с которой дышишь.")),
            ("se-affirm.png", "se-affirm.ru.png", ("Affirmations", "Аффирмации"), ("Twelve themes and your daily mix.", "Двенадцать тем и микс дня.")),
            ("se-journal.png", "se-journal.ru.png", ("Journal", "Дневник"), ("Mood, gratitude and your practice.", "Настроение, благодарность и практика.")),
            ("se-visions.png", "se-visions.ru.png", ("Vision board", "Доска визуализаций"), ("What you want, ready to visualize.", "То, чего хочешь, готово к визуализации.")),
        ],
        "extra": {
            "title": ("Six ways to breathe", "Шесть способов дышать"),
            "head": [("Pattern", "Техника"), ("Rhythm", "Ритм"), ("Good for", "Когда помогает")],
            "rows": [
                [("Calming", "Успокаивающее"), ("4 · 6", "4 · 6"), ("Winding down", "Чтобы расслабиться")],
                [("Box", "Квадратное"), ("4 · 4 · 4 · 4", "4 · 4 · 4 · 4"), ("A racing mind", "Когда мысли скачут")],
                [("4-7-8", "4-7-8"), ("4 · 7 · 8", "4 · 7 · 8"), ("Falling asleep", "Чтобы уснуть")],
                [("Coherent", "Резонансное"), ("5.5 · 5.5", "5,5 · 5,5"), ("Balance", "Для равновесия")],
                [("Physiological sigh", "Физиологический вздох"), ("2.5 · 1 · 6", "2,5 · 1 · 6"), ("The fastest release", "Быстрее всего снимает напряжение")],
                [("Equal", "Ровное"), ("4 · 4", "4 · 4"), ("Centring", "Чтобы собраться")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Serene.apk", "Serene.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer", "Android 8.0 (API 26) или новее")),
            (("Permissions", "Разрешения"), ("Notifications, start after reboot and vibration. The microphone only when you record your own voice. No internet.",
                                            "Уведомления, запуск после перезагрузки и вибрация. Микрофон — только когда записываешь свой голос. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Pick the themes that matter to you, then start with Calm in 3 minutes.", "Выбери близкие тебе темы и начни со «Спокойствия за 3 минуты»."),
        ],
        "note": ("The voice needs nothing on your phone: the narration is built into the app. On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Serene so reminders arrive on time.",
                 "Для голоса на телефоне ничего ставить не нужно: озвучка встроена в приложение. На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Serene автозапуск, чтобы напоминания приходили вовремя."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/serene.git\ncd serene\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug          <c># app.serene.dev</c>\n./gradlew installDebug -Pdemo   <c># demo build with made-up visions</c>",
        "faq": [
            (("Is there a premium version?", "Есть ли премиум-версия?"),
             ("No. Every meditation, visualization, sound and affirmation is unlocked for everyone, with no ads, no trial and no subscription.",
              "Нет. Все медитации, визуализации, звуки и аффирмации открыты для всех, без рекламы, пробного периода и подписки.")),
            (("Is anything sent anywhere?", "Что-то отправляется в сеть?"),
             ("No. No accounts, no servers, no analytics, and the app has no internet permission. Your journal, favourites and visions live in a local database on the phone. Settings → Backup saves everything except photos to a file you keep.",
              "Нет. Ни аккаунтов, ни серверов, ни аналитики, и у приложения нет доступа к интернету. Дневник, избранное и визуализации хранятся в локальной базе на телефоне. «Настройки → Резервная копия» сохранит всё, кроме фото, в файл, который останется у тебя.")),
            (("Is it medical or psychological treatment?", "Это лечение или психотерапия?"),
             ("No. Serene is for relaxation and well-being. It doesn't replace a doctor or a therapist.",
              "Нет. Serene — для расслабления и хорошего самочувствия. Приложение не заменяет врача или психотерапевта.")),
            (("Whose voices and sounds are these?", "Чьи это голоса и звуки?"),
             ("The narration was made with open neural voices: Silero for Russian (CC BY-NC-SA 4.0) and Kokoro-82M for English (Apache 2.0). The nature recordings come from the Blanket project, under CC0, CC BY, CC BY-SA or public domain. Full credits are in the README.",
              "Озвучка сделана открытыми нейросетевыми голосами: Silero для русского (CC BY-NC-SA 4.0) и Kokoro-82M для английского (Apache 2.0). Записи природы взяты из проекта Blanket, под лицензиями CC0, CC BY, CC BY-SA или в общественном достоянии. Полный список авторов — в README.")),
        ],
    },
    {
        "slug": "ember",
        "name": "Ember",
        "panel": "app--ember",
        "gallery": "g-ember",
        "icon": "ember-logo.svg",
        "visual": "em-fast.png", "visual_ru": "em-fast.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/ember",
        "download": "https://github.com/bigdevwhale/ember/releases/latest/download/Ember.apk",
        "version": "v1.0.0",
        "tagline": ("Intermittent fasting, made warm and simple.", "Интервальное голодание — тепло и просто."),
        "badge": ("Fasting · New", "Голодание · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Fasting is simple. Doing it day after day is the hard part. <em>Intermittent fasting, made warm and simple.</em>",
                  "Голодать просто. Сложно делать это день за днём. <em>Интервальное голодание — тепло и просто.</em>"),
        "desc": ("Ember is a fasting timer that explains what your body is doing as the hours pass, cheers you on when the goal is reached and is there when hunger knocks. Streaks, levels, badges and weekly challenges keep the fire going. Most fasting apps lock their best parts behind a subscription. Here everything is free, with no ads and no account, and nothing leaves your phone.",
                 "Ember — таймер голодания, который объясняет, что происходит в теле с каждым часом, радуется вместе с тобой, когда цель достигнута, и помогает, когда подступает голод. Серии, уровни, награды и испытания недели поддерживают огонь. Большинство приложений для голодания прячут лучшее за подпиской. Здесь всё бесплатно, без рекламы и аккаунта, и ничего не покидает телефон."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · No internet permission · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Без доступа к интернету · English и Русский"),
        "features": [
            (("A timer that explains", "Таймер, который объясняет"),
             ("The ring is split into eight coloured stages, from digestion and the fuel switch to fat burning, ketosis, autophagy, the growth-hormone rise and deep renewal. You see the stage you're in, the time to the next one and a short note for every hour.",
              "Кольцо разделено на восемь цветных этапов — от переваривания и смены топлива до жиросжигания, кетоза, аутофагии, подъёма гормона роста и глубокого обновления. Видно текущий этап, время до следующего и короткую заметку на каждый час.")),
            (("Plans for every level", "Планы для любого уровня"),
             ("12:12, 14:10, 16:8, 18:6, 20:4, one meal a day, 24, 36, 48 and 72 hours, or a length of your own. Set when the daily fast begins and Ember shows your eating window.",
              "12:12, 14:10, 16:8, 18:6, 20:4, еда раз в день, 24, 36, 48 и 72 часа или своя длительность. Укажи, когда начинается голодание, и Ember покажет окно питания.")),
            (("Streaks and levels", "Серии и уровни"),
             ("Every day you reach your goal keeps the fire going. Levels grow with the hours you fast, from Spark to Sun.",
              "Каждый день с достигнутой целью поддерживает огонь. Уровни растут вместе с часами голодания — от Искры до Солнца.")),
            (("33 badges and weekly challenges", "33 награды и испытания недели"),
             ("Badges for long fasts, streaks, total hours, weight, water, check-ins and hunger waves ridden out. A new challenge arrives every Monday: five good days, an early dinner, a longer fast.",
              "Награды за долгие голодания, серии, общее время, вес, воду, отметки самочувствия и пережитые волны голода. Каждый понедельник — новое испытание: пять хороших дней, ранний ужин, голодание подольше.")),
            (("Hunger SOS", "Голод SOS"),
             ("Hunger comes in waves and passes in 15–20 minutes. A 15-minute timer with a breathing circle helps you ride it out, with ten quick things that help right now.",
              "Голод приходит волнами и проходит за 15–20 минут. Пятнадцатиминутный таймер с дыхательным кругом помогает переждать волну, а рядом десять быстрых способов себе помочь.")),
            (("Progress and a calendar", "Прогресс и календарь"),
             ("Hours fasted per week or month, a calendar of reached goals, stats and the full history. Edit any fast, add one you forgot or discard one started by mistake.",
              "Часы голодания за неделю или месяц, календарь достигнутых целей, статистика и вся история. Любое голодание можно поправить, добавить забытое или удалить начатое по ошибке.")),
            (("Weight, water and check-ins", "Вес, вода и самочувствие"),
             ("A weight chart with a goal and BMI, in kilograms or pounds, a daily water counter, and quick check-ins for hunger, energy and mood.",
              "График веса с целью и ИМТ в килограммах или фунтах, счётчик воды на день и быстрые отметки голода, энергии и настроения.")),
            (("18 short articles", "18 коротких статей"),
             ("Short, honest reading: what breaks a fast, electrolytes, how to break a fast well, exercise, sleep, fasting for women, longer fasts and safety. Plus the eight stages explained.",
              "Коротко и честно: что прерывает голодание, электролиты, как правильно выходить из голодания, спорт, сон, голодание для женщин, долгие голодания и безопасность. И подробно о каждом из восьми этапов.")),
            (("Notifications and a widget", "Уведомления и виджет"),
             ("A quiet live timer in the notification shade, alerts for the goal and each new stage, a nudge at your scheduled start with a Start now button, and a home-screen widget.",
              "Тихий живой таймер в шторке, сообщения о цели и каждом новом этапе, напоминание по расписанию с кнопкой «Начать сейчас» и виджет на главный экран.")),
            (("Nothing leaves your phone", "Всё остаётся на телефоне"),
             ("No account, no servers, no analytics, no ads and no internet permission. Fasts, weight, water and check-ins live on the phone, and a JSON backup stays with you.",
              "Ни аккаунта, ни серверов, ни аналитики, ни рекламы, ни доступа к интернету. Голодания, вес, вода и самочувствие хранятся на телефоне, а резервная копия в JSON остаётся у тебя.")),
            (("Safety first", "Сначала безопасность"),
             ("Fasting isn't for everyone. Ember shares general information and is not medical advice. Talk to a doctor first if you're pregnant, under 18, have diabetes, an eating disorder or a chronic condition.",
              "Голодание подходит не всем. Ember делится общей информацией и не заменяет врача. Сначала посоветуйся с врачом при беременности, если тебе меньше 18, есть диабет, расстройство пищевого поведения или хроническое заболевание.")),
            (("Yours, in two languages", "Твоё, на двух языках"),
             ("Light and dark themes, and English and Russian written natively, not machine-translated. The Russian texts are gender-neutral.",
              "Светлая и тёмная темы, английский и русский, написанные вручную, без машинного перевода. Русские тексты гендерно-нейтральны.")),
        ],
        "shots": [
            ("em-fast.png", "em-fast.ru.png", ("Fast", "Голодание"), ("The ring of stages and where you are now.", "Кольцо этапов и то, где ты сейчас.")),
            ("em-today.png", "em-today.ru.png", ("Today", "Сегодня"), ("Hunger SOS, water and the weekly challenge.", "Голод SOS, вода и испытание недели.")),
            ("em-stages.png", "em-stages.ru.png", ("Stages", "Этапы"), ("What your body is doing, hour by hour.", "Что происходит в теле, час за часом.")),
            ("em-hunger.png", "em-hunger.ru.png", ("Hunger SOS", "Голод SOS"), ("Breathe and ride the wave.", "Дыши и пережди волну.")),
            ("em-progress.png", "em-progress.ru.png", ("Progress", "Прогресс"), ("Hours fasted, week by week.", "Часы голодания, неделя за неделей.")),
            ("em-calendar.png", "em-calendar.ru.png", ("Calendar", "Календарь"), ("Reached goals and your weight.", "Достигнутые цели и вес.")),
            ("em-learn.png", "em-learn.ru.png", ("Learn", "Знания"), ("Short, honest articles.", "Короткие честные статьи.")),
            ("em-badges.png", "em-badges.ru.png", ("Badges", "Награды"), ("Your level and 33 badges.", "Твой уровень и 33 награды.")),
        ],
        "extra": {
            "title": ("Eight stages of a fast", "Восемь этапов голодания"),
            "head": [("From", "С"), ("Stage", "Этап"), ("What happens", "Что происходит")],
            "rows": [
                [("0 h", "0 ч"), ("Digesting food", "Идёт переваривание"), ("Your body is busy with your last meal", "Тело переваривает еду и запасает энергию")],
                [("4 h", "4 ч"), ("Settling down", "Сахар выравнивается"), ("Blood sugar and insulin drift back to baseline", "Сахар и инсулин возвращаются к исходному уровню")],
                [("8 h", "8 ч"), ("Shifting gears", "Смена топлива"), ("Glycogen runs lower and your body turns toward fat", "Гликоген убывает, тело переходит на жир")],
                [("12 h", "12 ч"), ("Fat burning", "Метаболическое переключение"), ("Fat becomes a main fuel", "Сжигание жира растёт, появляются кетоны")],
                [("16 h", "16 ч"), ("Into ketosis", "Лёгкий кетоз"), ("Ketones climb, and many people feel clear and steady", "Кетонов больше, голова часто яснее")],
                [("24 h", "24 ч"), ("Cellular cleanup", "Клеточная уборка"), ("Autophagy is thought to increase", "Аутофагия, вероятно, усиливается")],
                [("48 h", "48 ч"), ("Growth hormone", "Гормон роста"), ("Growth hormone rises and insulin stays very low", "Гормон роста выше, инсулин очень низкий")],
                [("72 h", "72 ч"), ("Deep renewal", "Глубокое обновление"), ("Early research hints at deeper renewal. Go carefully", "Глубокая перестройка — только при крепком здоровье")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Ember.apk", "Ember.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer", "Android 8.0 (API 26) или новее")),
            (("Permissions", "Разрешения"), ("Notifications, start after reboot and vibration, for the timer and reminders. No internet.",
                                            "Уведомления, запуск после перезагрузки и вибрация — для таймера и напоминаний. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Pick a plan that fits, 14:10 or 16:8 is a good start, and light the first fast.", "Выбери подходящий план — 14:10 или 16:8 для начала — и зажги первое голодание."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Ember and remove battery limits so the timer notification and reminders arrive on time.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Ember автозапуск и сними ограничения батареи, чтобы таймер в шторке и напоминания приходили вовремя."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/ember.git\ncd ember\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug -Pdemo   <c># app.ember.demo with a made-up history</c>",
        "faq": [
            (("Is there a premium version?", "Есть ли премиум-версия?"),
             ("No. Every plan, stage, article, badge and challenge is unlocked for everyone, with no ads, no trial and no subscription.",
              "Нет. Все планы, этапы, статьи, награды и испытания открыты для всех, без рекламы, пробного периода и подписки.")),
            (("Is anything sent anywhere?", "Что-то отправляется в сеть?"),
             ("No. No accounts, no servers, no analytics, and the app has no internet permission. Fasts, weight, water and check-ins live in a local database on the phone. Settings → Backup exports everything to a JSON file you keep.",
              "Нет. Ни аккаунтов, ни серверов, ни аналитики, и у приложения нет доступа к интернету. Голодания, вес, вода и самочувствие хранятся в локальной базе на телефоне. «Настройки → Резервная копия» выгрузит всё в JSON-файл, который останется у тебя.")),
            (("Is fasting safe for me?", "Мне можно голодать?"),
             ("Fasting isn't for everyone. Talk to a doctor first if you're pregnant or breastfeeding, under 18, have had an eating disorder, have diabetes or take medication that lowers blood sugar, or live with a chronic condition. Stop a fast whenever you feel faint or unwell. Ember shares general information and is not medical advice.",
              "Голодание подходит не всем. Сначала посоветуйся с врачом, если ты ждёшь ребёнка или кормишь грудью, тебе меньше 18 лет, было расстройство пищевого поведения, есть диабет или ты принимаешь препараты, снижающие сахар, или есть хроническое заболевание. Прекращай голодание при слабости или плохом самочувствии. Ember делится общей информацией и не заменяет врача.")),
            (("What if I forget to start or stop the timer?", "А если забыть запустить или остановить таймер?"),
             ("Fix the start or end time of any fast, add a past fast you forgot to log, or discard one started by mistake. Streaks and badges are counted from the history, so they follow your edits.",
              "Время начала и конца любого голодания можно поправить, прошлое голодание — добавить задним числом, а начатое по ошибке — удалить. Серии и награды считаются по истории, поэтому учтут правки.")),
        ],
    },
]

COMMON = {
    "pg.inside": ("What's inside", "Что внутри"),
    "pg.captured": ("Screens", "Экраны"),
    "pg.get": ("Get it", "Скачать"),
    "pg.install": ("Install", "Установка"),
    "pg.source": ("Build from source", "Сборка из исходников"),
    "pg.requires": ("Requires", "Нужно"),
    "pg.faq": ("Good to know", "Полезно знать"),
    "pg.family": ("More from Stillcraft", "Ещё от Stillcraft"),
    "pg.familyTitle": ("Other tools on the shelf.", "Другие инструменты на полке."),
    "pg.github": ("View on GitHub", "Открыть на GitHub"),
    "pg.allrel": ("All releases", "Все релизы"),
    "pg.issue": ("Open an issue", "Написать в issues"),
    "pg.helpDesc": ("Found a bug, missing a feature, or want it in your language? Tell us on GitHub.",
                    "Нашёл ошибку, не хватает функции или нужен твой язык? Напиши на GitHub."),
    "ap.explore": ("Explore", "Подробнее"),
    "nav.apps": ("Apps", "Приложения"),
}


def esc(s):
    return html.escape(s, quote=True)


class Page:
    def __init__(self):
        self.ru = {}
        self.n = 0

    def t(self, pair, key=None, tag=None, cls=None):
        """Return the English text and register its Russian twin under a key."""
        if key is None:
            self.n += 1
            key = "pg.k%d" % self.n
        en, ru = pair
        self.ru[key] = ru
        attrs = ' data-i18n="%s"' % key
        if cls:
            attrs = ' class="%s"' % cls + attrs
        if tag:
            return "<%s%s>%s</%s>" % (tag, attrs, en, tag)
        return attrs, en


def card(app, p):
    status_cls, s_en, s_ru = app["status"]
    vis_cls = "cv-" + {"anyway": "aw", "swisszen": "sz", "focusshield": "fs", "ties": "ti", "unhook": "un", "dayquest": "dq", "serene": "se", "ember": "em"}[app["slug"]]
    shot = {"anyway": ("en-now.png", "ru-now.png"), "swisszen": ("sz-home.png", "sz-home.ru.png"), "focusshield": ("fs-break.gif", None),
            "ties": ("ti-home.png", "ti-home.ru.png"), "unhook": ("un-home.png", "un-home.ru.png"), "dayquest": ("dq-tasks.png", "dq-tasks.ru.png"),
            "serene": ("se-today.png", "se-today.ru.png"), "ember": ("em-fast.png", "em-fast.ru.png")}[app["slug"]]
    ru_attr = ' data-src-ru="%s%s"' % (A, shot[1]) if shot[1] else ""
    return """        <a class="card" href="../{slug}/">
          <div class="card-visual {vis}">
            <img src="{A}{img}"{ru} alt="{name}" loading="lazy">
          </div>
          <div class="card-body">
            <div class="card-id">
              <img src="{A}{icon}" alt="" width="44" height="44">
              <h3>{name}</h3>
              <span class="ver">{ver}</span>
            </div>
            {tagline}
            <div class="badges">
              {status}
              {fileb}
            </div>
            <div class="badges">
              <span class="badge plat">{plat}</span>
              <span class="badge plat">EN · RU</span>
            </div>
            <span class="card-more">{explore} {name}</span>
          </div>
        </a>""".format(
        slug=app["slug"], vis=vis_cls, A=A, img=shot[0], ru=ru_attr, name=app["name"], icon=app["icon"], ver=app["version"],
        tagline=p.t(app["tagline"], "fam.%s.tag" % app["slug"], "p", "card-tagline"),
        status=p.t((s_en, s_ru), "fam.%s.st" % app["slug"], "span", "badge " + status_cls),
        fileb=p.t(app["file_badge"], "fam.%s.fb" % app["slug"], "span", "badge ok"),
        plat=app["plat_badge"], explore=p.t(COMMON["ap.explore"], "ap.explore", "span"))


def build(app):
    p = Page()
    name = app["name"]

    ru_vis = ' data-src-ru="%s%s"' % (A, app["visual_ru"]) if app["visual_ru"] else ""
    features = "\n".join(
        """        <article class="moment">
          {h}
          {d}
        </article>""".format(h=p.t(h, tag="h3", cls="when"), d=p.t(d, tag="p")) for h, d in app["features"])

    shots = "\n".join(
        """        <figure>
          <div class="shot-box"><img src="{A}{src}"{ru} alt="{alt}" loading="lazy"></div>
          <figcaption>{cap}{desc}</figcaption>
        </figure>""".format(A=A, src=s, ru=(' data-src-ru="%s%s"' % (A, r)) if r else "", alt=esc(name + ": " + c[0]),
                            cap=p.t(c, tag="b"), desc=p.t(d, tag="span")) for s, r, c, d in app["shots"])

    extra = ""
    if app["extra"]:
        x = app["extra"]
        head = "".join(p.t(h, tag="th") for h in x["head"])
        rows = "\n".join("            <tr>%s</tr>" % "".join(p.t(c, tag="td") for c in row) for row in x["rows"])
        extra = """
  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        {title}
      </div>
      <div class="spec">
        <table>
          <thead><tr>{head}</tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </div>
  </section>
""".format(title=p.t(x["title"], tag="h2"), head=head, rows=rows)

    facts = "\n".join("            %s<dd>%s</dd>" % (p.t(k, tag="dt"), p.t(v, tag="span")) for k, v in app["facts"])
    steps = "\n".join("            " + p.t(s, tag="li") for s in app["steps"])
    note = ('          ' + p.t(app["note"], tag="p", cls="note")) if app["note"] else ""
    faq = "\n".join(
        """        <details>
          <summary>{q}</summary>
          {a}
        </details>""".format(q=p.t(q, tag="span"), a=p.t(a, tag="p")) for q, a in app["faq"])
    family = "\n".join(card(o, p) for o in APPS if o is not app)

    a_cta, cta_en = p.t(app["cta"], "pg.cta")
    a_title, title_en = p.t(app["title"], "pg.title")
    target = "" if app["download"].endswith((".apk", ".exe")) else ' target="_blank" rel="noopener"'
    for k in COMMON:
        p.ru[k] = COMMON[k][1]

    def ct(key):
        a, en = p.t(COMMON[key], key)
        return a, en

    a_gh, gh_en = ct("pg.github")
    out = TEMPLATE.format(
        name=name, slug=app["slug"], A=A, desc_meta=esc(app["tagline"][0]),
        panel=app["panel"], icon=app["icon"],
        badge=p.t(app["badge"], tag="span", cls="app-tag"),
        a_title=a_title, title_en=title_en,
        desc=p.t(app["desc"], tag="p", cls="app-desc"),
        download=app["download"], target=target, a_cta=a_cta, cta_en=cta_en,
        repo=app["repo"], a_gh=a_gh, gh_en=gh_en,
        plat=p.t(app["plat"], tag="p", cls="ap-plat"),
        visual=app["visual"], ru_vis=ru_vis, wide=" wide" if app["visual_wide"] else "",
        inside=p.t(COMMON["pg.inside"], "pg.inside", "span", "eyebrow"),
        inside_title=p.t(("Everything %s does." % name, "Всё, что умеет %s." % name), "pg.insideTitle", "h2"),
        features=features,
        captured=p.t(COMMON["pg.captured"], "pg.captured", "span", "eyebrow"),
        captured_title=p.t(("Captured in %s." % name, "Снято в %s." % name), "pg.capTitle", "h2"),
        gallery=app["gallery"], shots=shots, extra=extra,
        get=p.t(COMMON["pg.get"], "pg.get", "span", "eyebrow"),
        get_title=p.t(("Get %s." % name, "Скачай %s." % name), "pg.getTitle", "h2"),
        install=p.t(COMMON["pg.install"], "pg.install", "h3"),
        facts=facts, steps=steps, note=note,
        allrel=p.t(COMMON["pg.allrel"], "pg.allrel", "span"),
        source=p.t(COMMON["pg.source"], "pg.source", "h3"),
        build_req=p.t(app["build_req"], tag="p", cls="card-tagline"),
        build=app["build"].replace("<c>", '<span class="c">').replace("</c>", "</span>"),
        faq_eyebrow=p.t(COMMON["pg.faq"], "pg.faq", "span", "eyebrow"),
        faq_title=p.t(("Questions people ask.", "Частые вопросы."), "pg.faqTitle", "h2"),
        faq=faq,
        fam=p.t(COMMON["pg.family"], "pg.family", "span", "eyebrow"),
        fam_title=p.t(COMMON["pg.familyTitle"], "pg.familyTitle", "h2"),
        family=family,
        help_title=p.t(("Help shape %s." % name, "Помоги сделать %s лучше." % name), "pg.helpTitle", "h2"),
        help_desc=p.t(COMMON["pg.helpDesc"], "pg.helpDesc", "p"),
        issue=p.t(COMMON["pg.issue"], "pg.issue", "span"),
        ru_json=json.dumps(p.ru, ensure_ascii=False, indent=0),
    )
    path = os.path.join(ROOT, "apps", app["slug"], "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("wrote", os.path.relpath(path, ROOT))


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{name} · Stillcraft</title>
<meta name="description" content="{desc_meta}">
<link rel="icon" href="{A}stillcraft.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,600&family=Figtree:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{A}site.css">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W6SRW929L"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-9W6SRW929L');
</script>
</head>
<!-- Generated by tools/build_app_pages.py. Edit the data there, not this file. -->
<body>

<nav class="nav" aria-label="Main">
  <div class="wrap">
    <a class="brand" href="../../" aria-label="Stillcraft home">
      <svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="14" r="7" fill="var(--lamp)"/><rect x="3" y="20.5" width="26" height="1.6" rx=".8" fill="currentColor"/><rect x="9" y="24.5" width="14" height="1.6" rx=".8" fill="currentColor" opacity=".45"/></svg>
      Stillcraft
    </a>
    <div class="nav-links">
      <a href="../" aria-current="page" data-i18n="nav.apps">Apps</a>
      <a href="../../#moments" data-i18n="nav.moments">Pick a moment</a>
      <a href="../../#principles" data-i18n="nav.principles">Principles</a>
      <a href="https://github.com/bigdevwhale" target="_blank" rel="noopener">GitHub</a>
    </div>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" id="lang-en" data-lang="en" aria-pressed="true">EN</button>
      <button type="button" id="lang-ru" data-lang="ru" aria-pressed="false">RU</button>
    </div>
  </div>
</nav>

<header class="wrap">
  <p class="crumbs"><a href="../../">Stillcraft</a> / <a href="../" data-i18n="nav.apps">Apps</a> / {name}</p>
  <div class="app {panel} ap-band">
    <div class="ap-copy">
      <div class="app-id">
        <img src="{A}{icon}" alt="" width="56" height="56">
        <div>
          {badge}
        </div>
      </div>
      <h1{a_title}>{title_en}</h1>
      {desc}
      <div class="app-actions">
        <a class="btn btn-primary" href="{download}"{target}{a_cta}>{cta_en}</a>
        <a class="btn btn-ghost" href="{repo}" target="_blank" rel="noopener"{a_gh}>{gh_en}</a>
      </div>
      {plat}
    </div>
    <div class="ap-visual{wide}">
      <img src="{A}{visual}"{ru_vis} alt="{name}">
    </div>
  </div>
</header>

<main>
  <section class="section">
    <div class="wrap">
      <div class="section-head">
        {inside}
        {inside_title}
      </div>
      <div class="moments feature-grid">
{features}
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        {captured}
        {captured_title}
      </div>
      <div class="gallery {gallery}">
{shots}
      </div>
    </div>
  </section>
{extra}
  <section class="section" id="get" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        {get}
        {get_title}
      </div>
      <div class="get">
        <div class="get-card">
          {install}
          <dl class="get-facts">
{facts}
          </dl>
          <ol class="steps">
{steps}
          </ol>
{note}
          <div class="app-actions">
            <a class="btn btn-primary" href="{download}"{target}{a_cta}>{cta_en}</a>
            <a class="btn btn-ghost" href="{repo}/releases" target="_blank" rel="noopener">{allrel}</a>
          </div>
        </div>
        <div class="get-card">
          {source}
          {build_req}
          <pre class="code">{build}</pre>
        </div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        {faq_eyebrow}
        {faq_title}
      </div>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="section-head">
        {fam}
        {fam_title}
      </div>
      <div class="lineup">
{family}
      </div>
    </div>
  </section>

  <section class="closing">
    <div class="wrap">
      {help_title}
      {help_desc}
      <a class="btn btn-primary" href="{repo}/issues/new" target="_blank" rel="noopener">{issue}</a>
    </div>
  </section>
</main>

<footer class="site">
  <div class="wrap">
    <div class="foot-brand">
      <a class="brand" href="../../">
        <svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="14" r="7" fill="var(--lamp)"/><rect x="3" y="20.5" width="26" height="1.6" rx=".8" fill="currentColor"/><rect x="9" y="24.5" width="14" height="1.6" rx=".8" fill="currentColor" opacity=".45"/></svg>
        Stillcraft
      </a>
      <p data-i18n="ft.tag">Small tools for a quieter mind.</p>
    </div>
    <div>
      <h4 data-i18n="ft.apps">Apps</h4>
      <ul>
        <li><a href="../anyway/">Anyway</a></li>
        <li><a href="../swisszen/">SwissZen</a></li>
        <li><a href="../focusshield/">FocusShield</a></li>
        <li><a href="../ties/">Ties</a></li>
        <li><a href="../unhook/">Unhook</a></li>
        <li><a href="../dayquest/">Dayquest</a></li>
        <li><a href="../serene/">Serene</a></li>
        <li><a href="../ember/">Ember</a></li>
        <li><a href="../" data-i18n="ft.all">All apps</a></li>
      </ul>
    </div>
    <div>
      <h4 data-i18n="ft.source">Source</h4>
      <ul>
        <li><a href="https://github.com/bigdevwhale" target="_blank" rel="noopener">GitHub</a></li>
        <li><a href="https://github.com/bigdevwhale/anyway/releases" target="_blank" rel="noopener" data-i18n="ft.awrel">Anyway releases</a></li>
        <li><a href="https://github.com/bigdevwhale/SwissZen/releases" target="_blank" rel="noopener" data-i18n="ft.szrel">SwissZen releases</a></li>
        <li><a href="https://github.com/bigdevwhale/focus-shield/releases" target="_blank" rel="noopener" data-i18n="ft.fsrel">FocusShield releases</a></li>
        <li><a href="https://github.com/bigdevwhale/ties/releases" target="_blank" rel="noopener" data-i18n="ft.tirel">Ties releases</a></li>
        <li><a href="https://github.com/bigdevwhale/unhook/releases" target="_blank" rel="noopener" data-i18n="ft.unrel">Unhook releases</a></li>
        <li><a href="https://github.com/bigdevwhale/dayquest/releases" target="_blank" rel="noopener" data-i18n="ft.dqrel">Dayquest releases</a></li>
        <li><a href="https://github.com/bigdevwhale/serene/releases" target="_blank" rel="noopener" data-i18n="ft.serel">Serene releases</a></li>
        <li><a href="https://github.com/bigdevwhale/ember/releases" target="_blank" rel="noopener" data-i18n="ft.emrel">Ember releases</a></li>
      </ul>
    </div>
    <div class="fine">
      <span data-i18n="ft.made">© 2026 Stillcraft. Made slowly.</span>
      <span data-i18n="ft.med">Breathing exercises are not medical treatment. Practice sitting or lying down, never in water or while driving.</span>
    </div>
  </div>
</footer>

<script>window.PAGE_RU = {ru_json};</script>
<script src="{A}site.js"></script>
</body>
</html>
"""

def stamp_assets():
    """Append ?v=<content hash> to site.css and site.js in every page so browsers drop stale copies."""
    versions = {}
    for name in ("site.css", "site.js"):
        with open(os.path.join(ROOT, "assets", name), "rb") as f:
            versions[name] = hashlib.sha1(f.read()).hexdigest()[:8]
    pages = [os.path.join(ROOT, "index.html")] + glob.glob(os.path.join(ROOT, "apps", "**", "index.html"), recursive=True)
    for page in pages:
        with open(page, encoding="utf-8") as f:
            s = f.read()
        for name, v in versions.items():
            s = re.sub(r'(assets/%s)(\?v=[0-9a-f]+)?"' % re.escape(name), r'\g<1>?v=%s"' % v, s)
        with open(page, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
    print("stamped", len(pages), "pages", versions)


if __name__ == "__main__":
    for app in APPS:
        build(app)
    stamp_assets()
