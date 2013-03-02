#!/usr/bin/env python

# Pure Data (pd) compiler front-end
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

import sys
import os.path

import pdom

input_file_path = sys.argv[1]
input_file_base, input_file_extension = os.path.splitext(input_file_path)
output_file_path = input_file_base + '.c'

parse_context = pdom.parse_patch(open(input_file_path, 'r'))

chain = []
def walk_object_inlets(o):
    global chain
    for inlet in o.inlet:
        outlet = inlet.source
        if outlet and outlet.parent:
            walk_object_inlets(outlet.parent)
    if o not in chain:
        chain.append(o)

dacs = tuple((o for o in parse_context.objects if isinstance(o, pdom.AudioDAC)))
for dac in dacs:
    walk_object_inlets(dac)

#print(chain)
#print

from emit_c import declare, init, dsptick_start, dsptick, dsptick_end, deinit

lines = ['#include <stdio.h>',
         '#include <math.h>',
         '',
         'static const float SAMPLING_RATE = 44100.0f;',
         '',
         ]

for o in chain:
    lines.extend(declare(o))
lines.append('')

lines.append('void init() {')
for o in chain:
    lines.extend(('\t%s' %s for s in init(o)))
lines.append('}')
lines.append('')

lines.append('void dsptick() {')
for o in chain:
    lines.extend(('\t%s' % s for s in dsptick_start(o)))
for o in chain:
    lines.extend(('\t%s' % s for s in dsptick(o)))
for o in chain:
    lines.extend(('\t%s' % s for s in dsptick_end(o)))
lines.append('}')
lines.append('')

lines.append('void deinit() {')
for o in chain:
    lines.extend(('\t%s' % s for s in deinit(o)))
lines.append('}')

c_code = '\n'.join(lines)
c_file = open(output_file_path, 'w')
c_file.write(c_code)
c_file.close()
