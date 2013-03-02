#!/usr/bin/env python

# Pure Data (pd) object model classes.
# 
# Copyright (C) 2013 Jared Boone, ShareBrained Technology, Inc.
# 
# This file is part of PD compiler.
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

class Message(object):
    def __init__(self, content):
        self._content = content

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._content)

class Text(object):
    def __init__(self, comment):
        self._comment = comment

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._comment)

class Connect(object):
    def __init__(self, source, outlet, target, inlet):
        self._source = int(source)
        self._outlet = int(outlet)
        self._target = int(target)
        self._inlet = int(inlet)

    @property
    def source_index(self):
        return self._source

    @property
    def source_outlet_index(self):
        return self._outlet

    @property
    def target_index(self):
        return self._target

    @property
    def target_inlet_index(self):
        return self._inlet

    def __repr__(self):
        return '%s(%s,%s,%s,%s)' % (self.__class__.__name__,
            self._source, self._outlet, self._target, self._inlet)

class UnsupportedObject(object):
    def __init__(self, name, parameters):
        self._name = name
        self._parameters = parameters

    def __repr__(self):
        return '%s(%s,%s)' % (self.__class__.__name__, self._name, self._parameters)

class Inlet(object):
    def __init__(self, parent, value_type):
        self._parent = parent
        self._value_type = value_type
        self._source = None

    @property
    def id(self):
        return self._parent.inlet.index(self)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

class Outlet(object):
    def __init__(self, parent):
        self._parent = parent

    @property
    def id(self):
        return self._parent.outlet.index(self)

    @property
    def parent(self):
        return self._parent

class ConstantOutlet(object):
    def __init__(self, value):
        self._value = value

    @property
    def parent(self):
        return None

    @property
    def value(self):
        return self._value

class DSPOperator(object):
    def __init__(self, **kwargs):
        self._inlets = tuple()
        self._outlets = tuple()
        self.id = None

    @property
    def inlet(self):
        return self._inlets

    @property
    def outlet(self):
        return self._outlets

    def __repr__(self):
        return self.__class__.__name__

class AudioDAC(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioDAC, self).__init__(**kwargs)

        self._left = Inlet(self, float)
        self._right = Inlet(self, float)
        self._inlets = (self._left, self._right)

