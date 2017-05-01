libvirt mixin
^^^^^^^^^^^^^

The libvirt need class provides access to libvirt connection object which is
allready initialized when used in this context.

There is only one method which needs to be defined.

.. code-block:: python

    @abstractmethod
    def get_virt_url(self):
        pass

**This method is already defined by default within the Attribute base class.
You can overwrite as you like.**

If you need help with libvirt's API checkout the Documentation. This can also be
troublesome since the full documentation sadly is not available for the python
bindings.

You always can inspect the objects by using the `pdb` inline debugger.

.. code-block:: python

  from xii.attribute import Attribute
  from xii.need import NeedLibvirt

  SampleAttribute(Attribute, NeedLibvirt):
    def spawn(self):
      domain = self.get_domain(self.component_name())
      import pdb; pdb.set_trace()

.. autoclass:: xii.need.NeedLibvirt
   :members:
