import numpy as np
import taichi as ti
import taichi_glsl as ts
from .geometry import *
from .shading import *
from .transform import *
from .common import *
from .model import *
import math


class ScatterModel(ModelBase):
    def __init__(self, num=None):
        self.L2W = Affine.field(())

        self.num = num

        if num is not None:
            self.pos = ti.Vector.field(3, float, num)

    def _init(self):
        self.L2W.init()

    @ti.func
    def render(self, camera):
        for i in ti.grouped(self.pos):
            render_particle(self, camera, i)

    @ti.func
    def colorize(self, pos, normal, color):
        opt = CookTorrance()
        opt.model = ti.static(self)
        return opt.colorize(pos, normal, color)
