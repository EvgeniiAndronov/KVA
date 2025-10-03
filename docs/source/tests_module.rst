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

tests_data_module
=================

Тесты для модуля анализа данных и экспорта результатов.

Тестируемые функции модуля make_export_file
-------------------------------------------

export_unknown_characters_csv()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для экспорта неизвестных символов в CSV файл.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_export_unknown_characters_csv.TestExportUnknownCharactersCSV
   :members:
   :undoc-members:
   :show-inheritance:

_get_quality_assessment()
~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для оценки качества текста.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_get_quality_assessment.TestGetQualityAssessment
   :members:
   :undoc-members:
   :show-inheritance:

create_csv_report()
~~~~~~~~~~~~~~~~~~~

Функция для создания CSV отчета.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_csv_report.TestCreateCSVReport
   :members:
   :undoc-members:
   :show-inheritance:

create_detailed_csv_report()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания детального CSV отчета по нескольким результатам.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_detailed_csv_report.TestCreateDetailedCSVReport
   :members:
   :undoc-members:
   :show-inheritance:

Тестируемые функции модуля make_export_plot
-------------------------------------------

create_analysis_charts()
~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания набора графиков анализа.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_analysis_charts.TestCreateAnalysisCharts
   :members:
   :undoc-members:
   :show-inheritance:

_create_coverage_pie_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для создания круговой диаграммы покрытия.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_coverage_pie_chart.TestCreateCoveragePieChart
   :members:
   :undoc-members:
   :show-inheritance:

_create_error_distribution_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для создания гистограммы распределения ошибок.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_error_distribution_chart.TestCreateErrorDistributionChart
   :members:
   :undoc-members:
   :show-inheritance:

create_history_comparison_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания графика истории ошибок.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_history_comparison_chart.TestCreateHistoryComparisonChart
   :members:
   :undoc-members:
   :show-inheritance:

create_layouts_comparison_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для создания сравнительного графика раскладок.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_layouts_comparison_chart.TestCreateLayoutsComparisonChart
   :members:
   :undoc-members:
   :show-inheritance:

_create_metrics_comparison_chart()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для создания радарной диаграммы метрик.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_data_module.test_create_metrics_comparison_chart.TestCreateMetricsComparisonChart
   :members:
   :undoc-members:
   :show-inheritance:

tests_database
==============

Тесты для модуля работы с базой данных.

Тестируемые функции модуля database
-----------------------------------

get_analysis_history()
~~~~~~~~~~~~~~~~~~~~~~

Функция для получения истории анализа.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_get_analysis_history.TestGetAnalysisHistory
   :members:
   :undoc-members:
   :show-inheritance:

take_lk_names_from_lk()
~~~~~~~~~~~~~~~~~~~~~~~

Функция для получения имен раскладок из базы данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_take_lk_names_from_lk.TestTakeLkNamesFromLk
   :members:
   :undoc-members:
   :show-inheritance:

take_lk_from_db()
~~~~~~~~~~~~~~~~~

Функция для получения раскладки из базы данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_take_lk_from_db.TestTakeLkFromDb
   :members:
   :undoc-members:
   :show-inheritance:

save_analysis_result()
~~~~~~~~~~~~~~~~~~~~~~

Функция для сохранения результатов анализа в базу данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_save_analysis_result.TestSaveAnalysisResult
   :members:
   :undoc-members:
   :show-inheritance:

take_all_data_from_lk()
~~~~~~~~~~~~~~~~~~~~~~~

Функция для получения всех данных из таблицы раскладок.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_take_all_data_from_lk.TestTakeAllDataFromLk
   :members:
   :undoc-members:
   :show-inheritance:

get_analysis_statistics()
~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для получения статистики анализа.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_get_analysis_statistics.TestGetAnalysisStatistics
   :members:
   :undoc-members:
   :show-inheritance:

delete_analysis_result()
~~~~~~~~~~~~~~~~~~~~~~~~

Функция для удаления результатов анализа из базы данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_delete_analysis_result.TestDeleteAnalysisResult
   :members:
   :undoc-members:
   :show-inheritance:

Тестируемые функции модуля db_init
----------------------------------

init_tables()
~~~~~~~~~~~~~

Функция для инициализации таблиц в базе данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_init_tables.TestInitTables
   :members:
   :undoc-members:
   :show-inheritance:

make_mok_data()
~~~~~~~~~~~~~~~

Функция для создания тестовых данных в базе данных.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_database.test_make_mok_data.TestMakeMokData
   :members:
   :undoc-members:
   :show-inheritance:

tests_processing
================

Тесты для модуля обработки данных.

Тестируемые функции модуля calculate_data
-----------------------------------------

make_processing()
~~~~~~~~~~~~~~~~~

Функция для обработки списка слов.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_processing.test_make_processing.TestMakeProcessing
   :members:
   :undoc-members:
   :show-inheritance:

