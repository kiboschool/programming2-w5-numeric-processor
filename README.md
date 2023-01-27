# Numeric Processor

Imagine that you are working in a scientific laboratory.

First, your equipment performs measurements, and creates digital files containing data. You then need to run mathematical computations on this data for the scientists to determine the results of their experiment. One of your computer systems produces the list of computations that need to be done, creating a file with contents like this,

```
{
    "computations":
    [
        ["add", "16.393504", "41.838937"],
        ["multiply", "ANS", "14.8865938"],
        ["subtract", "ANS", "28.911410"],
        ["display", "ANS"]
    ]
}

```

The special string `ANS` means that you should use result of the previous computation that was done.

You will build a Python program to read a file like this, go through the list of computations, and display the result.

## Using cloud computation

For processing large amounts of data, programmers will sometimes send the data over the internet so that it can be processed by servers in the cloud, for example sending the data to servers set up by Amazon Web Services.

These dedicated servers can be faster and more cost-effective for programmers, because it is expensive to set up and maintain your own group of servers.

As described later, your program will similarly be able to offload processing to an online server, by connecting to a real API.

## Details

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

After each, the result should be stored, so that in the next line that comes up, `ANS` can be used to refer to the last result.

You will also support the operation `api-compute`.

```
{
    "computations":
    [
        ["api-compute", "45*(44.847626-24.022232)"],
        ["display", "ANS"]
    ]
}

```

This can be done by sending the string with an api call to mathjs.org. For example, to compute `45*(44.847626-24.022232)`, read the results of a GET sent to `http://api.mathjs.org/v4/?expr=45*(44.847626-24.022232)`.

## What you'll do

You need to create classes and methods with the exact names mentioned here.

It's recommended to follow these steps to solve the problem,

* Open numeric_processor.py and create a new empty class called NumericProcessor
* Create a `__init__` method that receives self and a filename
* Open the file and load json from it
* Get the list of computations from the results of loading the json
* Store this list as an attribute
* Write a `run_computations` method that does this:
    * For each entry in the list that was stored, pass it to a `run_computation` method:
        * This method checks the computation name and calls a corresponding method,
        * So your class should have a `add` method, a `subtract` method, etc.

Now, make it possible for computation to refer to the previous result as `ANS`. Tip: using an attribute on the class would be one way to do this.

The `NumericProcessor` should now work for basic input.

## Adding the online feature

Now create a class `NumericProcessorWithCloudComputation` that inherits from `NumericProcessor`.

A good way to add the feature is this:

* First write a new `send_to_api` method on the child class
    * it takes a string expression, which could be '1+1'.
    * build a url string like this, `http://api.mathjs.org/v4/?expr=1+1`.
    * use `urlopen` to send the request to the server.
    * the results don't come back as json, all we need is response.read().
    * use `float()` on the results to get a number back.
* Write a `run_computation` method (which overrides the parent class `run_computation` method)
    * if the type is `api-compute`, send it to the new `send_to_api` method
    * if the type is not `api-compute`, call the parent class's version by calling `super().run_computation(self ...)`

When you're done, both classes, NumericProcessor and NumericProcessorWithCloudComputation, should work for basic input. And NumericProcessorWithCloudComputation should work for basic input and the `api-compute` operation.

## Example

When you run your program on `example.json`, the answer shown should be `76.87316`.


