from output_data.console_strings import *
from scan_module.read_layout import *
from database_module.database import *

def menue() -> None:
    """
    Метод реализует логику сценария, через использование меню.
    """
    print(f"{rat_img_msg}")
    flag = True
    while flag:
        print(choice_layout_msg)
        print(choice_exit_from_program)
        
        choice_data = -10
        
        try:
            choice_data = int(input("--> "))
        except:
            print(error_input_data)
            continue
        
        if choice_data == 0:
            break
        elif choice_data == 1:
            choice_layout_keyboard()
        else: print(error_input_data); continue

def choice_layout_keyboard() -> None:
    """
    Метод реализует выбор раскладки из базы или из файла.
    """
    flag_layout = True
    while flag_layout:
        print(choice_take_layout_from_file)
        print(choice_take_layout_from_db)
        print(choice_exit_from_program)
    
    choice_data = -10

    try:
        choice_data = int(input("--> "))
    except:
        print(error_input_data)
        continue

    if choice_data == 0:
        break
    elif choice_data == 1:
        read_layout()
    elif choice_data == 2:
        take_lk_from_db()
    else: print(error_input_data); continue

def main() -> None:
    menue()


if __name__ == "__main__":
    main()
