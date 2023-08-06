# Expression

## About

Serialize and deserialize nested compound expression strings such as `(a = 1 or (b = 2 and c = 3))` into parsable expression trees such as `[key:a operator:= value:1, conjunction:or, [key:b operator:= value:2, conjunction:and, key:c operator:= value:3]]`.

You may want to:-
- provide an easy to configure filter on an endpoint such as `GET /services?filter=(price lt 200 and duration is 2hrs)`.
- build an ORM filter based on the expression.
- simply evaluate that an expression is `True` or `False`.

These sets of classes make few assumptions as to how conditions will be evaluated. It lets the author configure handlers that can be used to resolve conditions.

## Install

- [ ] Todo

## Configure

## Use

Deserialize a string into a tree of conditions.

```python
expression = Expression('(a = 1 and b = 2)')
conditions = expression.to_conditions()

print(conditions.conditions[0].key))        # a
print(conditions.conditions[0].operator))   # =
print(conditions.conditions[0].value))      # 1

print(conditions.conditions[1].value))      # and

print(conditions.conditions[2].key)))       # b
print(conditions.conditions[2].operator))   # =
print(conditions.conditions[2].value))      # 2
```

Evaluate an expression such `date date_between 2020-09-26,2020-09-28` as a boolean.

Instantiate the Evaluate object, passing through resolved expression arguments. In this case the `date` key will be resolved to a date object of `2020-09-27`.

```python
evaluate = Evaluate({
    "date": datetime.strptime("2020-09-27", '%Y-%M-%d')
})
```

Before evaluating ensure that the `date_between` expression can be handled by a designated Handler such as `DateBetweenHandler`.
```python
evaluate.add_condition_handlers({
    'date_between': DateBetweenHandler
})
```

Now evaluate the expression from string.
```python
result = evaluate.from_expression('date date_between 2020-09-26,2020-09-28')
self.assertTrue(result)
```

You can plug in any custom handler to suit the usecase.
```python
class DateBetweenHandler(Handler):

    def handle(self, condition):
        key = self._data.get(condition.key)

        values = condition.value.split(',')
        date1 = datetime.strptime(values[0], '%Y-%M-%d')
        date2 = datetime.strptime(values[1], '%Y-%M-%d')

        return date1 <= key <= date2
```

## Contribute

### Running tests
```
coverage run -m unittest2 discover -p="*Test.py"
coverage html
```

or use

```
bash bin/run-tests
```

```
bash bin/run-tests *Test.py
```