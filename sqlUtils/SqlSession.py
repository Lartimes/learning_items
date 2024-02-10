import pymysql
from  PropertiesUtils.ResourceBundle import ResourceBundle as resource_bundle

class SqlSession:
    # username password database host
    properties = resource_bundle.get_bundle()
    username = properties['mysql']['username']
    password = properties['mysql']['password']
    database = properties['mysql']['database']
    host = properties['mysql']['host']

    @classmethod
    def del_by_stu_id(cls, stu_id):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"delete from student where id = {stu_id}"
            cursor.execute(sql)
            conn.commit()
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_stu_id(cls, name, college):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"insert into student (name , college) values ('{name}','{college}')"
            cursor.execute(sql)
            conn.commit()
            return int(cursor.lastrowid)
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_class_id(cls, class_name):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""SELECT id  from class where class_name = '{class_name}'"""
            cursor.execute(sql)
            ret = cursor.fetchone()
            return int(ret[0])
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def add_stu(cls, name="", class_name="", college=""):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            class_id = SqlSession.get_class_id(class_name)
            print(class_id)
            pri_key = SqlSession.get_stu_id(name, college)
            sql = f"insert into student_class_rela values(NUll, {pri_key} , {class_id} ) "
            print(sql)
            cursor.execute(sql)
            conn.commit()
            return pri_key
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_score(cls, name="lartimes2099", page=1, page_size=8):  # TODO pagesize 分页查询
        cursor = None
        conn = None
        try:
            start_index = (page - 1) * page_size;
            limit = f"limit {start_index} , {page_size}"
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
                    SELECT  DISTINCT stu_name , cl.class_name  as class_name 
                    , college , sum_score  , tmp.stu_id 
            FROM  (SELECT 
                        s.id  as stu_id , s.`name` as stu_name , s.college
                            as college , SUM(sc.score) as sum_score 
			        FROM 
				        student s LEFT JOIN score sc on sc.stu_id = s.id    
				    GROUP BY s.id)
            tmp 
			join  student_class_rela re on tmp.stu_id = re.stu_id 
            join class cl  on cl.id = re.class_id
            ORDER BY tmp.sum_score DESC {limit}
                    """
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_conn(cls, host=host, user=username,
                 password=password,
                 database=database,
                 port=3306):
        return pymysql.connect(host=host,
                               user=user,
                               password=password,
                               database=database,
                               port=port)

    @classmethod
    def get_auth(cls, role_id=1):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
                             SELECT  a.acl_value
                            FROM role_auth_rela ra 
                            JOIN    auth a
                            on ra.role_id = {role_id} and a.id = ra.auth_id
                            """
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def login(cls, username="lartimes", password="2004"):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
                      SELECT u.username ,r.role_name , r.id 
                    FROM 
                        user u 
                    inner JOIN 
                        user_role_rela ur
                    on u.username = '{username}' and u.password = '{password}' 
                    and u.id = ur.user_id
                    join 
                     role r
                    on r.id = ur.role_id and r.is_valid = '1'
                    order by  r.role_level desc
                    """
            print("login:" + sql)
            cursor.execute(sql)
            data = cursor.fetchone()
            return data
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def update_stu(cls, stu_id, name, class_name, college):
        cursor = None
        conn = None
        try:
            new_cls_id = SqlSession.get_class_id(class_name)
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"select class_id from  student_class_rela where stu_id = {stu_id}"
            cursor.execute(sql)
            cls_id = int(cursor.fetchone()[0])
            sql1 = f"""
                update student set name = '{name}' , college = '{college}' where id = {stu_id} ;
                """
            SqlSession.modify_stu(sql1);
            sql2 = f"""
                update student_class_rela set class_id = {new_cls_id} where  class_id = {cls_id};
                """
            cursor.execute(sql2)
            conn.commit()
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def modify_stu(cls, sql):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except:
            if conn is not None:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def check_score(cls, stu_id=1):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
            SELECT  s.name ,s.id , cr.` name` , sc.score
            FROM  student s  join  score sc 
            on s.id = {stu_id} and sc.stu_id = s.id
            join 	course cr
            on cr.id  = sc.course_id 
            ORDER BY sc.score ASC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except:
            if conn is not None:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def select_like(cls, name, class_name, college):
        cursor = None
        conn = None
        name_sql = ""
        college_sql = ""
        class_sql = ""
        if not name_sql:
            name_sql = f"and   s.`name` like '%{name}%' "
        if not class_sql:
            print("class_sql =================")
            class_sql = f"and  c.class_name like '%{class_name}%'"
        if not college_sql:
            college_sql = f"and s.college like '%{college}%' "

        #   and   s.`name` like '%{name}%'
        # 	    and s.college like '%{college}%'
        # 	    and  c.class_name like '%{class_name}%'
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
        select s.name as stu_name  , 
        c.class_name as class_name ,
        s.college as college_name ,
        sum(sr.score)  as sum_score ,
        s.id as stu_id  
        FROM  student s
        JOIN	class c
	    on 1 = 1
	    {name_sql} {college_sql} {class_sql}
        JOIN score  sr	 
        on  sr.stu_id = s.id 
        GROUP BY s.id , c.class_name
        limit 0 , 8
              """
            cursor.execute(sql)
            return cursor.fetchall()
        except:
            if conn is not None:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def export_all(cls):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = """  select  s.name as stu_name  , 
                    s.college as college_name ,
                  c.class_name as class_name ,
                  sr.score  as score,
                    cr.` name` as course_name 
                FROM  student s
                 JOIN   student_class_rela sc on sc.stu_id = s.id
                 JOIN  class c ON sc.class_id = c.id 
                 join  score sr on s.id = sr.stu_id 
                 join  course cr on cr.id = sr.course_id 
                 order by  s.name , course_name ASC"""
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result
        except:
            if conn is not None:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_course_id(cls, list_course: list):  # list(course)
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            temp = "("
            for e in list_course:
                temp += '\''
                temp += e
                temp += '\''
                temp += ","
            temp = temp[:-1]
            temp += ")"
            sql = f""" SELECT * FROM course  where ` name` in {temp} """
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result
        except:
            if conn is not None:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def insert_score_by_id(cls, stu_id: int, cr_id: int, score):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""insert into score values (NULL , {stu_id} , {cr_id}  , {score})"""
            cursor.execute(sql)
            conn.commit()
        except:
            if conn is not None:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()

    #  # user , file_name , obj_name
    @classmethod
    def insert_file_obj(cls, user: str, file_name: str, obj_name: str):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
            insert into oss_path_obj values (NULL , '{user}' , '{file_name}'  , '{obj_name}' )
            """
            cursor.execute(sql)
            conn.commit()
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_obj_path(cls, user: str, file_name: str):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
              select obj_name from oss_path_obj where username  = '{user}' 
              and file_name = '{file_name}'
               """
            cursor.execute(sql)
            conn.commit()
            return cursor.fetchone()[0]
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_stu_count(cls):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
               select count(*) from student 
                 """
            cursor.execute(sql)
            return cursor.fetchone()[0]
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_oss_files(cls , username:str="lartimes"):
        cursor = None
        conn = None
        try:
            conn = SqlSession.get_conn()
            cursor = conn.cursor()
            sql = f"""
                   select  file_name , obj_name  from oss_path_obj 
                   where  username = '{username}'
                     """
            cursor.execute(sql)
            return cursor.fetchall()
        except:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()


