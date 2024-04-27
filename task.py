from datetime import date
from typing import NewType

class Task:
    """Data Structure for tasks."""
    id = 0

    def __init__(self,
                 **attributes
                 ) -> None:

        self.id = Task.id
        if Task.id == self.id:
            Task.id += 1
        
        if "title" in attributes.keys():
            if isinstance(attributes["title"], str):
                self._title = attributes['title']
            else:
                raise TypeError(f'{attributes['title']} is not a string.')

        if 'description' in attributes.keys():
            if isinstance(attributes['description'], str):
                self._description = attributes['description']
            else:
                raise TypeError(f'{attributes['description']} is not a string.')

        if 'due_date' in attributes.keys():
            if isinstance(attributes['due_date'], date):
                self._due_date = attributes['due_date']
            elif isinstance(attributes['due_date'], str): #datetime):
                if attributes['due_date'] == "":
                    self._due_date = None
                else:
                    self._due_date = date.fromisoformat(attributes['due_date'])
            else:
                raise TypeError(f'{attributes['due_date']} is not a date.')
        
        if 'completion_status' in attributes.keys():
            if isinstance(attributes['completion_status'], bool):
                self._completion_status = attributes['completion_status']
            else:
                raise TypeError(f'{attributes['completion_status']} is not a boolean.')
        else:
            self._completion_status = False

    @property
    def title(self) -> str:
        if "_title" in self.__dict__:
            return self._title
        else:
            return ""
    
    @title.setter
    def title(self, new_title : str) -> None:
        if isinstance(new_title, str):
            self._title = new_title 
        else:
            raise TypeError(f'{new_title} is not a string.')
        
    @property
    def description(self) -> str:
        if "_description" in self.__dict__:
            return self._description
        else:
            return ""
            
    @description.setter
    def description(self, new_description : str) -> None:
        if isinstance(new_description, str):
            self._description = new_description
        else:
            raise TypeError(f'{new_description} is not a string.')
        
    @property
    def due_date(self) -> date:
        if "_due_date" in self.__dict__:
            if self._due_date == None:
                return "None"
            elif self._due_date == "None":
                return "None"
            else:
                return self._due_date.isoformat()
        else:
            return "None"
    
    @due_date.setter
    def due_date(self, new_due_date : date | str) -> None:
        if isinstance(new_due_date, date):
            self._due_date = new_due_date

        elif isinstance(new_due_date, str):
            if new_due_date == "" or new_due_date == "None":
                self._due_date = "None"
            elif new_due_date.lower() == "tomorrow":
                self._due_date = date.fromordinal(date.today().toordinal() + 1)
            else:
                self._due_date = date.fromisoformat(new_due_date)
        else:
            raise TypeError(f'{new_due_date} is not a date.')
        
    @property
    def completion_status(self) -> bool:
        return self._completion_status
        
    @completion_status.setter
    def completion_status(self, new_completion_status : bool) -> None:
        if isinstance(new_completion_status, bool):
            self._completion_status = new_completion_status
        else:
            raise TypeError(f'{new_completion_status} is not a boolean.')
        
    def __lt__(self, other: "Task") -> bool:
        if isinstance(other, Task):
            return self.id < other.id
        else:
            raise TypeError(f'{other} is not a Task class instance.')
        
    def __le__(self, other: "Task") -> bool:
        if isinstance(other, Task):
            return self.id <= other.id
        else:
            raise TypeError(f'{other} is not a Task class instance.')
        
    def __gt__(self, other: "Task") -> bool:
        if isinstance(other, Task):
            return self.id > other.id
        else:
            raise TypeError(f'{other} is not a Task class instance.')
        
    def __ge__(self, other: "Task") -> bool:
        if isinstance(other, Task):
            return self.id >= other.id
        else:
            raise TypeError(f'{other} is not a Task class instance.')
        
    def __eq__(self, other: "Task") -> bool:
        if isinstance(other, Task):
            return self.id == other.id
        else:
            raise TypeError(f'{other} is not a Task class instance.')
        
    def __ne__(self, other: "Task") -> bool:
        if isinstance(other, Task):
            return self.id != other.id
        else:
            raise TypeError(f'{other} is not a Task class instance.')
        
TaskList = NewType("TaskList", list[Task])