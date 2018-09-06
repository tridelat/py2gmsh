class Field(object):
    __slots__ = ['nb', 'add_bg', 'name']
    nb_total = 0
    field_instances = []
    def __init__(self, nb=None, add_bg=True, name=None, mesh=None):
        Field.nb_total += 1
        if nb is None:
            self.nb = Field.nb_total
        else:
            self.nb = nb
        if mesh is not None:
            mesh.addField(self)
        self.add_bg = add_bg
        self.name = name
        Field.field_instances.append(self)

class BoundaryLayer(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(BoundaryLayer, self).__init__(nb=nb, add_bg=add_bg,
                                            name='BoundaryLayer',
                                            mesh=mesh)
        self.hwall_t = None
        self.hwall_n = None
        self.ratio = None
        self.EdgesList = None
        self.FacesList = None
        self.FanNodesList = None
        self.FansList = None
        self.IntersectMetrics = None
        self.NodesList = None
        self.Quads = None
        self.hfar = None
        self.thickness = None

class Box(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(Box, self).__init__(nb=nb, add_bg=add_bg, name='Box', mesh=mesh)
        self.VIn = None
        self.VOut = None
        self.XMax = None
        self.XMin = None
        self.YMax = None
        self.YMin = None
        self.ZMax = None
        self.ZMin = None

class MathEval(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(MathEval, self).__init__(nb=nb, add_bg=add_bg, name='MathEval',
                                       mesh=mesh)
        self.F = None

class Restrict(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(Restrict, self).__init__(nb=nb, add_bg=add_bg, name='Restrict',
                                       mesh=mesh)
        self.IField = None
        self.EdgesList = None
        self.FacesList = None
        self.RegionsList = None
        self.VerticesList = None

class Attractor(Field):
    def __init__(self, nb=None, add_bg=False, mesh=None):
        super(Attractor, self).__init__(nb=nb, add_bg=add_bg, name='Attractor',
                                        mesh=mesh)
        self.EdgesList = None
        self.FacesList = None
        self.FieldX = None
        self.FieldY = None
        self.FieldZ = None
        self.NNodesByEdge = None
        self.NodesList = None

class Threshold(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(Threshold, self).__init__(nb=nb, add_bg=add_bg, name='Threshold',
                                        mesh=mesh)
        self.DistMax = None
        self.DistMin = None
        self.IField = None
        self.LcMax = None
        self.LcMin = None
        self.Sigmoid = None
        self.StopAtDistMax = None

class Ball(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(Ball, self).__init__(nb=nb, add_bg=add_bg, name='Ball', mesh=mesh)
        self.Radius = None
        self.VIn = None
        self.VOut = None
        self.XCenter = None
        self.YCenter = None
        self.ZCenter = None

class Cylinder(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(Cylinder, self).__init__(nb=nb, add_bg=add_bg, name='Cylinder', mesh=mesh)
        self.Radius = None
        self.VIn = None
        self.VOut = None
        self.XCenter = None
        self.YCenter = None
        self.ZCenter = None
        self.XAxis = None
        self.YAxis = None
        self.ZAxis = None

class Min(Field):
    def __init__(self, nb=None, add_bg=True, mesh=None):
        super(Min, self).__init__(nb=nb, add_bg=add_bg, name='Min', mesh=mesh)
        self.FieldsList = None

