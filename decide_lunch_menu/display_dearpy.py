import dearpygui.dearpygui as dpg  # ライブラリをdpgの名前でインポート
from DataBase import DataBase, operation_menu
import dearpygui.demo as demo
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
font_path = os.path.join(parent_dir, "NotoSerifJP-Black.otf")
image_path = os.path.join(current_dir, "cake.jpeg")
width, height, channels, texture_data = dpg.load_image(image_path)

dpg.create_context()
with dpg.texture_registry(show=False):
    texture_id = dpg.add_static_texture(width/2, height/2, texture_data)

with dpg.font_registry():
    with dpg.font(font_path, 20, default_font=True) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)

class display_menu:
    def __init__(self):
        self.operation  = operation_menu()
        with dpg.window(label="Menu", width=500) as main_window:
            # dpg.add_image(texture_id)

            button1 = dpg.add_button(label="店名の追加", callback=self.add_store_button_call_back)
            button2 = dpg.add_button(label="店名の変更", callback=self.change_store_name_call_back)
            button3 = dpg.add_button(label="店名の削除", callback=self.delete_store_name_call_back)
            button4 = dpg.add_button(label="店名の表示", callback=self.display_store_name_call_back)
            button5 = dpg.add_button(label="ルーレット", callback=self.roulette_call_back)
            button6 = dpg.add_button(label="終了", callback=self.exit_call_back, user_data=main_window)

    def add_store_button_call_back(self):
        with dpg.window(label="店名の追加", width=600, pos=[0, 0], height=500) as add_store_window:
            store_name = dpg.add_input_text(label="店名を入力してください")
            priority = dpg.add_input_text(label="優先度を入力してください")
            add_store_button = dpg.add_button(label="追加", callback=self.add_store_to_Database_call_back, user_data=(store_name, priority, add_store_window))

    def add_store_to_Database_call_back(self, sender, app_data, user_data):
        store_name = dpg.get_value(user_data[0])
        priority = dpg.get_value(user_data[1])
        store = DataBase(store_name, priority)
        store.add_data()
        print("データを追加しました")
        self.delete_window_call_back(sender, app_data, user_data = user_data[2])

    def change_store_name_call_back(self):
        with dpg.window(label="店名の変更", width=600, pos=[0, 0], height=500) as change_store_window:
            all_storage_store_name = self.operation.display_store_name()
            for i in range(len(all_storage_store_name)):
                dpg.add_text(all_storage_store_name[i])

            store_name = dpg.add_input_text(label="変更前の店名を入力してください")
            change_store_name = dpg.add_input_text(label="変更後の店名を入力してください")
            change_store_button = dpg.add_button(label="変更", callback=self.change_store_button_call_back, user_data=(store_name, change_store_name, all_storage_store_name, change_store_window))

    def change_store_button_call_back(self, sender, app_data, user_data):
        store_name = dpg.get_value(user_data[0])
        change_store_name = dpg.get_value(user_data[1])
        if store_name not in user_data[2]:
            print("入力された店名は存在しません")
        elif store_name == change_store_name:
            print("変更前の店名と変更後の店名が同じです")
        elif store_name == "" | change_store_name == "":
            print("店名が入力されていません")
        else:
            store = DataBase(store_name, change_store_name)
            store.change_data()
            print("店名を変更しました")
            self.delete_window_call_back(user_data[3])

    def delete_store_name_call_back(self):
        with dpg.window(label="店名の削除", width=600, pos=[0, 0], height=500) as delete_store_window:
            all_storage_store_name = self.operation.display_store_name()
            for i in range(len(all_storage_store_name)):
                dpg.add_text(all_storage_store_name[i])
            delete_store_name = dpg.add_input_text(label="削除する店名を入力してください")
            delete_store_button = dpg.add_button(label="削除")

            if dpg.is_item_clicked(delete_store_button):
                store_name = dpg.get_value(delete_store_name)
                if store_name not in all_storage_store_name:
                    print("入力された店名は存在しません")
                else:
                    store = DataBase(store_name)
                    store.delete_store_name()
                    print("データを削除しました")
                    self.delete_window_call_back(delete_store_window)

    def display_store_name_call_back(self):
        with dpg.window(label="店名の表示", width=600, pos=[0, 0], height=500) as display_store_window:
            all_storage_store_name = self.operation.display_store_name()
            for i in range(len(all_storage_store_name)):
                dpg.add_text(all_storage_store_name[i])

            exit_button = dpg.add_button(label="終了", callback=self.delete_window_call_back, user_data=display_store_window)

    def roulette_call_back(self):
        selected_store = self.operation.roulette()
        with dpg.window(label="ルーレット", width=600, pos=[0, 0], height=500) as roulette_window:
            dpg.add_text(selected_store)
            accept_button = dpg.add_button(label="OK", callback=self.delete_roulette_window_call_back, user_data=(selected_store, roulette_window))
            roulette_button = dpg.add_button(label="再抽選", callback=self.roulette_again_call_back, user_data=roulette_window)

    def roulette_again_call_back(self, sender=None, app_data=None, user_data=None):
        dpg.delete_item(user_data)
        self.roulette_call_back()


    def delete_roulette_window_call_back(self, sender, app_data, user_data):
        self.operation.change_priority(selected_store_name=user_data[0])
        dpg.delete_item(user_data[1])


    def delete_window_call_back(self, sender, app_data, user_data):
        dpg.delete_item(user_data)

    def exit_call_back(self):
        dpg.stop_dearpygui()

    



if __name__ == "__main__":
    display = display_menu()
    dpg.bind_font(default_font)

    dpg.create_viewport(title="Lunch Menu", width=920, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
