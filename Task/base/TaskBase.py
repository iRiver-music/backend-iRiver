from Task.models import TaskLog


class BaseTask:
    def __init__(self, **opcode_mes):
        # Use .get() to safely access dictionary keys
        self.opcode = opcode_mes.get("opcode")
        self.opcode_mes = opcode_mes
        self.OK = 200
        self.ERROR = 404
        self.respjson = None  # Initialize respjson attribute

    def run(self):
        try:
            print(self.opcode)
            if self.opcode == 200:
                self.run_task()  # Call the specific task logic for opcode 200
            elif self.opcode == 500:
                self.handle_error()  # Call the specific error handling logic for opcode 500
            else:
                self.set_error(self.ERROR, "Invalid opcode")
        except Exception as e:
            self.set_error(self.ERROR, f"Exception occurred: {e}")
            self.handle_exception(e)
        finally:
            self.save()

    def set_error(self, code, mes):
        self.opcode_mes["code"] = code
        self.opcode_mes["mes"] = mes
        self.respjson = {"code": code, "mes": mes}

    def save(self):
        # Save task related data using Django model (TaskLog)
        task_log = TaskLog(**self.opcode_mes)
        task_log.save()

    def run_task(self):
        self.opcode_mes["code"] = self.OK
        self.opcode_mes["mes"] = "Task executed successfully"
        self.respjson = {"code": self.OK,
                         "mes": "Task executed successfully"}
        print("Running the task")

    def handle_error(self):
        self.opcode_mes["code"] = self.ERROR
        self.opcode_mes["mes"] = "Error occurred"
        self.respjson = {"code": self.ERROR, "mes": "Error occurred"}
        print("Handling error")

    def handle_exception(self, exception):
        self.opcode_mes["code"] = self.ERROR
        self.opcode_mes["mes"] = f"Exception occurred: {exception}"
        self.respjson = {"code": self.ERROR,
                         "mes": f"Exception occurred: {exception}"}
        print(f"Exception occurred: {exception}")

    def stop(self):
        self.opcode_mes["code"] = self.OK
        self.opcode_mes["mes"] = "Task stopped"
        self.respjson = {"code": self.OK, "mes": "Task stopped"}
        print("Stopping the task")

    def remove_task(self):
        self.opcode_mes["code"] = self.OK
        self.opcode_mes["mes"] = "Task removed"
        self.respjson = {"code": self.OK, "mes": "Task removed"}
        print("Removing the task")
