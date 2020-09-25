from ferris_cli.ferris_cli import ExecutionTime
from ferris_cli.ferris_cli import MetricMessage
from ferris_cli.ferris_cli import MetricsAPI

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
print(e.logtime_data)

for k1 in e.logtime_data.keys():
		for k2 in e.logtime_data[k1].keys():
			print(f"{k1}.{k2}={e.logtime_data[k1][k2]}")
			mm = MetricMessage(f"{k1}.{k2}",f"{e.logtime_data[k1][k2]}")
			MetricsAPI().send(mm)

## {'foo': {'times_called': 1, 'total_time': 0.0745, 'average_time': 0.0745}, 'bar': {'times_called': 3, 'total_time': 0.2054, 'average_time': 0.0685}}
