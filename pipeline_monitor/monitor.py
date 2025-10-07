class PipelineMonitor:
    def __init__(self, github_client, poll_interval=120):
        self.github_client = github_client
        self.poll_interval = poll_interval
        self.callbacks = []
        self.previous_status = None

    def on_status_change(self, callback):
        self.callbacks.append(callback)

    def _poll_once(self):
        current_status = self.github_client.get_pipeline_status()

        # Call callbacks on first poll OR when status changes
        if self.previous_status is None or current_status != self.previous_status:
            for callback in self.callbacks:
                callback(current_status)

        self.previous_status = current_status

    def start(self):
        pass

    def stop(self):
        pass