class AudioPhasor(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioPhasor, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._ft1 = Inlet(self, float)
        self._inlets = (self._in, self._ft1,)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in.source = ConstantOutlet(float(parameters[0]))

class AudioOscillator(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioOscillator, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._ft1 = Inlet(self, float)
        self._inlets = (self._in, self._ft1,)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in.source = ConstantOutlet(float(parameters[0]))

class AudioMultiply(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioMultiply, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioDivide(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioDivide, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioAdd(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioAdd, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioSubtract(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioSubtract, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioMaximum(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioMaximum, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioMinimum(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioMinimum, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioPower(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioPower, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioLogarithm(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioLogarithm, self).__init__(**kwargs)

        self._in1 = Inlet(self, float)
        self._in2 = Inlet(self, float)
        self._inlets = (self._in1, self._in2)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in2.source = ConstantOutlet(float(parameters[0]))

class AudioAbsolute(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioAbsolute, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._inlets = (self._in,)

        self._out = Outlet(self)
        self._outlets = (self._out,)

class AudioExponent(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioExponent, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._inlets = (self._in,)

        self._out = Outlet(self)
        self._outlets = (self._out,)

class AudioWrap(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioWrap, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._inlets = (self._in,)

        self._out = Outlet(self)
        self._outlets = (self._out,)

class AudioCosine(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioCosine, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._phase = Inlet(self, float)
        self._inlets = (self._in, self._phase,)

        self._out = Outlet(self)
        self._outlets = (self._out,)

class AudioSignal(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioSignal, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._inlets = (self._in,)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._in.source = ConstantOutlet(float(parameters[0]))

class AudioClip(DSPOperator):
    def __init__(self, parameters, **kwargs):
        super(AudioClip, self).__init__(**kwargs)

        self._in = Inlet(self, float)
        self._lo = Inlet(self, float)
        self._hi = Inlet(self, float)
        self._inlets = (self._in, self._lo, self._hi)

        self._out = Outlet(self)
        self._outlets = (self._out,)

        if len(parameters) > 0:
            self._lo.source = ConstantOutlet(float(parameters[0]))
        if len(parameters) > 1:
            self._hi.source = ConstantOutlet(float(parameters[1]))

object_constructor = {
    'dac~': AudioDAC,
    'phasor~': AudioPhasor,
    'osc~': AudioOscillator,
    '+~': AudioAdd,
    '-~': AudioSubtract,
    '*~': AudioMultiply,
    '/~': AudioDivide,
    'max~': AudioMaximum,
    'min~': AudioMinimum,
    'abs~': AudioAbsolute,
    'exp~': AudioExponent,
    'wrap~': AudioWrap,
    'pow~': AudioPower,
    'log~': AudioLogarithm,
    'cos~': AudioCosine,
    'sig~': AudioSignal,
    'clip~': AudioClip,
}

def connect_parser(text):
    args = text.split()
    source, outlet, target, inlet = args
    new_connect = Connect(source, outlet, target, inlet)
    return new_connect

def msg_parser(text):
    args = text.split(None, 2)
    x_pos = args[0]
    y_pos = args[1]
    content = args[2]
    return Message(content)

def obj_parser(text):
    args = text.split()
    x_pos = args[0]
    y_pos = args[1]
    object_name = args[2]   # TODO: optional!
    parameters = args[3:]
    new_object = object_constructor[object_name](parameters)
    return new_object

def text_parser(text):
    args = text.split(None, 2)
    x_pos = args[0]
    y_pos = args[1]
    comment = args[2]
    return Text(comment)

element_type_parser = {
    'connect': connect_parser,
    'msg': msg_parser,
    'obj': obj_parser,
    'text': text_parser,
}

class ParseContext(object):
    def __init__(self):
        self.connects = []
        self.objects = []

    def chunk_parser_regular_element(self, text):
        element_type, text = text.split(None, 1)
        new_object = element_type_parser[element_type](text)
        if isinstance(new_object, Connect):
            self.connects.append(new_object)
        else:
            self.objects.append(new_object)

    def chunk_parser_array_data(self, text):
        return None

    def chunk_parser_frameset(self, text):
        return None

    chunk_parser = {
        'A': chunk_parser_array_data,
        'N': chunk_parser_frameset,
        'X': chunk_parser_regular_element,
    }

    def parse_record(self, text):
        chunk_type = text[0]
        return self.chunk_parser[chunk_type](self, text[1:].strip())

    def parse_patch(self, patch_file):
        patch = patch_file.read()
        patch_file.close()

        patch_split = patch.split('\\;')
        patch_split = map(lambda s: s.split(';'), patch_split)
        records = []
        for split_items in patch_split:
            if records:
                records[-1] += ';' + split_items[0]
                records.extend(split_items[1:])
            else:
                records = split_items
        records = map(str.strip, records)
        #print('\n'.join(records))

        for record in records:
            if len(record) and record[0] == '#':
                self.parse_record(record[1:])

        for i in range(len(self.objects)):
            o = self.objects[i]
            o.id = i
            #print('%d: %s' % (i, o))

        for i in range(len(self.connects)):
            c = self.connects[i]
            source_object = self.objects[c.source_index]
            outlet = source_object.outlet[c.source_outlet_index]
            target_object = self.objects[c.target_index]
            inlet = target_object.inlet[c.target_inlet_index]
            inlet.source = outlet
            #print('%d: %s' % (i, c))

def parse_patch(f):
    context = ParseContext()
    context.parse_patch(f)
    return context
