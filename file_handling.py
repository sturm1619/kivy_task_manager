import json
from datetime import date
from typing import Any
from task import Task, TaskList

def format_Task_as_dict(task : Task) -> dict[str, Any]:
    reformatted_task_dict : dict[str, Any] = {}
    for key in task.__dict__:
        if key == "_title":
            reformatted_task_dict["title"] = task.__dict__[key]
        elif key == "_description":
            reformatted_task_dict["description"] = task.__dict__[key]
        elif key == "_due_date":
            if isinstance(task.__dict__[key], date):
                reformatted_task_dict["due_date"] = task.__dict__[key].isoformat()
            elif isinstance(task.__dict__[key], str):
                reformatted_task_dict["due_date"] = task.__dict__[key]
        elif key == "_completion_status":
            if task.__dict__[key] == True:
                reformatted_task_dict["completion_status"] = "True"
            else:
                reformatted_task_dict["completion_status"] = "False"
    return reformatted_task_dict

def write_json(task_list : TaskList, json_filepath : str) -> None:
    """Writes the contents of the list into a .json file."""
    tasklist_with_dict : list[dict[str, Any]] = []
    for task in task_list:
        tasklist_with_dict.append(format_Task_as_dict(task))

    file = open(json_filepath, "w", encoding = "utf-8")
    json.dump(tasklist_with_dict, file, indent = "\t")


def read_json(json_filepath : str) -> TaskList:
    """Reads a json file andd imports a TaskList"""
    task_list : TaskList = []
    json_tasklist : list[str] = json.load(open(json_filepath, "r", encoding = "utf-8"))

    for json_task in json_tasklist:
        task = Task()
        if "title" in json_task:
            task.title = json_task["title"]
        if "description" in json_task:
            task.description = json_task["description"]
        if "due_date" in json_task:
            task.due_date = json_task["due_date"]
        if "completion_status" in json_task:
            if json_task["completion_status"].lower() == "true":
                task.completion_status = True
            else:
                task.completion_status = False 
        task_list.append(task)
    return task_list

if __name__ == "__main__":
    task_list = read_json("task_database.json")
    for task in task_list:
        print(f'{task.id}, {task.title}')
    
    write_json(task_list, "destination.json")
    task_list_destination = read_json("destination.json")
    print("This is the content from destination.json:")
    for task in task_list_destination:
        print(f'{task.id}, {task.title}, {task.due_date}, {task.completion_status}')
