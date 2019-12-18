class PhysicalGroup(object):
    """PhysicalGroup

    Parameters
    ----------
    nb: Optional[int]
        Physical group number. If not set, it will use the count 
        number (incrementing automatically upon creation of new
        physical groups).
    name: Optional[str]
        Name of physical group.
    mesh: Optional[py2gmsh.Mesh.Mesh]
        Mesh class instance to which the group belongs.
    """
    def __init__(self, nb=None, name=None, mesh=None):
        self.nb = nb
        self.name = name
        self.points = {}
        self.curves = {}
        self.curveloops = {}
        self.surfaces = {}
        self.surfaceloops = {}
        self.volumes = {}
        self.regions = {}
        if mesh is not None:
            mesh.addGroup(self)

    def addEntity(self, entity):
        """Adds entity to PhysicalGroup instance

        Parameters
        ----------
        entity: py2gmsh.Entity.Entity
            Entity to add to group (e.g. Point, Curve, CurveLoop).
        """
        if isinstance(entity, Point):
            assert not self.points.get(entity.nb), 'Point nb '+str(entity.nb)+' already exists!'
            self.points[entity.nb] = entity
        elif isinstance(entity, CurveEntity):
            assert not self.curves.get(entity.nb), 'Curve nb '+str(entity.nb)+' already exists!'
            self.curves[entity.nb] = entity
        elif isinstance(entity, SurfaceEntity):
            assert not self.surfaces.get(entity.nb), 'Surface nb '+str(entity.nb)+' already exists!'
            self.surfaces[entity.nb] = entity
        elif isinstance(entity, VolumeEntity):
            assert not self.volumes.get(entity.nb), 'Volume nb '+str(entity.nb)+' already exists!'
            self.volumes[entity.nb] = entity

    def addEntities(self, entities):
        for entity in entities:
            self.addEntity(entity)


class Entity(object):
    """Base class for all entities.
    (!) Should not be created manually

    Parameters
    ----------
    nb: int
        Entity number.
    group: Optional[PhysicalGroup]
        Physical group of Entity.
    name: Optional[str]
        Name of Entity.
    mesh: Optional[py2gmsh.Mesh.Mesh]
        Mesh of entity.
    """
    __slots__ = ['nb', 'name' 'PhysicalGroup']
    def __init__(self, nb, group=None, name=None, mesh=None):
        self.nb = nb
        self.name = name
        self.PhysicalGroup = group
        if mesh is not None:
            mesh.addEntity(self)
        if group is not None:
            group.addEntity(self)

    def check_instance(self, entities, entity_class, index, mesh):
        if index is False and mesh is not None:
            for entity in entities:
                assert isinstance(entity, entity_class), 'points must be class instances of '+str(entity_class)
        elif index is True and mesh is not None:
        #    assert isinstance(mesh, Mesh), 'Mesh instance must be passed when defining entities per index'
            for entity in entities:
                assert isinstance(entity, int), 'index must be integers'



# POINTS

class Point(Entity):
    """Creates a Point.

    Parameters
    ----------
    xyz: array_like
        Coordinates of point (array of length 3)
    nb: Optional[int]
        Point number. If not set, it will use the class count 
        number (incrementing automatically upon creation of new
        points).
    group: Optional[PhysicalGroup]
        Physical group of Entity.
    mesh: Optional[py2gmsh.Mesh.Mesh]
        Mesh of entity.
    """
    def __init__(self, xyz, nb=None, group=None, mesh=None):
        super(Point, self).__init__(nb=nb, group=group, name='Point', mesh=mesh)
        self.xyz = xyz

    def setCoords(self, xyz):
        self.xyz[:] = [xyz]

    def _val2str(self):
        return '{'+str([v for v in self.xyz])[1:-1]+'}'


# CURVES

class CurveEntity(Entity):
    """Parent class for all curve type entities.

    Parameters
    ----------
    nb: Optional[int]
        Point number. If not set, it will use the class count 
        number (incrementing automatically upon creation of new
        curves).
    group: Optional[PhysicalGroup]
        Physical group of Entity.
    name: Optional[str]
        Name of curve.
    mesh: Optional[py2gmsh.Mesh.Mesh]
        Mesh of curve.
    """
    def __init__(self, nb=None, group=None, name=None, mesh=None):
        super(CurveEntity, self).__init__(nb=nb, group=group, name=name, mesh=mesh)

