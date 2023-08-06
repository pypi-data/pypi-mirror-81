
Const Protocols
===============

Python is inherently mutable, only a handful of builtin classes enjoy true
immutability such as ``int``\ , ``str``\ , and ``tuple``\ ; everything else is up for
grabs. This allows a lot of clever tricks, but it also leads to some
difficult bugs. Just think about code like this:

.. code-block:: python

   class MyClass:

       def __init__(self) -> None:
           self._mylist: List[str] = []

       def get_mylist(self) -> List[str]:
           return self._mylist

What happens when someone gets that list and mutates it? Of course, you get
bugs because MyClass now has something it doesn't expect. The easiest way to
fix that is of course to do this:

.. code-block:: python

   class MyClass:

       def __init__(self) -> None:
           self._mylist: List[str] = []

       def get_mylist(self) -> List[str]:
           return self._mylist.copy()

Problem solved, right? What if _mylist has a million entires? That can
quickly become a huge bottle neck in your program. In most statically typed
languages you have some kind of "const" or "immutable" modifier that tells
the compiler/interpreter "don't let anyone modify this". Normally that would
be impossible in python, but we have static type checkers like mypy, and
Protocols. We can create a protocol that implements all of the methods that
don't mutate a class, and expose only those. Then the static type checker can
catch the mutation for us.

.. code-block:: python

   from constprotocol import ConstList

   class MyClass:

       def __init__(self) -> None:
           self._mylist: List[str] = []

       def get_mylist(self) -> ConstList[str]:
           return self._mylist

   c = MyClass()
   c.get_mylist().append('foo')  # Error: ConstList has not method append!

Of course, the underlying python values have not actually become immutable,
but like C and C++ it's more of a promise that if you take a ConstList or
return one that you're not going to modify it.

One of the goals of const protocol is to have 0 runtime performance impact. You
could create an immutable proxy, that wraps a value and only exposes it's const
methods, and all of it's attributes as read only (using properties and more
proxies). But that has runtime overhead and adds code complexity. This approach
adds zero run time overhead and very little complexity to the code.

What if I want to mutate the value after all?
---------------------------------------------

You don't.

No seriously, if you say you're not going to modify it, don't.

What you probably want to do is copy the constified value, which will give
you a mutable value:

.. code-block:: python

   l: ConstList[str] = ['a', 'b', 'c']
   ml = l.copy()
   reveal_type(ml)

Which will be ``List[str]``

If you really, really, need to, you can use ``typing.cast``. of course, you get
to keep the pieces.

Status
------

Right now there are four classes ``ConstSet`` for ``set``\ , ``ConstList`` for
``list``\ , ``ConstMapping`` for ``mappings``\ , and ``ContDict`` for ``Dict``. There's
likely bugs, this is alpha quality software, and a kind of crazy idea to get
better error checking in cases where the author knows that someone shouldn't
be mutating their data.

I found a bug
-------------

Cool, file an issue.

I want fix something or add something
-------------------------------------

Even better, open a Merge Request
