# NOnion

NOnion is a Python package that provides tools for Functional Programming. It aims to eliminate nested function calls such as **z(g(f(x)))** which remind an *onion*.

# Installing

```bash
pip install nonion
```

# Tutorial

NOnion consists of two main concepts:

* *Function* - a wrapper of **any** Python *Callable*,
* *Pipeline* - a wrapper of **any** Python *Iterable*.

## *Function*

In order to create a *Function*, you simply pass any *Callable*:

```python
f = Function(lambda x: x + 1)
f(5) # returns 6
```

You can also create an identity *Function*:

```python
g = Function()
```

Notice, that a *Function* takes exactly single value and returns exactly single value.

### compose

A ``Function composition" defined as $( f \circ g )(x) = f(g(x))$ could be done in the following way:

```python
z = f @ g

# alternatively

z = f.compose(g)
```

You can also use *compose* several times:

```python
z = f @ g @ f
```

Instead of wrapping each *Callable* with a *Function*, you can wrap only __first__ *Callable* and use *compose* on the rest.

```python
def f(x):
  return x + 1

g = Function() @ (lambda x: x * 2) @ f
g(5) # returns 12
```

The *@* (at) operator was used, because it reminds $\circ$ symbol.

### then

Function composition sometimes might be hard to read, because you have to read it from right-to-left.
In order to achieve better readability, you can use *then*.

```python
g = Function() / (lambda x: x * 2)  / f
g(5) # returns 11

# alternatively

g = Function().then(lambda x: x * 2).then(f)
g(5) # returns 11
```

The */* (slash) operator was used, because it reminds *|* (vertical bar) used for piping.

### call

Sometimes you want to call a function ``inline'' after several compositions. In this case, you might use:

```python
(Function() / (lambda x: x * 2)  / f)(5) # returns 11
```

But it might be hard to read. Especially, when you mostly pass lambdas. A better way to call a function is by using:

```python
Function() / (lambda x: x * 2)  / f & 5 # returns 11
```

The *&* (ampersand) operator was used, because it looks similar to *$* (dollar), which is a Haskell operator.

### star (function)

Suppose, that you defined a function with multiple arguments such as:

```python
def f(x, y):
  return x + y * x
```

And you want to wrap that function using Function. In this case, you have to use *star*.

```python
Function() @ star(f) & (1, 2) # returns 5
```

*star* simply passes arguments to a function using Python *\** (star) operator.

### foreach

You can also call a function for each value in some *Iterable* in the following way:

```python
ys = Function() / (lambda x: x * 2)  / (lambda x: x + 1) * range(5)

for y in ys:
  print(y)

# 1
# 3
# 5
# 7
# 9
#
```

The *\** (star) operator was used, because instead of passing an *Iterable* to a function, you pass its content as with Python *\** (star) operator and functions that take *\*args*.

## Pipeline

In order to create a *Pipeline*, you simply pass any *Iterable*:

```python
xs = Pipeline(range(5))

# notation abuse, do not use that:

xs = Function() / Pipeline & range(5)
```

You can also create an empty *Pipeline*:

```python
xs = Pipeline()
```

Under the hood Pipeline is simply uses *iter* on a passed *Iterable*. It means, that if you will pass an *Iterable*, that could be exhausted, you iterate over *Pipeline* only once.

```python
xs = Pipeline(range(2))

for x in xs:
  print(x)

# 1
# 2
#

# perfectly fine, because range(x) returns a special object
for x in xs:
  print(x)

# 1
# 2
#

xs = Pipeline(x for x in range(2))

for x in xs:
  print(x)

# 1
# 2
#

# xs already exhausted
for x in xs:
  print(x)
```

### map

*map* allows you to call a *Callable*, which takes a single value and returns a single value, on each value of the *Pipeline*.

```python
ys = Pipeline(range(3)) / (lambda x: x + 1) / (lambda x: (x, x + 1)) / star(lambda x, y: x + y * x)

for y in ys:
  print(y)

# 3
# 8
# 15
#

# alternatively

ys = Pipeline(range(3)).map(lambda x: x + 1).map(lambda x: (x, x + 1)).map(star(lambda x, y: x + y * x))
```

The */* (slash) operator was used, because it reminds *|* (vertical bar) used for piping.

### filter

*filter* allows you to filter *Pipeline* values.

```python
ys = Pipeline(range(3)) % (lambda x: x > 1)

for y in ys:
  print(y)

# 2
#

# alternatively

ys = Pipeline(range(3)).filter(lambda x: x > 1)
```

### flatmap

*flatmap* allows you to call a *Callable*, which takes a single value and returns an *Iterable*, on each value of the *Pipeline* and flatten results into single *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) * (lambda x: (x, x + 1))

for y in ys:
  print(y)

# 1
# 2
# 2
# 3
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).flatmap(lambda x: (x, x + 1))
```

The *\** (star) operator was used, because intuitively you use Python *\** (star) operator on each result.

### apply

*apply* allows you to call a *Callable*, which takes an *Iterable* and returns an *Iterable*, on whole *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) // tuple # internally Pipeline now has a tuple

for y in ys:
  print(y)

# 1
# 2
#

# now multiple itertations is possible
for y in ys:
  print(y)

# 1
# 2
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).apply(tuple)
```

### collect

*collect* allows you to call a *Callable*, which takes an *Iterable* and returns any single value, on whole *Pipeline*. The difference between *apply* and *collect* is that *collect* returns the result of a function instead of wrapping it with *Pipeline*.

```python
ys = Pipeline(range(2)) / (lambda x: x + 1) >> tuple
print(ys)

# (1, 2)
#

# alternatively

ys = Pipeline(range(2)).map(lambda x: x + 1).collect(tuple)
```

### foreach

*foreach* allows you to call a *Callable*, which takes a single value, on each value of the *Pipeline*.

```python
Pipeline(range(2)) / (lambda x: x + 1) & print

# 1
# 2
#

# alternatively

Pipeline(range(2)).map(lambda x: x + 1).foreach(print)
```
