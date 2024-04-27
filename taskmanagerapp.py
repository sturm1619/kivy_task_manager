''' Kivy Libraries '''
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

''' DateTime Libraries'''
from calendar import Calendar
import datetime

''' Personal Libraries '''
from taskbutton import TaskButton

from task import Task, TaskList
from file_handling import read_json, write_json

class MainScreen(Screen):
    pass

class TaskDetailsScreen(Screen):
    pass

class AddEditTaskScreen(Screen):
    pass

class ChildBox(BoxLayout):
    pass


class DateButton(Button):
    def switch_to_date(self, instance):
        for date in list(App.get_running_app().calendar):
                    date_tasks = []
                    for task in App.get_running_app().taskList:
                        if task.due_date == date.isoformat():
                            date_tasks.append(task)

        App.get_running_app().dateScreen.date_label.text = f"{self.date: %A, %B %dth, %Y}"
        App.get_running_app().dateScreen.taskListBoxLayout.clear_widgets()
        for task in self.taskList:
            if task.completion_status:
                completion_status = "Done"
            else:
                completion_status = "Not Done"
            taskButton = TaskButton(text=f'{task.title}\nDue Date: {task.due_date}\nStatus: {completion_status}', font_size = 24)
            taskButton.task = task
            taskButton.on_press = taskButton.edit_task
            App.get_running_app().dateScreen.taskListBoxLayout.add_widget(taskButton)
            if taskButton.task.completion_status:
                taskButton.background_color = "lime"
            else:
                taskButton.background_color = "red"
        App.get_running_app().screenManager.current = "date"


