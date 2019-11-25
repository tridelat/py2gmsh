from . import Entity as ent
from . import Field as fld
from . import Options as opt

class Mesh:
    def __init__(self):
        self.points = {}
        self.points_count = 0
        self.lines = {}
        self.lines_count = 0
        self.lineloops = {}
        self.lineloops_count = 0
        self.surfaces = {}
        self.surfaces_count = 0
        self.surfaceloops = {}
        self.surfaceloops_count = 0
        self.volumes = {}
        self.volumes_count = 0
        self.regions = {}
        self.regions_count = 0
        self.fields = {}
        self.fields_count = 0
        self.groups = {}
        self.groups_count = 0
        self.Options = opt.OptionsHolder()
        self.BackgroundField = None
        self.BoundaryLayerField = None
        self.Coherence = False

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
            if entity.nb is None:
                self.points_count += 1
                entity.nb = self.points_count
            assert not self.points.get(entity.nb), 'Point nb '+str(entity.nb)+' already exists!'
            self.points[entity.nb] = entity
        elif isinstance(entity, ent.LineEntity):
            if entity.nb is None:
                self.lines_count += 1
                entity.nb = self.lines_count
            assert not self.lines.get(entity.nb), 'Line nb '+str(entity.nb)+' already exists!'
            self.lines[entity.nb] = entity
        elif isinstance(entity, ent.LineLoop):
            if entity.nb is None:
                self.lineloops_count += 1
                entity.nb = self.lineloops_count
            assert not self.lineloops.get(entity.nb), 'LineLoop nb '+str(entity.nb)+' already exists!'
            self.lineloops[entity.nb] = entity
        elif isinstance(entity, ent.SurfaceEntity):
            if entity.nb is None:
                self.surfaces_count += 1
                entity.nb = self.surfaces_count
            assert not self.surfaces.get(entity.nb), 'Surface nb '+str(entity.nb)+' already exists!'
            self.surfaces[entity.nb] = entity
        elif isinstance(entity, ent.SurfaceLoop):
            if entity.nb is None:
                self.surfaceloops_count += 1
                entity.nb = self.surfaceloops_count
            assert not self.surfaceloops.get(entity.nb), 'SurfaceLoop nb '+str(entity.nb)+' already exists!'
            self.surfaceloops[entity.nb] = entity
        elif isinstance(entity, ent.VolumeEntity):
            if entity.nb is None:
                self.volumes_count += 1
                entity.nb = self.volumes_count
            assert not self.volumes.get(entity.nb), 'Volume nb '+str(entity.nb)+' already exists!'
            self.volumes[entity.nb] = entity
        elif isinstance(entity, ent.PhysicalGroup):
            self.addGroup(entity)
        elif isinstance(entity, fld.Field):
            self.addField(entity)
        else:
            raise TypeError("not a valid Entity instance")

    def addEntities(self, entities):
        for entity in entities:
            self.addEntity(entity)

    def addGroup(self, group):
        assert isinstance(group, ent.PhysicalGroup), 'Not a valid PhysicalGroup instance'
        if group.nb is None:
            self.groups_count += 1
            group.nb = self.groups_count
        assert not self.groups.get(group.nb), 'PhysicalGroup nb '+str(group.nb)+' already exists!'
        self.groups[group.nb] = group

    def addField(self, field):
        assert isinstance(field, fld.Field), 'Not a valid Field instance'
        if field.nb is None:
            self.fields_count += 1
            field.nb = self.fields_count
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
        for key, entity in self.surfaceloops.items():
            geo.write("{0}({1}) = {2};\n".format(entity.name, key, entity._val2str()))
        for key, entity in self.volumes.items():
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
                    elif attr == 'EdgesList' or attr =='NodesList' or attr == 'FacesList' or attr == 'RegionsList' or attr == 'FieldsList' or attr == 'VerticesList':
                        val_str = '{'+str([v.nb for v in val])[1:-1]+'}'
                    elif attr == 'IField' or attr == 'FieldX' or attr == 'FieldY' or attr == 'FieldZ':
                        val_str = str(val.nb)
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
                        geo.write(class_name+'.'+key+'= {0};\n'.format(val))
                else:
                    for key2 in class_instance.Color.__dict__:
                        val2 = getattr(class_instance.Color, key2)
                        if val2:
                            geo.write(class_name+'.Color.'+key2+'= {0};\n'.format(val2))

        for key in self.Options.__dict__:
            options = getattr(self.Options, key)
            write_option(options)

        if self.Coherence:
            geo.write("Coherence;\n") # remove duplicates

        geo.close()


