# Project with Lesson 17 - Calling Functions 
### Part 1: 

##### Learning Objectives: 

1. Define what a function is in the context of function calls 
2. List the components of a function call 
3. Interpret documentation for function calls 
4. Create programs with function calls 



##### Lesson Refresher: 
**A function is a reusable, easily accessible chuck of code.** 
Each function has a few parts: 
- Name

   This is what you refer to the function as in your code
- Return Value

    This is what the function returns. A function always returns a value, even if that value is None. 
- Arguments (optional) 

    Not every function has arguments. If it does, arguments are values that you as the programmer provide when you call the function. These values will be used in the function.
    
To call a function you absolutely need two components: the function name and the parentheses () after the name. If a function accepts arguments, you place the arguments inside the parentheses.  

Let’s look at a Designer function and its documentation as an example.
**insert documentation for line()** 

`line(start: int, end: int, thickness: int, color): Line`

`line` is a function that will create a line on the screen. The function `line` has six parameters. When you call the function, you place the parameters in the parentheses in the order they are explained in the documentation. 
1. start_x is the first argument, an int representing the x position of the starting point of the line the function will make. 
2. start_y is the second argument, an int representing the y position of the starting point of the line the function will make. 
3. end_x is the third argument, an int representing the x position of where the line will stop.
4. end_y is the fourth argument, an int representing the y position of where the line will stop
5. thickness is an int that represents how thick the line will be in pixels
6. color is a string that represents the color the line will be. 

`line` also has a return value: a Line. This returns the Line the function creates based on your arguments. 

Say we want to draw a green line from (0, 0) to (100, 100) on the screen, that is a little thick (10 pixels thick). This is what the function call would look like: 

`line(0, 0, 100, 100, 10, ‘green’)`

Now it’s your turn! Take a look at `mock_functions.py`
Play around with the code - change some of the arguments or the order of the function calls
and see how the output changes! 

Once you're familiar with the code, complete the following instructions. 
Your assignment is to: 
- Note how many function calls there are in the program
    - For each function call: 
        - Explain what the function does (What is its purpose?) 
        - Note any arguments and what the arguments represent 
        - Identify the return value 

### Part 2: 

Let’s transform this moving circle into something a little more recognizable. Your task is to: 

- Stop the circle from moving

- Add your own function calls to make the circle into an emoji  

- Extra credit: check out the other Designer functions and make the entire emoji move! 
