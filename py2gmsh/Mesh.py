from py2gmsh import Entity as ent
from py2gmsh import Fields as fld
from py2gmsh import Options as opt

class Mesh:
    def __init__(self):
        self.points = {}
        self.lines = {}
        self.lineloops = {}
        self.surfaces = {}
        self.surfaceloops = {}
        self.volumes = {}
        self.regions = {}
        self.fields = {}
        self.groups = {}
        self.Options = OptionsHolder()
        self.BackgroundField = None
        self.BoundaryLayerField = None
        self.Coherence = True

    def getPointsFromIndex(self, index):
        if isinstance(index, int):
            index = [index]
        points = []
        for i in index:
            points += [self.points[i]]
        return points

    def getLinesFromIndex(self, index):
        if isinstance(index, int):
            index = [index]
        lines = []
        for i in index:
            lines += [self.lines[i]]
        return lines

    def getSurfacesFromIndex(self, index):
        if isinstance(index, int):
            index = [index]
        surfaces = []
        for i in index:
            surfaces += [self.surfaces[i]]
        return surfaces

    def getSurfaceLoopsFromIndex(self, index):
        if isinstance(index, int):
            index = [index]
        surfaceloops = []
        for i in index:
            surfaceloops += [self.surfaceloops[i]]
        return surfaceloops

    def getVolumesFromIndex(self, index):
        if isinstance(index, int):
            index = [index]
        volumes = []
        for i in index:
            volumes += [self.volumes[i]]
        return volumes

    def getFieldsFromIndex(self, index):
        if isinstance(index, int):
            index = [index]
        fields = []
        for i in index:
            fields += [self.fields[i]]
        return fields

    def getGroupsFromIndex(self, index):
        if isinstance(index, int):
            index = [index]
        groups = []
        for i in index:
            groups += [self.groups[i]]
        return groups

    def addEntity(self, entity):
        if isinstance(entity, ent.Point):
            assert not self.points.get(entity.nb), 'Point nb '+str(entity.nb)+' already exists!'
            self.points[entity.nb] = entity
        elif isinstance(entity, ent.Line):
            assert not self.lines.get(entity.nb), 'Line nb '+str(entity.nb)+' already exists!'
            self.lines[entity.nb] = entity
        elif isinstance(entity, ent.LineLoop):
            assert not self.lineloops.get(entity.nb), 'LineLoop nb '+str(entity.nb)+' already exists!'
            self.lineloops[entity.nb] = entity
        elif isinstance(entity, ent.PlaneSurface):
            assert not self.surfaces.get(entity.nb), 'Surface nb '+str(entity.nb)+' already exists!'
            self.surfaces[entity.nb] = entity
        elif isinstance(entity, ent.SurfaceLoop):
            assert not self.surfaceloops.get(entity.nb), 'SurfaceLoop nb '+str(entity.nb)+' already exists!'
            self.surfaceloops[entity.nb] = entity
        elif isinstance(entity, ent.Volume):
            assert not self.volumes.get(entity.nb), 'Volume nb '+str(entity.nb)+' already exists!'
            self.volumes[entity.nb] = entity

    def addGroup(self, group):
        assert isinstance(group, ent.PhysicalGroup), 'Not a PhysicalGroup object'
        assert not self.groups.get(group.nb), 'PhysicalGroup nb '+str(group.nb)+' already exists!'
        self.groups[group.nb] = group

    def addField(self, field):
        assert isinstance(field, fld.Field), 'Not a Field object'
        assert not self.fields.get(field.nb), 'Field nb '+str(field.nb)+' already exists!'
        self.fields[field.nb] = field

    def setBackgroundField(self, field):
        if not self.fields.get(field.nb):
            self.fields[field.nb] = field
        self.BackgroundField = field

    def writeGeo(self, filename):
        geo = open(filename,'w')
        for key, entity in self.points.items():
            geo.write("{0}({1}) = {2};\n".format(entity.name, key, entity._val2str()))
        for key, entity in self.lines.items():
            geo.write("{0}({1}) = {2};\n".format(entity.name, key, entity._val2str()))
        for key, entity in self.lineloops.items():
            geo.write("{0}({1}) = {2};\n".format(entity.name, key, entity._val2str()))
        for key, entity in self.surfaces.items():
            geo.write("{0}({1}) = {2};\n".format(entity.name, key, entity._val2str()))

        # Physical Groups
        geo.write('\n// Physical Groups\n')
        for i, group in self.groups.items():
            if group.name:
                name = '"'+group.name+'", '+str(group.nb)
            else:
                name = group.nb
            if group.points:
                points = []
                for key, point in group.points.items():
                    points.append(point.nb)
                geo.write("Physical Point({0}) = {{{1}}};\n".format(name, str(points)[1:-1]))
            if group.lines:
                lines = []
                for key, line in group.lines.items():
                    lines.append(line.nb)
                geo.write("Physical Line({0}) = {{{1}}};\n".format(name, str(lines)[1:-1]))
            if group.surfaces:
                surfaces = []
                for key, surface in group.surfaces.items():
                    surfaces.append(surface.nb)
                    geo.write("Physical Surface({0}) = {{{1}}};\n".format(name, str(surfaces)[1:-1]))
            if group.volumes:
                volumes = []
                for key, volume in group.volumes.items():
                    volumes.append(volume.nb)
                geo.write("Physical Volume({0}) = {{{1}}};\n".format(name, str(volumes)[1:-1]))

        for i, field in self.fields.items():
            geo.write('Field[{0}] = {1};\n'.format(field.nb, field.name))
            for attr in field.__dict__:
                val = getattr(field, attr)
                if val is not None:
                    if isinstance(val, str):
                        val_str = '"'+val+'"'
                    elif attr == 'EdgesList' or attr =='NodesList' or attr == 'FacesList' or attr == 'RegionsList' or attr == 'FieldsList':
                        val_str = '{'+str([v.nb for v in val])[1:-1]+'}'
                    else:
                        val_str = str(val)
                        if isinstance(val, (list, tuple)):
                            val_str = '{'+val_str[1:-1]+'}' # replace () by {} in string
                    geo.write('Field[{0}].{1} = {2};\n'.format(field.nb, attr, val_str))

        if self.BackgroundField:
            geo.write("Background Field = {0};\n".format(self.BackgroundField.nb))
        if self.BoundaryLayerField:
            geo.write("BoundaryLayer Field = {0};\n".format(self.BoundaryLayerField.nb))

        def write_option(class_instance):
            class_name = class_instance.__class__.__name__
            for key in class_instance.__dict__:
                val = getattr(class_instance, key)
                if key != 'Color':
                    if val:
                        geo.write('{0}.'+key+'= {1};\n'.format(class_name, val))
                else:
                    for key2 in class_instance.Color.__dict__:
                        val2 = getattr(class_instance.Color, key2)
                        if val2:
                            geo.write('{0}.Color.'+key+'= {1};\n'.format(class_name, val2))

        for key in self.Options.__dict__:
            options = getattr(self.Options, key)
            write_option(options)

        if self.Coherence:
            geo.write("Coherence;\n") # remove duplicates

        geo.close()


