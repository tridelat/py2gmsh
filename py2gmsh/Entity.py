import numpy as np

class PhysicalGroup(object):

    count = 0
    def __init__(self, nb=None, name=None, mesh=None):
        type(self).count += 1
        if nb is None:
            self.nb = type(self).count
        else:
            self.nb = nb
        self.name = name
        self.points = {}
        self.lines = {}
        self.lineloops = {}
        self.surfaces = {}
        self.surfaceloops = {}
        self.volumes = {}
        self.regions = {}
        if mesh is not None:
            mesh.addGroup(self)

    def addEntity(self, entity):
        if isinstance(entity, Point):
            assert not self.points.get(entity.nb), 'Point nb '+str(entity.nb)+' already exists!'
            self.points[entity.nb] = entity
        elif isinstance(entity, Line):
            assert not self.lines.get(entity.nb), 'Line nb '+str(entity.nb)+' already exists!'
            self.lines[entity.nb] = entity
        elif isinstance(entity, PlaneSurface):
            assert not self.surfaces.get(entity.nb), 'Surface nb '+str(entity.nb)+' already exists!'
            self.surfaces[entity.nb] = entity
        elif isinstance(entity, Volume):
            assert not self.volumes.get(entity.nb), 'Volume nb '+str(entity.nb)+' already exists!'
            self.volumes[entity.nb] = entity
        # entity.group = self


class Entity(object):
    __slots__ = ['nb', 'name' 'PhysicalGroup']
    def __init__(self, nb=None, group=None, name=None, mesh=None):
        self.nb = nb
        self.name = name
        self.PhysicalGroup = group
        if mesh is not None:
            mesh.addEntity(self)
        if group is not None:
            group.addEntity(self)


# POINTS

class Point(Entity):
    count = 0
    def __init__(self, xyz, nb=None, group=None, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Point, self).__init__(nb=nb, group=group, name='Point', mesh=mesh)
        self.xyz = xyz

    def setCoords(self, xyz):
        self.xyz[:] = [xyz]

    def _val2str(self):
        return '{'+str([v for v in self.xyz])[1:-1]+'}'


# LINES

class Line(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Line, self).__init__(nb=nb, group=group, name='Line', mesh=mesh)
        self.points = points
        self._index = index

    def setPoints(self, points):
        self.points[:] = [points]

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Circle(Entity):
    count = 0
    def __init__(self, start, center, end, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Circle, self).__init__(nb=nb, group=group, name='Circle', mesh=mesh)
        self.start = start
        self.center = center
        self.end = end
        self._index = index

    def _val2str(self):
        return '{'+str([self.start, self.center, self.end])[1:-1]+'}'


class CatmullRom(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='CatmullRom', mesh=mesh)
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Ellipse(Entity):
    count = 0
    def __init__(self, start, center, axis_point, end, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Circle, self).__init__(nb=nb, group=group, name='Ellipse', mesh=mesh)
        self.start = start
        self.center = center
        self.end = end
        self.axis_point = axis_point
        self._index = index

    def _val2str(self):
        return '{'+str([self.start, self.center, self.axis_point, self.end])[1:-1]+'}'


class BSpline(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(BSpline, self).__init__(nb=nb, group=group, name='BSpline', mesh=mesh)
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Spline(Entity):
    count = 0
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='Spline', mesh=mesh)
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class CompoundLine(Entity):
    count = 0
    def __init__(self, lines, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='Compound Line', mesh=mesh)
        self.lines = lines
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.lines])[1:-1]+'}'


class LineLoop(Entity):
    count = 0
    def __init__(self, lines, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(LineLoop, self).__init__(nb=nb, group=group, name='Line Loop', mesh=mesh)
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
    def __init__(self, lineloops, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(PlaneSurface, self).__init__(nb=nb, group=group, name='Plane Surface', mesh=mesh)
        self.lineloops = lineloops
        self._index = index

    def setLineLoops(self, lineloops):
        self.lineloops[:] = [lineloops]

    def _val2str(self):
        return '{'+str([v.nb for v in self.lineloops])[1:-1]+'}'


class RuledSurface:
    count = 0
    def __init__(self, lineloops, nb=None, group=None, sphere=None, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(RuledSurface, self).__init__(nb=nb, group=group, name='Ruled Surface', mesh=mesh)
        self.lineloops = lineloops
        self.Sphere = sphere

    def setLineLoops(self, lineloops):
        self.lineloops[:] = [lineloops]

    def _val2str(self):
        return '{'+str([v.nb for v in self.lineloops])[1:-1]+'}'


class CompoundSurface(Entity):
    count = 0
    def __init__(self, surfaces, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Spline, self).__init__(nb=nb, group=group, name='Compound Surface', mesh=mesh)
        self.surfaces = surfaces
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaces])[1:-1]+'}'


class SurfaceLoop(Entity):
    count = 0
    def __init__(self, surfaces, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(SurfaceLoop, self).__init__(nb=nb, group=group, name='Surface Loop', mesh=mesh)
        self.surfaces = surfaces
        self._index = index

    def setSurfaces(self, surfaces):
        self.surfaces[:] = [surfaces]

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaces])[1:-1]+'}'


# VOLUMES

class Volume(Entity):
    count = 0
    def __init__(self, surfaceloops, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Volume, self).__init__(nb=nb, group=group, name='Volume', mesh=mesh)
        self.surfaceloops = None
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaceloops])[1:-1]+'}'

    def setSurfaceLoops(self, surfaceloops):
        self.surfaceloops[:] = [surfaceloops]


class CompoundVolume(Entity):
    count = 0
    def __init__(self, volumes, nb=None, group=None, index=False, mesh=None):
        type(self).count += 1
        if nb is None:
            nb = type(self).count
        super(Volume, self).__init__(nb=nb, group=group, name='Compound Volume', mesh=mesh)
        self.volumes = None
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.volumes])[1:-1]+'}'
