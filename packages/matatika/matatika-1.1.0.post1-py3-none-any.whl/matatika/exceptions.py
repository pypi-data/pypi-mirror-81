'''exceptions module'''

class MatatikaException(Exception):
    """Class to handle custom Matatika exceptions"""

    def __init__(self, message=None):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

class WorkspaceNotFoundError(Exception):
    """Class to raise an exception when a workspace is not found"""

    def __init__(self, workspace_id):
        super().__init__()
        self.workspace_id = workspace_id

    def __str__(self):
        return "Workspace {} does not exist within the current authorisation context" \
            .format(self.workspace_id)
