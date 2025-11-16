import sqlite3
from GISTOGR import plot_finger_usage_7_layouts_only_with_fines

def make_mok():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
            """INSERT INTO data_to_diograms 
            (name_lk, 
        count_errors,
        count_tap_bl, 
        count_tap_bl_e, 
        count_tap_bp, 
        count_tap_bp_e, 
        count_tap_ly,
        count_tap_ly_e,
        count_tap_py,
        count_tap_py_e,
        count_tap_ls,
        count_tap_ls_e,
        count_tap_ps,
        count_tap_ps_e,
        count_tap_lb,
        count_tap_lb_e,
        count_tap_pb,
        count_tap_pb_e,
        count_tap_lm,
        count_tap_lm_e,
        count_tap_pm,
        count_tap_pm_e
            ) 
            VALUES (?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("test6", 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1)
        )
        

    data = cursor.fetchall()
    
    conn.commit()
    conn.close()

# make_mok()

def get_data_to_result_dioram() -> list:
    """

    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * from data_to_diograms")

    data = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    return data

def make_buty_data():
    data = get_data_to_result_dioram()
    print(data)
    result = {}
    for d in data:
        if not d[1] in result:
            result[d[1]] = [d[i] for i in range(2, len(d))]
        else:
            for o in range(len(result[d[1]])):
                result[d[1]][o] += d[o + 2] 

    print(result)
    
    keys = []
    fingers_tap = []
    errors_finger = []
    
    for key, value in result.items():
        keys.append(key)
        mid = []
        mid.append(value[1])
        mid.append(value[3])
        mid.append(value[5])
        mid.append(value[7])
        mid.append(value[9])
        mid.append(value[11])
        mid.append(value[13])
        mid.append(value[15])
        mid.append(value[17])
        mid.append(value[19])

        er = []
        er.append(value[2])
        er.append(value[4])
        er.append(value[6])
        er.append(value[8])
        er.append(value[10])
        er.append(value[12])
        er.append(value[14])
        er.append(value[16])
        er.append(value[18])
        er.append(value[20])

        fingers_tap.append(mid)
        errors_finger.append(er)

    print(fingers_tap, "\n", errors_finger, "\n", keys)

    plot_finger_usage_7_layouts_only_with_fines(
        fingers_tap[0], errors_finger[0], 
        fingers_tap[1], errors_finger[1], 
        fingers_tap[2], errors_finger[2], 
        fingers_tap[3], errors_finger[3], 
        fingers_tap[4], errors_finger[4], 
        fingers_tap[5], errors_finger[5], 
        fingers_tap[6], errors_finger[6],
        )


make_buty_data()