make_processing_stream()
~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потоковой обработки слов.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_processing.test_make_processing_stream.TestMakeProcessingStream
   :members:
   :undoc-members:
   :show-inheritance:

make_text_processing()
~~~~~~~~~~~~~~~~~~~~~~

Функция для обработки текста.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_processing.test_make_text_processing.TestMakeTextProcessing
   :members:
   :undoc-members:
   :show-inheritance:

make_text_processing_stream()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потоковой обработки текста.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_processing.test_make_text_processing_stream.TestMakeTextProcessingStream
   :members:
   :undoc-members:
   :show-inheritance:

validate_rules()
~~~~~~~~~~~~~~~~

Функция для валидации правил раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_processing.test_validate_rules.TestValidateRules
   :members:
   :undoc-members:
   :show-inheritance:

tests_scan
==========

Тесты для модуля сканирования и чтения файлов.

Тестируемые функции модуля read_layout
--------------------------------------

read_kl()
~~~~~~~~~

Функция для чтения раскладки из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_read_kl.TestReadKl
   :members:
   :undoc-members:
   :show-inheritance:

_is_numeric()
~~~~~~~~~~~~~

Внутренняя функция для проверки числовых строк.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test__is_numeric.TestIsNumeric
   :members:
   :undoc-members:
   :show-inheritance:

_extract_layout_from_dict()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для извлечения раскладки из словаря.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_extract_layout_from_dict.TestExtractLayoutFromDict
   :members:
   :undoc-members:
   :show-inheritance:

_read_json_layout()
~~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения JSON раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_read_json_layout.TestReadJsonLayout
   :members:
   :undoc-members:
   :show-inheritance:

_read_xml_layout()
~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения XML раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_read_xml_layout.TestReadXmlLayout
   :members:
   :undoc-members:
   :show-inheritance:

_auto_detect_and_read()
~~~~~~~~~~~~~~~~~~~~~~~

Внутренняя функция для автоматического определения и чтения формата.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_auto_detect_and_read.TestAutoDetectAndRead
   :members:
   :undoc-members:
   :show-inheritance:

_read_text_layout()
~~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения текстовой раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_read_text_layout.TestReadTextLayout
   :members:
   :undoc-members:
   :show-inheritance:

save_layout_to_file()
~~~~~~~~~~~~~~~~~~~~~

Функция для сохранения раскладки в файл.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_save_layout_to_file.TestSaveLayoutToFile
   :members:
   :undoc-members:
   :show-inheritance:

validate_layout()
~~~~~~~~~~~~~~~~~

Функция для валидации раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_validate_layout.TestValidateLayout
   :members:
   :undoc-members:
   :show-inheritance:

_read_csv_layout()
~~~~~~~~~~~~~~~~~~

Внутренняя функция для чтения CSV раскладки.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_read_csv_layout.TestReadCsvLayout
   :members:
   :undoc-members:
   :show-inheritance:

Тестируемые функции модуля read_files
-------------------------------------

get_words_from_file()
~~~~~~~~~~~~~~~~~~~~~

Функция для чтения слов из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_get_words_from_file.TestGetWordsFromFile
   :members:
   :undoc-members:
   :show-inheritance:

get_words_from_file_stream()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потокового чтения слов из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_get_words_from_file_stream.TestGetWordsFromFileStream
   :members:
   :undoc-members:
   :show-inheritance:

get_file_size_mb()
~~~~~~~~~~~~~~~~~~

Функция для получения размера файла в мегабайтах.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_get_file_size_mb.TestGetFileSizeMb
   :members:
   :undoc-members:
   :show-inheritance:

count_lines_in_file()
~~~~~~~~~~~~~~~~~~~~~

Функция для подсчета строк в файле.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_count_lines_in_file.TestCountLinesInFile
   :members:
   :undoc-members:
   :show-inheritance:

count_characters_in_file()
~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для подсчета символов в файле.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_count_characters_in_file.TestCountCharactersInFile
   :members:
   :undoc-members:
   :show-inheritance:

get_text_from_file()
~~~~~~~~~~~~~~~~~~~~

Функция для чтения текста из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_get_text_from_file.TestGetTextFromFile
   :members:
   :undoc-members:
   :show-inheritance:

get_text_from_file_stream()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Функция для потокового чтения текста из файла.

Тесты:
^^^^^^

.. autoclass:: tests_module.test_scan.test_get_text_from_file_stream.TestGetTextFromFileStream
   :members:
   :undoc-members:
   :show-inheritance:

test_imports
============

Тесты для проверки корректности импортов всех модулей проекта.

test_imports.py
---------------

.. automodule:: tests_module.test_imports
   :members:
   :undoc-members:
   :show-inheritance:

Индексирование
==============

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`