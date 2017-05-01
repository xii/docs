abstract IO mixin
^^^^^^^^^^^^^^^^^

This class implements IO functionality without the need to know
wether the host used is localhost or any remote host.

The only function which is required to work properly is the same
as for the `NeedLibvirt` mixin.

.. code-block:: python

    @abstractmethod
    def get_virt_url(self):
        pass

**This method is already defined by default within the Attribute base class.
You can overwrite as you like.**

.. note:

  Never use python builtin io methods unless your are sure you want to work 
  only on localhost (Think about if the attribute/command/component can also
  work on remote hosts aswell or not).

.. autoclass:: xii.need.NeedIO
   :members:


Every connection object comes with a set of default implmented function which 
can be used.

Every connection object implements:

.. autoclass:: xii.connection.Connection
  :members:
