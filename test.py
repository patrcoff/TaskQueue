from TaskQueue import TaskQueue


def f1(temp_null_arg):
    print('first example')

definition = {'f1':{'function':f1}}

tq = TaskQueue.TaskQueue(definition)

tq.run_queue(tq.parser(['f1','f1']),None)
