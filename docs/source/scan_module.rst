Модуль сканирования (scan_module)
=================================

Модуль для чтения файлов, раскладок клавиатуры и работы с различными форматами данных.

.. automodule:: scan_module
   :members:
   :undoc-members:
   :show-inheritance:

Подмодули
---------

read_files
~~~~~~~~~~

Модуль для чтения файлов различных типов с поддержкой потоковой обработки.

.. automodule:: scan_module.read_files
   :members:
   :undoc-members:
   :show-inheritance:

Функции чтения слов
^^^^^^^^^^^^^^^^^^^

.. autofunction:: scan_module.read_files.get_words_from_file
.. autofunction:: scan_module.read_files.get_words_from_file_stream

Функции чтения текста
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: scan_module.read_files.get_text_from_file
.. autofunction:: scan_module.read_files.get_text_from_file_stream

Вспомогательные функции
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: scan_module.read_files.get_file_size_mb
.. autofunction:: scan_module.read_files.count_lines_in_file
.. autofunction:: scan_module.read_files.count_characters_in_file

read_layout
~~~~~~~~~~~

Модуль для работы с раскладками клавиатуры в различных форматах.

.. automodule:: scan_module.read_layout
   :members:
   :undoc-members:
   :show-inheritance:

Основные функции
^^^^^^^^^^^^^^^^

.. autofunction:: scan_module.read_layout.read_kl
.. autofunction:: scan_module.read_layout.save_layout_to_file
.. autofunction:: scan_module.read_layout.validate_layout

Функции чтения форматов
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: scan_module.read_layout._read_json_layout
.. autofunction:: scan_module.read_layout._read_csv_layout
.. autofunction:: scan_module.read_layout._read_text_layout
.. autofunction:: scan_module.read_layout._read_xml_layout

Вспомогательные функции
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: scan_module.read_layout._auto_detect_and_read
.. autofunction:: scan_module.read_layout._extract_layout_from_dict
.. autofunction:: scan_module.read_layout._is_numeric