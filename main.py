from distutils.log import Log
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
from kivy.app import App
from numpy import roots
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
import kivy 
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.graphics import *
from databaseops import *
from functools import partial 
from kivy.clock import Clock
from datetime import date
from datetime import datetime
from datetime import timedelta
from kivy.uix.popup import Popup
from kivy.lang import Builder
from habit import Habit
kivy.require('1.0.0')

Builder.load_string("""
<Login>:

<DailyHab>:
    GridLayout:
        id: grid1

<QuittingHab>:
    GridLayout:
        id: grid2
 
 
""")


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        login_layout = GridLayout(cols=2, padding = [50,50,50,50])
        Login.inp_login = TextInput(hint_text="Enter username", multiline=False, write_tab=False, on_text_validate = partial(self.run_login))
        login_btn = Button(text = "Login", on_release=partial(self.run_login))#, on_press=partial(self.build_tasks, "continue"))
        login_layout.add_widget(Login.inp_login)
        login_layout.add_widget(login_btn)
        self.add_widget(login_layout)

    def run_login(self, obj):
        run_build_task = partial(Login.build_tasks, Login, "continue", 0)
        run_build_task()
        self.manager.transition.direction = "left"
        self.manager.current = "daily_hab"

    def build_tasks(self, category, obj):
        Login.db_name = Login.inp_login.text + ".db"
        Login.connection = create_connection(Login.db_name)
        create_habit_table(Login.connection)
        allHabits = get_all_habits(Login.connection, Login.db_name[:-3], category)

        j=0

        if category == "continue":
            habType = DailyHab
            var_edit_popup = DailyHab.delete_task_popup
            var_name_labels = DailyHab.habit_name_labels
            var_count_labels = DailyHab.habit_count_labels
            var_green_btn = DailyHab.check_yes_buttons
            var_green_btn_fn = DailyHab.count_up_new
            var_red_btn = DailyHab.check_no_buttons
            var_red_btn_fn = DailyHab.count_down_new
            var_task_layouts = DailyHab.tasklayouts
            while j in range(len(var_task_layouts)):
                ScnMgrApp.root.get_screen("daily_hab").ids.grid1.remove_widget(var_task_layouts[j])
                ScnMgrApp.root.get_screen("daily_hab").ids.grid1.remove_widget(var_name_labels[j])
                ScnMgrApp.root.get_screen("daily_hab").ids.grid1.remove_widget(var_count_labels[j])
                ScnMgrApp.root.get_screen("daily_hab").ids.grid1.remove_widget(var_green_btn[j])
                ScnMgrApp.root.get_screen("daily_hab").ids.grid1.remove_widget(var_red_btn[j])
                j = j + 1
            # clear the lists to rewrite 
            var_name_labels *= 0 
            var_count_labels *= 0 
            var_green_btn *= 0 
            var_red_btn *= 0 
            var_task_layouts *= 0
        elif category == "quit":
            habType = QuittingHab
            var_edit_popup = QuittingHab.edit_quit_task_popup
            var_name_labels = QuittingHab.quit_habit_name_labels
            var_count_labels = QuittingHab.quit_habit_count_labels
            var_green_btn = QuittingHab.quit_max_streak_labels
            var_green_btn_fn = QuittingHab.edit_quit_task_popup
            var_red_btn = QuittingHab.quit_check_no_buttons
            var_red_btn_fn = QuittingHab.count_down_quit
            var_task_layouts = QuittingHab.quit_tasklayouts
            while j in range(len(var_task_layouts)):
                ScnMgrApp.root.get_screen("quitting_hab").ids.grid2.remove_widget(var_task_layouts[j])
                ScnMgrApp.root.get_screen("quitting_hab").ids.grid2.remove_widget(var_name_labels[j])
                ScnMgrApp.root.get_screen("quitting_hab").ids.grid2.remove_widget(var_count_labels[j])
                ScnMgrApp.root.get_screen("quitting_hab").ids.grid2.remove_widget(var_green_btn[j])
                ScnMgrApp.root.get_screen("quitting_hab").ids.grid2.remove_widget(var_red_btn[j])
                j = j + 1
            # clear the lists to rewrite 
            var_name_labels *= 0 
            var_count_labels *= 0 
            var_green_btn *= 0 
            var_red_btn *= 0 
            var_task_layouts *= 0

        for i in range(len(allHabits)):
                        
            if (i%2==0):
                var_name_labels.append(Button(
                    text=str(allHabits[i][2]),  
                    # disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5], #))
                    on_press = partial(var_edit_popup, habType, i)))
                
                var_count_labels.append(Button(
                    text=str(allHabits[i][3]),  
                    disabled=True, 
                    background_disabled_normal='atlas://data/images/defaulttheme/button', 
                    background_color=[52/255, 110/255, 235/255, 0.5]))

            else:
                var_name_labels.append(Button(
                    text=str(allHabits[i][2]),  
                    # disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 1],#))
                    on_press = partial(var_edit_popup, habType, i)))
                
                var_count_labels.append(Button(
                    text=str(allHabits[i][3]),  
                    disabled=True, 
                    background_disabled_normal='atlas://data/images/defaulttheme/button', 
                    background_color=[52/255, 110/255, 235/255, 1]))

            last_mod_date = allHabits[0][5]
            hab_category = allHabits[0][1]
            today = str(date.today())

            if hab_category == "continue":
                var_green_btn.append(Button(text = "Did it!", on_press = partial(var_green_btn_fn, DailyHab, Login.connection, i), background_color = [169/255,255/255,221/255,1]))
                if (allHabits[i][5] == str(date.today())): 
                    var_green_btn[i].text = "Done!"
                    var_green_btn[i].disabled = True
                    var_green_btn[i].background_color = [169/255,255/255,221/255,1]
                var_red_btn.append(Button(text = "Didn't", on_press = partial(var_red_btn_fn, DailyHab, Login.connection, i), background_color = [253/255, 129/255, 129/255, 1]))
                self.task=GridLayout(rows=1, cols_minimum={0:200, 1:200})
            elif hab_category == "quit":
                if (allHabits[i][6]<= allHabits[i][3]):
                    var_green_btn.append(Button(text = "       Max Streak: " + str(allHabits[0][6]) + "\n Earned on: " + str(date.today()), disabled=True, background_disabled_normal='atlas://data/images/defaulttheme/button', background_color = [169/255,255/255,221/255,.5]))
                else:
                    var_green_btn.append(Button(text = "       Max Streak: " + str(allHabits[0][6]) + "\n Earned on: " + str(allHabits[0][7]), disabled=True, background_disabled_normal='atlas://data/images/defaulttheme/button', background_color = [169/255,255/255,221/255,.5]))
                if (allHabits[i][5] == str(date.today())):
                    var_red_btn.append(Button(text = "Try again tomorrow!", on_press = partial(var_red_btn_fn, QuittingHab, Login.connection, i), background_color = [253/255, 129/255, 129/255, 1]))
                else:
                    var_red_btn.append(Button(text = "fuckied it up :(", on_press = partial(var_red_btn_fn, QuittingHab, Login.connection, i), background_color = [253/255, 129/255, 129/255, 1]))
                self.task=GridLayout(rows=2, cols_minimum={0:200, 1:200})

            self.task.add_widget(var_name_labels[i])
            self.task.add_widget(var_count_labels[i])
            self.task.add_widget(var_green_btn[i])
            self.task.add_widget(var_red_btn[i])
            var_task_layouts.append(self.task)
            if hab_category == "continue":
                DailyHab.header.text="Habit Tracker for " + Login.db_name[:-3]
                ScnMgrApp.root.get_screen("daily_hab").ids.grid1.add_widget(self.task)
                DailyHab.i = DailyHab.i+1
            elif hab_category == "quit":
                QuittingHab.header.text="Quitting Tracker for " + Login.db_name[:-3]
                ScnMgrApp.root.get_screen("quitting_hab").ids.grid2.add_widget(self.task)
                new_counts = partial(QuittingHab.count_up_by_days, QuittingHab, Login.connection, i)
                new_counts(i)
                QuittingHab.quit_i = QuittingHab.quit_i+1


