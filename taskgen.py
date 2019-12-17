from TaskGen.Input import InputUtils
from TaskGen.Generation import GenTask


def taskgen():
    InputUtils.set_memory()
    InputUtils.set_processor()
    InputUtils.set_tasks()
    GenTask.gen_task(1)

taskgen()
