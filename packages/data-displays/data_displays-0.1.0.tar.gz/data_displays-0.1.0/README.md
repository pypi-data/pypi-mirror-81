## data_displays
### Asynchronus loading bars and more
Example:
```
from data_diplays import data

if __name__ == "__main__":
	from os import get_terminal_size
	from time import sleep
	
	data.bar.create("Download progress", duration=10, length=get_terminal_size()[0], lineno=1, size=250, unit="kb")
	data.bar.create("Working", duration=5, length=50, lineno=3, size=125, unit="bytes")
	data.bar.create("Decoding text", duration=5, length=25, lineno=5, size=2000)
	sleep(3) # wait one second
	data.bar.create("Uploading data", duration=10, length=15, lineno=7)
	data.wait() # Wait until all displays are complete (This is absolutely necessary. It must be called after all the displays are created.)
	print("Done!")
```