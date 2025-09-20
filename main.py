from database_module.db_init import init_tables, make_mok_data
from database_module.database import take_lk_from_db, take_all_data_from_lk, take_lk_names_from_lk
from scan_module.read_files import get_words_from_file
from processing_module.calculate_data import make_processing
from output_data.console_strings import *
from scan_module.read_layout import read_kl


def menu():
    pass
    flag1 = True
    flag2 = True

    while flag1:
        print(f"{rat_img_msg}")
        print(f"{choice_layout_msg}")
        print(f"{choice_exit_from_program}")

        try:
            choice = int(input("--> "))
            if choice == 0:
                flag1 = False
                break

            if choice == 1:
                while flag2:
                    try:
                        print(f"{choice_take_layout_from_file}")
                        print(f"{choice_take_layout_from_db}")
                        print(f"{choice_exit_from_program}")

                        choice = int(input("--> "))
                        if choice == 0:
                            flag1 = False
                            break

                        if choice == 1:
                            file_name = str(input(f"{file_name_to_read}"))
                            layout = read_kl(file_name)
                            if layout is None:
                                print(f"{error_take_layout}")
                                break
                            print("success to read file!")
                            #TODO: make it

                        if choice == 2:

                            all_lk_in_db = take_lk_names_from_lk()
                            if len(all_lk_in_db) >= 1:
                                for i in range(len(all_lk_in_db)):
                                    print(f"№{i+1} - {all_lk_in_db[i]}")
                                try:
                                    choice = int(input(f"{make_choice_lk}"))

                                except Exception:
                                    print(f"{error_input_data}")

                            else:
                                print("В базе данных сейчас нет доступных раскладок.")
                                flag2 = False
                                break


                    except ValueError:
                        print(f"{error_input_data}")

        except ValueError:
            print(f"{error_input_data}")



def main():
    """

    """
    init_tables()

    lk = take_lk_from_db("testing_en")
    print(lk)
    words = get_words_from_file("test_words.txt")
    print(words)
    result = make_processing(words, lk)
    print(result)

    menu()

if __name__ == "__main__":
    main()
