
import time

from .tasks import longtime_add


if __name__ == "__main__":
    result = longtime_add.delay(1, 2)
    print("Task finished?  ", result.ready())
    print("Task result: ", result.result)

    time.sleep(4)
    print("Task finished?  ", result.ready())
    print("Task result: ", result.result)
