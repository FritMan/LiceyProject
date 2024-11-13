#Приложение создано для изучения французского языка путём тестов на память и сопоставления слов
		
    main.py:
        Выступает в роли направляющего звена, в него входят три кнопки, их функционал
        написан на них же, если необходимо больше информации, читайте ниже

    btn_menu.py:
        Ещё одно меню, отвечаюшее за вспомогательные программы/скрипты. В него,
        как и во все интерфейсы, можно попасть из главного меню (main.py).

	dictionary.db:
        Просто словарь, включающий в себя сами слова и их значения
	
	edit_dictionary.py:
		Интерфейс для реализации изменения слов и добавления слов в БД
	
	word_match.py:
		Тест подбора правильного перевода к выбранному слову.
		Выбранное для перевода слово в левом столбце выделяется жёлтым фоном.
		В правом столбце окно ввода поиска
		Запуск поиска настроен на клавишу "Enter". При нажатии "Enter"
		найденные в столбце слова с совпадениями выделяются красным цветом.
		В консоле печатается список слов, содержащих совпадение и 
		количество оставшихся строк для теста. Если совпадений не найдено, печатается пустой список.
	
	from_memory.py:
		Тест "Перевод по памяти".
		Из перемешанного списка подаётся слово для перевода По нажатии клавиши "Enter"
		или кнопки "да" подаётся следующее слово, а поле ввода очищается.
		По окончании списка открывается таблица из трёх столбцов: Французское
		слово - вариант перевода пользователя - правильный вариант.
		Также можно вызвать таблицу не дожидаясь конца теста.
		Для этого надо нажать клавишу "стоп". Таблица отобразит переведённые 
		слова. Закрыв таблицу, можно продолжить тест дальше.

	write_in_file.py:
        Программа создаст текстовый файл translation.txt и перепишет в него 
        построчно БД французских слов и их переводов. Текстовый файл можно
        скопировать на смартфон и в любое удобное время тренироваться, запоминать перевод слов.

    
    create_new_db.py:
        Программа создаст БД (Может быть пользователю потребуется, кто знает ("_"))