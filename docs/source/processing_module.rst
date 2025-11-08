Модуль обработки (processing_module)
====================================

Модуль для анализа текстов и подсчета ошибок на основе правил раскладки с поддержкой статистики пальцев.

.. automodule:: processing_module
   :members:
   :undoc-members:
   :show-inheritance:

Подмодули
---------

calculate_data
~~~~~~~~~~~~~~

Модуль для расчета ошибок и сбора статистики.

.. automodule:: processing_module.calculate_data
   :members:
   :undoc-members:
   :show-inheritance:

Функции обработки слов
^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: processing_module.calculate_data.make_processing
.. autofunction:: processing_module.calculate_data.make_processing_stream

Функции обработки текста
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: processing_module.calculate_data.make_text_processing
.. autofunction:: processing_module.calculate_data.make_text_processing_stream

Вспомогательные функции
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: processing_module.calculate_data.validate_rules