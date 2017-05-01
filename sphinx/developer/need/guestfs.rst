guestfs mixin
^^^^^^^^^^^^^

To use the guestfs feature you need to add the `NeedGuestFS` Class to your
class.

To use the class one method is required to work properly:

.. code-block:: python

  @abstractmethod
  def get_tmp_volume_path(self):
      pass

A default implementation is provided by the NodeAttribute class.

The implementation looks like:

.. code-block:: python

    def get_tmp_volume_path(self):
        return self.other_attribute("image").get_tmp_volume_path()

This module starts guestfs copies the selected image to a temporary
path and starts the guestfs vm. To make sure the class works as intended,
guestfs only works when in the image is not used yet (since it works on a tmp
image all changes are missed if the domain was already started).

You may want to checkout the guestfs documentation, too

.. autoclass:: xii.need.NeedGuestFS
   :members:
