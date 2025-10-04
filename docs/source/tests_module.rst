Модуль тестов (tests_module)
=====================

Обзор тестовых модулей для проверки функциональности проекта.

.. toctree::
   :maxdepth: 2
   :caption: Модули тестов:

   tests_data_module
   tests_database
   tests_processing
   tests_scan
   test_imports

.. _tests_data_module_section:

tests_data_module
=================

Тесты для модуля анализа данных и экспорта результатов.

Тестируемые функции модуля make_export_file
-------------------------------------------

.. _test_export_unknown_characters_csv:

export_unknown_characters_csv()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для экспорта неизвестных символов в CSV файл.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_export_unknown_characters_csv.TestExportUnknownCharactersCSV
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_get_quality_assessment:

_get_quality_assessment()
~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для оценки качества текста.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_get_quality_assessment.TestGetQualityAssessment
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_create_csv_report:

create_csv_report()
~~~~~~~~~~~~~~~~~~~

Функция для создания CSV отчета.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_csv_report.TestCreateCSVReport
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_create_detailed_csv_report:

create_detailed_csv_report()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания детального CSV отчета по нескольким результатам.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_detailed_csv_report.TestCreateDetailedCSVReport
   :members:
   :undoc-members:
   :show-inheritance:

Тестируемые функции модуля make_export_plot
-------------------------------------------

.. _test_create_analysis_charts:

create_analysis_charts()
~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания набора графиков анализа.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_analysis_charts.TestCreateAnalysisCharts
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_create_coverage_pie_chart:

_create_coverage_pie_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для создания круговой диаграммы покрытия.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_coverage_pie_chart.TestCreateCoveragePieChart
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_create_error_distribution_chart:

_create_error_distribution_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для создания гистограммы распределения ошибок.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_error_distribution_chart.TestCreateErrorDistributionChart
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_create_history_comparison_chart:

create_history_comparison_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания графика истории ошибок.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_history_comparison_chart.TestCreateHistoryComparisonChart
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_create_layouts_comparison_chart:

create_layouts_comparison_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания сравнительного графика раскладок.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_layouts_comparison_chart.TestCreateLayoutsComparisonChart
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_create_metrics_comparison_chart:

_create_metrics_comparison_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для создания радарной диаграммы метрик.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_data_module.test_create_metrics_comparison_chart.TestCreateMetricsComparisonChart
   :members:
   :undoc-members:
   :show-inheritance:

.. _tests_database_section:

tests_database
==============

Тесты для модуля работы с базой данных.

Тестируемые функции модуля database
-----------------------------------

.. _test_get_analysis_history:

get_analysis_history()
~~~~~~~~~~~~~~~~~~~~~~

Функция для получения истории анализа.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_get_analysis_history.TestGetAnalysisHistory
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_take_lk_names_from_lk:

take_lk_names_from_lk()
~~~~~~~~~~~~~~~~~~~~~~~

Функция для получения имен раскладок из базы данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_take_lk_names_from_lk.TestTakeLkNamesFromLk
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_take_lk_from_db:

take_lk_from_db()
~~~~~~~~~~~~~~~~~

Функция для получения раскладки из базы данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_take_lk_from_db.TestTakeLkFromDb
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_save_analysis_result:

save_analysis_result()
~~~~~~~~~~~~~~~~~~~~~~

Функция для сохранения результатов анализа в базу данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_save_analysis_result.TestSaveAnalysisResult
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_take_all_data_from_lk:

take_all_data_from_lk()
~~~~~~~~~~~~~~~~~~~~~~~

Функция для получения всех данных из таблицы раскладок.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_take_all_data_from_lk.TestTakeAllDataFromLk
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_get_analysis_statistics:

get_analysis_statistics()
~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для получения статистики анализа.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_get_analysis_statistics.TestGetAnalysisStatistics
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_delete_analysis_result:

delete_analysis_result()
~~~~~~~~~~~~~~~~~~~~~~~~

Функция для удаления результатов анализа из базы данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_delete_analysis_result.TestDeleteAnalysisResult
   :members:
   :undoc-members:
   :show-inheritance:

Тестируемые функции модуля db_init
----------------------------------

.. _test_init_tables:

init_tables()
~~~~~~~~~~~~~

Функция для инициализации таблиц в базе данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_init_tables.TestInitTables
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_make_mok_data:

make_mok_data()
~~~~~~~~~~~~~~~

Функция для создания тестовых данных в базе данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_database_module.test_make_mok_data.TestMakeMokData
   :members:
   :undoc-members:
   :show-inheritance:

.. _tests_processing_section:

tests_processing
================

Тесты для модуля обработки данных.

Тестируемые функции модуля calculate_data
-----------------------------------------

.. _test_make_processing:

make_processing()
~~~~~~~~~~~~~~~~~

Функция для обработки списка слов.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_processing_module.test_make_processing.TestMakeProcessing
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_make_processing_stream:

make_processing_stream()
~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потоковой обработки слов.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_processing_module.test_make_processing_stream.TestMakeProcessingStream
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_make_text_processing:

make_text_processing()
~~~~~~~~~~~~~~~~~~~~~~

Функция для обработки текста.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_processing_module.test_make_text_processing.TestMakeTextProcessing
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_make_text_processing_stream:

make_text_processing_stream()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потоковой обработки текста.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_processing_module.test_make_text_processing_stream.TestMakeTextProcessingStream
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_validate_rules:

validate_rules()
~~~~~~~~~~~~~~~~

Функция для валидации правил раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_processing_module.test_validate_rules.TestValidateRules
   :members:
   :undoc-members:
   :show-inheritance:

.. _tests_scan_section:

tests_scan
==========

Тесты для модуля сканирования и чтения файлов.

Тестируемые функции модуля read_layout
--------------------------------------

.. _test_read_kl:

read_kl()
~~~~~~~~~

Функция для чтения раскладки из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_read_kl.TestReadKl
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_is_numeric:

_is_numeric()
~~~~~~~~~~~~~

Внутренняя функция для проверки числовых строк.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_is_numeric.TestIsNumeric
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_extract_layout_from_dict:

_extract_layout_from_dict()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для извлечения раскладки из словаря.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_extract_layout_from_dict.TestExtractLayoutFromDict
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_read_json_layout:

_read_json_layout()
~~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения JSON раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_read_json_layout.TestReadJsonLayout
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_read_xml_layout:

_read_xml_layout()
~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения XML раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_read_xml_layout.TestReadXmlLayout
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_auto_detect_and_read:

_auto_detect_and_read()
~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для автоматического определения и чтения формата.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_auto_detect_and_read.TestAutoDetectAndRead
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_read_text_layout:

_read_text_layout()
~~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения текстовой раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_read_text_layout.TestReadTextLayout
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_save_layout_to_file:

save_layout_to_file()
~~~~~~~~~~~~~~~~~~~~~

Функция для сохранения раскладки в файл.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_save_layout_to_file.TestSaveLayoutToFile
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_validate_layout:

validate_layout()
~~~~~~~~~~~~~~~~~

Функция для валидации раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_validate_layout.TestValidateLayout
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_read_csv_layout:

_read_csv_layout()
~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения CSV раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_read_csv_layout.TestReadCsvLayout
   :members:
   :undoc-members:
   :show-inheritance:

Тестируемые функции модуля read_files
-------------------------------------

.. _test_get_words_from_file:

get_words_from_file()
~~~~~~~~~~~~~~~~~~~~~

Функция для чтения слов из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_get_words_from_file.TestGetWordsFromFile
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_get_words_from_file_stream:

get_words_from_file_stream()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потокового чтения слов из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_get_words_from_file_stream.TestGetWordsFromFileStream
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_get_file_size_mb:

get_file_size_mb()
~~~~~~~~~~~~~~~~~~

Функция для получения размера файла в мегабайтах.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_get_file_size_mb.TestGetFileSizeMb
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_count_lines_in_file:

count_lines_in_file()
~~~~~~~~~~~~~~~~~~~~~

Функция для подсчета строк в файле.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_count_lines_in_file.TestCountLinesInFile
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_count_characters_in_file:

count_characters_in_file()
~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для подсчета символов в файле.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_count_characters_in_file.TestCountCharactersInFile
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_get_text_from_file:

get_text_from_file()
~~~~~~~~~~~~~~~~~~~~

Функция для чтения текста из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_get_text_from_file.TestGetTextFromFile
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_get_text_from_file_stream:

get_text_from_file_stream()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потокового чтения текста из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.tests_scan_module.test_get_text_from_file_stream.TestGetTextFromFileStream
   :members:
   :undoc-members:
   :show-inheritance:

.. _test_imports_section:

test_imports
============

Тесты для проверки корректности импортов всех модулей проекта.

.. _test_imports:

test_imports.py
---------------

**Описание**: Скрипт для проверки корректности импортов всех основных модулей проекта.

**Назначение**: Проверяет, что все модули могут быть успешно импортированы без ошибок.

**Проверяемые импорты**:

- ``database_module.db_init`` - функции инициализации БД
- ``database_module.database`` - функции работы с базой данных  
- ``scan_module.read_files`` - функции чтения файлов
- ``processing_module.calculate_data`` - функции обработки данных
- ``data_module.make_export_file`` - функции экспорта в файлы
- ``data_module.make_export_plot`` - функции создания графиков
- ``output_data.console_strings`` - строки для консольного вывода
- ``scan_module.read_layout`` - функции чтения раскладок

**Исходный код**:

.. literalinclude:: ../../tests_module/test_imports.py
   :language: python
   :linenos:
   :caption: test_imports.py
   :emphasize-lines: 7-45

**Результат выполнения**:
При успешном выполнении скрипт выводит сообщение "🎉 Все импорты успешны!".
При ошибках импорта выводится соответствующее сообщение об ошибке.

Индексирование
==============

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`