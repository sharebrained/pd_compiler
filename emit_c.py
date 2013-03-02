#!/usr/bin/env python

# Visitor functions for Pure Data (pd) object model which produce C code.
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

from pdom import *
from peak.rules import when

# TODO: Maybe instead of passing back language-specific strings, pass back statements...
# initialize variable, assignments, ???

def declare(o):
    return tuple()

def init(o):
    return tuple()

def dsptick_start(o):
    return tuple()

def dsptick(o):
    return tuple()

def dsptick_end(o):
    return tuple()

def deinit(o):
    return tuple()

#######################################
def obj_prop(obj, name):
    return 'object_%s_%s' % (obj.id, name)

def outlet_str(outlet):
    return obj_prop(outlet.parent, 'outlet_%d' % outlet.id)
    
def source_str(inlet):
    source = inlet.source
    if isinstance(source, Outlet):
        return outlet_str(source)
    elif isinstance(source, ConstantOutlet):
        return '%ff' % source.value
    else:
        raise Exception('Unknown source %s' % source)

#######################################
@when(declare, AudioDAC)
def audio_dac_declare(o):
    return ('static FILE* %s = NULL;' % (obj_prop(o, 'file'),),
            )
    
@when(init, AudioDAC)
def audio_dac_init(o):
    return ('%s = fopen("dac_%d.f32", "wb");' % (obj_prop(o, 'file'), o.id),
            )

@when(dsptick, AudioDAC)
def audio_dac_dsptick(o):
    left = source_str(o._left) if o._left.source else '0.0f'
    right = source_str(o._right) if o._right.source else '0.0f'
    return ('const float %s[2] = { %s, %s };' % (obj_prop(o, 'buffer'), left, right),
            'fwrite(%s, sizeof(%s), 1, %s);' % (obj_prop(o, 'buffer'), obj_prop(o, 'buffer'), obj_prop(o, 'file')),
            )

@when(deinit, AudioDAC)
def audio_dac_deinit(o):
    return ('fclose(%s);' % (obj_prop(o, 'file'),),
            '%s = NULL;' % (obj_prop(o, 'file'),),
            )

#######################################
@when(declare, 'isinstance(o, AudioOscillator)')
def osc_declare(o):
    return ('static float %s = 0.0f;' % (obj_prop(o, 'phase'),),
            )
    
@when(init, 'isinstance(o, AudioOscillator)')
def osc_init(o):
    return ('%s = 0.0f;' % (obj_prop(o, 'phase'),),
            )

@when(dsptick, 'isinstance(o, AudioOscillator)')
def osc_dsptick(o):
    outlet = outlet_str(o._out)
    result = ('const float %s = cosf(%s);' % (outlet, obj_prop(o, 'phase')),
              'const float %s = %s * 2.0f * M_PI / SAMPLING_RATE;' % (obj_prop(o, 'phase_increment'), source_str(o._in)),
              '%s = fmodf(%s + %s, 2.0f * M_PI);' % (obj_prop(o, 'phase'), obj_prop(o, 'phase'), obj_prop(o, 'phase_increment')),
               )
    return result

#######################################
@when(declare, 'isinstance(o, AudioPhasor)')
def phasor_declare(o):
    return ('static float %s = 0.0f;' % (obj_prop(o, 'phase'),),
            )

@when(init, 'isinstance(o, AudioPhasor)')
def phasor_init(o):
    return ('%s = 0.0f;' % (obj_prop(o, 'phase'),),
            )

@when(dsptick, 'isinstance(o, AudioPhasor)')
def phasor_dsptick(o):
    outlet = outlet_str(o._out)
    result = ('const float %s = %s;' % (outlet, obj_prop(o, 'phase')),
              'const float %s = %s / SAMPLING_RATE;' % (obj_prop(o, 'phase_increment'), source_str(o._in)),
              '%s = fmodf(%s + %s, 1.0f);' % (obj_prop(o, 'phase'), obj_prop(o, 'phase'), obj_prop(o, 'phase_increment')),
               )
    return result

#######################################
def _unfn(o, function_str, scale_str=''):
    outlet = outlet_str(o._out)
    arg = source_str(o._in)
    return ('const float %s = %s(%s%s);' % (outlet, function_str, arg, scale_str),
            )
    
def _binop(o, operator_str):
    outlet = outlet_str(o._out)
    left = source_str(o._in1)
    right = source_str(o._in2)
    return ('const float %s = %s %s %s;' % (outlet, left, operator_str, right),
            )

def _binfn(o, function_str):
    outlet = outlet_str(o._out)
    left = source_str(o._in1)
    right = source_str(o._in2)
    return ('const float %s = %s(%s, %s);' % (outlet, function_str, left, right),
            )
    
#######################################
@when(dsptick, 'isinstance(o, AudioAdd)')
def add_dsptick(o):
    return _binop(o, '+')

@when(dsptick, 'isinstance(o, AudioSubtract)')
def subtract_dsptick(o):
    return _binop(o, '-')

@when(dsptick, 'isinstance(o, AudioMultiply)')
def multiply_dsptick(o):
    return _binop(o, '*')

@when(dsptick, 'isinstance(o, AudioDivide)')
def divide_dsptick(o):
    return _binop(o, '/')

#######################################
@when(dsptick, 'isinstance(o, AudioCosine)')
def cos_dsptick(o):
    return _unfn(o, 'cosf', ' * 2.0f * M_PI')

@when(dsptick, 'isinstance(o, AudioAbsolute)')
def abs_dsptick(o):
    return _unfn(o, 'fabsf')

@when(dsptick, 'isinstance(o, AudioExponent)')
def exp_dsptick(o):
    return _unfn(o, 'expf')

@when(dsptick, 'isinstance(o, AudioSignal)')
def sig_dsptick(o):
    outlet = outlet_str(o._out)
    arg = source_str(o._in)
    return ('const float %s = %s;' % (outlet, arg),
            )

@when(dsptick, 'isinstance(o, AudioWrap)')
def wrap_dsptick(o):
    outlet = outlet_str(o._out)
    arg = source_str(o._in)
    return ('const float %s = (%s > 0.0f) ? (%s - (int)%s) : (%s - ((int)%s - 1.0f));' % (outlet,
            arg, arg, arg, arg, arg),
            )

#######################################
@when(dsptick, 'isinstance(o, AudioMaximum)')
def max_dsptick(o):
    return _binfn(o, 'fmaxf')

@when(dsptick, 'isinstance(o, AudioMinimum)')
def min_dsptick(o):
    return _binfn(o, 'fminf')

@when(dsptick, 'isinstance(o, AudioPower)')
def pow_dsptick(o):
    return _binfn(o, 'powf')

#######################################
@when(dsptick, 'isinstance(o, AudioClip)')
def clip_dsptick(o):
    outlet = outlet_str(o._out)
    i = source_str(o._in)
    lo = source_str(o._lo)
    hi = source_str(o._hi)
    return ('const float %s = (%s < %s) ? %s : (%s > %s) ? %s : %s;' % (outlet,
            i, lo, lo, i, hi, hi, i),
            )

@when(dsptick, 'isinstance(o, AudioLogarithm)')
def log_dsptick(o):
    outlet = outlet_str(o._out)
    in1 = source_str(o._in1)
    if o._in2.source:
        in2 = source_str(o._in2)
        return ('const float %s = logf(%s) / logf(%s);' % (outlet, in1, in2),
                )
    else:
        return ('const float %s = logf(%s);' % (outlet, in1),
                )
