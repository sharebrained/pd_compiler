# Hey Emacs, this is a -*- makefile -*-

# Makefile for generating C code for an example patch, and compiling
# the C code into an executable.
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

PYTHON_SRC = pd_compile.py pdom.py emit_c.py
C_SRC = main.c out.c

PATCHFILE=web-pure-data/unittests/subtract~.pd

all: main

main: $(C_SRC)
	gcc -std=c99 -O2 -o main $(C_SRC)

out.c: $(PYTHON_SRC)
	python pd_compile.py $(PATCHFILE)

clean:
	rm -f main
	rm -f out.c