class Curve(CurveEntity):
    """Creates a Curve.

    Parameters
    ----------
    points: array_like[Points]
        Points instances (array of length 2)
    nb: Optional[int]
        CurveEntity number. If not set, it will use the class count 
        number (incrementing automatically upon creation of new
        points).
    group: Optional[PhysicalGroup]
        Physical group of entity.
    mesh: Optional[py2gmsh.Mesh.Mesh]
        Mesh of entity.
    """
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        assert len(points) == 2, 'points array must be of length 2 when creating a curve'
        self.check_instance(points, Point, index, mesh)
        super(Curve, self).__init__(nb=nb, group=group, name='Curve', mesh=mesh)
        self.points = points
        self._index = index

    def setPoints(self, points):
        self.points[:] = [points]

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


Line = Curve


class Circle(CurveEntity):
    """Creates a Circle.

    Parameters
    ----------
    start: Point
        start point of circle arc.
    center: Point
        center point of circle arc.
    end: Point
        end point of circle arc.
    nb: Optional[int]
        CurveEntity number. If not set, it will use the class count 
        number (incrementing automatically upon creation of new
        points).
    group: Optional[PhysicalGroup]
        Physical group of entity.
    index: Optional[bool]
        Look for points defining the circle per index if True.
    mesh: Optional[py2gmsh.Mesh.Mesh]
        Mesh of entity.
    """
    def __init__(self, start, center, end, nb=None, group=None, index=False, mesh=None):
        self.check_instance([start, center, end], Point, index, mesh)
        super(Circle, self).__init__(nb=nb, group=group, name='Circle', mesh=mesh)
        self.start = start
        self.center = center
        self.end = end
        self._index = index

    def _val2str(self):
        return '{'+str([self.start.nb, self.center.nb, self.end.nb])[1:-1]+'}'


class CatmullRom(CurveEntity):
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        self.check_instance(points, Point, index, mesh)
        super(Spline, self).__init__(nb=nb, group=group, name='CatmullRom', mesh=mesh)
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Ellipse(CurveEntity):
    def __init__(self, start, center, axis_point, end, nb=None, group=None, index=False, mesh=None):
        self.check_instance([start, center, acis_point, end], Point, index, mesh)
        super(Circle, self).__init__(nb=nb, group=group, name='Ellipse', mesh=mesh)
        self.start = start
        self.center = center
        self.end = end
        self.axis_point = axis_point
        self._index = index

    def _val2str(self):
        return '{'+str([self.start, self.center, self.axis_point, self.end])[1:-1]+'}'


class BSpline(CurveEntity):
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        self.check_instance(points, Point, index, mesh)
        super(BSpline, self).__init__(nb=nb, group=group, name='BSpline', mesh=mesh)
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class Spline(CurveEntity):
    def __init__(self, points, nb=None, group=None, index=False, mesh=None):
        self.check_instance(points, Point, index, mesh)
        super(Spline, self).__init__(nb=nb, group=group, name='Spline', mesh=mesh)
        self.points = points
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.points])[1:-1]+'}'


class CompoundCurve(CurveEntity):
    def __init__(self, curves, nb=None, group=None, index=False, mesh=None):
        self.check_instance(curves, Curve, index, mesh)
        super(Spline, self).__init__(nb=nb, group=group, name='Compound Curve', mesh=mesh)
        self.curves = curves
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.curves])[1:-1]+'}'


CompoundLine = CompoundCurve


# CURVE LOOPS

