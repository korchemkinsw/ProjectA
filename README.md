# ProjectA
(первый самостоятельный, неучебный, уровня "стажёр")

admin@admin.ad nthvbyfnjh - для меня, чтоб не забыть

##Предыстория, благодарности...

- За идею! - моей основной работе, которая несколько лет не может организовать нормальную систему передачи указаний нескольким сотрудникам и проекту: https://www.redmine.org/, которым довелось попользоваться...
- За выбор! - https://www.officer24.ru/, получив который, пришлось изучать ньюансы...
- За реализацию! - https://practicum.yandex.ru/learn/backend-developer/ - без комментариев... Результат на оценку...)))
- И самое главное! - всему интернет-сообщесву увлеченных людей, которые деляться своими решениями и напутственному слову моего руководителя дипломного проекта!


## app Orders
(часть первая - начало...)

###Суть. 
1. Пользователь "секретарь" выпускает документ с наименованием "приказ" по одному из нескольких предприятий с указанием ряда исполнителей из числа пользователей "инженер" со статусом "новый".
2. Пользователь "инженер" принимает документ и переводит его в один из статусов "в работе", "завершен", "отклонен".
3. Если текущая дата больше даты поля "выполнить до:" документ переходит в статус "просрочен!"
4. В базе содержится информация о:
    - авторе и дате создания
    - номер приказа и предприятие
    - крайняя дата выполнения
    - список исполнителей
    - файлы документов

###Реализация.
    - множественный ввод с использованием formset и jqery
    - пользователи для выбора отфильтрованы по параметру "инженер"
    - выбор дат инструментами администратора (как передать начальное значение в виджет в форме редактирования пока не освоил, поэтому там admin!)
    - автоматическая фильтрация для автора по автору, для исполнителя - по исполнителю
    - для вывода доступна фильтрация по поям "статус", "номер", "примечание", диапазону дат с пагинацией результата

