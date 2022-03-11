#!/usr/bin/env python

# Copyright 2021 daohu527 <daohu527@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Geometry:
  def __init__(self, s = None, x = None, y = None, hdg = None, length = None):
    self.s = s
    self.x = x
    self.y = y
    self.hdg = hdg
    self.length = length

  def parse_from(self, raw_geometry):
    self.s = float(raw_geometry.attrib.get('s'))
    self.x = float(raw_geometry.attrib.get('x'))
    self.y = float(raw_geometry.attrib.get('y'))
    self.hdg = float(raw_geometry.attrib.get('hdg'))
    self.length = float(raw_geometry.attrib.get('length'))

class Spiral(Geometry):
  def __init__(self, s = None, x = None, y = None, hdg = None, length = None, \
               curv_start = None, curv_end = None):
    super().__init__(s, x, y, hdg, length)
    self.curv_start = curv_start
    self.curv_end = curv_end

  def parse_from(self, raw_geometry):
    super().parse_from(raw_geometry)
    raw_spiral = raw_geometry.find('spiral')
    self.curv_start = float(raw_spiral.attrib.get('curvStart'))
    self.curv_end = float(raw_spiral.attrib.get('curvEnd'))


class Arc(Geometry):
  def __init__(self, s = None, x = None, y = None, hdg = None, length = None, \
               curvature = None):
    super().__init__(s, x, y, hdg, length)
    self.curvature = curvature

  def parse_from(self, raw_geometry):
    super().parse_from(raw_geometry)
    raw_arc = raw_geometry.find('arc')
    self.curvature = float(raw_arc.attrib.get('curvature'))

class Poly3(Geometry):
  def __init__(self, s = None, x = None, y = None, hdg = None, length = None, \
               a = None, b = None, c = None, d = None):
    super().__init__(s, x, y, hdg, length)
    self.a = a
    self.b = b
    self.c = c
    self.d = d

  def parse_from(self, raw_geometry):
    super().parse_from(raw_geometry)

    raw_poly3 = raw_geometry.find('poly3')
    self.a = float(raw_poly3.attrib.get('a'))
    self.b = float(raw_poly3.attrib.get('b'))
    self.c = float(raw_poly3.attrib.get('c'))
    self.d = float(raw_poly3.attrib.get('d'))


class ParamPoly3(Geometry):
  def __init__(self, s = None, x = None, y = None, hdg = None, length = None, \
               aU = None, bU = None, cU = None, dU = None, \
               aV = None, bV = None, cV = None, dV = None, pRange = None):
    super().__init__(s, x, y, hdg, length)
    self.aU = aU
    self.bU = bU
    self.cU = cU
    self.dU = dU
    self.aV = aV
    self.bV = bV
    self.cV = cV
    self.dV = dV
    self.pRange = pRange

  def parse_from(self, raw_geometry):
    super().parse_from(raw_geometry)
    raw_param_poly3 = raw_geometry.find('paramPoly3')

    self.aU = float(raw_param_poly3.attrib.get('aU'))
    self.bU = float(raw_param_poly3.attrib.get('bU'))
    self.cU = float(raw_param_poly3.attrib.get('cU'))
    self.dU = float(raw_param_poly3.attrib.get('dU'))
    self.aV = float(raw_param_poly3.attrib.get('aV'))
    self.bV = float(raw_param_poly3.attrib.get('bV'))
    self.cV = float(raw_param_poly3.attrib.get('cV'))
    self.dV = float(raw_param_poly3.attrib.get('dV'))
    self.pRange = raw_param_poly3.attrib.get('pRange')


class PlanView:
  def __init__(self):
    self.geometrys = []

  def add_geometry(self, geometry):
    self.geometrys.append(geometry)

  def parse_from(self, raw_plan_view):
    for raw_geometry in raw_plan_view.iter('geometry'):
      if raw_geometry[0].tag == 'line':
        geometry = Geometry()
      elif raw_geometry[0].tag == 'spiral':
        geometry = Spiral()
      elif raw_geometry[0].tag == 'arc':
        geometry = Arc()
      elif raw_geometry[0].tag == 'poly3':  # deprecated in OpenDrive 1.6.0
        geometry = Poly3()
      elif raw_geometry[0].tag == 'paramPoly3':
        geometry = ParamPoly3()
      else:
        # Todo(zero): raise an exception
        print("geometry type not support")

      geometry.parse_from(raw_geometry)
      self.add_geometry(geometry)
