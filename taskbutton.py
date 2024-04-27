from kivy.app import App
from kivy.uix.button import Button

class TaskButton(Button):
    ''''''

    def edit_task(self):
        ''''''
        app = App.get_running_app()

        app.current_task = self.task
        app.edit_name_input.text = self.task.title
        app.edit_description_input.text = self.task.description
        app.edit_date_input.text = self.task.due_date
        if self.task.completion_status:
            app.edit_status_checkbox.active = True
        else:
            app.edit_status_checkbox.active = False


        # This line proves that the current_task is being updated
        # print(app.current_task)

        app.go_to_task_details()