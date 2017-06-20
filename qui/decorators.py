#!/usr/bin/env python3
''' Decorators wrap a `qui.models.PropertiesModel` in a class
containing helpful representation methods.
'''

import gi  # isort:skip
gi.require_version('Gtk', '3.0')  # isort:skip
from gi.repository import Gtk  # isort:skip

import qubesadmin
from qui.models.qubes import LABELS


class PropertiesDecorator():
    ''' Base class for all decorators '''

    # pylint: disable=too-few-public-methods

    def __init__(self, obj, margins=(5, 5)) -> None:
        self.obj = obj
        self.margin_left = margins[0]
        self.margin_right = margins[1]
        super(PropertiesDecorator, self).__init__()

    def set_margins(self, widget):
        ''' Helper for setting the default margins on a widget '''
        widget.set_margin_left(self.margin_left)
        widget.set_margin_right(self.margin_right)


class DomainDecorator(PropertiesDecorator):
    ''' Useful methods for domain data representation '''

    # pylint: disable=missing-docstring
    def __init__(self, vm: qubesadmin.vm.QubesVM, margins=(5, 5)) -> None:
        super(DomainDecorator, self).__init__(vm, margins)

    def name(self):
        label = Gtk.Label(self.obj['name'], xalign=0)
        self.set_margins(label)
        return label

    def memory(self) -> Gtk.Label:
        label = Gtk.Label(str(self.obj['memory']) + ' MB', xalign=0)
        self.set_margins(label)
        label.set_sensitive(False)
        return label

    def icon(self) -> Gtk.Image:
        ''' Returns a `Gtk.Image` containing the colored lock icon '''
        label_path = self.obj['label']
        assert label_path in LABELS.children
        label = LABELS.children[label_path]
        if label is None:
            label = LABELS.BLACK  # pylint: disable=no-member
        icon_vm = Gtk.IconTheme.get_default().load_icon(label['icon'], 22, 0)
        icon_img = Gtk.Image.new_from_pixbuf(icon_vm)
        self.set_margins(icon_img)
        return icon_img

    def state(self) -> Gtk.Image:
        state = self.obj['state']
        if state == "Halting":
            icon = Gtk.IconTheme.get_default().load_icon('application-exit', 22, 0)
        elif state == "Starting":
            icon = Gtk.IconTheme.get_default().load_icon('system-run', 22, 0)
        elif state == "Started":
            icon = Gtk.IconTheme.get_default().load_icon('media-playback-start', 22, 0)
        elif state == "Halted":
            icon = Gtk.IconTheme.get_default().load_icon('media-playback-stop', 22, 0)
        else:
            icon = Gtk.IconTheme.get_default().load_icon('media-record', 22, 0)

        icon_image = Gtk.Image.new_from_pixbuf(icon)
        icon_image.set_margin_right(self.margin_right)
        return icon_image

    def netvm(self) -> Gtk.Label:
        netvm = self.obj['netvm']
        if netvm is None:
            label = Gtk.Label('No', xalign=0)
        else:
            label = Gtk.Label(netvm['name'], xalign=0)

        self.set_margins(label)
        return label