class DailyHab(Screen):
    def __init__(self, **kwargs):
        super(DailyHab, self).__init__(**kwargs)
        self.ids.grid1.cols=1
        self.ids.grid1.padding=[50,50,50,50]

        DailyHab.header = Button(
            text="Habit Tracker", 
            font_size="35sp", 
            disabled=True, 
            background_disabled_normal='background_normal', 
            background_color=[52/255, 110/255, 235/255, 0.5])

        self.ids.grid1.add_widget(DailyHab.header)
        
        self.homepage=GridLayout(cols=3)

        self.homepage.press = Button(text="Add Task")
        self.homepage.press.bind(on_press=self.show_popup)
        self.homepage.add_widget(self.homepage.press)

        self.homepage.press = Button(text="View Weekly Habs", on_press=partial(Login.build_tasks, Login, "weekly"), on_release=self.show_quitting_popup)
        self.homepage.add_widget(self.homepage.press)

        self.homepage.press = Button(text="View Quitting", on_press=partial(Login.build_tasks, Login, "quit"), on_release=self.show_quitting_popup)
        self.homepage.add_widget(self.homepage.press)

        self.ids.grid1.add_widget(self.homepage)

        DailyHab.tasklayouts = []
        DailyHab.habit_name_labels = []
        DailyHab.habit_count_labels = []
        DailyHab.check_yes_buttons = []
        DailyHab.check_no_buttons = []
        DailyHab.i=0
        DailyHab.quit_i=0    

    def show_popup(self, obj):
        playout = GridLayout(cols = 2, padding=[200, 200, 200, 200], rows_minimum={0:200})
        self.popup = Popup(title = "Add Task", content = playout)
        self.popup.plabel = Button(
                    text="Add Task",  
                    disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5])
        self.popup.ptext = TextInput(write_tab = False, multiline = False, on_text_validate = partial(self.add_task_new, Login.connection))
        self.popup.pbutton = Button(text = "Cancel", on_press = self.close_popup)
        self.popup.pbutton_add = Button(text = "Add", on_press = partial(self.add_task_new, Login.connection))
        playout.add_widget(self.popup.plabel)
        playout.add_widget(self.popup.ptext)
        playout.add_widget(self.popup.pbutton)
        playout.add_widget(self.popup.pbutton_add)
        self.popup.open()

    def add_task_new(self, xconnection, instance):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        h2 = Habit(Login.db_name[:-3],"continue", self.popup.ptext.text, 0, today, yesterday, 0)
        insert_habit(h2, xconnection)
        self.popup.dismiss()
        run_build_task = partial(Login.build_tasks, Login, "continue", h2)
        run_build_task()

    def close_popup(self, obj):
        self.popup.dismiss()

    def delete_task_popup(self, i, obj):
        self.edit_task_layout = GridLayout(cols=1, padding=[200,100,200,200])
        self.edit_task_popup = Popup(title="Edit a task", content = self.edit_task_layout)
        self.edit_task_popup.pname = TextInput(text = DailyHab.habit_name_labels[i].text, multiline = False, on_text_validate = partial(self.update_task_name, DailyHab, i))
        close_button = GridLayout(cols=6)
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Button(text="x", size_hint_y=None, height=80, on_press = self.edit_task_popup.dismiss))
        edit_row = GridLayout(cols=2)
        edit_row.add_widget(Button(text="Edit Task Name: ", disabled=True, background_disabled_normal='atlas://data/images/defaulttheme/button', background_color=[52/255, 110/255, 235/255, 0.5]))
        edit_row.add_widget(self.edit_task_popup.pname)
        self.edit_task_layout.add_widget(close_button)
        self.edit_task_layout.add_widget(edit_row)
        self.edit_task_layout.add_widget(Button(text="Save Changes", on_press = partial(self.update_task_name, DailyHab, i), background_color=[52/255, 110/255, 235/255, 0.5]))
        self.edit_task_layout.add_widget(Button(text="Delete Task: " + DailyHab.habit_name_labels[i].text, background_color = [253/255, 129/255, 129/255, 1], on_press = partial(self.delete_task_action, DailyHab, i, Login.connection)))
        self.edit_task_popup.open()
        pass

    def update_task_name(self, i, obj):
        update_name(self.edit_task_popup.pname.text, DailyHab.habit_name_labels[i].text, Login.connection)
        DailyHab.habit_name_labels[i].text = self.edit_task_popup.pname.text
        self.edit_task_popup.dismiss()
        pass

    def delete_task_action(self, i , xconnection, obj):
        delete_task_db(DailyHab.habit_name_labels[i].text, xconnection)
        self.edit_task_popup.dismiss()
        run_build_task = partial(Login.build_tasks, Login, "continue", i)
        run_build_task()
        pass

    def count_up_new(self, xconnection, ind, instance):
        button_name = DailyHab.check_yes_buttons[ind].text
        name = DailyHab.habit_name_labels[ind].text
        if (button_name.find("Done!") != -1):
            return
        else:
            habit_list = get_habit_by_name(xconnection, name)
            last_mod_date = habit_list[0][5]
            category = habit_list[0][1]
            today = str(date.today())
            if (last_mod_date == today):
                DailyHab.check_yes_buttons[ind].text = "Done!"
            else:
                DailyHab.habit_count_labels[ind].text = str(int(DailyHab.habit_count_labels[ind].text) + 1)
                DailyHab.check_yes_buttons[ind].text = "Done!"
                update_count(DailyHab.habit_count_labels[ind].text, name, category, xconnection)
                update_last_mod_date(name, xconnection)
                update_max_earn_date(name, xconnection)

    def count_down_new(self, xconnection, ind, instance):
        name = DailyHab.habit_name_labels[ind].text
        DailyHab.habit_count_labels[ind].text = str(0)
        DailyHab.check_yes_buttons[ind].disabled = True
        update_count(0, name, 'continue', xconnection)
        pass

    def show_quitting_popup(self, obj):
        self.manager.transition.direction = "left"
        self.manager.current = "quitting_hab"

