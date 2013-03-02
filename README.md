pd_compiler
===========

Pure Data compiler, translates pd files into C code for compilation on embedded systems.
Presently targeting ARM Cortex-M4F microcontrollers.

Status
======

This project is in a very early stage of development. It can only comprehend and compile
patches comprised of a very limited set of objects -- all of them audio-rate objects.

Example Output
==============

Using an example "A01.sinewave.pd" that (I think) comes with Pure Data, here is the
generated C code.

```C
#include <stdio.h>
#include <math.h>

static const float SAMPLING_RATE = 44100.0f;

static float object_0_phase = 0.0f;
static FILE* object_1_file = NULL;

void init() {
	object_0_phase = 0.0f;
	object_1_file = fopen("dac_1.f32", "wb");
}

void dsptick() {
	const float object_0_outlet_0 = cosf(object_0_phase);
	const float object_0_phase_increment = 440.000000f * 2.0f * M_PI / SAMPLING_RATE;
	object_0_phase = fmodf(object_0_phase + object_0_phase_increment, 2.0f * M_PI);
	const float object_3_outlet_0 = object_0_outlet_0 * 0.050000f;
	const float object_1_buffer[2] = { object_3_outlet_0, 0.0f };
	fwrite(object_1_buffer, sizeof(object_1_buffer), 1, object_1_file);
}

void deinit() {
	fclose(object_1_file);
	object_1_file = NULL;
}
```

Requirements
============

To run pd_compile.py, you will need:

* [Peak-Rules](https://pypi.python.org/pypi/PEAK-Rules), which is used for conditionally
  binding visitor functions to classes of Pure Data objects. These visitor functions
  generate C code that is run at different times over the PD patch lifespan.


Usage
=====

Run pd_compile.py with a single argument, the name of a Pure Data patch file. A bunch of
parsing and debugging junk will be printed, along with the generated C code. The
generated C code is also placed in a file called "out.c".

There is also a Makefile which will generate C code for a Pure Data patch file, and
compile it with a wrapper main() function into an executable "main" that generates three
seconds worth of audio into a zero or more dac_*.f32 files (containing 32-bit float
sample data). The number of dac_*.f32 files is determined by the number of DAC objects
in the patch file.

This is totally half-baked test code, if you couldn't tell...

License
=======

Copyright (C) 2011 Jared Boone, ShareBrained Technology, Inc.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.

Contact
=======

ShareBrained Technology, Inc.

<http://www.sharebrained.com/>