# simppl
package for writing simple command-line pipelines, and organized command-line tools
The package is composed of two seperate but intertwined python scripts:
1. simple_pipeline.py - defines SimplePipeline class
2. cli.py - defines CommandLineInterface class, and utility functions

## SimplePipeline
SimplePipeline conveniently enables turning a python cli script into a pipeline of os commands.
- It enables running os commands sequentially / concurrently.
- Each command / commands-batch is given an index.
- The user can run a sub-sequence of commands by specifying -fc (first_command) and -lc (last_command) flags.
- It is also possible to dry_run the pipeline using -d flag.
- Each command is printed before execution, and is also optionally timed.
- outputs/errors from sub-commands are collected and logged.

### Using SimplePipeline
SimplePipeline can be used together with CommandLineInterface, or independently. <br>
The simplest indepent usage will look like this:
~~~
from simple_pipeline import SimplePipeline
sp = SimplePipeline(debug=False, start=0, end=100):
sp.print_and_run('<YOUR_OS_COMMAND_HERE>)
~~~

## cli
CommandLineInterface enables turning a collection of python executable scripts into a unified cli.
- Creates a single entrypoint for running the command-line tools
- Standardized tool development and documentation
- adds a manual which lists all available tools and packages with minimal development overhead

### Using cli:
- example_module gives an example of how to use CommandLineInterface in your project
- requirements:
    - __main__.py - define toolbox logo, constructs and runs the CommandLineInterface. 
    - __init__.py - set logging configuration
    - logging_config.ini - python.logging configuration
    - tools - each script defined as command_line_tool will be automatically added to the toolbox
    

## Examples 
### Command-line-tool example:
- See example_module/add_two_numbers.py
~~~
python -m example_module add_two_numbers 5 6
~~~
- Should print 11.0 to stdout  
- Note how simple decoration of the run method accepting argv, added this script to the tools list
~~~
@command_line_tool
def run(argv):
~~~


### Example for running command-line-tool using SimplePipeline
~~~
python -m example_module analyze_file_pipeline resources/analyze_file_pipeline_input.txt test_outputs
~~~
- Should print the following (except date-time) to stdout:
~~~
python -m <module_name> analyze_file_pipeline  resources/analyze_file_pipeline_input.txt  test_outputs 
2020-09-11 14:31:05,639 - analyze_file_pipeline - INFO - 1) wc resources/analyze_file_pipeline_input.txt > test_outputs/wc.txt
2020-09-11 14:31:05,643 - analyze_file_pipeline - INFO - Time elapsed wc: 0 s
2020-09-11 14:31:05,643 - analyze_file_pipeline - INFO - 2) ls -l resources/analyze_file_pipeline_input.txt > test_outputs/ls.txt
2020-09-11 14:31:05,648 - analyze_file_pipeline - INFO - Time elapsed ls: 0 s
2020-09-11 14:31:05,649 - analyze_file_pipeline - INFO - 3) sed 's/\s/\n/g' resources/analyze_file_pipeline_input.txt | sort | uniq -c | sort -n > test_outputs/word_count.txt
2020-09-11 14:31:05,653 - analyze_file_pipeline - INFO - Time elapsed sed: 0 s
~~~
