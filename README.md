# v 1.5 - D7. Работа с асинхронными данными

## NEWS:

¯\_(ツ)_/¯

## FIXES: 

Исправлена рассылка еженедельных новостей на каждую пятницу в 18:00 (крон был поставлен на ежеминутную рассылку для дебага)

Рассылка больше не содержит новостей без категорий

Исправлена ссылка в рассылке новостей (ID-код поста дублировался)

## QoL:

Переделана еженедельная рассылка и рассылка при публикации поста под celery
(tbh с celery тормозит сильнее нежели без него, может при большом объеме данных поможет ¯\_(ツ)_/¯ )


# v 1.4 - D6. Работа с почтой

## NEW:

Добавлена возможность указания категорий для новостей ~~Почему этого изначально не было?~~

Добавлена возможность перехода в детальный просмотр новостей, нажав на заголовок новости

Произведён рефактор проекта:

- Весь список публикаций доступен по ссылке /allnews
- Редактирование (в т.ч. создание и удаление) публикаций теперь доступны по ссылкам /news/.. и /articles/..

В связи с рефактором создана приветственная страница (по адресу localhost:8000) с просьбой фидбека по каким-либо
проглядевшим мною недочётам

Кнопка логина/логаута оптимизирована для пользователя в связи с его статусом аутентификации

Исправлено отображение вида типа записи и её категорий

Добавлена возможность подписки для рассылки новых записей по категориям
- При публикации новости - отправляется сообщение пользователям, которые указали в подписке соответствующие категории
- Каждую пятницу отправляется список новостей за последнюю неделю, с возможностью перехода к постам


## FIXES:

Исправлено отображение категорий и типа поста в детальном просмотре новостей

Исправлен поиск новостей по категориям


# v 1.3 - D5. Авторизация и регистрация

## NEW:

Добавлена страница-ошибка 403

Добавлена аутентификация и регистрация, доступные по ссылкам:
- ../accounts/login<br>
- ../accounts/signup<br>

Добавлена авторизация через Yandex-аккаунт

Добавлена группа прав для создания новостей

Добавлены кнопки для создания новостей и статей на странице со всеми новостями пользователям с соответствующими правами

Добавлены кнопки для быстрого взаимодействия с существующими новостями на главной странице для пользователей с
 соответствующими правами

## FIXES:

Исправлена ошибка добавления новостей под категорией статей и наоборот


# V 1.2 - D4. Фильтры и формы

Added Search page by various args

Limited news counter per page to 10

Created paginator to main "news" page and search page

Added option to Add/Edit/Delete News and Articles separately, which may be accessed by links:

- ../news(or article instead)/create
- ../news(or article instead)/<int:pk>/update
- ../news(or article instead)/<int:pk>/delete


# V 1.1

Improved news and specific new description;

Added detailed description of each post and for all of them together;

Added censure filter for words which starts with 'редиск'
