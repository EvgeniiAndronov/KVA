#!/usr/bin/env python3
"""
Тестовый скрипт для проверки импортов
"""

try:
    print("Тестируем импорты...")
    
    from database_module.db_init import init_tables, make_mok_data
    print("✅ database_module.db_init - OK")
    
    from database_module.database import (
        take_lk_from_db, 
        take_all_data_from_lk, 
        take_lk_names_from_lk,
        save_analysis_result,
        get_analysis_history,
        get_analysis_statistics
    )
    print("✅ database_module.database - OK")
    
    from scan_module.read_files import (
        get_words_from_file, 
        get_words_from_file_stream, 
        get_text_from_file,
        get_text_from_file_stream,
        get_file_size_mb,
        count_lines_in_file,
        count_characters_in_file
    )
    print("✅ scan_module.read_files - OK")
    
    from processing_module.calculate_data import (
        make_processing, 
        make_processing_stream,
        make_text_processing,
        make_text_processing_stream,
        validate_rules
    )
    print("✅ processing_module.calculate_data - OK")
    
    from data_module.make_export_file import create_csv_report, export_unknown_characters_csv
    print("✅ data_module.make_export_file - OK")
    
    from data_module.make_export_plot import (
        create_analysis_charts, 
        create_history_comparison_chart, 
        create_layouts_comparison_chart
    )
    print("✅ data_module.make_export_plot - OK")
    
    from output_data.console_strings import rat_img_msg, error_input_data
    print("✅ output_data.console_strings - OK")
    
    from scan_module.read_layout import read_kl, validate_layout, save_layout_to_file
    print("✅ scan_module.read_layout - OK")
    
    print("\n🎉 Все импорты успешны!")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
except Exception as e:
    print(f"❌ Неожиданная ошибка: {e}")