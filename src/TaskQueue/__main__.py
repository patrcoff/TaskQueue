from TaskQueue import TaskQueue
#from TaskQueue import builtin_functions as bf
#from inspect import getmembers, isfunction   

#THIS IS USED FOR TESTING THE MODULE USNIG THE MODULE SCRIPT COMMAND: 'test-TaskQueue'
#OTHERWISE IT'S TOO EASY TO MIX UP HOW THE IMPORTS SHOULD WORK WHILE WORKING WITHIN THE MODULE DIR
#THERE IS NO CURRENT OTHER PURPOSE TO THE MODULE'S SCRIPT
#IN FUTURE MAY ADD CMDLINE ARGS OF TASKS WHICH COULD ALLOW AD-HOC SEQUENCES OF BUILTINS

def f1(temp_null_arg):
    print('first example')


def main():  
    #definition = TaskQueue.load_module([])


    #print(definition)

    tq = TaskQueue.TaskQueue()
    print('AVAILABLE TASKS:',tq.available_tasks)
    tq.run_queue(tq.parser(['test_func','test_func']))

if __name__ == '__main__':
    main()