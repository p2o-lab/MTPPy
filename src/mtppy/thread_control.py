import logging
from threading import Thread


class ThreadControl:
    def __init__(self):
        """
        Represents a thread control to be able to run with multithreading.
        """
        self.thread = None
        self.running_state = ''
        self.requested_state = ''
        self.callback_function = None

    def request_state(self, state: str, cb_function: callable):
        logging.debug(f'State {state} requested')
        self.requested_state = state
        self.callback_function = cb_function

    def reallocate_running_thread(self):
        logging.debug(f'Reallocate thread to state {self.requested_state}')
        if self.requested_state is not self.running_state:
            self.thread = Thread(target=self.callback_function)
            self.thread.start()
            self.running_state = self.requested_state
