import contextlib
import threading
import time

import uvicorn

from drivr import app


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        ...

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


config = uvicorn.Config(
    app,
    host="127.0.0.1",
    port=5000,
    log_level="info",
    loop="asyncio",
)

server = Server(config=config)
