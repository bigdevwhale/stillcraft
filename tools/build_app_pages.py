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
    {
        "slug": "fogwalk",
        "name": "Fogwalk",
        "panel": "app--fogwalk",
        "gallery": "g-fogwalk",
        "icon": "fogwalk-logo.svg",
        "visual": "fw-map.png", "visual_ru": "fw-map.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/fogwalk",
        "download": "https://github.com/bigdevwhale/fogwalk/releases/latest/download/Fogwalk.apk",
        "version": "v1.0.0",
        "tagline": ("Your city, hidden in mist. Walk to reveal it.", "Ваш город скрыт туманом. Пройдите, чтобы открыть его."),
        "badge": ("Fantasy walks · New", "Фэнтези-прогулки · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Most of us walk the same three routes for years. <em>Your city, hidden in mist. Walk to reveal it.</em>",
                  "Большинство из нас годами ходит тремя одними и теми же маршрутами. <em>Ваш город скрыт туманом. Пройдите, чтобы открыть его.</em>"),
        "desc": ("Fogwalk turns your city into an old atlas lost in mist. Wherever you walk, the mist parts and stays parted. Week by week your neighbourhood fills in, then the next one, and the grey patches start to itch. On the way there are chests to open, a shrine to reach every day and relics to collect, so there is always a reason to go out again. Free, with no ads and no account.",
                 "Fogwalk превращает город в старинный атлас, затерянный в тумане. Где бы вы ни прошли, туман расступается и больше не возвращается. Неделя за неделей открывается ваш район, потом соседний, и серые пятна начинают манить. По пути встречаются сундуки, каждый день пробуждается святилище, собираются реликвии, так что всегда есть повод выйти снова. Бесплатно, без рекламы и аккаунта."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · GPS · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · GPS · English и Русский"),
        "features": [
            (("The mist", "Туман"),
             ("The world is cut into cells 20–40 m across. Everything within 40 m of your path is revealed for good, as soft clearings in a cloudy mist over a sepia OpenStreetMap atlas.",
              "Мир поделён на клетки по 20–40 м. Всё в радиусе 40 м от вашего пути открывается навсегда: мягкие просветы в облачном тумане над картой OpenStreetMap в тонах сепии.")),
            (("Treasure chests", "Сундуки с сокровищами"),
             ("Common, rare, epic and legendary chests are hidden all over the map and refill every Monday, even on streets you know. Nearby ones glimmer through the mist. Walk within 30 m to open one.",
              "Обычные, редкие, эпические и легендарные сундуки спрятаны по всей карте и появляются заново каждый понедельник, даже на знакомых улицах. Ближние мерцают сквозь туман. Подойдите на 30 м, чтобы открыть.")),
            (("Shrine of the day", "Святилище дня"),
             ("Each day a shrine awakens 0.6–1.7 km away, where the mist is thickest. An arrow points the way, and reaching it is the best reward of the day.",
              "Каждый день в 0,6–1,7 км, там, где туман гуще всего, пробуждается святилище. Стрелка показывает путь, а награда за него — лучшая за день.")),
            (("36 relics", "36 реликвий"),
             ("Six sets, from the Wayfarer's Pack to the Gifts of the Heavens: a brass compass, a dragon's scale, a void pearl. A full set earns a title and gold.",
              "Шесть наборов, от «Котомки странника» до «Даров небес»: латунный компас, чешуя дракона, жемчужина пустоты. За полный набор — титул и золото.")),
            (("160 deeds", "160 деяний"),
             ("25 ladders of deeds: walk 1 km, 100 km, 1,000 km, 5,000 km; chart a clearing, then a kingdom; open a chest, then a thousand; keep a streak for a year.",
              "25 лестниц деяний: пройти 1 км, 100 км, 1000 км, 5000 км; нанести на карту полянку, а потом королевство; открыть сундук, а потом тысячу; держать серию целый год.")),
            (("Lands", "Земли"),
             ("The realm is divided into named lands about a kilometre across, like Whispering Hollow or Mossy Wharf. Chart 5, 15, 25 and 40 % of a land for rewards.",
              "Королевство поделено на земли около километра в поперечнике с именами вроде «Шепчущая Лощина» или «Мшистый Причал». За 5, 15, 25 и 40 % земли на карте — награды.")),
            (("Quests and streaks", "Квесты и серии"),
             ("Three new quests every dawn and a great quest every week. Reveal 25 cells, walk 1 km or reach the shrine to keep the streak alive; a ward guards a missed day.",
              "Три новых квеста каждый рассвет и великий квест на неделю. Откройте 25 клеток, пройдите 1 км или дойдите до святилища, чтобы серия не прервалась; оберег спасёт пропущенный день.")),
            (("Gold and the merchant", "Золото и торговец"),
             ("Gold buys mists for the map, from Old Parchment to Elven Lights, a torch that burns a wider path, a seeing stone that shows every chest, wards and a scroll that moves the shrine.",
              "За золото — туманы для карты, от «Старого пергамента» до «Эльфийских огней», факел для широкой тропы, камень прозрения, который показывает все сундуки, обереги и свиток, переносящий святилище.")),
            (("Journeys with the screen off", "Странствие с выключенным экраном"),
             ("Tap Set out and Fogwalk keeps charting in a quiet notification, with a call when a chest is close. Anything faster than a bike doesn't count.",
              "Нажмите «В путь», и Fogwalk продолжит наносить карту с тихим уведомлением, а когда рядом сундук, позовёт. Всё быстрее велосипеда не считается.")),
            (("Chronicle and levels", "Летопись и уровни"),
             ("Charted area and your share of the known world, lands, days on the road, recent journeys, and ranks from Wanderer to Legend of the Realm.",
              "Нанесённая площадь и ваша доля известного мира, земли, дни в пути, последние странствия и ранги от Странника до Легенды королевства.")),
            (("Your path stays with you", "Ваш путь остаётся у вас"),
             ("No account, no servers, no analytics, no ads. Explored cells and progress live on the phone; only map tiles come from the network. A JSON backup keeps your atlas safe.",
              "Ни аккаунта, ни серверов, ни аналитики, ни рекламы. Открытые клетки и прогресс хранятся на телефоне, из сети приходят только тайлы карты. Резервная копия в JSON сохранит ваш атлас.")),
            (("Yours, in two languages", "Ваше, на двух языках"),
             ("A storybook look in light and dark, and English and Russian written natively, down to land names that agree in gender.",
              "Сказочный вид в светлой и тёмной теме, английский и русский, написанные вручную, вплоть до имён земель, согласованных по роду.")),
        ],
        "shots": [
            ("fw-map.png", "fw-map.ru.png", ("Map", "Карта"), ("Charted streets and the mist around them.", "Открытые улицы и туман вокруг.")),
            ("fw-quests.png", "fw-quests.ru.png", ("Quests", "Квесты"), ("Three every dawn, one for the week.", "Три каждый рассвет и один на неделю.")),
            ("fw-onboarding.png", "fw-onboarding.ru.png", ("Welcome", "Приветствие"), ("The realm is lost in mist.", "Королевство скрыто туманом.")),
            ("fw-hoard.png", "fw-hoard.ru.png", ("Hoard", "Сокровищница"), ("36 relics in six sets.", "36 реликвий в шести наборах.")),
            ("fw-merchant.png", "fw-merchant.ru.png", ("Merchant", "Торговец"), ("Mists of the realm and charms.", "Туманы королевства и обереги.")),
            ("fw-chronicle.png", "fw-chronicle.ru.png", ("Chronicle", "Летопись"), ("Your area, days on the road and lands.", "Площадь, дни в пути и земли.")),
            ("fw-deeds.png", "fw-deeds.ru.png", ("Deeds", "Деяния"), ("160 deeds in 25 ladders.", "160 деяний в 25 лестницах.")),
        ],
        "extra": {
            "title": ("Chests", "Сундуки"),
            "head": [("Kind", "Вид"), ("How often", "Как часто"), ("What's inside", "Что внутри")],
            "rows": [
                [("Common", "Обычный"), ("About 6 in 10", "Около 6 из 10"), ("12–18 gold, sometimes a common relic", "12–18 золота, иногда обычная реликвия")],
                [("Rare", "Редкий"), ("About 1 in 4", "Около 1 из 4"), ("35–52 gold, usually a relic", "35–52 золота, обычно реликвия")],
                [("Epic", "Эпический"), ("About 1 in 11", "Около 1 из 11"), ("90–135 gold and a relic", "90–135 золота и реликвия")],
                [("Legendary", "Легендарный"), ("About 1 in 33", "Около 1 из 33"), ("220–330 gold and a relic of the heavens", "220–330 золота и небесная реликвия")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Fogwalk.apk", "Fogwalk.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer with GPS. No Google services needed.", "Android 8.0 (API 26) или новее с GPS. Сервисы Google не нужны.")),
            (("Permissions", "Разрешения"), ("Location while in use, a location service for journeys with the screen off, notifications, and internet for map tiles only.",
                                            "Геолокация во время использования, служба для странствий с выключенным экраном, уведомления и интернет только для тайлов карты.")),
            (("License", "Лицензия"), ("MIT · map data © OpenStreetMap contributors", "MIT · картографические данные © участники OpenStreetMap")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачайте APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Откройте файл и разрешите установку из этого источника, когда Android спросит."),
            ("Allow location, tap Set out and head for the shrine of the day.", "Разрешите геолокацию, нажмите «В путь» и идите к святилищу дня."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Fogwalk and remove battery limits so journeys with the screen off aren't cut short.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разрешите Fogwalk автозапуск и снимите ограничения батареи, чтобы странствия с выключенным экраном не обрывались."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/fogwalk.git\ncd fogwalk\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK; long-press the map to walk there</c>\n./gradlew installDebug -Pdemo   <c># app.fogwalk.demo with walks through Prague</c>",
        "faq": [
            (("Is there a premium version?", "Есть ли премиум-версия?"),
             ("No. Every chest, relic, mist and deed is there for everyone, with no ads, no trial and no subscription. Gold is earned only by walking.",
              "Нет. Все сундуки, реликвии, туманы и деяния доступны всем, без рекламы, пробного периода и подписки. Золото зарабатывается только ходьбой.")),
            (("Does it track me?", "Оно за мной следит?"),
             ("No. There are no accounts, servers or analytics. Your path is stored only as explored cells in a local database on the phone. The only network traffic is map tiles from OpenStreetMap.",
              "Нет. Ни аккаунтов, ни серверов, ни аналитики. Ваш путь хранится только как открытые клетки в локальной базе на телефоне. В сеть уходят лишь запросы тайлов карты OpenStreetMap.")),
            (("Does riding a bus count?", "А если ехать на автобусе?"),
             ("No. Anything faster than about 30 km/h is treated as a vehicle and reveals nothing, so the map stays a record of where you actually walked or cycled.",
              "Нет. Всё быстрее примерно 30 км/ч считается транспортом и ничего не открывает, так что карта остаётся летописью мест, где вы правда прошли или проехали на велосипеде.")),
            (("How much battery does it use?", "Сколько уходит батареи?"),
             ("GPS runs only while the map is open or during a journey you started. Stop the journey when you get home, and the app goes quiet.",
              "GPS работает, только пока открыта карта или идёт начатое вами странствие. Остановите его, когда вернётесь домой, и приложение затихнет.")),
        ],
    },
    {
        "slug": "dearme",
        "name": "DearMe",
        "panel": "app--dearme",
        "gallery": "g-dearme",
        "icon": "dearme-logo.svg",
        "visual": "dm-letters.png", "visual_ru": "dm-letters.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/dearme",
        "download": "https://github.com/bigdevwhale/dearme/releases/latest/download/DearMe.apk",
        "version": "v1.0.0",
        "tagline": ("Letters to your future self. Sealed until the day comes.", "Письма себе в будущее. Запечатаны до нужного дня."),
        "badge": ("Letters to your future self · New", "Письма себе в будущее · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("We remember what happened, but not how it felt. <em>Letters to your future self, sealed until the day comes.</em>",
                  "Мы помним, что происходило, но не помним, каково это было. <em>Письма себе в будущее, запечатанные до нужного дня.</em>"),
        "desc": ("DearMe keeps what fades in envelopes: what we were afraid of, what the street looked like, how our voice sounded on an ordinary Tuesday. Write a letter, add a photo or a minute of your voice, pick a day and seal it. Until then it can't be opened, not even by you. And at a random moment each day it calls: two minutes, what's happening right now? Free, with no ads and no account, and nothing leaves the phone.",
                 "DearMe хранит в конвертах то, что забывается: чего мы боялись, как выглядела улица, как звучал наш голос в самый обычный вторник. Напиши письмо, добавь снимок или минуту голоса, выбери день и запечатай. До этого дня письмо не открыть, даже тебе. А в случайный момент каждого дня приложение зовёт: две минуты — что происходит прямо сейчас? Бесплатно, без рекламы и аккаунта, ничего не покидает телефон."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · Works offline · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Работает офлайн · English и Русский"),
        "features": [
            (("Letters", "Письма"),
             ("Text, several photos and a voice note of up to a minute. A letter opens in a week, a month, 1, 5, 10 or 30 years, or on any date you pick.",
              "Текст, несколько снимков и голос до минуты. Письмо откроется через неделю, месяц, 1, 5, 10 или 30 лет — или в любую выбранную дату.")),
            (("Photos, any way you like", "Снимки как угодно"),
             ("The back camera, a selfie, both at once BeReal-style (back first, a selfie a second later), or pictures from the gallery.",
              "Задняя камера, селфи, обе сразу, как в BeReal (сначала задняя, через секунду селфи), или снимки из галереи.")),
            (("Random moments", "Случайные моменты"),
             ("Every day at a surprise time inside your window, DearMe calls. You have two minutes for a dual shot and one line. Late answers get a stamp.",
              "Каждый день в неожиданное время внутри твоего окна DearMe зовёт. У тебя две минуты на двойной снимок и одну строку. На опоздавших ответах остаётся штамп.")),
            (("Rituals", "Ритуалы"),
             ("Your own rules for when to be called: a random or exact time, on chosen weekdays, once a month or once a year, with what goes in and how long it stays sealed.",
              "Свои правила, когда звать: случайное или точное время, выбранные дни недели, раз в месяц или раз в год, что внутри и на сколько запечатывать.")),
            (("Step by step", "Постепенно"),
             ("Moments open after a week while the habit is new, after a month during the first year, after a year from then on, so there is something to open from the second week.",
              "Пока привычка новая, моменты открываются через неделю, в первый год — через месяц, дальше — через год. Открывать есть что уже со второй недели.")),
            (("Breaking the seal", "Печать"),
             ("A sealed letter shows only its date, a countdown and what's inside: 📷 2 · 🎙 0:42 · 340 words. When the day comes, you break the wax and the flap lifts.",
              "У запечатанного письма видны только дата, обратный отсчёт и что внутри: 📷 2 · 🎙 0:42 · 340 слов. Когда день приходит, ты ломаешь сургуч, и клапан конверта поднимается.")),
            (("Then &amp; now", "Тогда и сейчас"),
             ("After opening, stand where you stood and take the same shot today. The two go side by side.",
              "После открытия встань там же, где тогда, и сделай такой же снимок. Они встанут рядом.")),
            (("Write back", "Ответ себе"),
             ("Reply to your past self, and the answer is sealed for the next stretch: a correspondence with yourself across years.",
              "Ответь себе из прошлого, и ответ запечатается на следующий срок — переписка с собой длиной в годы.")),
            (("Share cards", "Открытки"),
             ("Story-sized pictures: “I sealed a letter to myself, it opens on 14 October 2056”, an opened letter with its photo, then &amp; now.",
              "Картинки для сторис: «Я запечатал(а) письмо себе, оно откроется 14 октября 2056 г.», открытое письмо со снимком, «тогда и сейчас».")),
            (("40 questions", "40 вопросов"),
             ("What are you most afraid of right now? Who do you miss? What will you laugh at when you read this? For when the page is blank.",
              "Чего ты сейчас боишься больше всего? По кому ты скучаешь? Над чем ты посмеёшься, когда это прочитаешь? Для пустой страницы.")),
            (("Clock check", "Проверка часов"),
             ("Moving the phone's date forward doesn't open anything: DearMe compares the clock with time since boot and, when online, with the network.",
              "Перевести дату вперёд не поможет: DearMe сверяет часы со временем с момента загрузки, а при интернете — с сетевым временем.")),
            (("Everything stays on the phone", "Всё остаётся на телефоне"),
             ("No account, no servers, no analytics, no ads. Every letter, photo and voice note fits in one scrambled .dearme backup file to carry to the next phone.",
              "Ни аккаунта, ни серверов, ни аналитики, ни рекламы. Все письма, снимки и записи помещаются в один зашифрованный файл бэкапа .dearme для переезда на новый телефон.")),
        ],
        "shots": [
            ("dm-letters.png", "dm-letters.ru.png", ("Letters", "Письма"), ("On their way, with the next countdown.", "В пути, с отсчётом до следующего.")),
            ("dm-sealed.png", "dm-sealed.ru.png", ("Sealed", "Запечатано"), ("Only the date and a countdown.", "Только дата и обратный отсчёт.")),
            ("dm-ceremony.png", "dm-ceremony.ru.png", ("The seal", "Печать"), ("The day has come.", "Нужный день настал.")),
            ("dm-opened.png", "dm-opened.ru.png", ("Opened", "Открыто"), ("A letter with a dual shot.", "Письмо с двойным снимком.")),
            ("dm-write.png", "dm-write.ru.png", ("Write", "Письмо"), ("A new letter with a question.", "Новое письмо с вопросом.")),
            ("dm-rituals.png", "dm-rituals.ru.png", ("Rituals", "Ритуалы"), ("When DearMe should call you.", "Когда DearMe будет звать.")),
        ],
        "extra": {
            "title": ("Rituals to start from", "Готовые ритуалы"),
            "head": [("Ritual", "Ритуал"), ("When it calls", "Когда зовёт"), ("What goes in", "Что внутри"), ("Opens", "Откроется")],
            "rows": [
                [("Random moment", "Случайный момент"), ("Every day at a surprise time between 10:00 and 22:00", "Каждый день в неожиданное время с 10:00 до 22:00"), ("Both cameras and one line, in two minutes", "Обе камеры и одна строка за две минуты"), ("Step by step: a week, a month, then a year", "Постепенно: через неделю, месяц, потом год")],
                [("Sunday letter", "Воскресное письмо"), ("Sundays at 21:00", "По воскресеньям в 21:00"), ("A selfie and a letter, with a question", "Селфи и письмо с вопросом"), ("In a year", "Через год")],
                [("First of the month", "Первое число"), ("The 1st of every month at 9:00", "1-го числа каждого месяца в 9:00"), ("What you expect from the month", "Чего ты ждёшь от месяца"), ("When the month ends", "Когда месяц закончится")],
                [("Birthday letter", "Письмо на день рождения"), ("Once a year", "Раз в год"), ("A selfie, your voice and a letter", "Селфи, голос и письмо"), ("In ten years", "Через десять лет")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("DearMe.apk", "DearMe.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer. No Google services needed.", "Android 8.0 (API 26) или новее. Сервисы Google не нужны.")),
            (("Permissions", "Разрешения"), ("Camera and microphone for letters, notifications and exact alarms for rituals, and internet only for a quiet network clock check.",
                                            "Камера и микрофон для писем, уведомления и точные будильники для ритуалов и интернет только для тихой сверки с сетевыми часами.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Write your first letter, pick a day and seal it.", "Напиши первое письмо, выбери день и запечатай его."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for DearMe and remove battery limits, or random moments may not ring.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши DearMe автозапуск и сними ограничения батареи, иначе случайные моменты могут не приходить."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/dearme.git\ncd dearme\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK; a ritual's Try it now calls right away</c>\n./gradlew installDebug -Pdemo   <c># app.dearme.demo with a year of made-up letters</c>",
        "faq": [
            (("Is there a premium version?", "Есть ли премиум-версия?"),
             ("No. Every letter, ritual, question and card is there for everyone, with no ads, no trial and no subscription.",
              "Нет. Все письма, ритуалы, вопросы и открытки доступны всем, без рекламы, пробного периода и подписки.")),
            (("Can I peek before the day?", "Можно подсмотреть раньше срока?"),
             ("Not easily. Moving the date forward doesn't work, and a backup is scrambled inside. There is no server, though, so the seal is a strong habit rather than a vault: a diary lock for the person you're going to be.",
              "Непросто. Перевод даты не сработает, а бэкап внутри зашифрован. Но сервера нет, поэтому печать — это крепкая привычка, а не сейф: замочек на дневнике для того, кем ты станешь.")),
            (("What if I change phones?", "А если я сменю телефон?"),
             ("Letters live only on your phone. Save a backup in Settings → Backup now and then, keep the .dearme file somewhere safe and restore it on the new phone. For a letter meant for 2056, this matters.",
              "Письма хранятся только на телефоне. Время от времени сохраняй бэкап в «Настройки → Бэкап», держи файл .dearme в надёжном месте и восстанови его на новом телефоне. Для письма в 2056 год это важно.")),
            (("Does anything leave my phone?", "Что-то уходит с телефона?"),
             ("No. Letters, photos and voice notes stay in the app's private storage. The only network request is a quiet look at the network clock before a seal is broken.",
              "Нет. Письма, снимки и записи лежат в закрытом хранилище приложения. Единственный сетевой запрос — тихая сверка с сетевыми часами перед тем, как сломать печать.")),
        ],
    },
    {
        "slug": "glow",
        "name": "Glow",
        "panel": "app--glow",
        "gallery": "g-glow",
        "icon": "glow-logo.svg",
        "visual": "gl-praise.png", "visual_ru": "gl-praise.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/glow",
        "download": "https://github.com/bigdevwhale/glow/releases/latest/download/Glow.apk",
        "version": "v1.0.0",
        "tagline": ("Every win deserves a little praise.", "Каждая победа заслуживает похвалы."),
        "badge": ("Praise for every win · New", "Похвала за каждую победу · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("The inner critic never misses a mistake. <em>Glow never misses a win.</em>",
                  "Внутренний критик не пропускает ни одной ошибки. <em>Glow не пропускает ни одной победы.</em>"),
        "desc": ("Write down what you did, from washing the dishes to landing the job, say how big it felt, and get praised for it. Every win drops into a glass jar as a stone that rolls when you tilt the phone. Five voices to cheer you on, an SOS for hard moments, a translator for your inner critic and a place to keep the kind things people said. Free, with no ads and no account, and nothing leaves the phone.",
                 "Запиши, что у тебя получилось, от помытой посуды до новой работы, скажи, насколько это большое дело, и получи похвалу. Каждая победа падает в стеклянную банку камешком, который катается, когда наклоняешь телефон. Пять голосов поддержки, SOS для трудных минут, переводчик для внутреннего критика и место для добрых слов, которые тебе говорили. Бесплатно, без рекламы и аккаунта, ничего не покидает телефон."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · Works offline · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Работает офлайн · English и Русский"),
        "features": [
            (("Praise for every win", "Похвала за каждую победу"),
             ("Tiny, solid or huge: the praise, the confetti and the vibration grow with the win. Quick ideas help on days when getting out of bed is the win.",
              "Крошечная, хорошая или огромная: похвала, конфетти и вибрация растут вместе с победой. Готовые идеи выручат в дни, когда победа — встать с кровати.")),
            (("A jar of wins", "Банка побед"),
             ("Each win drops in as a stone coloured by its area. Tilt or shake the phone and the stones roll; tap one to remember the win. One jar per month.",
              "Каждая победа падает камешком цвета своей сферы. Наклони или встряхни телефон, и камешки покатятся; нажми на камешек, чтобы вспомнить победу. Своя банка на каждый месяц.")),
            (("Five voices", "Пять голосов"),
             ("A warm friend, a granny, a sports commentator, a wise mentor or a butler. Each praises, comforts and says goodnight in its own way.",
              "Тёплый друг, бабушка, спортивный комментатор, мудрый наставник или дворецкий. Каждый хвалит, утешает и желает спокойной ночи по-своему.")),
            (("Praise of the day", "Похвала дня"),
             ("A new one every morning, in a notification and a home-screen widget. Keep it, ask for another, share it.",
              "Каждое утро новая — в уведомлении и в виджете на главном экране. Сохрани её, попроси другую, поделись.")),
            (("I feel bad", "Мне плохо"),
             ("A dark, quiet room with drifting sparkles, the kindest words one by one, a soft heartbeat and a breathing circle.",
              "Тёмная тихая комната с плывущими искрами, самые добрые слова одно за другим, мягкий стук сердца и круг для дыхания.")),
            (("Self-criticism translator", "Переводчик с самокритичного"),
             ("Write the harsh thought. Glow names the thinking trap and offers a kinder way to say the same thing. Fully offline.",
              "Напиши жёсткую мысль. Glow назовёт ловушку мышления и предложит сказать то же самое добрее. Полностью офлайн.")),
            (("Kind words", "Добрые слова"),
             ("Keep compliments from real people, with a screenshot if you like, and read them in shuffle mode on hard days.",
              "Храни комплименты от настоящих людей, со скриншотом, если хочешь, и перечитывай их вперемешку в трудные дни.")),
            (("Evening of pride", "Вечер гордости"),
             ("Before sleep, three things you're proud of today. They collect in a pride diary.",
              "Перед сном — три вещи, которыми ты гордишься сегодня. Они собираются в дневник гордости.")),
            (("A streak that never burns", "Серия, которая не сгорает"),
             ("Days in a row with wins. Miss one and the jar simply waits; the best run stays.",
              "Дни подряд с победами. Пропустишь день — банка просто подождёт, а рекорд останется.")),
            (("Weekly report", "Отчёт за неделю"),
             ("Every Sunday, the report on how great you are: wins per day, your strongest area, your best day and the huge wins, shareable as a picture.",
              "По воскресеньям — отчёт о твоей крутости: победы по дням, самая сильная сторона, лучший день и огромные победы. Можно поделиться картинкой.")),
            (("Orders and certificates", "Ордена и грамоты"),
             ("16 orders with three degrees each, from the Order of Small Things to the Order of Quiet Courage, and a certificate of honour for every one.",
              "16 орденов по три степени, от Ордена Маленьких Дел до Ордена Тихой Отваги, и почётная грамота за каждый.")),
            (("Speaks to you properly", "Обращается правильно"),
             ("In Russian, Glow asks whether to address you in the masculine or the feminine, so it's «ты сделал» or «ты сделала», never «сделал(а)».",
              "По-русски Glow спрашивает, обращаться к тебе в мужском или женском роде, и пишет «ты сделал» или «ты сделала», а не «сделал(а)».")),
        ],
        "shots": [
            ("gl-today.png", "gl-today.ru.png", ("Today", "Сегодня"), ("The praise of the day.", "Похвала дня.")),
            ("gl-praise.png", "gl-praise.ru.png", ("A huge win", "Огромная победа"), ("Confetti as big as the win.", "Конфетти размером с победу.")),
            ("gl-jar.png", "gl-jar.ru.png", ("The jar", "Банка"), ("A month of wins, ready to shake.", "Месяц побед, можно встряхнуть.")),
            ("gl-kind.png", "gl-kind.ru.png", ("Kind words", "Добрые слова"), ("Proof for the days you forget.", "Доказательства на дни, когда забываешь.")),
            ("gl-sos.png", "gl-sos.ru.png", ("I feel bad", "Мне плохо"), ("A quiet room for hard moments.", "Тихая комната для трудных минут.")),
            ("gl-me.png", "gl-me.ru.png", ("Me", "Я"), ("The streak, stats and orders.", "Серия, статистика и ордена.")),
            ("gl-report.png", "gl-report.ru.png", ("Weekly report", "Отчёт за неделю"), ("How great the week was.", "Какой крутой была неделя.")),
            ("gl-certificate.png", "gl-certificate.ru.png", ("Certificate", "Грамота"), ("For every degree of every order.", "За каждую степень каждого ордена.")),
        ],
        "extra": {
            "title": ("Who praises you", "Кто тебя хвалит"),
            "head": [("Voice", "Голос"), ("Style", "Стиль"), ("For a huge win", "За огромную победу")],
            "rows": [
                [("🤗 Warm friend", "🤗 Тёплый друг"), ("Gentle, honest, always on your side", "Мягко, честно и всегда на твоей стороне"), ("Stop for a second and let this sink in. You did that.", "Остановись на секунду и прочувствуй. Это сделала ты.")],
                [("👵 Granny", "👵 Бабушка"), ("Fusses over you, feeds you, adores you", "Причитает, кормит и обожает"), ("This calls for the good china!", "Доставай парадный сервиз!")],
                [("🎙️ Sports commentator", "🎙️ Спортивный комментатор"), ("Every move you make is live on air", "Каждый твой шаг — в прямом эфире"), ("THE STADIUM IS SHAKING!", "СТАДИОН ДРОЖИТ!")],
                [("🦉 Wise mentor", "🦉 Мудрый наставник"), ("Calm words, long view, quiet pride", "Спокойные слова, долгий взгляд, тихая гордость"), ("Today the river reached the sea.", "Сегодня река достигла моря.")],
                [("🎩 Butler", "🎩 Дворецкий"), ("Impeccably polite, deeply impressed", "Безупречно вежлив, глубоко впечатлён"), ("I have dropped a tray. That has not happened since 1987.", "Я уронил поднос. Такого не случалось с 1987 года.")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Glow.apk", "Glow.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer. No Google services needed.", "Android 8.0 (API 26) или новее. Сервисы Google не нужны.")),
            (("Permissions", "Разрешения"), ("Notifications for the morning praise and evening reminder, and vibration. No internet.",
                                            "Уведомления для утренней похвалы и вечернего напоминания и вибрация. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Pick a voice and tell it about your first win.", "Выбери голос и расскажи ему о первой победе."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Glow and remove battery limits so the morning praise arrives on time.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Glow автозапуск и сними ограничения батареи, чтобы утренняя похвала приходила вовремя."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/glow.git\ncd glow\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug -Pdemo   <c># app.glow.demo with seven weeks of made-up wins</c>",
        "faq": [
            (("Is there a premium version?", "Есть ли премиум-версия?"),
             ("No. Every voice, order and feature is there for everyone, with no ads, no trial and no subscription.",
              "Нет. Все голоса, ордена и функции доступны всем, без рекламы, пробного периода и подписки.")),
            (("Is it therapy?", "Это терапия?"),
             ("No. Glow is a kind companion. If things have felt heavy for a long time, please talk to someone you trust or a professional.",
              "Нет. Glow — добрый спутник. Если тяжело уже долго, пожалуйста, поговори с близким человеком или специалистом.")),
            (("Does the translator use AI?", "Переводчик работает на ИИ?"),
             ("No. It matches word stems against ten common thinking traps and picks a kinder phrasing. Nothing you write leaves the phone.",
              "Нет. Он ищет основы слов для десяти частых ловушек мышления и подбирает более добрую формулировку. Ничего из написанного не покидает телефон.")),
            (("What if I change phones?", "А если я сменю телефон?"),
             ("Settings → Backup saves wins, kind words with their screenshots and evenings into one JSON file. Restore it on the new phone.",
              "«Настройки → Резервная копия» сохраняет победы, добрые слова со скриншотами и вечера в один JSON-файл. Восстанови его на новом телефоне.")),
        ],
    },
    {
        "slug": "waypoint",
        "name": "Waypoint",
        "panel": "app--waypoint",
        "gallery": "g-waypoint",
        "icon": "waypoint-logo.svg",
        "visual": "wp-mandala.png", "visual_ru": "wp-mandala.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/waypoint",
        "download": "https://github.com/bigdevwhale/waypoint/releases/latest/download/Waypoint.apk",
        "version": "v1.0.0",
        "tagline": ("Goals under a night sky: 17 methods in one app.", "Цели под ночным небом: 17 методов в одном приложении."),
        "badge": ("Goals under a night sky · New", "Цели под ночным небом · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("17 proven ways to reach a goal. <em>Every step lights a star.</em>",
                  "17 проверенных способов дойти до цели. <em>Каждый шаг зажигает звезду.</em>"),
        "desc": ("Goals differ, and so do the ways to reach them. Waypoint gathers the methods that work into one free app: Ohtani's Mandala 64, OKR, the 12-week year, WOOP and thirteen more, each with a short guide. Every goal is drawn as a constellation, every finished step lights a star, and Today brings the steps from all your goals into one course. No ads, no account, and nothing leaves the phone.",
                 "Цели бывают разные, и пути к ним тоже. Waypoint собирает работающие методы в одно бесплатное приложение: Мандалу 64 Сёхэя Отани, OKR, 12-недельный год, WOOP и ещё тринадцать, у каждого есть короткое объяснение. Каждая цель рисуется созвездием, каждый сделанный шаг зажигает звезду, а экран «Сегодня» собирает шаги всех целей в один курс. Без рекламы и аккаунта, ничего не покидает телефон."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · Works offline · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Работает офлайн · English и Русский"),
        "features": [
            (("Mandala 64", "Мандала 64"),
             ("Ohtani's chart: a goal in the centre, eight pillars around it and eight actions for each, 64 in all, on one star map. Light a star when an action has become part of you. Share the chart as a poster.",
              "Таблица Отани: цель в центре, вокруг восемь опор и по восемь действий на каждую, всего 64, на одной звёздной карте. Зажигай звезду, когда действие стало частью тебя. Карту можно отправить постером.")),
            (("Eight ways to drive a goal", "Восемь способов вести цель"),
             ("OKR with key results and check-ins, the 12-week year scored every week, 4DX with a scoreboard, 1% a day, a 30-day pact, a reverse plan from the finish line, or simple milestones.",
              "OKR с ключевыми результатами и отметками, 12-недельный год с оценкой каждую неделю, 4DX с табло, 1% в день, пакт на 30 дней, обратный план от финиша или простые вехи.")),
            (("Lenses for any goal", "Линзы для любой цели"),
             ("SMART for clear wording, WOOP for if-then plans, GROW for a coaching session with yourself, five whys for the real reason, and a pre-mortem to find out how it could fail.",
              "SMART для ясной формулировки, WOOP для планов «если–то», GROW — коуч-сессия с собой, пять «почему» для настоящей причины и пре-мортем, чтобы понять, как цель может провалиться.")),
            (("When you don't know what you want", "Когда не знаешь, чего хочешь"),
             ("Rate eight areas on the wheel of life, sketch three Odyssey lives, keep five of twenty-five, or put a price on your dreams. A five-question quiz suggests a method.",
              "Оцени восемь сфер на колесе баланса, набросай три жизни «Одиссеи», оставь пять из двадцати пяти или назначь мечтам цену. Квиз из пяти вопросов подскажет метод.")),
            (("One course for today", "Один курс на сегодня"),
             ("Steps from every goal on one screen, with streaks and reminders. On bad days, a backup course of your if-then plans.",
              "Шаги всех целей на одном экране, с сериями и напоминаниями. В трудный день — запасной курс из твоих планов «если–то».")),
            (("Focus and review", "Фокус и итоги"),
             ("A focus limit keeps you from spreading thin, and extra goals wait in a queue. A short weekly review, a home-screen widget, and a wall of reached goals.",
              "Лимит фокуса не даёт распыляться, лишние цели ждут в очереди. Короткие итоги недели, виджет на главном экране и стена достигнутых целей.")),
        ],
        "shots": [
            ("wp-today.png", "wp-today.ru.png", ("Today", "Сегодня"), ("Steps from every goal, lit as you go.", "Шаги всех целей, зажигаются по ходу дня.")),
            ("wp-goals.png", "wp-goals.ru.png", ("Goals", "Цели"), ("Each goal is its own constellation.", "У каждой цели своё созвездие.")),
            ("wp-goal.png", "wp-goal.ru.png", ("A goal", "Цель"), ("Progress, the why and the method.", "Прогресс, «зачем» и метод.")),
            ("wp-mandala.png", "wp-mandala.ru.png", ("Mandala 64", "Мандала 64"), ("Eight pillars, 64 stars.", "Восемь опор, 64 звезды.")),
            ("wp-okr.png", "wp-okr.ru.png", ("OKR", "OKR"), ("Key results and a weekly check-in.", "Ключевые результаты и отметка раз в неделю.")),
            ("wp-weeks12.png", "wp-weeks12.ru.png", ("12-week year", "12-недельный год"), ("Every week scored, 85% is excellent.", "Оценка каждой недели, 85% — отлично.")),
            ("wp-compass.png", "wp-compass.ru.png", ("Compass", "Компас"), ("17 methods, grouped by the road.", "17 методов по этапам пути.")),
            ("wp-wheel.png", "wp-wheel.ru.png", ("Wheel of life", "Колесо баланса"), ("Where a goal would help most.", "Где цель поможет больше всего.")),
            ("wp-journal.png", "wp-journal.ru.png", ("Journal", "Журнал"), ("Reviews and reached goals.", "Итоги недель и достигнутые цели.")),
        ],
        "extra": {
            "title": ("Which method for which goal", "Какой метод для какой цели"),
            "head": [("Method", "Метод"), ("Good for", "Подходит для"), ("You get", "Что получаешь")],
            "rows": [
                [("Mandala 64", "Мандала 64"), ("A big dream with many sides", "Большая мечта с разными сторонами"), ("The whole road on one page", "Весь путь на одной странице")],
                [("OKR", "OKR"), ("A result you can measure, in a quarter", "Измеримый результат за квартал"), ("3–5 numbers that prove it", "3–5 цифр, которые это подтвердят")],
                [("12-week year", "12-недельный год"), ("Putting things off", "Когда всё откладывается"), ("A deadline that is always close", "Дедлайн, который всегда рядом")],
                [("4DX", "4DX"), ("One key goal among daily noise", "Одна главная цель среди текучки"), ("Actions you control and a scoreboard", "Действия в твоих руках и табло")],
                [("1% a day", "1% в день"), ("Anything you can count", "Всё, что можно посчитать"), ("Compounding: double in 70 days", "Сложный процент: вдвое за 70 дней")],
                [("30-day pact", "Пакт на 30 дней"), ("Trying something new", "Попробовать что-то новое"), ("An experiment, not a test", "Эксперимент, а не экзамен")],
                [("Reverse plan", "Обратный план"), ("A project with a date", "Проект с датой"), ("Dated steps from the finish back to today", "Шаги с датами от финиша до сегодня")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Waypoint.apk", "Waypoint.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer. No Google services needed.", "Android 8.0 (API 26) или новее. Сервисы Google не нужны.")),
            (("Permissions", "Разрешения"), ("Notifications for the morning course, the evening check, the weekly review and step reminders. No internet.",
                                            "Уведомления для утреннего курса, вечерней проверки, итогов недели и напоминаний о шагах. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Pick a method, or take the quiz, and set your first goal.", "Выбери метод или пройди квиз и поставь первую цель."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Waypoint and remove battery limits so reminders arrive on time.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Waypoint автозапуск и сними ограничения батареи, чтобы напоминания приходили вовремя."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/waypoint.git\ncd waypoint\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug -Pdemo   <c># app.waypoint.demo with made-up goals</c>",
        "faq": [
            (("Is there a premium version?", "Есть ли премиум-версия?"),
             ("No. All 17 methods and every feature are there for everyone, with no ads, no trial and no subscription.",
              "Нет. Все 17 методов и все функции доступны всем, без рекламы, пробного периода и подписки.")),
            (("Which method should I pick?", "Какой метод выбрать?"),
             ("Take the five-question quiz in the Compass tab. Every method also explains itself where you choose it, and you can add lenses to any goal later.",
              "Пройди квиз из пяти вопросов во вкладке «Компас». Каждый метод объясняет себя прямо там, где его выбираешь, а линзы можно добавить к любой цели позже.")),
            (("Why a limit on goals?", "Зачем лимит целей?"),
             ("With too many goals at once, none of them moves. You choose the limit, or turn it off; extra goals wait in a queue.",
              "Когда целей слишком много, не движется ни одна. Лимит выбираешь ты, его можно выключить, а лишние цели ждут в очереди.")),
            (("What if I change phones?", "А если я сменю телефон?"),
             ("Settings → Backup saves every goal, step, review and note into one JSON file. Restore it on the new phone.",
              "«Настройки → Резервная копия» сохраняет все цели, шаги, итоги и заметки в один JSON-файл. Восстанови его на новом телефоне.")),
        ],
    },
    {
        "slug": "obol",
        "name": "Obol",
        "panel": "app--obol",
        "gallery": "g-obol",
        "icon": "obol-logo.svg",
        "visual": "ob-gate.png", "visual_ru": "ob-gate.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/obol",
        "download": "https://github.com/bigdevwhale/obol/releases/latest/download/Obol.apk",
        "version": "v1.0.1",
        "tagline": ("Earn obols with useful apps, pay Charon for the feed.", "Зарабатывай оболы полезными приложениями, плати Харону за ленту."),
        "badge": ("Pay Charon for the feed · New", "Плати Харону за ленту · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("Every crossing of Lethe costs an obol. <em>Earn them first.</em>",
                  "Каждая переправа через Лету стоит обол. <em>Сначала заработай.</em>"),
        "desc": ("In the myth, Lethe is the river of forgetting, and Charon ferries souls across it for an obol. An endless feed is the same river. Obol pays you in obols for books, languages, lessons and meditations, and puts Charon at the gate of Reels, Shorts and TikTok. Night costs triple, every crossing costs more than the last, and turning back is always free. No ads, no account, no internet access.",
                 "В мифе Лета — река забвения, а Харон перевозит через неё души за обол. Бесконечная лента — та же река. Обол платит тебе оболами за книги, языки, уроки и медитации и ставит Харона у ворот Reels, Shorts и TikTok. Ночью втрое дороже, каждая переправа дороже прошлой, а повернуть назад можно всегда бесплатно. Без рекламы, аккаунта и доступа в интернет."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · Works offline · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Работает офлайн · English и Русский"),
        "features": [
            (("Charon's gate", "Ворота Харона"),
             ("Open Reels and the gate appears over it: why do you want to cross, a few breaths, then 5, 15 or 30 minutes, the meter, or a free pass from Hermes' staff. The reel underneath is paused.",
              "Открываешь Reels — поверх появляются ворота: зачем тебе на тот берег, несколько вдохов, затем 5, 15 или 30 минут, счётчик или бесплатный проход с посохом Гермеса. Ролик под воротами встаёт на паузу.")),
            (("Only the feed costs", "Платна только лента"),
             ("Reels and Shorts are paid; messages and the rest of the app stay free. Sites count in the browser too, down to a part like youtube.com/shorts.",
              "Платны Reels и Shorts, а переписка и остальное приложение бесплатны. Сайты тоже считаются в браузере, вплоть до части вроде youtube.com/shorts.")),
            (("A pantheon of your own", "Свой пантеон"),
             ("Calliope pays for reading, Hermes for languages, Athena for learning, Hestia for stillness, Nike for sport. Dedicate your own patron to guitar or code, with a symbol, a rate, a daily cap, apps and sites.",
              "Каллиопа платит за чтение, Гермес — за языки, Афина — за учёбу, Гестия — за тишину, Ника — за спорт. Посвяти своего покровителя гитаре или коду: символ, курс, дневной лимит, приложения и сайты.")),
            (("Time left and the mist", "Остаток времени и туман"),
             ("On the far shore a small plaque in the corner counts down the time you paid for. After five minutes a grey mist of Lethe creeps in from the edges of the screen.",
              "На том берегу маленькая плашка в углу отсчитывает оплаченное время. Через пять минут с краёв экрана наползает серый туман Леты.")),
            (("Tariffs, debt and the oracle", "Тарифы, долг и оракул"),
             ("Nyx's hour triples the fare, every crossing of the day costs half again, Hades lends at interest, and the oracle names a patron who pays double for two hours.",
              "Час Никты утраивает плату, каждая переправа за день дороже в полтора раза, Аид даёт в долг под проценты, а оракул называет покровителя, который два часа платит вдвойне.")),
            (("Temple, rites and the Styx", "Храм, обряды и Стикс"),
             ("Save obols for a real reward or let the treasury grow each Monday. Earn by rites with the phone face down. Swear by the Styx, and the gate locks until the oath ends.",
              "Копи оболы на настоящую награду или дай сокровищнице расти каждый понедельник. Зарабатывай обрядами с телефоном экраном вниз. Поклянись Стиксом — и ворота будут заперты, пока клятва в силе.")),
        ],
        "shots": [
            ("ob-shore.png", "ob-shore.ru.png", ("The shore", "Берег"), ("The purse, the oracle and today's potsherd.", "Кошель, оракул и черепок дня.")),
            ("ob-gate.png", "ob-gate.ru.png", ("The gate", "Ворота"), ("Charon asks why before you cross.", "Харон спрашивает, зачем тебе на тот берег.")),
            ("ob-fare.png", "ob-fare.ru.png", ("The fare", "Плата"), ("Minutes, the meter or Hermes' staff.", "Минуты, счётчик или посох Гермеса.")),
            ("ob-pantheon.png", "ob-pantheon.ru.png", ("Pantheon", "Пантеон"), ("Pedestals grow with the hours.", "Пьедесталы растут с часами служения.")),
            ("ob-patron.png", "ob-patron.ru.png", ("Your own patron", "Свой покровитель"), ("Name, symbol, rate, cap, apps, sites.", "Имя, символ, курс, лимит, приложения, сайты.")),
            ("ob-lethe.png", "ob-lethe.ru.png", ("Lethe", "Лета"), ("Streams that cost obols.", "Потоки, которые стоят оболов.")),
            ("ob-ledger.png", "ob-ledger.ru.png", ("Ledger", "Книга"), ("Four weeks and what was remembered.", "Четыре недели и что запомнилось.")),
            ("ob-temple.png", "ob-temple.ru.png", ("Temple", "Храм"), ("The treasury and vows.", "Сокровищница и обеты.")),
            ("ob-rite.png", "ob-rite.ru.png", ("A rite", "Обряд"), ("Time away from the phone.", "Время без телефона.")),
        ],
        "extra": {
            "title": ("What things cost on the far shore", "Сколько стоит тот берег"),
            "head": [("Rule", "Правило"), ("When", "Когда"), ("Effect", "Что даёт")],
            "rows": [
                [("Base fare", "Базовая плата"), ("Any time", "В любое время"), ("2 obols a minute for Instagram, 3 for TikTok, your choice for the rest", "2 обола в минуту за Instagram, 3 за TikTok, для остальных — на твой выбор")],
                [("Nyx's hour", "Час Никты"), ("23:00–06:00", "23:00–06:00"), ("×3", "×3")],
                [("Early morning", "Раннее утро"), ("Until 09:00", "До 09:00"), ("×2", "×2")],
                [("Rising fare", "Растущая плата"), ("Each crossing after the first today", "Каждая переправа после первой за день"), ("×1.5, ×2, up to ×3", "×1,5, ×2, до ×3")],
                [("Debt to Hades", "Долг Аиду"), ("When the purse is empty", "Когда кошель пуст"), ("Up to 30 obols, 20 % on the borrowed part", "До 30 оболов, 20 % на занятую часть")],
                [("Hermes' staff", "Посох Гермеса"), ("3 times a week", "3 раза в неделю"), ("5 free minutes for real business", "5 бесплатных минут для настоящих дел")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.1", "v1.0.1")),
            (("File", "Файл"), ("Obol.apk", "Obol.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer. No Google services needed.", "Android 8.0 (API 26) или новее. Сервисы Google не нужны.")),
            (("Permissions", "Разрешения"), ("Accessibility, to see the app and site in front and draw the gate; a quiet notification that keeps Charon awake, and the oracle; device administrator only during an oath. No internet.",
                                            "Специальные возможности, чтобы видеть открытое приложение и сайт и ставить ворота; тихое уведомление, которое не даёт системе усыпить Харона, и оракул; администратор устройства только на время клятвы. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone and install it.", "Скачай APK на телефон и установи."),
            ("Open Obol, then switch it on in Settings → Accessibility.", "Открой Обол и включи его в «Настройки → Специальные возможности»."),
            ("Check your patrons and streams, then open a book instead of Reels.", "Проверь покровителей и потоки — и открой книгу вместо Reels."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Obol and remove battery limits, or the system will put Charon to sleep.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Оболу автозапуск и сними ограничения батареи, иначе система усыпит Харона."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/obol.git\ncd obol\n./gradlew testDebugUnitTest     <c># unit tests</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug -Pdemo   <c># app.obol.demo with four weeks of made-up history</c>",
        "faq": [
            (("Why isn't it on Google Play?", "Почему его нет в Google Play?"),
             ("Charon needs the accessibility service to see Reels inside Instagram and the address in a browser, and Google Play restricts that use. So Obol ships as an APK, like the other Stillcraft apps.",
              "Харону нужна служба специальных возможностей, чтобы видеть Reels внутри Instagram и адрес в браузере, а Google Play ограничивает такое использование. Поэтому Обол распространяется APK-файлом, как и другие приложения Stillcraft.")),
            (("Does it read my messages?", "Он читает мои сообщения?"),
             ("No. Charon looks at which app is in front, the browser's address bar and the names of screen elements that mark Reels or Shorts. Nothing is stored except the ledger lines, and the app has no internet access at all.",
              "Нет. Харон смотрит, какое приложение открыто, адресную строку браузера и названия элементов экрана, по которым видно Reels или Shorts. Хранятся только строки книги, а доступа в интернет у приложения нет вовсе.")),
            (("Can I cheat by leaving Duolingo open?", "Можно схитрить, оставив Duolingo открытым?"),
             ("Not for long. A patron counts only while you touch, scroll or type, and past its daily cap the rate halves.",
              "Ненадолго. Покровитель считает, только пока ты касаешься экрана, листаешь или печатаешь, а после дневного лимита курс падает вдвое.")),
            (("What if I really need Instagram right now?", "А если Instagram нужен прямо сейчас?"),
             ("Turn on \"only the endless feed\": messages stay free. For a link from a friend there are three free 5-minute passes a week.",
              "Включи «только бесконечная лента» — переписка останется бесплатной. Для ссылки от друга есть три бесплатных прохода по 5 минут в неделю.")),
        ],
    },
    {
        "slug": "prism",
        "name": "Prism",
        "panel": "app--prism",
        "gallery": "g-prism",
        "icon": "prism-logo.svg",
        "visual": "pr-home.png", "visual_ru": "pr-home.ru.png", "visual_wide": False,
        "repo": "https://github.com/bigdevwhale/prism",
        "download": "https://github.com/bigdevwhale/prism/releases/latest/download/Prism.apk",
        "version": "v1.0.0",
        "tagline": ("One light, many colours: choose who you are in every part of life.", "Один свет, много цветов: выбери, кем быть в каждой части жизни."),
        "badge": ("One light, many colours · New", "Один свет, много цветов · Новинка"),
        "status": ("ok", "New", "Новинка"),
        "file_badge": ("APK ready", "APK готов"),
        "plat_badge": "Android 8.0+",
        "title": ("One person at home, another at work. <em>Choose who.</em>",
                  "Дома один, на работе другой. <em>Выбери, кем быть.</em>"),
        "desc": ("Everyone plays many roles: partner, parent, colleague, friend, and someone else entirely when angry. Prism helps you choose them instead of slipping into them. Name your core values, describe who you want to be in each sphere of life or borrow from a library of 71 good roles, name the shadows you fall into, and practise the switch with short rituals. Your values are the white light, your roles are its colours. No ads, no account, and nothing leaves the phone.",
                 "Каждый играет много ролей: партнёр, родитель, коллега, друг — и кто-то совсем другой, когда злится. Prism помогает выбирать роли, а не соскальзывать в них. Назови свои ценности, опиши, кем хочешь быть в каждой сфере жизни, или возьми роль из библиотеки, где их 71. Назови тени, в которые проваливаешься, и тренируй переход короткими ритуалами. Ценности — белый свет, роли — его цвета. Без рекламы и аккаунта, ничего не покидает телефон."),
        "cta": ("Download APK", "Скачать APK"),
        "plat": ("Android 8.0+ · Free · Works offline · English &amp; Русский",
                 "Android 8.0+ · Бесплатно · Работает офлайн · English и Русский"),
        "features": [
            (("22 spheres and your own", "22 сферы и свои"),
             ("Home, partner, children, parents, work, leading, money, body, meaning, conflict, hard times, life online and more. Add your own sphere with a name, an icon and a colour.",
              "Дом, партнёр, дети, родители, работа, руководство, деньги, тело, смысл, конфликт, трудные времена, онлайн и другие. Добавь свою сферу — с названием, иконкой и цветом.")),
            (("A library of 71 good roles", "Библиотека из 71 роли"),
             ("Quiet Harbor, Safe Base, Calm Mountain, Friend to Myself… Each has a voice, three things it does, two it never does, a posture, a motto and a daily practice. Add one and rewrite it your way.",
              "Тихая гавань, Надёжный тыл, Спокойная гора, Друг себе… У каждой роли есть манера речи, три вещи, которые она делает, и две, которых не делает никогда, осанка, девиз и ежедневная практика. Добавь и перепиши под себя.")),
            (("18 shadows", "18 теней"),
             ("The Prosecutor, the Sulking Teen, the Workaholic, the Endless Feed. What sets each one off, what it's protecting, how to spot it early and which role answers it.",
              "Прокурор, Обиженный подросток, Трудоголик, Бесконечная лента. Что запускает каждую тень, что она защищает, как заметить её заранее и какая роль ей отвечает.")),
            (("The threshold", "Порог"),
             ("A minute between roles: breathe out the last scene, then step into the next as its colour, motto and posture fade in. Schedule it for the way home or before work.",
              "Минута между ролями: выдохнуть прошлую сцену и войти в новую, пока проявляются её цвет, девиз и осанка. Можно поставить по расписанию — на дорогу домой или перед работой.")),
            (("Practices for hard moments", "Практики для трудных минут"),
             ("The Mountain for anger, a rehearsal before a hard conversation, a council of roles for a hard choice, letters from a role, meeting a shadow, an anchor and three-week acts.",
              "Гора на случай злости, репетиция перед трудным разговором, совет ролей для трудного выбора, письмо от роли, встреча с тенью, якорь и трёхнедельные акты.")),
            (("The prism of your week", "Призма недели"),
             ("One coloured ray per role: wide when the role came up often, bright when you came close to it. The journal adds the balance of spheres and what charges or drains you.",
              "По цветному лучу на каждую роль: широкий, если роль звучала часто, и яркий, если получилось близко к задуманному. В дневнике — баланс сфер и то, что заряжает или истощает.")),
        ],
        "shots": [
            ("pr-home.png", "pr-home.ru.png", ("Prism", "Призма"), ("This week's light and today's role.", "Свет недели и роль дня.")),
            ("pr-roles.png", "pr-roles.ru.png", ("Roles", "Роли"), ("The core and the spheres of life.", "Ядро и сферы жизни.")),
            ("pr-role.png", "pr-role.ru.png", ("A role", "Роль"), ("Motto, cut, voice and actions.", "Девиз, огранка, манера речи и действия.")),
            ("pr-library.png", "pr-library.ru.png", ("Library", "Библиотека"), ("71 roles and 18 shadows.", "71 роль и 18 теней.")),
            ("pr-shadow.png", "pr-shadow.ru.png", ("A shadow", "Тень"), ("What it protects and what answers it.", "Что она защищает и что ей отвечает.")),
            ("pr-threshold.png", "pr-threshold.ru.png", ("Threshold", "Порог"), ("Stepping into a role.", "Вход в роль.")),
            ("pr-review.png", "pr-review.ru.png", ("Evening review", "Вечерний разбор"), ("How close you came today.", "Насколько близко получилось сегодня.")),
            ("pr-practices.png", "pr-practices.ru.png", ("Practices", "Практики"), ("Every day, hard moments and deeper.", "Каждый день, трудные минуты и глубже.")),
            ("pr-journal.png", "pr-journal.ru.png", ("Journal", "Дневник"), ("The balance of spheres.", "Баланс сфер.")),
        ],
        "extra": {
            "title": ("A good role and the shadow it answers", "Хорошая роль и тень, которой она отвечает"),
            "head": [("Sphere", "Сфера"), ("A good role", "Хорошая роль"), ("Shadow", "Тень")],
            "rows": [
                [("Home & family", "Дом и семья"), ("Quiet Harbor: home feels safe because you are calm in it", "Тихая гавань: дома спокойно, потому что спокойно тебе"), ("The Grumbler", "Ворчун")],
                [("Partner", "Партнёр"), ("Ally: whatever happens, you are on the same side", "Союзник: что бы ни случилось, вы на одной стороне"), ("The Prosecutor", "Прокурор")],
                [("Parents", "Родители"), ("Grateful Grown-up: an adult beside them, not a child again", "Благодарный взрослый: взрослый человек рядом с ними, а не снова ребёнок"), ("Child Again", "Снова ребёнок")],
                [("Conflict & anger", "Конфликт и гнев"), ("Calm Mountain: storms pass over you", "Спокойная гора: буря проходит мимо"), ("The Volcano", "Вулкан")],
                [("Rest & play", "Отдых и игра"), ("Master of Rest: rest properly, without guilt", "Мастер отдыха: отдыхать по-настоящему, без вины"), ("The Workaholic", "Трудоголик")],
                [("Online", "Онлайн"), ("Feed Gardener: you decide what grows in your attention", "Садовник ленты: что растёт в твоём внимании, решаешь ты, а не лента"), ("The Endless Feed", "Бесконечная лента")],
                [("Alone with yourself", "Наедине с собой"), ("Friend to Myself: the kindness you give to people you love", "Друг себе: к себе та же доброта, что и к тем, кого любишь"), ("The Inner Critic", "Внутренний критик")],
            ],
        },
        "facts": [
            (("Version", "Версия"), ("v1.0.0", "v1.0.0")),
            (("File", "Файл"), ("Prism.apk", "Prism.apk")),
            (("Requires", "Нужно"), ("Android 8.0 (API 26) or newer. No Google services needed.", "Android 8.0 (API 26) или новее. Сервисы Google не нужны.")),
            (("Permissions", "Разрешения"), ("Notifications for the morning choice, the evening review and scheduled thresholds. No internet.",
                                            "Уведомления для утреннего выбора роли, вечернего разбора и порогов по расписанию. Без интернета.")),
            (("License", "Лицензия"), ("MIT", "MIT")),
        ],
        "steps": [
            ("Download the APK on your phone.", "Скачай APK на телефон."),
            ("Open it and allow installs from this source when Android asks.", "Открой файл и разреши установку из этого источника, когда Android спросит."),
            ("Name your core, pick your spheres and take a first role from the library.", "Назови своё ядро, выбери сферы и возьми первую роль из библиотеки."),
        ],
        "note": ("On Xiaomi (MIUI / HyperOS), Huawei and some other phones, allow Autostart for Prism and remove battery limits so the morning choice, the evening review and thresholds arrive on time.",
                 "На Xiaomi (MIUI / HyperOS), Huawei и некоторых других телефонах разреши Prism автозапуск и сними ограничения батареи, чтобы утренний выбор, вечерний разбор и пороги приходили вовремя."),
        "build_req": ("JDK 17+ (Android Studio's bundled JBR works) and the Android SDK.", "JDK 17+ (подойдёт JBR из Android Studio) и Android SDK."),
        "build": "git clone https://github.com/bigdevwhale/prism.git\ncd prism\n./gradlew testDebugUnitTest     <c># unit tests, including the library check</c>\n./gradlew assembleDebug         <c># debug APK</c>\n./gradlew installDebug -Pdemo   <c># app.prism.demo with a made-up month of roles</c>",
        "faq": [
            (("Isn't playing roles fake?", "Играть роли — разве это не фальшь?"),
             ("You already play them; the question is whether you choose them. Every role in Prism grows out of the same core values, so it's still you, just the version you want to be in that place.",
              "Роли и так есть у каждого, вопрос только в том, выбраны ли они. Каждая роль в Prism растёт из одного и того же ядра ценностей, так что это всё равно ты — просто та версия, которой хочется быть именно здесь.")),
            (("What is a shadow?", "Что такое тень?"),
             ("The version of you that takes over when you're tired, hurt or scared: the Prosecutor, the Ghost, the Martyr. Prism treats each one as a part trying to help clumsily, and helps you notice it early and answer it with a role.",
              "Та версия тебя, которая берёт верх от усталости, обиды или страха: Прокурор, Призрак, Мученик. Prism считает каждую тень частью тебя, которая неуклюже пытается помочь, и учит замечать её заранее и отвечать ей ролью.")),
            (("Do I have to use the library?", "Обязательно брать роли из библиотеки?"),
             ("No. Write your own roles and shadows from scratch, or add one from the library and rewrite it in your own words. Spheres can be your own too.",
              "Нет. Роли и тени можно написать с нуля, а можно взять из библиотеки и переписать своими словами. Сферы тоже можно создавать свои.")),
            (("What if I change phones?", "А если я сменю телефон?"),
             ("Settings → Backup saves every role, scene, letter and council into one JSON file. Restore it on the new phone.",
              "«Настройки → Резервная копия» сохраняет все роли, сцены, письма и советы в один JSON-файл. Восстанови его на новом телефоне.")),
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
    vis_cls = "cv-" + {"anyway": "aw", "swisszen": "sz", "focusshield": "fs", "ties": "ti", "unhook": "un", "dayquest": "dq", "serene": "se", "ember": "em", "fogwalk": "fw", "dearme": "dm", "glow": "gl", "waypoint": "wp", "obol": "ob", "prism": "pr"}[app["slug"]]
    shot = {"anyway": ("en-now.png", "ru-now.png"), "swisszen": ("sz-home.png", "sz-home.ru.png"), "focusshield": ("fs-break.gif", None),
            "ties": ("ti-home.png", "ti-home.ru.png"), "unhook": ("un-home.png", "un-home.ru.png"), "dayquest": ("dq-tasks.png", "dq-tasks.ru.png"),
            "serene": ("se-today.png", "se-today.ru.png"), "ember": ("em-fast.png", "em-fast.ru.png"),
            "fogwalk": ("fw-map.png", "fw-map.ru.png"), "dearme": ("dm-letters.png", "dm-letters.ru.png"),
            "glow": ("gl-praise.png", "gl-praise.ru.png"), "waypoint": ("wp-mandala.png", "wp-mandala.ru.png"), "obol": ("ob-gate.png", "ob-gate.ru.png"), "prism": ("pr-home.png", "pr-home.ru.png")}[app["slug"]]
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
        <li><a href="../fogwalk/">Fogwalk</a></li>
        <li><a href="../dearme/">DearMe</a></li>
        <li><a href="../glow/">Glow</a></li>
        <li><a href="../waypoint/">Waypoint</a></li>
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
        <li><a href="https://github.com/bigdevwhale/fogwalk/releases" target="_blank" rel="noopener" data-i18n="ft.fwrel">Fogwalk releases</a></li>
        <li><a href="https://github.com/bigdevwhale/dearme/releases" target="_blank" rel="noopener" data-i18n="ft.dmrel">DearMe releases</a></li>
        <li><a href="https://github.com/bigdevwhale/glow/releases" target="_blank" rel="noopener" data-i18n="ft.glrel">Glow releases</a></li>
        <li><a href="https://github.com/bigdevwhale/waypoint/releases" target="_blank" rel="noopener" data-i18n="ft.wprel">Waypoint releases</a></li>
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
