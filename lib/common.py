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


import math


class Vector3d:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def dot_product(self, other) -> float:
    return self.x*other.x + self.y*other.y + self.z*other.z

  def cross_product(self, other):
    x = self.y*other.z - self.z*other.y
    y = self.z*other.x - self.x*other.z
    z = self.x*other.y - self.y*other.x
    return Vector3d(x, y, z)

  def normalize(self):
    length = self.length()
    if length != 0:
      self.x /= length
      self.y /= length
      self.z /= length
    return self

  def length(self) -> float:
    return math.sqrt(self.x**2 + self.y**2 + self.z**2)

  def __add__(self, other):
    self.x += other.x
    self.y += other.y
    self.z += other.z
    return self

  def __sub__(self, other):
    self.x -= other.x
    self.y -= other.y
    self.z -= other.z
    return self

  def __mul__(self, ratio):
    self.x *= ratio
    self.y *= ratio
    self.z *= ratio
    return self

  def __truediv__(self, ratio):
    self.x /= ratio
    self.y /= ratio
    self.z /= ratio
    return self

  def __str__(self):
    return "Vector3d x: {}, y: {}, z: {}".format(self.x, self.y, self.z)

class Point3d:
  def __init__(self, x, y, z, s):
    self.x = x
    self.y = y
    self.z = z
    self.s = s

  def set_rotate(self, yaw = 0.0, roll = 0.0, pitch = 0.0):
    self.yaw = yaw
    self.roll = roll
    self.pitch = pitch

  def shift_t(self, offset):
    vec_x = Vector3d(math.cos(self.yaw), math.sin(self.yaw), 0)
    vec_z = Vector3d(math.cos(self.roll), 0, math.sin(self.roll))
    normal_xz = vec_x.cross_product(vec_z)
    vec_y = normal_xz.normalize() * offset
    self.x += vec_y.x
    self.y += vec_y.y
    self.z += vec_y.z

  def __str__(self):
    return "Point3d x: {}, y: {}, z: {}, s: {}, heading: {}".format(self.x, \
        self.y, self.z, self.s, self.yaw)
