(function () {
  var I18N = {
    ru: {
      "nav.apps": "Приложения", "nav.moments": "По ситуации", "nav.principles": "Принципы",
      "hero.eyebrow": "Спокойные инструменты для телефона и компьютера",
      "hero.title": "Маленькие инструменты для <em>тихой</em> головы.",
      "hero.lede": "Карманные приложения на минуту между делами. Подышать, отпустить тревогу, вспомнить, что ты жив. Без аккаунтов, лент и обязательств.",
      "hero.cta": "Смотреть приложения", "hero.source": "Код на GitHub",
      "hero.meta": "Android и Windows · Бесплатно · English и Русский · Работает офлайн",
      "breath.idle": "Квадратное дыхание", "breath.start": "Подышать вместе", "breath.stop": "Хватит",
      "breath.in": "Вдох", "breath.hold": "Пауза", "breath.out": "Выдох",
      "apps.eyebrow": "На полке · 3 приложения, будут ещё",
      "apps.title": "Каждое делает несколько вещей хорошо и не мешает жить.",
      "aw.tag": "Memento mori без черепов",
      "aw.lede": "Все мы когда-нибудь умрём. <em>Так что иди и сделай это.</em>",
      "aw.desc": "У тебя нет лет. У тебя есть субботы, около 4 000, если повезёт. Anyway показывает это число и помогает не тратить их на то, чего не запомнит даже Солнце.",
      "cta.apk": "Скачать APK", "aw.note": "Без доступа к интернету вообще",
      "aw.f1": "Сейчас", "aw.f1d": "Сколько суббот осталось, вопрос дня и большая оранжевая кнопка ANYWAY для того, что страшно сделать.",
      "aw.f2": "Фильтр тревог", "aw.f2d": "Будет ли это важно через 5 лет? Через 100? Когда Солнце станет красным гигантом? Если нет — тревога сжимается и улетает.",
      "aw.f3": "Пока не поздно", "aw.f3d": "То, о чём пожалеешь, если не сделаешь. Каждый пункт считает, сколько ждёт, и через неделю становится оранжевым.",
      "aw.f4": "Ты всё ещё жив", "aw.f4d": "Одно уведомление в день, в случайный момент между 10:00 и 21:00.",
      "sz.tag": "Мультитул осознанности",
      "sz.lede": "Открой нож. <em>Минуты достаточно.</em>",
      "sz.desc": "Большинство приложений для медитации требуют обязательств. SwissZen — карманный нож: раскрой один инструмент под момент, используй и сложи обратно.",
      "sz.note": "Лицензия MIT",
      "sz.f1": "Дыхание", "sz.f1d": "Сфера, растущая на вдохе. Квадрат 4‑4‑4‑4, Спокойствие 4‑7‑8, Когерентное 5‑5, на 2, 5 или 10 минут.",
      "sz.f2d": "Раунды силового дыхания, четыре уровня, задержки от 0:30 до 3:00+.",
      "sz.f3": "Колокольчик", "sz.f3d": "Колокольчик осознанности звонит при закрытом приложении: случайно, по интервалу или в заданное время, с тихими часами.",
      "sz.f4": "Практики", "sz.f4d": "Пять микропрактик на 1–5 минут и пять медитаций на 5–20.",
      "sz.f5": "Дневник", "sz.f5d": "Одна строка в день и «Эхо» — то, что ты написал несколько недель назад.",
      "next.eyebrow": "В мастерской", "next.title": "Следующий инструмент уже делается.",
      "next.desc": "Новые приложения появятся здесь первыми. Подпишись на GitHub, чтобы увидеть их ещё сырыми.",
      "next.cta": "Подписаться на GitHub",
      "mo.eyebrow": "По ситуации", "mo.title": "Что тебе нужно прямо сейчас?",
      "mo.lede": "Начни с того, что чувствуешь, а не с того, какое приложение открыть.",
      "mo.1": "Тревога ходит по кругу", "mo.1t": "Фильтр тревог", "mo.1d": "Три вопроса, последний — про Солнце-красный гигант. Большинство тревог отсеивается уже на втором.", "mo.1m": "~1 мин",
      "mo.2": "Слишком много в голове", "mo.2t": "Заземление 5‑4‑3‑2‑1", "mo.2d": "Пять вещей, которые видишь, четыре — слышишь, три — можешь потрогать. Ты снова в комнате.", "mo.2m": "3 мин",
      "mo.3": "«Всего минутку» на YouTube", "mo.3t": "Фокус-сессия с намерением", "mo.3d": "Назови одно дело и запусти 50 минут. Защита вкладок закроет YouTube раньше, чем рука до него дотянется.", "mo.3m": "25–90 мин",
      "mo.4": "Всё время откладываешь", "mo.4t": "Кнопка ANYWAY", "mo.4d": "Напиши сообщение. Купи билет. Потанцуй плохо. Нажми и иди.", "mo.4m": "10 сек",
      "mo.5": "Не получается уснуть", "mo.5t": "Дыхание 4‑7‑8 и медитация перед сном", "mo.5d": "Вдох на 4, пауза на 7, выдох на 8. Потом медленная медитация на последние минуты дня.", "mo.5m": "10 мин",
      "mo.6": "День на автопилоте", "mo.6t": "Колокольчик и напоминание", "mo.6d": "Колокольчик просит остановиться. «Ты всё ещё жив» спрашивает, что ты с этим сделаешь.",
      "pr.eyebrow": "Как они сделаны", "pr.title": "Спокойствие не должно быть подпиской.",
      "pr.1": "Ничего не покидает телефон", "pr.1d": "Без аккаунтов, аналитики и рекламы. Тревоги, дневник и дата рождения остаются на устройстве. Anyway даже не просит доступ к интернету.",
      "pr.2": "Бесплатно и с открытым кодом", "pr.2d": "Все приложения на GitHub. Скачай APK или EXE напрямую, почитай код, собери сам. Никаких пробных периодов, превращающихся в счёт.",
      "pr.3": "Сделаны, чтобы их закрывали", "pr.3d": "Ни ленты, ни бесконечной прокрутки. Открыл на минуту, получил своё, отложил телефон. В этом весь смысл.",
      "cl.title": "Удели одну минуту.", "cl.lede": "Бесплатно для Android 8.0+ и Windows 10 / 11. Выбери то, что подходит сегодня.",
      "cl.aw": "Скачать Anyway", "cl.sz": "Скачать SwissZen", "cl.fs": "Скачать FocusShield", "ft.fsrel": "Релизы FocusShield",
      "cta.exe": "Скачать для Windows",
      "fs.tag": "Глубокая работа на Windows",
      "fs.lede": "Отсеки шум. <em>Будь честен с собой.</em>",
      "fs.desc": "Таймер фокуса, построенный на трении. Пока идёт сессия, отвлекающие сайты не открываются, выбранные приложения закрываются, а чтобы выйти раньше, нужно подождать 10 секунд и набрать фразу. Когда время выходит, всё разблокируется и начинается настоящий перерыв.",
      "fs.note": "Windows 10 / 11 · 100% локально",
      "fs.f1": "Сначала намерение", "fs.f1d": "Каждая сессия начинается с того, что именно будет сделано, и заканчивается вопросом: получилось?",
      "fs.f2": "Настоящая блокировка", "fs.f2d": "Сайты, вкладки YouTube (даже через VPN), приложения и папки закрыты, пока идёт таймер.",
      "fs.f3": "Перерывы, которые восстанавливают", "fs.f3d": "Дыхание 4‑7‑8 с анимированным кругом, правило 20‑20‑20 для глаз, разминка и стакан воды.",
      "fs.f4": "Росток, который растёт", "fs.f4d": "Необязательный маскот отращивает лист с каждым помидоро и расцветает на длинном перерыве.",
      "fs.cap": "Спит · в фокусе · в фокусе · последняя минута · почти · длинный перерыв",
      "ft.all": "Все приложения",
      "ap.eyebrow": "Приложения Stillcraft",
      "ap.meta": "3 приложения · Бесплатно · Код открыт · English и Русский",
      "ap.title": "Три приложения. <em>Одна тихая мастерская.</em>",
      "ap.lede": "Каждое — маленький инструмент для одного момента: подышать, отпустить тревогу, вспомнить о главном, удержать фокус. Без аккаунтов, без рекламы, без интернета, если он не нужен.",
      "ap.follow": "Подписаться на GitHub", "ap.home": "На главную",
      "ap.lineup": "Все приложения", "ap.lineupTitle": "Выбери инструмент под момент.",
      "ap.early": "Ранняя версия", "ap.stable": "Стабильная", "ap.apk": "APK готов", "ap.exe": "Установщик готов",
      "ap.aw": "Сколько суббот у тебя осталось, и что ты с ними сделаешь.",
      "ap.sz": "Мультитул осознанности: дыхание, Вим Хоф, колокольчик, практики, дневник.",
      "ap.fs": "Строгий таймер фокуса, который правда блокирует отвлечения.",
      "ap.explore": "Подробнее",
      "ap.nextTitle": "Скоро будут ещё.", "ap.nextDesc": "Есть идея спокойного инструмента или хочешь тестировать ранние сборки? Напиши в issues.",
      "ap.suggest": "Предложить приложение",
      "ap.prEyebrow": "Принципы", "ap.prTitle": "Сделано не спеша.",
      "ap.p1": "Без аккаунтов", "ap.p1d": "Ни регистрации, ни входа, ни почты. Открыл и пользуешься.",
      "ap.p2": "Данные остаются у тебя", "ap.p2d": "Дневник, тревоги, фото фокуса и статистика хранятся только на устройстве. Аналитики нет.",
      "ap.p3": "Открытый код", "ap.p3d": "Каждое приложение лежит на GitHub. Можно прочитать, собрать самому и предложить правку.",
      "ap.p4": "Родные для платформы", "ap.p4d": "Kotlin и Jetpack Compose на Android, приложение в трее на Windows. Никаких веб-обёрток.",
      "ap.p5": "Два языка", "ap.p5d": "Каждый экран, практика и подсказка — на английском и русском.",
      "ap.p6": "Ничего не продаём", "ap.p6d": "Без рекламы, подписок и платных уровней. Просто скачай файл с GitHub.",
      "ap.clTitle": "Сделаем следующий вместе.", "ap.clDesc": "Расскажи, в какой момент дня тебе не хватает тишины. Возможно, это и будет следующее приложение.",
      "ft.tag": "Маленькие инструменты для тихой головы.", "ft.apps": "Приложения", "ft.soon": "Скоро ещё",
      "ft.source": "Исходники", "ft.awrel": "Релизы Anyway", "ft.szrel": "Релизы SwissZen",
      "ft.made": "© 2026 Stillcraft. Сделано не спеша.",
      "ft.med": "Дыхательные упражнения — не лечение. Практикуй сидя или лёжа, не в воде и не за рулём."
    }
  };
  var MARQUEE = {
    en: ["Saturdays left", "Box 4‑4‑4‑4", "The Worry Filter", "Wim Hof rounds", "Tab guard", "Mindfulness bell", "Calm 4‑7‑8", "Before it's too late", "Body scan", "One line a day", "Pomodoro sprout", "5‑4‑3‑2‑1 grounding", "You're still alive", "Loving-kindness"],
    ru: ["Сколько суббот осталось", "Квадрат 4‑4‑4‑4", "Фильтр тревог", "Раунды Вима Хофа", "Блокировка YouTube", "Колокольчик осознанности", "Дыхание 4‑7‑8", "Пока не поздно", "Сканирование тела", "Строка в день", "Росток-помидоро", "Заземление 5‑4‑3‑2‑1", "Ты всё ещё жив", "Медитация доброты"]
  };

  if (window.PAGE_RU) Object.keys(window.PAGE_RU).forEach(function (k) { I18N.ru[k] = window.PAGE_RU[k]; });
  var nodes = document.querySelectorAll("[data-i18n]");
  var EN = {};
  nodes.forEach(function (n) { EN[n.dataset.i18n] = n.innerHTML; });
  EN["breath.start"] = "Breathe with me"; EN["breath.stop"] = "Stop";
  EN["breath.in"] = "Inhale"; EN["breath.hold"] = "Hold"; EN["breath.out"] = "Exhale";
  var imgs = document.querySelectorAll("img[data-src-ru]");
  imgs.forEach(function (i) { i.dataset.srcEn = i.getAttribute("src"); });

  var lang = "en";
  function t(key) { return (lang === "ru" && I18N.ru[key]) || EN[key] || key; }

  function renderMarquee() {
    var items = MARQUEE[lang].map(function (s) { return "<span>" + s + "</span>"; }).join("");
    var m = document.getElementById("marquee");
    if (m) m.innerHTML = items + items;
  }

  function setLang(next) {
    lang = next;
    document.documentElement.lang = lang;
    nodes.forEach(function (n) { n.innerHTML = t(n.dataset.i18n); });
    imgs.forEach(function (i) { i.src = lang === "ru" ? i.dataset.srcRu : i.dataset.srcEn; });
    document.querySelectorAll(".lang button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.lang === lang)); });
    renderMarquee();
    syncBreath();
    try { localStorage.setItem("stillcraft-lang", lang); } catch (e) {}
  }
  document.querySelectorAll(".lang button").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.dataset.lang); });
  });

  /* Box breathing: 4 s per phase. Scale goes up on inhale, stays on hold, down on exhale. */
  var PHASES = [
    { key: "breath.in", scale: 1 },
    { key: "breath.hold", scale: 1 },
    { key: "breath.out", scale: 0.72 },
    { key: "breath.hold", scale: 0.72 }
  ];
  var orb = document.getElementById("orb"), mirror = document.getElementById("orb-mirror");
  var phaseEl = document.getElementById("phase"), countEl = document.getElementById("count");
  var toggle = document.getElementById("breath-toggle");
  var timer = null, step = 0, sec = 0;
  var hasBreath = !!(orb && toggle);

  function setScale(s) { orb.style.setProperty("--s", s); mirror.style.setProperty("--s", s); }
  function syncBreath() {
    if (!hasBreath) return;
    if (timer) {
      var p = PHASES[step];
      phaseEl.textContent = t(p.key);
      countEl.textContent = String(4 - sec);
      toggle.textContent = t("breath.stop");
    } else {
      phaseEl.textContent = t("breath.idle");
      countEl.textContent = "4 · 4 · 4 · 4";
      toggle.textContent = t("breath.start");
    }
  }
  function tick() {
    sec++;
    if (sec >= 4) { sec = 0; step = (step + 1) % 4; setScale(PHASES[step].scale); }
    syncBreath();
  }
  if (hasBreath) toggle.addEventListener("click", function () {
    if (timer) { clearInterval(timer); timer = null; setScale(0.72); }
    else { step = 0; sec = 0; setScale(PHASES[0].scale); timer = setInterval(tick, 1000); }
    syncBreath();
  });

  var saved = null;
  try { saved = localStorage.getItem("stillcraft-lang"); } catch (e) {}
  var initial = saved || ((navigator.language || "").toLowerCase().indexOf("ru") === 0 ? "ru" : "en");
  setLang(initial);
})();
