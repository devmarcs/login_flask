from.entities.User import User



class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, password, fullname FROM user WHERE email = '{}'".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT id, email, fullname FROM user WHERE id = {id}"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                 return User(row[0], row[1], None, row[2]) 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)