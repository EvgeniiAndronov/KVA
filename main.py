from database_module.db_init import init_tables, make_mok_data
from database_module.database import take_lk_from_db, take_all_data_from_lk

def main():
    """

    """
    init_tables()
#    make_mok_data()
    lk = take_lk_from_db("test")
    #take_all_data_from_lk()



if __name__ == "__main__":
    main()
