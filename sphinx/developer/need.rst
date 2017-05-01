Special mechanics (need mixin)
================================

To gain more flexibility every special functionality is packaged in his own
class. All special classes are prefixed with `Need`.

Available special classes are:

.. toctree::
  :maxdepth: 2

  need/libvirt
  need/guestfs
  need/io
  need/ssh

If a additional functionality is required (for io for example) it can be added
like:
::
  from xii.attribute import Attribute
  from xii.need import NeedIO

  MyAttribute(Attribute, NeedIO):
    # do something useful

Every class has requirements which must be met to make it work. Requirements
are all defined as abstract functions which must be defined to work.

You can also chain multiple need classes together if you require more than one
extra functionality.

For a more practical approach you can checkout all bultin attributes.

Example hostname attribute:
::

  from xii.need import NeedGuestFS
  from xii.validator import Bool
  from xii.components.node import NodeAttribute


  class HostnameAttribute(NodeAttribute, NeedGuestFS):
      atype = "hostname"
      requires = ["image"]
      defaults = True
  
      keys = Bool(True)
  
      def spawn(self):
          if not self.settings():
              return
  
          name = self.component_entity()
  
          for replace in ["#", "."]:
              name = name.replace(replace, "-")
  
          self.say("setting hostname to {}...".format(name))
          self.guest().write('/etc/hostname', name)
