import numpy as np

class Entity(object):
    __slots__ = ['nb', 'name' 'PhysicalGroup']
    def __init__(self, nb=None, group=None, name=None):
        self.nb = nb
        self.name = name
        self.PhysicalGroup = group


# POINTS

class Point(Entity):
    count = 0
    def __init__(self, xyz, nb=None, group=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Point, self).__init__(nb=nb, group=group, name='Point')
        self.xyz = xyz

    def setCoords(self, xyz):
        self.xyz[:] = [xyz]

    def _val2str(self):
        return '{'+str([v for v in self.xyz])[1:-1]+'}'


# LINES

class Line(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Line, self).__init__(nb=nb, group=group, name='Line')
        self.points = points
        self._index = index

    def setPoints(self, points):
        self.points[:] = [points]

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Circle(Entity):
    count = 0
    def __init__(self, start, center, end, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Circle, self).__init__(nb=nb, group=group, name='Circle')
        self.start = start
        self.center = center
        self.end = end
        self._index = index

    def _val2str(self):
        return '{'+str([self.start, self.center, self.end])[1:-1]+'}'


class CatmullRom(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='CatmullRom')
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Ellipse(Entity):
    count = 0
    def __init__(self, start, center, axis_point, end, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Circle, self).__init__(nb=nb, group=group, name='Ellipse')
        self.start = start
        self.center = center
        self.end = end
        self.axis_point = axis_point
        self._index = index

    def _val2str(self):
        return '{'+str([self.start, self.center, self.axis_point, self.end])[1:-1]+'}'


class BSpline(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(BSpline, self).__init__(nb=nb, group=group, name='BSpline')
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Spline(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='Spline')
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class CompoundLine(Entity):
    count = 0
    def __init__(self, lines, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='Compound Line')
        self.lines = lines
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.lines])[1:-1]+'}'


class LineLoop(Entity):
    count = 0
    def __init__(self, lines, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(LineLoop, self).__init__(nb=nb, group=group, name='Line Loop')
        self.lines = lines
        self._index = index

    def setLines(self, lines):
        self.lines[:] = [lines]

    def _val2str(self):
        ll = []
        if self._index is False:
            for i, line in enumerate(self.lines):
                if self.lines[i-1].points[1] == self.lines[i].points[0]:
                    ll += [self.lines[i].nb]
                elif self.lines[i-1].points[1] == self.lines[i].points[1]:
                    ll += [-self.lines[i].nb]
                elif self.lines[i-1].points[0] == self.lines[i].points[0]:
                    ll += [self.lines[i].nb]
                else:
                    assert 2<3, 'lineloop is wrong'
        else:
            ll = self.lines
        return '{'+str(ll)[1:-1]+'}'

# SURFACES

class PlaneSurface(Entity):
    count = 0
    def __init__(self, lineloops, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(PlaneSurface, self).__init__(nb=nb, group=group, name='Plane Surface')
        self.lineloops = lineloops
        self._index = index

    def setLineLoops(self, lineloops):
        self.lineloops[:] = [lineloops]

    def _val2str(self):
        return '{'+str([v.nb for v in self.lineloops])[1:-1]+'}'


class RuledSurface:
    count = 0
    def __init__(self, lineloops, nb=None, group=None, sphere=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(RuledSurface, self).__init__(nb=nb, group=group, name='Ruled Surface')
        self.lineloops = lineloops
        self.Sphere = sphere

    def setLineLoops(self, lineloops):
        self.lineloops[:] = [lineloops]

    def _val2str(self):
        return '{'+str([v.nb for v in self.lineloops])[1:-1]+'}'


class CompoundSurface(Entity):
    count = 0
    def __init__(self, surfaces, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='Compound Surface')
        self.surfaces = surfaces
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaces])[1:-1]+'}'


class SurfaceLoop(Entity):
    count = 0
    def __init__(self, surfaces, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(SurfaceLoop, self).__init__(nb=nb, group=group, name='Surface Loop')
        self.surfaces = surfaces
        self._index = index

    def setSurfaces(self, surfaces):
        self.surfaces[:] = [surfaces]

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaces])[1:-1]+'}'


# VOLUMES

class Volume(Entity):
    count = 0
    def __init__(self, surfaceloops, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Volume, self).__init__(nb=nb, group=group, name='Volume')
        self.surfaceloops = None
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaceloops])[1:-1]+'}'

    def setSurfaceLoops(self, surfaceloops):
        self.surfaceloops[:] = [surfaceloops]


class CompoundVolume(Entity):
    count = 0
    def __init__(self, volumes, nb=None, group=None, index=False):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Volume, self).__init__(nb=nb, group=group, name='Compound Volume')
        self.volumes = None
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.volumes])[1:-1]+'}'
