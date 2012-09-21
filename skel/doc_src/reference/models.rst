===============
Model Reference
===============

ModelName
=========

.. py:class:: ModelName

   .. py:attribute:: parent
   
      :py:class:`TreeForeignKey` ``(self)``
   
      The category's parent category. Leave this blank for an root category.

   .. py:attribute:: name
   
      **Required** ``CharField(100)``
   
      The name of the category.

   .. py:attribute:: slug
   
      **Required** ``SlugField``
   
      URL-friendly title. It is automatically generated from the title.

   .. py:attribute:: active
   
      **Required** ``BooleanField`` *default:* ``True``
   
      Is this item active. If it is inactive, all children are set to inactive as well.

