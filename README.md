## Managing logger handlers

The python logger is a static object that may be instantiated several times but remains managed by the logger module itself.

When  we create a new logger it's the same static object that other classes have access inside of our runtime and because of this when we add a handler it remains present in the logger despite the class that created the handler being destroyed, this effect is more noticeable when the class containing the logger is intantiated and destroyed several times during the execution of the script.

### Examples usage of the handler
In this example a class is creating and instance of the logger in its contructor and assigning a handler.

#### Incorrect usage
The handler is added to the logger when it's instantiated inside the class and the class in turn is created and destroyed several times.

```python
import logging
from logging.handlers import RotatingFileHandler


class Example(object):
    def __init__(self):
        log_handler = RotatingFileHandler('app.log', maxBytes=100 * 1024 * 1024, backupCount=10, mode='a')
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        log_handler.setFormatter(formatter)
        self.logger = logging.getLogger("example_logger")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)

        self.logger.info("A new instance of the example has been created")


for i in iter(range(0, 3)):
    example = Example()
```

When the class Example is first instantiated it'll assign a handler to the global logger and print one new line to inform the class has been created, the second time the class is instantiated a new handler will be created this time the logger will add two lines one for the newly created handler and another one for the already existing one, by the third time another handler will be added resulting in a total of 6 messages being written to the log.

```text
2019-03-05 11:46:31,296 example_logger INFO     A new instance of the example has been created
2019-03-05 11:46:31,296 example_logger INFO     A new instance of the example has been created
2019-03-05 11:46:31,296 example_logger INFO     A new instance of the example has been created
2019-03-05 11:46:31,297 example_logger INFO     A new instance of the example has been created
2019-03-05 11:46:31,297 example_logger INFO     A new instance of the example has been created
2019-03-05 11:46:31,297 example_logger INFO     A new instance of the example has been created
```

#### Correct usage
The class gets a new instance of the logger but the handler is only added once to the global logger object, this way every time the logger is instance it'll use the already existing handler
```python
import logging
from logging.handlers import RotatingFileHandler


class Example(object):
    def __init__(self):
        self.logger = logging.getLogger("example_logger")
        self.logger.setLevel(logging.INFO)

        self.logger.info("A new instance of the example has been created")


logger = logging.getLogger()
log_handler = RotatingFileHandler('app.log', maxBytes=100 * 1024 * 1024, backupCount=10, mode='a')
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

for i in iter(range(0, 3)):
    example = Example()
```

Instantiating the example three times results in only three new lines in the log file

```text
2019-03-05 11:46:40,149 example_logger INFO     A new instance of the example has been created
2019-03-05 11:46:40,150 example_logger INFO     A new instance of the example has been created
2019-03-05 11:46:40,150 example_logger INFO     A new instance of the example has been created
```

As a note, when instantiating a new logger with **logging.getLogger("example_logger")** and adding a handler to it will make the handler only be available to the "example_logger"
