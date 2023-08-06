##############
Right Triangle
##############

Simple Python package that can be used to do calculations with
right-angled triangles.

Installation
============

Use pip to install right-triangle.

.. code-block:: shell

    pip install right-triangle


Usage
=====

The RightTriangle class
-----------------------

A RightTriangle instance is a representation of a right-angled triangle.

It has 6 attributes:

* side_a - first leg, the length of the side opposed to angle_a
* side_b - second leg, the length of the side opposed to angle_b
* side_c - the length of the hypotenuse of the triangle
* angle_a - first acute angle, the angle opposed to side_a, measured in degrees
* angle_b - second acute angle, the angle opposed to side_b, measured in degrees
* angle_c - the right angle, always 90 degrees

You can instantiate a RightTriangle with one of the following information:

* The lengths of any two sides of the triangle
* One angle (in degrees) and the length of one side of the triangle

You can use either a specialised factory method (.from_*)
or the universal one (.make) to construct an instance.

During the instantiation the other attributes are calculated and become
accessible.

.. code-block:: python

    >>> from right_triangle import RightTriangle
    >>> rt1 = RightTriangle.from_side_a_and_side_b(3, 4)
    >>> rt2 = RightTriangle.make(side_a=3, side_b=4)
    >>> rt1.side_c
    5.0
    >>> rt2.side_c
    5.0

Functions
---------

The module also provides some functions. You can use them to calculate some
attributes of a right triangle without actually instantiating a *RightTriangle*
object.

.. code-block:: python

    >>> import right_triangle
    >>> right_triangle.calculate_hypotenuse_from_legs(3, 4)
    5.0
    >>> right_triangle.calculate_acute_angles_from_legs(3, 4)
    (36.86989764584402, 53.13010235415598)
    >>> right_triangle.calculate_leg_from_other_leg_and_hypotenuse(3, 5)
    4.0
    >>> right_triangle.calculate_leg_from_hypotenuse_and_opposed_angle(5, 36.8699)
    3.000000164351089
    >>> right_triangle.calculate_leg_from_other_leg_and_adjacent_angle(4, 53.1301)
    3.000000256798589
