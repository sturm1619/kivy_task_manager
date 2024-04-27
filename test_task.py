from task import Task
from datetime import date
import pytest

def test_title():

    """ Positive Cases """
    
    test_task : Task = Task("test")
    assert test_task.title == "test"

    """ Negative Cases """
    try:
        test_task.title = 100
    except TypeError:
        assert True
    except:
        assert False

def test_description():

    """ Positive Cases """

    test_task = Task("test", description = "test_task")
    assert test_task.description == "test_task"

    test_task.description = "test task 2"
    assert test_task.description == "test task 2"

    """ Negative Cases """

    try:
        test_task_2 = Task("test 2", description = 2000)
        assert not(test_task_2 == Task("test 2", description = 2000))
    except TypeError:
        assert True
    except:
        assert False

    try:
        test_task.title = 100
    except TypeError:
        assert True
    except:
        assert False

def test_date():
    
    """ Positive Case """
    test_task = Task("test", due_date = date.today())
    assert test_task.due_date == date.today()

    test_task.due_date = date(2023, 3, 29)
    assert test_task.due_date == date(2023, 3, 29)

    test_task.due_date = "1999-05-12"
    assert test_task.due_date == date(1999, 5, 12)

    """ Error Cases """
    try:
        test_task_2 = Task("test", due_date = 15)
        assert test_task_2.due_date == 15
    except TypeError:
        assert True
    except:
        assert False
    

if __name__ == "__main__":
    pytest.main()