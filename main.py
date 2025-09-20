from database_module.db_init import init_tables, make_mok_data
from database_module.database import take_lk_from_db, take_all_data_from_lk
from scan_module.read_files import get_words_from_file
from processing_module.calculate_data import make_processing

def main():
    """

    """
    init_tables()
    make_mok_data("a", "testing_en")
    lk = take_lk_from_db("testing_en")
    print(lk)
    #take_all_data_from_lk()
    words = get_words_from_file("test_words.txt")
    print(words)
    result = make_processing(words, lk)
    print(result)

if __name__ == "__main__":
    main()
