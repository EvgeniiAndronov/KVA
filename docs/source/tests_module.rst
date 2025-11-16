Модуль тестов (tests_module)
============================

Модуль для тестирования функциональности проекта. 

.. automodule:: tests_module
   :members:
   :undoc-members:
   :show-inheritance:

Подмодули тестов
----------------

test_imports
~~~~~~~~~~~~~~~

Проверяет успешность импорта всех необходимых модулей и зависимостей.

.. automodule:: tests_module.test_imports
   :members:
   :undoc-members:
   :show-inheritance:

test_database_module
~~~~~~~~~~~~~~~~~~~~~~~

Тестирует взаимодействие с базой данных (подключение, запросы, транзакции, статистика пальцев).

.. automodule:: tests_module.test_database_module
   :members:
   :undoc-members:
   :show-inheritance:

test_processing_module
~~~~~~~~~~~~~~~~~~~~~~~~~

Проверяет логику обработки данных (алгоритмы, преобразования, результаты, статистика пальцев).

.. automodule:: tests_module.test_processing_module
   :members:
   :undoc-members:
   :show-inheritance:

test_scan_module
~~~~~~~~~~~~~~~~~~~

Тестирует функционал сканирования (чтение файлов, работа с раскладками различных форматов).

.. automodule:: tests_module.test_scan_module
   :members:
   :undoc-members:
   :show-inheritance:

conftest
~~~~~~~~~~~

Содержит общие фикстуры и настройки для всех тестов.

**Фикстуры:**

* ``temp_file`` - временный файл с текстом
* ``temp_db`` - временная база данных
* ``sample_rules_old`` - правила в старом формате
* ``test_analysis_result`` - результаты анализа со статистикой пальцев
* ``test_layout_file`` - временный файл раскладки
* Генераторы для потоковой обработки

Запуск тестов
-------------

Для запуска всех тестов выполните:

.. code-block:: bash

   pytest tests_module/

Для запуска конкретного модуля тестов:

.. code-block:: bash

   pytest tests_module/test_database_module.py
   pytest tests_module/test_processing_module.py -v