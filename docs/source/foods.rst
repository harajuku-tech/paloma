=================================
Sample : Foods
=================================


Models
========

Target
--------

.. _app.foods.models.Customer:

Customer
^^^^^^^^

Customer is a profile information for signed-up Django User.

.. autoclass:: app.foods.models.Customer
    :members:

.. _app.foods.models.Shop:

Shop
^^^^^^^^

Shop is a profile information for a :ref:`paloma.models.Group` defined by :ref:`paloma.models.Owner`.

.. autoclass:: app.foods.models.Shop
    :members:


Owner
-------

.. _app.foods.models.Company:

Company
^^^^^^^^

Company is bound to :ref:`paloma.models.Owner`.
Comapny is a chainstore and has many :ref:`app.foods.models.Shop` s to sell :ref:`app.foods.models.Product` s.

.. autoclass:: app.foods.models.Company
    :members:


Promotion Material
-------------------

.. _app.foods.models.Product:

Product
^^^^^^^^

:ref:`app.foods.models.Company` sells many Products.

.. autoclass:: app.foods.models.Product
    :members:

.. _app.foods.models.Promotion:

Promotion
^^^^^^^^^^^^^^^^

:ref:`app.foods.models.Product` can execute many Promotions.
A Promotion can be bound to :ref:`paloma.models.Schedule` of sending emails to members in :ref:`paloma.models.Group`.

.. autoclass:: app.foods.models.Promotion
    :members:

.. _app.foods.models.GoldPromotion:

GoldPromotion
^^^^^^^^^^^^^^^^

:ref:`app.foods.models.Product` can also execute many GoldPromotions.
A GoldPromotion can be bound to :ref:`paloma.models.Schedule` of sending emails to members in :ref:`paloma.models.Group`.

.. autoclass:: app.foods.models.GoldPromotion
    :members:

.. _app.foods.models.Price:

Price
^^^^^^^^^^^^^^^^

:ref:`app.foods.models.Product`' Price can vary from each :ref:`app.foods.models.Shop`.

.. autoclass:: app.foods.models.Price
    :members:

ER
----

.. include:: foods_models.dot

