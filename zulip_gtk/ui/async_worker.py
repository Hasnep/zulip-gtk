from typing import Any, Callable, Optional, Tuple

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, GObject  # noqa: E402


class AsyncWorker(GObject.Object):
    """
    Represents an asynchronous worker.

    An async worker's job is to run a blocking operation in the background using a Gio.Task to avoid blocking the app's main thread and freezing the user interface.

    The terminology used here is closely related to the Gio.Task API.

    There are two ways to specify the operation that should be run in the background:

    1. By passing the blocking operation (a function or method) to the constructor.
    2. By defining the work() method in a subclass.

    An example of (1) can be found in AppWindow.on_start_button_clicked.

    Constructor parameters:

    OPERATION (callable)
      The function or method that needs to be run asynchronously.
      This is only necessary when using a direct instance of AsyncWorker, not when using an instance of a subclass of AsyncWorker, in which case an AsyncWorker.work() method must be defined by the subclass instead.

    OPERATION_INPUTS (tuple)
      Input data for OPERATION, if any.

    OPERATION_CALLBACK (callable)
      A function or method to call when the OPERATION is complete.

      See AppWindow.on_lunch_finished for an example of such callback.

    OPERATION_CALLBACK_INPUTS (tuple)
      Optional. Additional input data for OPERATION_CALLBACK.

    CANCELLABLE (Gio.Cancellable)
      Optional. It defaults to None, meaning that the blocking operation is not cancellable.
    """

    def __init__(
        self,
        main_callback: Callable,
        main_callback_data: Tuple[Any, ...] = (),
        completion_callback: Optional[
            Callable[["AsyncWorker", Gio.AsyncResult, Any], None]
        ] = None,
        completion_callback_data: Tuple[Any, ...] = (),
        cancellable: Optional[Gio.Cancellable] = None,
    ) -> None:
        super().__init__()
        self.main_callback = main_callback
        self.main_callback_data = main_callback_data
        self.completion_callback = completion_callback
        self.completion_callback_data = completion_callback_data
        self.cancellable = cancellable

        # Holds the actual data referenced from the Gio.Task created in the AsyncWorker.start method
        self.pool = {}

    def _thread_callback(self, task, _worker, _task_data, _cancellable) -> None:
        # FIXME: task_data is always None for Gio.Task.run_in_thread callback.
        # The value passed to this callback as task_data always seems to be None, so we get the data for the blocking operation as follows instead.
        data_id = task.get_task_data()
        data = self.pool[data_id]

        # Run the blocking operation.
        outcome = self.main_callback(*data)

        task.return_value(outcome)

    def start(self) -> None:
        """
        Schedule the blocking operation to be run asynchronously.

        The blocking operation is either self.operation or self.work, depending on how the AsyncWorker was instantiated.

        This method corresponds to the function referred to as "blocking_function_async" in GNOME Developer documentation.
        """
        task: Gio.Task = Gio.Task.new(
            self,
            self.cancellable,
            self.completion_callback,
            self.completion_callback_data,
        )

        if self.cancellable is None:
            task.set_return_on_cancel(False)  # The task is not cancellable

        data_id = id(self.main_callback_data)
        self.pool[data_id] = self.main_callback_data
        task.set_task_data(
            data_id,
            # FIXME: Data destroyer function always gets None as argument.
            # This function is supposed to take as an argument the same value passed as data_id to task.set_task_data, but when the destroyer function is called, it seems it always gets None as an argument instead.
            # That's why the "key" parameter is not being used in the body of the anonymous function.
            lambda _key: self.pool.pop(data_id),
        )
        task.run_in_thread(self._thread_callback)

    def return_value(self, result: Gio.AsyncResult):
        if Gio.Task.is_valid(result, self):
            return result.propagate_value().value
        else:
            raise ValueError(f"Result `{result}` is not valid.")