class CurveLoop(Entity):
    def __init__(self, curves, nb=None, group=None, index=False, mesh=None):
        self.check_instance(curves, Curve, index, mesh)
        super(CurveLoop, self).__init__(nb=nb, group=group, name='Curve Loop', mesh=mesh)
        self.curves = curves
        self._index = index

    def setCurves(self, curves):
        self.curves[:] = [curves]

    def _val2str(self):
        ll = []
        if self._index is False:
            for i, curve in enumerate(self.curves):
                if self.curves[i-1].points[1] == self.curves[i].points[0]:
                    ll += [self.curves[i].nb]
                elif self.curves[i-1].points[1] == self.curves[i].points[1]:
                    ll += [-self.curves[i].nb]
                elif self.curves[i-1].points[0] == self.curves[i].points[0]:
                    ll += [self.curves[i].nb]
                elif self.curves[i-1].points[0] == self.curves[i].points[1]:
                    ll += [-self.curves[i].nb]
                else:
                    assert 2<3, 'curveloop is wrong'
        else:
            ll = self.curves
        return '{'+str(ll)[1:-1]+'}'


LineLoop = CurveLoop


# SURFACES

class SurfaceEntity(Entity):
    """
    Parent class of all surface type entities
    """
    def __init__(self, nb=None, group=None, name=None, mesh=None):
        super(SurfaceEntity, self).__init__(nb=nb, group=group, name=name, mesh=mesh)


class PlaneSurface(SurfaceEntity):
    def __init__(self, curveloops, nb=None, group=None, index=False, mesh=None):
        self.check_instance(curveloops, CurveLoop, index, mesh)
        super(PlaneSurface, self).__init__(nb=nb, group=group, name='Plane Surface', mesh=mesh)
        self.curveloops = curveloops
        self._index = index

    def setCurveLoops(self, curveloops):
        self.curveloops[:] = [curveloops]

    def _val2str(self):
        return '{'+str([v.nb for v in self.curveloops])[1:-1]+'}'


class RuledSurface(SurfaceEntity):
    def __init__(self, curveloops, nb=None, group=None, sphere=None, mesh=None):
        self.check_instance(curveloops, CurveLoop, index, mesh)
        super(RuledSurface, self).__init__(nb=nb, group=group, name='Ruled Surface', mesh=mesh)
        self.curveloops = curveloops
        self.Sphere = sphere

    def setCurveLoops(self, curveloops):
        self.curveloops[:] = [curveloops]

    def _val2str(self):
        return '{'+str([v.nb for v in self.curveloops])[1:-1]+'}'


class CompoundSurface(SurfaceEntity):
    def __init__(self, surfaces, nb=None, group=None, index=False, mesh=None):
        self.check_instance(surfaces, SurfaceEntity, index, mesh)
        super(Spline, self).__init__(nb=nb, group=group, name='Compound Surface', mesh=mesh)
        self.surfaces = surfaces
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaces])[1:-1]+'}'


# SURFACE LOOPS

class SurfaceLoop(Entity):
    def __init__(self, surfaces, nb=None, group=None, index=False, mesh=None):
        self.check_instance(surfaces, SurfaceLoop, index, mesh)
        super(SurfaceLoop, self).__init__(nb=nb, group=group, name='Surface Loop', mesh=mesh)
        self.surfaces = surfaces
        self._index = index

    def setSurfaces(self, surfaces):
        self.surfaces[:] = [surfaces]

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaces])[1:-1]+'}'


# VOLUMES

class VolumeEntity(Entity):
    """
    Parent class of all surface type entities
    """
    def __init__(self, nb=None, group=None, name=None, mesh=None):
        super(VolumeEntity, self).__init__(nb=nb, group=group, name=name, mesh=mesh)


class Volume(VolumeEntity):
    def __init__(self, surfaceloops, nb=None, group=None, index=False, mesh=None):
        self.check_instance(surfaceloops, SurfaceLoop, index, mesh)
        super(Volume, self).__init__(nb=nb, group=group, name='Volume', mesh=mesh)
        self.surfaceloops = surfaceloops
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.surfaceloops])[1:-1]+'}'

    def setSurfaceLoops(self, surfaceloops):
        self.surfaceloops[:] = [surfaceloops]


class CompoundVolume(VolumeEntity):
    def __init__(self, volumes, nb=None, group=None, index=False, mesh=None):
        self.check_instance(volumes, Volume, index, mesh)
        super(Volume, self).__init__(nb=nb, group=group, name='Compound Volume', mesh=mesh)
        self.volumes = volumes
        self._index = index

    def _val2str(self):
        return '{'+str([v.nb for v in self.volumes])[1:-1]+'}'
 
