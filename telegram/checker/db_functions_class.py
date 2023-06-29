import sqlite3

class DbFunctions:
    
    @staticmethod
    def connect_to_database(database_name):
        connection = sqlite3.connect(database_name)
        return connection

    #save message to db
    @staticmethod
    def save_message(config_values, message_text, user_id, message_id, chat_id):
        table_prefix_msg = config_values['table_prefix_msg']
        connection = config_values['connection']

        query = f'CREATE TABLE IF NOT EXISTS "{table_prefix_msg}{chat_id}" \
                (message_id INTEGER PRIMARY KEY, user_id INTEGER, message_text TEXT, deleted INTEGER)'
        connection.execute(query)
        connection.commit()
        
        #we don't save message text
        data = (message_id, user_id, "", 0)
        query = f'REPLACE INTO "{table_prefix_msg}{chat_id}" (message_id, user_id, message_text, deleted) VALUES (?, ?, ?, ?)'
        connection.execute(query, data)
        connection.commit()

        return True

    #work with user. we have one table usr_main for all chats
    @staticmethod
    def save_user(config_values, message_text, user_id, message_id, chat_id):
        table_prefix_user = config_values['table_prefix_user']
        connection = config_values['connection']
        #create table if not exists (quick operation)
        query = f'CREATE TABLE IF NOT EXISTS "{table_prefix_user}_main" \
                (user_id INTEGER PRIMARY KEY, message_hash TEXT, human INTEGER, messages_count INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
        connection.execute(query)
        connection.commit()
        
        #check user. TODO: rewrite sql (update) and think about the logic
        query = f'SELECT * FROM "{table_prefix_user}_main" where  user_id = {user_id}'
        result = connection.execute(query)
        existing_user = result.fetchone()
        if existing_user:
            user_id = existing_user['user_id']
            messages_count = existing_user['messages_count'] + 1
            human = existing_user['human']
            if messages_count < 20:
                message_hash = existing_user['message_hash'] + "," + hash(message_text[:1000])
            else:
                human = 1
            
            data = (user_id, message_hash, human, messages_count,)
            query = f'REPLACE INTO "{table_prefix_user}_main" (user_id, message_hash, human, messages_count) VALUES (?, ?, ?, ?)'
            connection.execute(query, data)
            connection.commit()                        
        else: 
            #new user: messages count = 0, human = 0
            data = (user_id, hash(message_text[:1000]), 0,0,)
            query = f'REPLACE INTO "{table_prefix_user}_main" (user_id, message_hash, human, messages_count) VALUES (?, ?, ?, ?)'
            connection.execute(query, data)
            connection.commit()

        return True
        
    @staticmethod
    def is_human(config_values, user_id):
        table_prefix_user = config_values['table_prefix_user']
        connection = config_values['connection']

        query = f'CREATE TABLE IF NOT EXISTS "{table_prefix_user}_main" \
                (user_id INTEGER PRIMARY KEY, message_hash TEXT, human INTEGER, messages_count INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
        connection.execute(query)
        connection.commit()
        
        data = (user_id, 1)
        query = f'SELECT * FROM "{table_prefix_user}_main" where  user_id = ? and human = ?'
        result = connection.execute(query, data)
        existing_user = result.fetchone()
        if existing_user:
            return True
        return False

    #check against duplicate messages
    @staticmethod
    def duplicate_messages(config_values, user_id, message_text):
        table_prefix_user = config_values['table_prefix_user']
        connection = config_values['connection']
        
        data = (user_id,)
        query = f'SELECT * FROM "{table_prefix_user}_main" where  user_id = ?'
        result = connection.execute(query, data)
        existing_user = result.fetchone()
        if existing_user:
            message_hash = existing_user['message_hash']
            if hash(message_text[:1000]) in message_hash:
                return True
        return False








