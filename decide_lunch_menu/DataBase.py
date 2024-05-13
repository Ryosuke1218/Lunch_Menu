import sqlalchemy
from sqlalchemy import Column, Integer, select, String, desc
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import numpy as np
import os

engine = sqlalchemy.create_engine('sqlite:///Lunch_Menu.sqlite', echo=False)   # エンジン作成
Base = declarative_base()   # ベース作成
Session = scoped_session(sessionmaker(autoflush=False, bind=engine))   # セッション作成


class DataBase(Base):
    __tablename__ = 'Lunch_Menu'  # テーブル名
    id = Column("id", Integer, primary_key=True)    # id
    store_name = Column("Store_Name", String)    # 店の名前
    priority = Column("Priority", Integer)   # 優先度


    def __init__(self, store_name=None, priority=None):
        self.store_name = store_name
        self.priority = priority

    def check_database_exists(self, db_path):
        return os.path.exists(db_path)

    def add_data(self):  # データベースに追加
        if self.check_database_exists("Lunch_Menu.sqlite"):
            if self.get_index(self.store_name) is not None:
                print("既に登録されています")
                return
            elif self.store_name is None:
                print("店名が入力されていません")
                return
        new_entry = DataBase(store_name=self.store_name, priority=self.priority)
        Session.add(new_entry)   # データベースに追加
        Session.commit()    # データベースにコミット
        # Session.close()

    def get(self, index: int):   # データベースからデータを取得
        action_info: list = []

        # with Session() as session:
        #     with session.begin():
        stmt = select(DataBase).where(DataBase.id == index)
        name = Session.execute(stmt)
        row = name.fetchone()
        if row is not None:
            action_info = row[0].store_name
            # action_info.append(row[0].priority)
        else:
            print("データが存在しません")
            action_info = None
        return action_info

    def get_index(self, store_name: str):   # データベースからデータを取得
        lunch = Session.query(DataBase).filter(DataBase.store_name == store_name).first()
        if lunch is not None:
            id = lunch.id
        else:
            id = None
        return id

    def delete(self, index: int):   # データベースからデータを削除
        Session.query(DataBase).filter(DataBase.id == index).delete()
        Session.commit()

    def delete_store_name(self, delete_store_name):
        Session.query(DataBase).filter(DataBase.store_name == delete_store_name).delete()
        Session.commit()
        # session.close()

    def get_priority(self, index: int):   # データベースからデータを取得
        database = Session.query(DataBase).filter(DataBase.id == index).first()
        if database is not None:
            priority = database.priority
        else:
            priority = None
        # session.close()
        return priority
    
    def change_store_name(self, index: int, store_name: str):
        Session.query(DataBase).filter(DataBase.id == index).update({DataBase.store_name: store_name})
        Session.commit()
        # session.close()

    def get_last_id(self):
        last_store_id = Session.query(DataBase).order_by(desc(DataBase.id)).first()
        if last_store_id is not None:
            last_id = last_store_id.id
        else:
            last_id = None
        # session.close()
        return last_id
    
    def get_all_priority(self):
        stmt = select(DataBase.priority)
        result = Session.execute(stmt)
        priority_list = [row[0] for row in result]
        return priority_list
    
    def get_all_store_name(self):
        stmt = select(DataBase.store_name)
        result = Session.execute(stmt)
        store_name_list = [row[0] for row in result]
        return store_name_list
    
    def change_priority(self, selected_store_name):
        selected_index = self.get_index(selected_store_name)
        next_priority = self.get_priority(selected_index) - 1
        if current_priority == 1:
            Session.query(DataBase).filter(DataBase.store_name == selected_store_name).update({DataBase.priority: 5})
            Session.commit()
        else:
            Session.query(DataBase).filter(DataBase.store_name == selected_store_name).update({DataBase.priority: next_priority})
            Session.commit()


class operation_menu:
    def __init__(self):
        pass
        # self.display_menu()

    def display_menu(self):
        while True:
            print("以下から選択してください")
            print("1: 店名の追加")
            print("2: 店名の変更")
            print("3: 店名の削除")
            print("4: 店名の表示")
            print("5: ルーレット")
            print("6: 終了")
            print("入力:", end="")
            selection = input()

            if selection == "1":
                self.add_store_name()
            elif selection == "2":
                self.change_name()
            elif selection == "3":
                self.delete_store()
            elif selection == "4":
                self.display_store_name()
            elif selection == "5":
                self.roulette()
            elif selection == "6":
                break


    def add_store_name(self):
        while True:
            print("店名を入力してください")
            store_name = input()
            print("優先度を入力してください")
            priority = int(input())
            store = DataBase(store_name, priority)
            store.add_data()
            print("データを追加しました")

            while True:
                print("データ追加を続けますか？(y/n)")
                answer = input()
                if answer in ["y", "n"]:
                    break
                else:
                    print("無効な入力です。'y' または 'n' を入力してください。")

            if answer == "n":
                break

    def change_name(self):
        self.display_store_name()
        print("変更する店名のIDを入力してください")
        store_id = input()
        print("変更後の店名を入力してください")
        store_name = input()
        store = DataBase(store_name, 5)
        store.change_store_name(store_id, store_name)
        print("店名を変更しました")

    def delete_store(self):
        print("削除する店名のIDを入力してください")
        self.display_store_name()
        store_id = input()
        store = DataBase()
        store.delete_store_name(store_id)
        print("店名を削除しました")

    def display_store_name(self):
        store = DataBase()
        # print("--------------------")
        store_name = store.get_all_store_name()
        # for i in range(len(store_name)):
        #     print(f"{i+1}: {store_name[i]}")
        # print("--------------------")
        return store_name

    def roulette(self):
        store = DataBase()
        priority_list = store.get_all_priority()

        index_list = list(range(len(priority_list)))
        total_priority = sum(priority for priority in priority_list)
        probabilities = [priority / total_priority for priority in priority_list]
        selected_index = np.random.choice(index_list, p=probabilities)
        selected_store_id = int(selected_index+1)
        print(selected_store_id)

        selected_store = store.get(selected_store_id)
        return selected_store
    
    def change_priority(self, selected_store_name):
        store = DataBase()
        store.change_priority(selected_store_name)


Base.metadata.create_all(engine)
if __name__ == "__main__":
    menu = operation_menu()
