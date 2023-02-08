from functools import partial
from inspect import getmembers, isfunction, getfullargspec
from TaskQueue import builtin_functions as bf
#import json
#import pathlib

def int_or_zero(x: int) -> int:
    if x > 0:
        return x
    else:
        return 0

def load_modules(module_names):
    """Takes in list of modules and returns a TaskQueue definition dict used for instantiating the TaskQueue class"""
    
    definition = {}

    for name in module_names:
        funcs = [el for el in getmembers(name) if not el[0].startswith('__') and isfunction(el[1])]
        for el in funcs:
            #definition[el[0]] = {'function':el[1],'arguments':getfullargspec(el[1])}
            #inspect.signature is preferred in favour of getfullargspec since 3.3 apparently
            definition[el[0]] = {'function':el[1],'arguments':int_or_zero(len(el[1].__annotations__)-2)}
    return definition
    
class Queue:
    """A class to define the task queue functionality and available tasks."""

    def __init__(self,definitions: list = []) -> None:
        self.available_tasks = {
            "DEFAULT": {"function": None, "arguments": 0},
            
        }  # Here we will first load the built-in functions before adding developer added ones
        definitions += [bf]
        self.available_tasks.update(load_modules(definitions))
        #self.available_tasks.update("ADD NEW": {"function": None, "arguments": 0})
        #self.available_tasks.update(definition)  # Do some error checking that definition is a dict

    def valid(self, previous):
        pass
        # function to return available next task in sequence

    def parser(self, coms):
        # the list of commands we take from the User interface  will include psudo-code-like "FOREACH/ENDFOR" commands, similar to jinja etc (but way more simplistic)
        # we  want to be able to perform the tasks between these FOREACH/ENDFOR tags, well, for each element within the input object (be that a list or a string)
        # the simplest way to handle this I could think of was to convert these sections of the command list to sublists within the main command list, rather than handle it at the input level in the UI part
        # I know this uses recursion and that's sometimes controversial but it works here, we're never going to have 1000 nested foor loops in a command list and for this purpose it just makes sense
        # I did not intend on making this eletist or unnessecarily complicated, if you can think of a nicer/simpler/easier to read way to do this with just for loops, let me know!
        out_list = []
        # fortag = False#pretty sure I don't need  this
        sublst = []
        forcount = 0
        for el in coms:
            if el == "FOREACH":
                # fortag = True#pretty sure I don't need  this
                forcount += 1  # using forcount to determine if this is a nested for loop
                if forcount > 1:
                    sublst.append(el)
            elif el == "ENDFOR":
                forcount -= 1  # using forcount to determine if this is a nested for loop
                if forcount == 0:
                    out_list.append(
                        self.parser(sublst)
                    )  # oooooh, recursion!!! (don't worry, it's not that scary, it just makes sense here)
                elif forcount > 0:
                    sublst.append(el)
            elif forcount > 0:
                sublst.append(el)
            else:
                out_list.append(el)
        return out_list

    def count_colons(self, word):
        return word.count(":")

    def call_task(self, task, working_text):
        tasks = self.available_tasks
        print(f"\ntask: {task} : colons : {self.count_colons(task)}")
        # count number of values passed to task (number of colons)
        if task.split(":")[0] not in tasks.keys():
            print(task, "not in keys!")

        if self.count_colons(task) == 0:
            working_text = tasks[task.split(":")[0]]["function"](working_text)
        elif self.count_colons(task) == 1:
            working_text = tasks[task.split(":")[0]]["function"](
                working_text, task.split(":")[1]
            )
        elif self.count_colons(task) == 2:
            working_text = tasks[task.split(":")[0]]["function"](
                working_text,
                task.split(":")[1],
                task.split(":")[2],
            )

        return working_text
        # this function massively reduces the code needed in run_queue, and is better at DRY
        # however, it has removed the functionality of using named 'arguments' - so the code creating tasks will
        # need to carefully enforce the order of 'arguments' passed to the task
        # i.e. in TASKNAME:arg1:arg2 must match order of the called function

    def run_queue(self, queue, in_text = None, debug=False):
        working_text = in_text

        for task in queue:
            if isinstance(task, list):
                # this is a FOREACH section, recursively call again on this
                intermediary = []

                for el in working_text:  # where task is a sublist of tasks
                    intermediary.append(
                        self.run_queue(task, el)
                    )  # this is either action on each char or list element, and either outputs a list or string
                    # however, to make it possible to manage, the intermediary is always a list, so if user is not careful, they could get lists of lists
                    # some thought is needed in how to guide the user to avoid this so they don't make broken task queues
                    if debug:
                        print(task, working_text)
                working_text = intermediary
            # --------------------------------------------------------------------------------------
            elif task.split(":")[0] in self.available_tasks.keys():
                # task is valid, process using dictionary
                working_text = self.call_task(task, working_text)

            if debug:
                print(task, working_text)

        return working_text

    def count_args(func):
        pass  # count the args in func based on .__annotations__