class OptionsHolder:
    def __init__(self):
        self.Mesh = opt.Mesh()
        self.General = opt.General()
        self.Geometry = opt.Geometry()


def geometry_to_gmsh(domain):
    self = domain
    lines_dict = {}

    mesh = Mesh()

    if self.boundaryTags:
        for i, tag in enumerate(self.boundaryTags):
            phys = PhysicalGroup(nb=i, name=tag)
            mesh.addPhysicalGroup(phys)

    for i, v in enumerate(self.vertices):
        p = Point(v)
        mesh.addEntity(p)
        g = mesh.physicalgroups.get(self.vertexFlags[i])
        if g:
            g.addEntity(p)
        
    for i, s in enumerate(self.segments):
        lines_dict[s[0]][s[1]] = i
        l = Line([s[0]+1, s[1]+1])
        mesh.addEntity(l)
        g = mesh.physicalgroups.get(self.segmentFlags[i])
        if g:
            g.addEntity(l)

    for i, f in enumerate(self.facets):
        if self.nd == 3 or (self.nd == 2 and i not in self.holes_ind):
            lineloop = []
            lineloops = []
            for j, subf in enumerate(f):
                # vertices in facet
                for k, ver in enumerate(subf):
                    if ver in lines_dict[subf[k-1]].keys():
                        lineloop += [lines_dict[subf[k-1]][ver]+1]
                    elif subf[k-1] in lines_dict[ver].keys():
                        # reversed
                        lineloop += [-(lines_dict[ver][subf[k-1]]+1)]
                    else:
                        l = Line(mesh.points[subf[k-1]+1], ver+1)
                        mesh.addEntity(l)
                        lineloop += [l.nb]
                ll = LineLoop(lineloop)
                mesh.addEntity(ll)
                lineloops += [ll.nb]
            s = Surface(lineloops)
            mesh.addEntity(s)
            g = mesh.physicalgroups.get(self.facetFlags[i])
            if g:
                g.addEntity(s)

    for i, V in enumerate(self.volumes):
        surface_loops = []
        if i not in self.holes_ind:
            for j, sV in enumerate(V):
                sl = SurfaceLoop((np.array(sV)+1).tolist())
                mesh.addEntity(sl)
                surface_loops += [sl.nb]
            vol = Volume(surface_loops)
            mesh.addEntity(vol)
            g = mesh.physicalgroups.get(self.regionFlags[i])
            if g:
                g.addEntity(vol)

    return mesh
 