class QuittingHab(Screen):
    def __init__(self, **kwargs):
        super(QuittingHab, self).__init__(**kwargs)
        self.ids.grid2.cols=1
        self.ids.grid2.padding=[50,50,50,50]

        QuittingHab.header = Button(
            text="Quitting Tracker", 
            font_size="35sp", 
            disabled=True, 
            background_disabled_normal='background_normal', 
            background_color=[52/255, 110/255, 235/255, 0.5])

        self.ids.grid2.add_widget(QuittingHab.header)

        self.homepage=GridLayout(cols=2)

        self.homepage.press = Button(text="Add Quitting Task")
        self.homepage.press.bind(on_press=self.add_quit_popup)
        self.homepage.add_widget(self.homepage.press)

        self.homepage.press = Button(text="Go Back")
        self.homepage.press.bind(on_press=self.go_back)
        self.homepage.add_widget(self.homepage.press)

        self.ids.grid2.add_widget(self.homepage)

        QuittingHab.quit_tasklayouts = []
        QuittingHab.quit_habit_name_labels = []
        QuittingHab.quit_habit_count_labels = []
        QuittingHab.quit_max_streak_labels = []
        QuittingHab.quit_check_no_buttons = []
        QuittingHab.quit_i=0
        
    def add_quit_popup(self, objs):
        self.quit_add_layout = GridLayout(cols = 2, padding=[200, 200, 200, 200], rows_minimum={0:200})
        self.quit_add_popup = Popup(title = "Add new task to quit", content = self.quit_add_layout)
        self.quit_add_popup.pq_prompt = Button(
                            text="Add Task",  
                            disabled=True, 
                            background_disabled_normal='background_normal', 
                            background_color=[52/255, 110/255, 235/255, 0.5])
        self.quit_add_layout.add_widget(self.quit_add_popup.pq_prompt)
        self.quit_add_popup.pq_text = TextInput(hint_text = "Quit a habit", multiline = False, on_text_validate = partial(self.add_quit_task_new, Login.connection))
        self.quit_add_layout.add_widget(self.quit_add_popup.pq_text)
        self.quit_add_popup.pq_button = Button(text = "Cancel", on_press = self.quit_add_popup.dismiss)
        self.quit_add_layout.add_widget(self.quit_add_popup.pq_button)
        self.quit_add_popup.pq_button_add = Button(text = "Add", on_press = partial(self.add_quit_task_new, Login.connection))
        self.quit_add_layout.add_widget(self.quit_add_popup.pq_button_add)
        self.quit_add_popup.open()

    def add_quit_task_new(self, xconnection, obj):
        h3 = Habit(Login.db_name[:-3],"quit", self.quit_add_popup.pq_text.text, 0, date.today(), date.today(), 0)
        insert_habit(h3, xconnection)
        self.quit_add_popup.dismiss()    
        run_build_task = partial(Login.build_tasks, Login, "quit", h3)
        run_build_task()
    
    def edit_quit_task_popup(self, i, obj):
        self.edit_quit_layout = GridLayout(cols=1, padding=[200,100,200,200])
        self.edit_quit_popup = Popup(title="Edit a task", content = self.edit_quit_layout)
        self.edit_quit_popup.pname = TextInput(text = QuittingHab.quit_habit_name_labels[i].text, multiline = False, on_text_validate = partial(self.update_quit_task_name, QuittingHab, i))
        close_button = GridLayout(cols=6)
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Label())
        close_button.add_widget(Button(text="x", size_hint_y=None, height=80, on_press = self.edit_quit_popup.dismiss))
        edit_row = GridLayout(cols=2)
        edit_row.add_widget(Button(text="Edit Task Name: ", disabled=True, background_disabled_normal='atlas://data/images/defaulttheme/button', background_color=[52/255, 110/255, 235/255, 0.5]))
        edit_row.add_widget(self.edit_quit_popup.pname)
        self.edit_quit_layout.add_widget(close_button)
        self.edit_quit_layout.add_widget(edit_row)
        self.edit_quit_layout.add_widget(Button(text="Save Changes", on_press = partial(self.update_quit_task_name, QuittingHab, i), background_color=[52/255, 110/255, 235/255, 0.5]))
        self.edit_quit_layout.add_widget(Button(text="Delete Task: " + QuittingHab.quit_habit_name_labels[i].text, background_color = [253/255, 129/255, 129/255, 1], on_press = partial(self.delete_quit_task_action, QuittingHab, i, Login.connection)))
        self.edit_quit_popup.open()
        pass

    def update_quit_task_name(self, i, obj):
        update_name(self.edit_quit_popup.pname.text, QuittingHab.quit_habit_name_labels[i].text, Login.connection)
        QuittingHab.quit_habit_name_labels[i].text = self.edit_quit_popup.pname.text
        self.edit_quit_popup.dismiss()

    def delete_quit_task_action(self, i, xconnection, obj):
        delete_task_db(QuittingHab.quit_habit_name_labels[i].text, xconnection)
        self.edit_quit_popup.dismiss()
        run_build_task = partial(Login.build_tasks, Login, "quit", i)
        run_build_task()

    def count_down_quit(self, xconnection, i, obj):
        habit_list = get_habit_by_name(xconnection, QuittingHab.quit_habit_name_labels[i].text)
        last_mod_date = datetime.strptime((habit_list[0][5]), "%Y-%m-%d").date()
        today = date.today()
        if (today-last_mod_date).days != 0:
            QuittingHab.quit_habit_count_labels[i].text = "0"
            update_count(0, QuittingHab.quit_habit_name_labels[i].text, "quit", xconnection)
            update_last_mod_date(QuittingHab.quit_habit_name_labels[i].text, xconnection)
            QuittingHab.quit_check_no_buttons[i].text = "Try again tomorrow!"
        else:
            QuittingHab.quit_check_no_buttons[i].text = "Try again tomorrow!"

    def count_up_by_days(self, xconnection, ind, instance):
        name = QuittingHab.quit_habit_name_labels[ind].text
        habit_list = get_habit_by_name(xconnection, name)
        last_mod_date = datetime.strptime((habit_list[0][5]), "%Y-%m-%d").date()
        today = date.today()
        if (today-last_mod_date).days != 0:
            QuittingHab.quit_habit_count_labels[ind].text = str((today-last_mod_date).days)
            update_count(QuittingHab.quit_habit_count_labels[ind].text, name, 'quit', xconnection)
        else:
            QuittingHab.quit_habit_count_labels[ind].text = str(habit_list[0][3])
        
        if (today-last_mod_date).days >= habit_list[0][6]:
            QuittingHab.quit_max_streak_labels[ind].text = "       Max Streak: " + str((today-last_mod_date).days) + "\n Earned on: " + str(date.today()) #+ "\n Last started on: " + habit_list[0][5]
            update_max_count((today-last_mod_date).days, QuittingHab.quit_habit_name_labels[ind].text, "quit", xconnection)
            update_max_earn_date(QuittingHab.quit_habit_name_labels[ind].text, xconnection)
        else:
            QuittingHab.quit_max_streak_labels[ind].text = "       Max Streak: " + str(habit_list[0][6]) + "\n Earned on: " + str(habit_list[0][7]) 
            
        pass

    def go_back(self, obj):
        run_build_task = partial(Login.build_tasks, Login, "continue", obj)
        run_build_task()
        self.manager.transition.direction = "right"
        self.manager.current = "daily_hab"

class ScnMgrApp(App):

    def build(self):
        ScnMgrApp.root = ScreenManager()
        ScnMgrApp.root.add_widget(Login(name="login"))
        ScnMgrApp.root.add_widget(DailyHab(name="daily_hab"))
        ScnMgrApp.root.add_widget(QuittingHab(name="quitting_hab"))
        return ScnMgrApp.root

if __name__ == '__main__':
    ScnMgrApp().run()