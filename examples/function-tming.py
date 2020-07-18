from ferris_cli.ferris_cli import ExecutionTime


e = ExecutionTime()

@e.timeit
def foo(arg1):
  #do_something(arg1) 
  return 

@e.timeit
def bar():
  #hello_world()
  return

foo("dragons")
bar()
bar()
bar()
print(e.logtime_data)

## {'foo': {'times_called': 1, 'total_time': 0.0745, 'average_time': 0.0745}, 'bar': {'times_called': 3, 'total_time': 0.2054, 'average_time': 0.0685}}