from Task.models import Library, TaskLog
from Task.serializers import TaskLogSerializer


class BaseTask:
    """
    input: 
    username,
    sources ??,
    opcode,
    taskID,
    """

    def __init__(self, task_name: str, **opcode_desc):
        # Use .get() to safely access dictionary keys
        self.task_name = task_name
        self.opcode = opcode_desc.get("opcode")
        self.opcode_desc = opcode_desc
        self.OK = 200
        self.ERROR = 404
        self.respjson = None  # Initialize respjson attribute

    def run(self):
        try:
            if self.opcode == 200:
                self.run_task()  # Call the specific task logic for opcode 200
            elif self.opcode == 500:
                self.handle_error()  # Call the soppecific error handling logic for opcode 500
            else:
                self.set_error(self.ERROR, "Invalid opcode")
        except Exception as e:
            self.set_error(self.ERROR, f"Exception occurred: {e}")
            self.handle_exception(e)
        finally:
            self.save()

    def set_error(self, code, desc):
        self.opcode_desc["code"] = code
        self.opcode_desc["desc"] = desc
        self.respjson = {"code": code, "desc": desc}

    def validate(self):
        # Use the serializer to validate the data
        serializer = TaskLogSerializer(data=self.opcode_desc)
        if not serializer.is_valid():
            return serializer.errors  # Return validation errors

        return None  # Return None when data is valid

    def save(self):
        # Validate the data using the serializer
        validation_errors = self.validate()
        if validation_errors:
            self.set_error(self.ERROR, validation_errors)
            return  # Data is not valid, don't save it

        if self.opcode_desc.get("code") == self.OK:
            Library.objects.filter(
                id=self.opcode_desc.get("taskID")).update(active=True)
        else:
            Library.objects.filter(
                id=self.opcode_desc.get("taskID")).update(active=False)

        # Save task related data using Django model (TaskLog)
        log = {}
        log["username"] = self.opcode_desc.get("username")
        log["opcode"] = self.opcode_desc.get("opcode")
        log["source"] = self.opcode_desc.get("source", "Server")
        log["code"] = self.opcode_desc.get("code")
        log["desc"] = self.opcode_desc.get("desc")

        task_log = TaskLog(**log)
        task_log.save()

    def run_task(self):
        self.opcode_desc["code"] = self.OK
        self.opcode_desc["desc"] = "{} successfully".format(self.task_name)
        self.respjson = {"code": self.OK,
                         "desc": "Task executed successfully"}

    def handle_error(self):
        self.opcode_desc["code"] = self.ERROR
        self.opcode_desc["desc"] = "{} Error occurred".format(self.task_name)
        self.respjson = {"code": self.ERROR, "desc": "Error occurred"}

    def handle_exception(self, exception):
        self.opcode_desc["code"] = self.ERROR
        self.opcode_desc["desc"] = f"{self.task_name} Exception occurred: {exception}"
        self.respjson = {"code": self.ERROR,
                         "desc": f"Exception occurred: {exception}"}
        print(f"Exception occurred: {exception}")

    def stop(self):
        self.opcode_desc["code"] = self.OK
        self.opcode_desc["desc"] = f"{self.task_name} Task stopped"
        self.respjson = {"code": self.OK, "desc": "Task stopped"}

    def remove_task(self):
        self.opcode_desc["code"] = self.OK
        self.opcode_desc["desc"] = "Task removed"
        self.respjson = {"code": self.OK, "desc": "Task removed"}
