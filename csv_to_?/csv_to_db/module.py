import csv
import cx_Oracle

# parameter 설명
# csv_f: csv 파일 경로
# db_dir: oracle db client programm 경로
# db_id: oracle db username(id)
# db_pw: oracle db pw
# db_dsn: oracle db dsn
# table_name: oracle db에 생성할 table 이름

# 자동으로 table을 만드는 원리
# 첫 번째 row의 자료형을 바탕으로 attribute의 datatype이 결정됨
# 첫 번째 row의 첫 번째 항목은 primary key로 설정됨


def csv_to_db(csv_f, db_dir, db_id, db_pw, db_dsn, table_name):
    csv_list = []

    # csv 파일 읽기
    with open(csv_f, encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            for i in range(0, len(row)-1):
                # row[1~3]에 있는 " ' 제거
                row[i+1] = row[i+1].replace('"', '').replace("'", '')
            csv_list.append(row)

    # oracle db 연결
    cx_Oracle.init_oracle_client(
        lib_dir=db_dir)
    with cx_Oracle.connect(user=db_id, password=db_pw, dsn=db_dsn) as conect:
        cursor = conect.cursor()

        # oracle db에 column 생성 query 실행
        # column의 datatype은 csv 파일의 첫번째 row의 datatype을 따름
        header_list = []
        for i in range(0, len(csv_list[0])):
            elem = csv_list[0][i]
            if elem.isdigit():
                header_list.append([header[i], 'NUMBER(30)'])
            else:
                header_list.append([header[i], 'VARCHAR2(255)'])

        # oracle db에 column(attribute) 생성 query 실행
        attr_txt = []
        for i in range(1, len(header_list)):
            attr_txt.append('{} {}'.format(
                header_list[i][0], header_list[i][1]))
        attr_txt = ', '.join(attr_txt) + ')'
        cursor.execute("""CREATE TABLE {} ({} {} PRIMARY KEY, """.format(
            table_name, header_list[0][0], header_list[0][1]) + attr_txt)

        conect.commit()

        # oracle db에 row(data) 생성 query 실행
        for row in csv_list:
            print('% :', row[0], '/', len(csv_list))

            data_txt = []
            for i in range(0, len(row)):
                if row[i].isdigit():
                    data_txt.append(row[i])
                else:
                    data_txt.append("'{}'".format(row[i]))
            data_txt = ', '.join(data_txt)
            cursor.execute("""
                                INSERT INTO {}
                                VALUES
                                ({})
            """.format(table_name, data_txt))

        conect.commit()
