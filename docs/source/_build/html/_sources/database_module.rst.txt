Модуль базы данных (database_module)
====================================

Модуль для работы с базой данных SQLite, хранения раскладок и результатов анализа.

.. automodule:: database_module
   :members:
   :undoc-members:
   :show-inheritance:

Подмодули
---------

database
~~~~~~~~

.. automodule:: database_module.database
   :members:
   :undoc-members:
   :show-inheritance:

Функции работы с раскладками
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: database_module.database.take_lk_from_db
.. autofunction:: database_module.database.take_all_data_from_lk
.. autofunction:: database_module.database.take_lk_names_from_lk

Функции работы с результатами анализа
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: database_module.database.save_analysis_result
.. autofunction:: database_module.database.get_analysis_history
.. autofunction:: database_module.database.get_analysis_statistics
.. autofunction:: database_module.database.delete_analysis_result

db_init
~~~~~~~

.. automodule:: database_module.db_init
   :members:
   :undoc-members:
   :show-inheritance: