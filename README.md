# Numeric Processor

Imagine that you are working in a scientific laboratory.

Your equipment performs measurements, and creates digital files containing data. You then need to run mathematical computations on this data, for the scientists to determine the results of the experiment. One of your computer systems produces the list of computations that need to be done. It creates a json file with contents like this:

```
{
    "computations":
    [
        {"operation": "add", "values": ["6.393504", "1.838937"]},
        {"operation": "multiply", "values": ["ANS", "4.659381"]},
        {"operation": "subtract", "values": ["ANS", "8.91116"]},
        {"operation": "display", "values": ["ANS"]}
    ]
}
```

(The special string `ANS` means that you should use result of the previous computation that was done.)

You will build a Python program to read a file like this, go through the list of computations, and display the result.

If it recieved the example above, your program would do the following:

* Run `6.393504 + 1.838937` and store the result `8.232441`.
* Run `ANS * 4.659381`, which is `8.232441 * 4.659381`, and store the result  `38.35808`.
* Run `ANS - 8.91141`, which is `38.35808 - 8.91116`, and store the result  `29.446919`.
* Show the result `29.446919`.

### Using cloud computation

For processing large amounts of data, programmers will sometimes send the data over the internet so that it can be processed by servers in the cloud, for example sending the data to servers set up by Amazon Web Services.

These dedicated servers can be faster and more cost-effective for programmers, because it is expensive to set up and maintain your own group of servers.

As described later, your program will similarly be able to offload processing to an online server, by connecting to a real API.

<img src="cloud.png" width="10%" height="10%" style="border:none, border-width: 0, border: 0; box-shadow: 0px 0px;" />

### Requirements

These are the types of processor operations that you should support, and what they should do.


```
"add"
    receives two numbers, add them
    
"multiply"
    receives two numbers, multiply them
    
"subtract"
    receives two numbers, subtract them
    
"divide"
    receives two numbers, divide them
    
"display"
    receives one number, show it to the screen using print
```

After each operation, the result should be stored, so that in the next line that comes up, `ANS` can be used to refer to the last result.

You will also support the operation `"api-compute"`.

```
{
    "computations": [
        {"operation": "api-compute", "values": ["5*(4.847626-2.022232)"]}
        {"operation": "display", "values": ["ANS"]}
    ]
}

```

You will make`"api-compute"` send the string with an api call to mathjs.org. A helper function is already there to create the url you will send to that server.

<img src="calc.png" width="10%" height="10%" style="border:none, border-width: 0, border: 0; box-shadow: 0px 0px;" />

### What you'll do

> *You'll need to use the exact names mentioned here. The automated tests in this project will pass when your code is working as expected.*

You can follow these steps:

* Open `numeric_processor.py`
* See that the `NumericProcessor` has an `__init__` method. This method stores `self.computations_list`.
* `computations_list` is a list of dictionaries. Each dictionary has a `operation` and a `values`.
* Write a `run_computations` method that does this:
    * For each entry in `self.computations_list`, pass the entry to a `run_computation` method:
        * This method looks at the computation name and calls a corresponding method and passing the `values`.
        * So your class should have a method for addition, a method for subtraction, etc.
        * Write a method for display.
* See the example code at the bottom of the file. You don't need to make any changes to `computations_list_from_file`.

Your program should now be able to run this json file:

```
{
    "computations":
    [
        {"operation": "add", "values": ["1", "2"]}
    ]
}
```

Next, make it possible for computation to refer to the previous result as `ANS`. Tip: using an attribute on the class would be a good way to do this.

The `NumericProcessor` should now be able to run the `example.json` file.

### Adding the online feature

* You will then write a new `send_to_api` method on the class
    * It should takes a string parameter, a string like '1+1'.
    * It should use the provided `get_mathjs_api_url` helper function to get the url. (The provided `get_mathjs_api_url` already works, you don't need to change it).
    * Use `urllib.request.urlopen` on the url to get a `response`.
    * Use `response.read().decode('utf-8')` to get a result.
    * Use `float(result)` to turn the result into a float (in other words, a number).
    * Return the number.
* Update the `run_computation` method to look for `"api-compute"`. If that is the operation, send the first value to this new `send_to_api` method and store the result.

The `NumericProcessor` should now be able to run the `example_api.json` file.

### Adding a mode that gathers statistics

Your program will also use **class inheritance** to be able to run in a different mode that gathers statistics.

* Create a class called `NumericProcessor_CountOperations` that inherits from `NumericProcessor`.
* Create a `__init__` method that takes a filename.
   * In this method, add `super().__init__(filename)` to call the parent class's init.
   * In this method, create a dictionary called `self.count_operations`.
* Create a `run_computation` method that takes a computation.
   * This method overrides the parent class `run_computation`.
   * Use the `count_operations` dictionary to keep track of how many times each type of operation is seen.
   * Use `super().run_computation(computation)` so that it still calls the parent class method.
* Create a `show_statistics` method.
   * It will loop through `self.count_operations`
   * For each type of operation, show the count.
  * It would show, for example
  
  ```
  operation: subtract, count: 2
  operation: multiply, count: 1
  operation: display, count: 1
  ```

You can now change the test code at the bottom of the file. You can now create an instance of `NumericProcessor_CountOperations` and use it just like  `NumericProcessor`. At the end, you can call `show_statistics` on the instance and see the counts.

## Rubric

Points | Criteria | Description
--------- | ------- | ---------
20 | Simple computation | Program can add two numbers and show the result
60 | All operations supported | Program can add (15 points), subtract (15 points), multiply (15 points), and divide (15 points)
5 | Display | Program supports more than one display in an input file
5 | Simple api call | Program can run a simple api call
5 | More-complicated api call | Program can run a more-complicated api call
5 | `NumericProcessor_CountOperations` | Program can count how many times operations were run

### Additional Challenges (Optional)

* The string sent to `api-compute` can contain `ANS`.
  * Before sending to the api you would replace `ANS` with the last result.
* Create a `NumericProcessor_BenchmarkOperations` class that inherits from `NumericProcessor`.
  * It measures the average duration for each type of operation.
  * Refer to the reflex-typing-speed project from Programming 1 for how to use `time.time()` to measure how long something takes.
  * It would show, for example, `operation: api-compute, average duration: 0.4564`.