class TaskManagerApp(App):
    def build(self):
        ''' Compose the task list'''
        self.taskList : TaskList = read_json("task_database.json")#[]
        # self.taskList.append(Task(title='Do homework'))
        # self.taskList.append(Task(title='Clean house'))
        self.current_task = self.taskList[0]

        '''Define ScreenManager'''
        self.screenManager = ScreenManager()

        ''' Define Screens'''
        self.mainScreen = self.build_MainScreen()
        self.taskDetailsScreen = self.build_TaskDetailsScreen()
        self.addEditTaskScreen = self.build_AddEditTaskScreen()

        '''Add Screens'''
        self.screenManager.add_widget(self.mainScreen)
        self.screenManager.add_widget(self.taskDetailsScreen)
        self.screenManager.add_widget(self.addEditTaskScreen)

        """CALENDAR FUNCTIONALITY"""
        self.calendar = list(Calendar(firstweekday=6).itermonthdates(datetime.date.today().year, datetime.date.today().month))

        self.calendarScreen = self.build_CalendarScreen()

        self.dateScreen = self.build_DateScreen()

        self.screenManager.add_widget(self.calendarScreen)
        self.screenManager.add_widget(self.dateScreen)

        # The next line is only for maintenance
        #print(self.screenManager.children[0].children)
        return self.screenManager
    




    ''' WIDGET CONSTRUCTORS '''
    def build_task_list_display(self) -> BoxLayout:
        """ Builds the Task List Display in the MainScreen."""

        taskListDisplayBox = BoxLayout(orientation='vertical')

        for task in self.taskList:
            if task.completion_status:
                completion_status = "Done"
            else:
                completion_status = "Not Done"
            taskButton = TaskButton(text=f'{task.title}\nDue Date: {task.due_date}\nStatus: {completion_status}', font_size = 24)
            taskButton.task = task
            if taskButton.task.completion_status:
                taskButton.background_color = "lime"
            else:
                taskButton.background_color = "red"
            taskButton.on_press = taskButton.edit_task

            taskListDisplayBox.add_widget(taskButton)

        return taskListDisplayBox
    
    def build_CalendarGUI(self) -> GridLayout:
        calendar_gui = GridLayout(cols=7)

        for date in list(self.calendar):
            date_tasks = []
            for task in self.taskList:
                if task.due_date == date.isoformat():
                    date_tasks.append(task)

            date_button = DateButton()
            date_button.date = date
            date_button.text = f"{date_button.date: %a, %b %d}"
            date_button.taskList = date_tasks
            if date_button.taskList != []:
                date_button.background_color = "blue"
                
            else:
                date_button.background_color = "yellow"
            date_button.bind(on_press = date_button.switch_to_date)
            calendar_gui.add_widget(date_button)

        return calendar_gui

    

    def build_MainScreen(self) -> MainScreen:
        """ Builds the Main Screen"""

        mainScreen = MainScreen(name='main')

        ''' MainScreen Widgets '''
        # Container in the MainScreen
        mainBox = BoxLayout(orientation='horizontal')

        # Subcontainer in the MainScreen for the TaskButtonList
        self.taskListDisplayBox = self.build_task_list_display()

        # Container for the menus 
        self.childBox = ChildBox()

        '''Define Task Widgets for Task List Display'''

        mainBox.add_widget(self.taskListDisplayBox)
        mainBox.add_widget(self.childBox)

        mainScreen.add_widget(mainBox)

        return mainScreen
    

    def build_TaskDetailsScreen(self) -> TaskDetailsScreen:
        """ Builds the Task Details Screen"""

        ''' Function for creating BoxLayouts with horizontal orientation '''
        def horizontal_Box(): return BoxLayout(orientation='horizontal')

        taskDetailsScreen = TaskDetailsScreen(name = 'taskDetails')

        ''' Vertical BoxLayout container for all the minor widgets '''
        superBox = BoxLayout(orientation='vertical')

        ''' Title Button '''
        title = Button(text = 'Task Details', font_size = 48)
        title.bind(on_press = self.go_to_main)


        ''' Task Name Box '''
        nameBox = horizontal_Box()

        name_label = Label(text='Title: ', size_hint_x = 0.45)
        self.edit_name_input = TextInput(text=self.current_task.title)

        nameBox.add_widget(name_label)
        nameBox.add_widget(self.edit_name_input)


        ''' Task Description Box '''
        descriptionBox = horizontal_Box()

        description_label = Label(text='Description: ', size_hint_x = 0.45)
        self.edit_description_input = TextInput(text=self.current_task.description)

        descriptionBox.add_widget(description_label)
        descriptionBox.add_widget(self.edit_description_input)

        ''' Due Date Box '''
        dateBox = horizontal_Box()

        date_label = Label(text='Due Date: ')
        self.edit_date_input = TextInput(text=self.current_task.due_date)
        status_label = Label(text='Completed: ')
        self.edit_status_checkbox = CheckBox()
        if self.current_task.completion_status:
            self.edit_status_checkbox.active = True

        dateBox.add_widget(date_label)
        dateBox.add_widget(self.edit_date_input)
        dateBox.add_widget(status_label)
        dateBox.add_widget(self.edit_status_checkbox)

        ''' Manage Box'''
        manageBox = horizontal_Box()

        save_button = Button(text = 'Save Changes')
        save_button.bind(on_press = self.modify_current_task)

        delete_button = Button(text = 'Delete Task')
        delete_button.bind(on_press = self.delete_current_task)

        manageBox.add_widget(save_button)
        manageBox.add_widget(delete_button)


        ''' Add all Widgets to the superBox'''
        superBox.add_widget(title)
        superBox.add_widget(nameBox)
        superBox.add_widget(descriptionBox)
        superBox.add_widget(dateBox)
        superBox.add_widget(manageBox)
        

        ''' Add superBox layout to the Screen '''
        taskDetailsScreen.add_widget(superBox)
        
        ''' Return the Screen '''
        return taskDetailsScreen


    def build_AddEditTaskScreen(self) -> AddEditTaskScreen:
        ''' Builds the Add Edit Task Screen'''

        ''' Function for creating BoxLayouts with horizontal orientation '''
        def horizontal_Box(): return BoxLayout(orientation='horizontal')

        addEditTaskScreen = AddEditTaskScreen(name = 'add')

        ''' Vertical BoxLayout container for all the minor widgets '''
        superBox = BoxLayout(orientation='vertical')

        ''' Title Button '''
        title = Button(text = 'Create New Task', font_size = 48)
        title.bind(on_press = self.go_to_main)

        ''' Task Name Box '''
        nameBox = horizontal_Box()

        name_label = Label(text='Title: ', size_hint_x = 0.45)
        self.add_name_input = TextInput()

        nameBox.add_widget(name_label)
        nameBox.add_widget(self.add_name_input)

        ''' Task Description Box '''
        descriptionBox = horizontal_Box()

        description_label = Label(text='Description: ', size_hint_x = 0.45)
        self.add_description_input = TextInput()

        descriptionBox.add_widget(description_label)
        descriptionBox.add_widget(self.add_description_input)

        ''' Due Date Box '''
        dateBox = horizontal_Box()

        date_label = Label(text='Due Date: ')
        self.add_date_input = TextInput()

        dateBox.add_widget(date_label)
        dateBox.add_widget(self.add_date_input)

        ''' Manage Box'''
        manageBox = horizontal_Box()

        add_button = Button(text = 'Add Task')
        add_button.bind(on_press = self.new_task)


        manageBox.add_widget(add_button)

        ''' Add all Widgets to the superBox'''
        superBox.add_widget(title)
        superBox.add_widget(nameBox)
        superBox.add_widget(descriptionBox)
        superBox.add_widget(dateBox)
        superBox.add_widget(manageBox)
        

        ''' Add superBox layout to t he Screen '''
        addEditTaskScreen.add_widget(superBox)
        
        ''' Return the Screen '''
        return addEditTaskScreen

    def build_CalendarScreen(self) -> Screen:


        calendar_layout = BoxLayout(orientation="vertical")
        
        calendar_layout.add_widget(Button(text="To Do Calendar", size_hint_y = 0.1, background_color="green"))
        
        calendar_gui = self.build_CalendarGUI()
        calendar_layout.add_widget(calendar_gui)

        go_to_main_button = Button(text="Go to Main Screen", size_hint_y = 0.1, background_color = "red")
        go_to_main_button.bind(on_press = self.go_to_main)
        calendar_layout.add_widget(go_to_main_button)
        
        calendarScreen = Screen(name="calendar")        
        calendarScreen.add_widget(calendar_layout)

        return calendarScreen


    def build_DateScreen(self) -> Screen:

        dateScreen = Screen(name="date")  
        
        dateScreen.boxLayout = BoxLayout(orientation="vertical")

        dateScreen.date_label = Label(text="", font_size = 48)
        dateScreen.boxLayout.add_widget(dateScreen.date_label)

        dateScreen.taskListBoxLayout = BoxLayout(orientation="vertical")
        dateScreen.boxLayout.add_widget(dateScreen.taskListBoxLayout)

        dateScreen.calendar_button = Button(text="Go back to month", font_size = 48, background_color = "red")
        dateScreen.calendar_button.bind(on_press=self.go_to_calendar)
        dateScreen.boxLayout.add_widget(dateScreen.calendar_button)

        dateScreen.add_widget(dateScreen.boxLayout)

        return dateScreen
    # def get_task_info(self) -> None:
    #     pass

    

    ''' EVENTS '''
    def go_to_main(self, instance) -> None:

        ''' Remove outdated MainScreen'''
        self.screenManager.remove_widget(self.mainScreen)

        ''' Build new MainScreen'''
        self.mainScreen = self.build_MainScreen()

        ''' Add new MainScreen'''
        self.screenManager.add_widget(self.mainScreen)

        self.screenManager.remove_widget(self.calendarScreen)

        self.calendarScreen = self.build_CalendarScreen()

        self.screenManager.add_widget(self.calendarScreen)

        ''' Move to new MainScreen'''
        self.screenManager.current = 'main'

    def go_to_task_details(self) -> None:

        self.screenManager.remove_widget(self.taskDetailsScreen)

        self.taskDetailsScreen = self.build_TaskDetailsScreen()

        self.screenManager.add_widget(self.taskDetailsScreen)

        self.screenManager.current = 'taskDetails'

    def go_to_calendar(self, instance):
        self.screenManager.remove_widget(self.calendarScreen)

        self.calendarScreen = self.build_CalendarScreen()

        self.screenManager.add_widget(self.calendarScreen)

        self.screenManager.current = "calendar"


    def quick_new_task(self) -> None:

        """Appends a task inputed in the main screen TextInput object."""
        ''' Get string from the text input'''

        task_info : str = self.childBox.ids['input_new_task_field'].text


        ''' Create a task object '''
        quick_new_task = Task(title=task_info)

        '''Append task object to the list'''
        self.taskList.append(quick_new_task)

        ''' Update Widgets'''
        self.screenManager.current = 'taskDetails'
        self.screenManager.remove_widget(self.mainScreen)
        self.mainScreen = self.build_MainScreen()
        self.screenManager.add_widget(self.mainScreen)
        self.screenManager.current = 'main'
        

    def modify_current_task(self, instance) -> None:
        ''' Updates a task from the Task Details Screen.'''
        self.current_task.title = self.edit_name_input.text
        self.current_task.description = self.edit_description_input.text
        self.current_task.due_date = self.edit_date_input.text
        self.current_task.completion_status = self.edit_status_checkbox.active


    def delete_current_task(self, instance) -> None:
        ''' Deletes current task from the Task Details Screen '''
        self.taskList.remove(self.current_task.name)


    def new_task(self, instance) -> None:
        ''' Creates a new task from the Add Edit Task Screen'''
        task = Task(title=self.add_name_input.text, description=self.add_description_input.text, due_date=self.add_date_input.text)
        self.taskList.append(task)

    def save_list_into_json(self) -> None:
        write_json(self.taskList, "task_database.json")

if __name__ == '__main__':
    TaskManagerApp().run()