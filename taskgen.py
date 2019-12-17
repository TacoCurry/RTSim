from TaskGen.Input import InputUtils
from TaskGen.Generation import GenTask
InputUtils.set_memory()
InputUtils.set_processor()
InputUtils.set_tasks()
GenTask.gen_task(1)
