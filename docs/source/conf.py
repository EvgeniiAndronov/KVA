# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Добавляем пути к проекту для корректного импорта модулей
sys.path.insert(0, os.path.abspath('../..'))  # путь к корню проекта
sys.path.insert(0, os.path.abspath('../../tests_module'))  # путь к тестам

project = 'kla'
copyright = '2025, diana'
author = 'diana'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
]

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True,
    'private-members': False,
}

# Автоматическое создание summary
autosummary_generate = True
autosummary_imported_members = True

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_preprocess_types = True

# Настройки для обработки аннотаций типов
napoleon_attr_annotations = True

# Пути к шаблонам
templates_path = ['_templates']

# Исключаемые шаблоны
exclude_patterns = []

# Язык документации
language = 'ru'

# Кодировка
source_encoding = 'utf-8'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# Пути к статическим файлам
html_static_path = ['_static']

# Настройки темы
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'display_version': False,
    'style_external_links': True,
}

# Фавикон
html_favicon = None

# Заголовок документации
html_title = "KLA Project Documentation"
html_short_title = "KLA Docs"

# Базовый URL
html_baseurl = ''

# Дополнительные CSS файлы
html_css_files = [
    'custom.css',
]

# Дополнительные JS файлы
html_js_files = []

# -- Options for internationalization ----------------------------------------
locale_dirs = ['locale/']  # путь к файлам перевода
gettext_compact = False     # отдельные файлы для каждого языка

# -- Options for extensions --------------------------------------------------

# Настройки подсветки синтаксиса
pygments_style = 'sphinx'
highlight_language = 'python3'

# Настройки todo
todo_include_todos = True
todo_emit_warnings = False

# Настройки coverage
coverage_show_missing_items = True

# -- Autodoc дополнительные настройки ----------------------------------------

# Автоматическое документирование всех членов
autoclass_content = 'both'  # показывать и класс, и __init__ docstring

# Показывать аннотации типов в сигнатурах
autodoc_typehints = 'description'

# Формат аннотаций типов
autodoc_typehints_format = 'short'

# Уровень детализации для аннотаций типов
autodoc_typehints_description_target = 'all'

# -- Дополнительные настройки для улучшения документации ---------------------

# Включить индексы
html_use_index = True
html_domain_indices = True

# Настройки для лучшего отображения исходного кода
viewcode_follow_imported_members = True
viewcode_line_numbers = True

# -- Настройки для обработки unittest тестов ---------------------------------

# Игнорировать определенные предупреждения
suppress_warnings = [
    'autodoc.import_object'
]

# -- Кастомные настройки для вашего проекта ----------------------------------

# Добавляем пути ко всем модулям проекта
project_modules = [
    'data_module',
    'database_module', 
    'processing_module',
    'scan_module',
    'output_data',
    'tests_module'
]

for module in project_modules:
    module_path = os.path.abspath(os.path.join('../..', module))
    if os.path.exists(module_path):
        sys.path.insert(0, module_path)

# -- Final setup -------------------------------------------------------------

def setup(app):
    """Дополнительная настройка при инициализации Sphinx"""
    # Здесь можно добавить кастомные CSS или JS
    pass