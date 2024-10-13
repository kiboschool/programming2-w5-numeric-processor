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
        {"operation": "api-compute", "values": ["5*(4.847626-2.022232)"]}
        {"operation": "display", "values": ["ANS"]}
    ]
}
```

(The special string `ANS` means that you should use result of the previous computation that was done. The `api-compute` operation is a special operation that connects to an online server to do the computation - more on that later.)

You will build a Python program to read a file like this, go through the list of computations, and display the result.
<img src="calc.png" width="10%" height="10%" style="border:none, border-width: 0, border: 0; box-shadow: 0px 0px;" />
Here is a sample input file:

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

If the program recieved the example above, it would do the following:

- Run `6.393504 + 1.838937` and store the result `8.232441`.
- Run `ANS * 4.659381`, which is `8.232441 * 4.659381`, and store the result `38.35808`.
- Run `ANS - 8.91141`, which is `38.35808 - 8.91116`, and store the result `29.446919`.
- Show the result `29.446919`.

### Using cloud computation

For processing large amounts of data, programmers will sometimes send the data over the internet so that it can be processed by servers in the cloud, for example sending the data to servers set up by Amazon Web Services.

These dedicated servers can be faster and more cost-effective for programmers, because it is expensive to set up and maintain your own group of servers.

You will add a `"api-compute"` instruction that sends the string with an api call to mathjs.org. A helper function is already there to create the url you will send to that server.

<img src="cloud.png" width="10%" height="10%" style="border:none, border-width: 0, border: 0; box-shadow: 0px 0px;" />

Here is a sample input file:

```
{
    "computations": [
        {"operation": "api-compute", "values": ["5*(4.847626-2.022232)"]}
        {"operation": "display", "values": ["ANS"]}
    ]
}

```

If the program recieved the example above, it would do the following:

- Call the mathjs.org API and send the operation `"5*(4.847626-2.022232)"`
- Store the result `14.12697`.
- Show the result `14.12697`.

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

"api-compute"
    receives a string, send it to the mathjs.org api and store the result

"display"
    receives one number, show it to the screen using print
```

After each operation, the result should be stored, so that in the next line that comes up, `ANS` can be used to refer to the last result.

### Task 1: Writing `run_computations`

> _You'll need to use the exact names mentioned here. The automated tests in this project will pass when your code is working as expected._

You can follow these steps:

* Open `numeric_processor.py`
* See that the `NumericProcessor` has an `__init__` method. This method stores `self.computations_list`.
* `computations_list` is a list of dictionaries. Each dictionary has a `operation` and a `values`.
* Write a `run_computations` method that does this:
  * For each element in `self.computations_list`, pass the element to a `run_one_computation` method:
    * This method looks at the element's type `computation['operation']` and calls a corresponding method and passing the values `computation['values']`.
    * So your class should have methods for all the supported operations like addition, subtraction, etc.
* You should read `load_computations_list_from_file` and understand what it does, but you don't need to make any changes.
* Use the example code at the bottom of the file to run the program.

You can place `print` calls to check that it is running correctly. The program should now be able to run this json file:

```
{
    "computations":
    [
        {"operation": "add", "values": ["1", "2"]}
    ]
}
```

Then, make it possible for computation to refer to the previous result as `ANS`. Tip: storing the result as an attribute on the class would be a good way to do this.

Once you are confident that the `add` method works, you can move on to the other methods and add a display method.

When `ANS` works, you are able to run the `example.json` file. The code to load computations from a file is given to you at the bottom of the file.

### Task 2: Adding the online feature

- There's code given to you to create the URL for the API call to the mathjs api. (`get_mathjs_api_url` already works, you don't need to change it).
- You will write a new `send_to_api` method on the class
  - It should takes a string parameter, a string like `'1+1'`.
  - It should use the provided `get_mathjs_api_url` helper function to get the url.
  - Use `urllib.request.urlopen` on the url to get a `response`.
  - Use `response.read().decode('utf-8')` to get a result.
  - Use `float(result)` to turn the result into a float (in other words, a number).
  - Return the number.
- Update the `run_one_computation` method to look for `"api-compute"`. If that is the operation, send the first value to this new `send_to_api` method and store the result.

The `NumericProcessor` should now be able to run the `example_api.json` file.

### Task 3: Adding a mode that gathers statistics

Use **class inheritance** to add the ability to run in a different mode that gathers statistics.

- Create a class called `OperationCounterNumericProcessor` that inherits from `NumericProcessor`.
- Create a `__init__` method that receives a list of computations (a parameter called `computations_list`).
  - In this method, add `super().__init__(computations_list)` to call the parent class's init.
  - In this method, create a dictionary called `self.count_operations`.
- Create a `run_one_computation` method that receives a computation.
  - This method overrides the parent class `run_one_computation`.
  - Use the `count_operations` dictionary to keep track of how many times each type of operation is seen.
  - Use `super().run_one_computation(computation)` so that it still calls the parent class method.
- Create a `show_statistics` method.

  - It will loop through `self.count_operations`
  - For each type of operation, show the count.
  - It would show, for example

```
operation: subtract, count: 2
operation: multiply, count: 1
operation: display, count: 1

```

You can now change the test code at the bottom of the file. You can create an instance of `OperationCounterNumericProcessor` and use it just like `NumericProcessor`. At the end, you can call `show_statistics` on the instance and see the counts.

## Correctness Rubric

| Points | Criteria                           | Description                                                                                         |
| ------ | ---------------------------------- | --------------------------------------------------------------------------------------------------- |
| 6      | Simple computation                 | Program can add two numbers and show the result                                                     |
| 18     | All operations supported           | Program can add (4.5 points), subtract (4.5 points), multiply (4.5 points), and divide (4.5 points) |
| 1.5    | Display                            | Program supports more than one display in an input file                                             |
| 1.5    | Simple api call                    | Program can run a simple api call                                                                   |
| 1.5    | More-complicated api call          | Program can run a more-complicated api call                                                         |
| 1.5    | `OperationCounterNumericProcessor` | Program can count how many times operations were run                                                |

### Additional Challenges (Optional)

- The string sent to `api-compute` can contain `ANS`.
  - Before sending to the api you would replace `ANS` with the last result.
- Create a `BenchmarkOperationsNumericProcessor` class that inherits from `NumericProcessor`.
  - It measures the average duration for each type of operation.
  - Refer to the reflex-typing-speed project from Programming 1 for how to use `time.time()` to measure how long something takes.
  - It would show, for example, `operation: api-compute, average duration: 0.4564`.
