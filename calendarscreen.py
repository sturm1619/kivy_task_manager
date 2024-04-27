from calendar import Calendar
from datetime import date

from task import Task, TaskList
from taskbutton import TaskButton

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle




class DateButton(Button):
    def switch_to_date(self, instance):
        App.get_running_app().dateScreen.date_label.text = f"{self.date}"
        App.get_running_app().dateScreen.taskListBoxLayout.clear_widgets()
        for task in self.taskList:
            taskButton = TaskButton(text=f"{task.title}")
            taskButton.task = task
            taskButton.on_press = task
            App.get_running_app().dateScreen.taskListBoxLayout.add_widget(taskButton)
        App.get_running_app().manager.current = "date"

    def switch_to_calendar(self, instance):
        App.get_running_app().manager.current = "calendar"
        

class MyApp(App):
    def build(self):

        self.taskList = [Task(title="Homework", due_date = date.fromordinal(date.today().toordinal()+1)), Task(title="Clean House", due_date = date.fromisoformat("2024-04-30"))]
        self.calendar = list(Calendar(firstweekday=6).itermonthdates(date.today().year, date.today().month))

        calendarScreen = Screen(name="calendar")

        calendar_layout = BoxLayout(orientation="vertical")
        calendar_layout.add_widget(Button(text="To Do Calendar", size_hint_y = 0.1, background_color="green"))
        calendar_gui = GridLayout(cols=7)

        for date in list(self.calendar):
            date_tasks = []
            for task in self.taskList:
                if task.due_date == date.isoformat():
                    date_tasks.append(task)

            date_button = DateButton()
            date_button.date = f"{date: %a %d %b}"
            date_button.text = date_button.date
            date_button.taskList = date_tasks
            if date_button.taskList != []:
                date_button.background_color = "blue"
            date_button.bind(on_press = date_button.switch_to_date)
            calendar_gui.add_widget(date_button)

        calendar_layout.add_widget(calendar_gui)
        calendar_layout.add_widget(Button(text="Go to Main Screen", size_hint_y = 0.1))
        calendarScreen.add_widget(calendar_layout)

        self.dateScreen = Screen(name="date")    

        self.dateScreen.boxLayout = BoxLayout(orientation="vertical")

        self.dateScreen.date_label = Label(text="")
        self.dateScreen.boxLayout.add_widget(self.dateScreen.date_label)

        self.dateScreen.taskListBoxLayout = BoxLayout(orientation="vertical")
        self.dateScreen.boxLayout.add_widget(self.dateScreen.taskListBoxLayout)

        self.dateScreen.calendar_button = Button(text="Go back to month")
        self.dateScreen.calendar_button.bind(on_press=date_button.switch_to_calendar)
        self.dateScreen.boxLayout.add_widget(self.dateScreen.calendar_button)

        self.dateScreen.add_widget(self.dateScreen.boxLayout)
        
        self.manager = ScreenManager()

        self.manager.add_widget(calendarScreen)
        self.manager.add_widget(self.dateScreen)
        return self.manager
    
MyApp().run()