def geometry2mesh(domain):
    lines_dict = {}

    mesh = Mesh()

    # add all physical groups
    for flag in domain.vertexFlags:
        if not mesh.groups.get(flag)
            mesh.addGroup(flag)
    for flag in domain.segmentFlags:
        if not mesh.groups.get(flag)
            mesh.addGroup(flag)
    for flag in domain.facetFlags:
        if not mesh.groups.get(flag)
            mesh.addGroup(flag)
    for flag in domain.regionFlags:
        if not mesh.groups.get(flag)
            mesh.addGroup(flag)

    # add tags for BCs
    if domain.boundaryTags:
        for tag, flag in domain.boundaryTags.items():
            phys = ent.PhysicalGroup(nb=flag, name=tag)
            mesh.addGroup(phys)

    for i, v in enumerate(domain.vertices):
        if domain.nd == 2:
            p = ent.Point([v[0], v[1], 0.])
        else:
            p = ent.Point(v)
        mesh.addEntity(p)
        g = mesh.groups.get(domain.vertexFlags[i])
        if g:
            g.addEntity(p)
    nb_points = i+1
    for i in range(nb_points):
        lines_dict[i] = {}

    for i, s in enumerate(domain.segments):
        lines_dict[s[0]][s[1]] = i
        l = ent.Line([mesh.points[s[0]+1], mesh.points[s[1]+1]])
        mesh.addEntity(l)
        g = mesh.groups.get(domain.segmentFlags[i])
        if g:
            g.addEntity(l)

    for i, f in enumerate(domain.facets):
        if domain.nd == 3 or (domain.nd == 2 and i not in domain.holes_ind):
            lineloops = []
            for j, subf in enumerate(f):
                lineloop = []
                # vertices in facet
                for k, ver in enumerate(subf):
                    if ver in lines_dict[subf[k-1]].keys():
                        lineloop += [lines_dict[subf[k-1]][ver]+1]
                    elif subf[k-1] in lines_dict[ver].keys():
                        # reversed
                        lineloop += [(lines_dict[ver][subf[k-1]]+1)]
                    else:
                        l = ent.Line([mesh.points[subf[k-1]+1], mesh.points[ver+1]])
                        mesh.addEntity(l)
                        lineloop += [l.nb]
                ll = ent.LineLoop(mesh.getLinesFromIndex(lineloop))
                mesh.addEntity(ll)
                lineloops += [ll.nb]
            s = ent.PlaneSurface([mesh.lineloops[loop] for loop in lineloops])
            mesh.addEntity(s)
            g = mesh.groups.get(domain.facetFlags[i])
            if g:
                g.addEntity(s)

    for i, V in enumerate(domain.volumes):
        surface_loops = []
        hole_loops = []
        for j, sV in enumerate(V):
            sl = ent.SurfaceLoop(mesh.getSurfacesFromIndex([sVnb + 1 for sVnb in sV]))
            mesh.addEntity(sl)
            surface_loops += [sl]
        vol = ent.Volume(surface_loops)
        mesh.addEntity(vol)
        g = mesh.groups.get(domain.regionFlags[i])
        if g:
            g.addEntity(vol)

    return mesh
