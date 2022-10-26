# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
import csv
import os
os.chdir(r"D:/Upload_GitHub")#Working directory for odb.files saving
filePath = "D:/Upload_GitHub/"#Working directory for cvs.files reading

fr = open(filePath+"Sample_result(example).csv",'r')#name of cvs. file
reader = csv.reader(fr)
paralist=list(reader)
PARALISTindex=range(len(paralist)-2)
mdb.models.changeKey(fromName='Model-1', toName='Model-0')

for i in PARALISTindex:
    print paralist[i+2]
    diameter=float(paralist[i+2][1])
    thickness=float(paralist[i+2][2])
    radius=float(paralist[i+2][3])
    frictionofbending=float(paralist[i+2][4])
    frictionofpressure=float(paralist[i+2][5])
    frictionofwiper=float(paralist[i+2][6])
    frictionofclamp=float(paralist[i+2][7])
    gapofbending=float(paralist[i+2][8])
    gapofpressure=float(paralist[i+2][9])
    gapofwiper=float(paralist[i+2][10])
    gapofclamp=float(paralist[i+2][11])
    #boosterdistanceofpressure=float(paralist[i+2][12])
    diffvelocityofpressure=float(paralist[i+2][12])
    initialpositionofpressure=float(paralist[i+2][13])
    angularvelocity=float(paralist[i+2][14])
    timeofstep1=float(paralist[i+2][16])
    lengthofclamp=0.5*radius
    lengthofpressure=3.5*radius
    lengthofwiper=1.5*radius
    widthofbending=diameter+50
    lengthofpipe=angularvelocity*timeofstep1*radius+lengthofpressure+0.5*radius;
    boostervelocityofpressure=(angularvelocity+diffvelocityofpressure)*radius;



    #1.1 Model for bending die
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(radius, 0.0), point1=(radius, -(diameter/2.0+gapofbending)), point2=(radius, 
        diameter/2.0+gapofbending), direction=CLOCKWISE)#Semicircular arc
    s.Line(point1=(radius, (diameter/2.0+gapofbending)), point2=(radius, widthofbending/2.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)#line
    s.Line(point1=(radius, -(diameter/2.0+gapofbending)), point2=(radius, -(widthofbending)/2.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)#line
    p = mdb.models['Model-0'].Part(name='bending-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['bending-die']
    p.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)#
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    p.ReferencePoint(point=(0.0, 0.0, 0.0))#Select the rigid body reference point
    mdb.models['Model-0'].parts['bending-die'].features.changeKey(fromName='RP', 
        toName='RP-bending')#rename reference point
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='bending-die')#creat reference point set

    #1.2 Tube model
        s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)

    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, diameter/2.0-thickness/2.0))
    p = mdb.models['Model-0'].Part(name='pipe', dimensionality=THREE_D, 
      type=DEFORMABLE_BODY)
    p = mdb.models['Model-0'].parts['pipe']
    p.BaseShellExtrude(sketch=s, depth=lengthofpipe)
    s.unsetPrimaryObject()
    p = mdb.models['Model-0'].parts['pipe']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3 ]', ), )
    p.Set(faces=faces, name='pipe')

    #1.3 Clamp model
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(radius, 0.0), point1=(radius, -(diameter/2.0+gapofclamp)), point2=(radius, 
        diameter/2.0+gapofclamp), direction=COUNTERCLOCKWISE)
    s.Line(point1=(radius, (diameter/2.0+gapofclamp)), point2=(radius, widthofbending/2.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.Line(point1=(radius, -(diameter/2.0+gapofclamp)), point2=(radius, -(widthofbending)/2.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    p = mdb.models['Model-0'].Part(name='clamp-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['clamp-die']
    p.BaseShellExtrude(sketch=s, depth=lengthofclamp)
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v1, e, d2, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e[4], rule=CENTER))
    mdb.models['Model-0'].parts['clamp-die'].features.changeKey(fromName='RP', 
        toName='RP-clamp')
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='clamp-die')

    #1.4 Pressure die model
    s1 = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, -(diameter/2.0+gapofpressure)), point2=(0.0, diameter/2.0+gapofpressure), 
        direction=CLOCKWISE)
    p = mdb.models['Model-0'].Part(name='pressure-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['pressure-die']
    p.BaseShellExtrude(sketch=s1, depth=lengthofpressure)
    s1.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v2, e1, d1, n1 = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e1[0], rule=CENTER))
    mdb.models['Model-0'].parts['pressure-die'].features.changeKey(fromName='RP', 
        toName='RP-pressure')
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='pressure-die')

    #1.5 Wiper die model
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, -(diameter/2.0+gapofwiper)), point2=(0.0, diameter/2.0+gapofwiper), 
        direction=CLOCKWISE)
    p = mdb.models['Model-0'].Part(name='wiper-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['wiper-die']
    p.BaseShellExtrude(sketch=s, depth=lengthofwiper)
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v1, e, d2, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e[2], rule=CENTER))
    mdb.models['Model-0'].parts['wiper-die'].features.changeKey(fromName='RP', 
        toName='RP-wiper')
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='wiper-die')

    #1.6 Insert model
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(radius, 0.0), point1=(radius, -(diameter/2.0+gapofclamp)), point2=(radius, 
        diameter/2.0+gapofclamp), direction=CLOCKWISE)
    p = mdb.models['Model-0'].Part(name='insert-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['insert-die']
    p.BaseShellExtrude(sketch=s, depth=lengthofclamp)
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v1, e, d2, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e[0], rule=CENTER))
    mdb.models['Model-0'].parts['insert-die'].features.changeKey(fromName='RP', 
        toName='RP-insert')
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='insert-die')


    #2.1 Define material
    mdb.models['Model-0'].Material(name='copper-T1')
    mdb.models['Model-0'].materials['copper-T1'].Elastic(table=((110000, 
        0.32), ))
    mdb.models['Model-0'].materials['copper-T1'].Density(table=((8.9e-09, ), ))
    mdb.models['Model-0'].materials['copper-T1'].Conductivity(table=((390, ), ))
    mdb.models['Model-0'].materials['copper-T1'].Plastic(table=((240.0, 0.0), (245.0, 
        0.01), (250.0, 0.02), (260.0, 0.03), (263.0, 0.04), (
        267.0, 0.05), (270.0, 0.06), (267.0, 0.07), (263.0, 0.08), 
        (260.0, 0.09),(255.0, 0.1)))

    mdb.models['Model-0'].Material(name='SI_mm113111_6061-T6(GB)')
    mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Elastic(table=((69000.0006661372, 
        0.33), ))
    mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Density(table=((2.7e-09, ), ))
    mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Conductivity(table=((166.9, ), ))
    mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Plastic(table=((275.0, 0.0), (275.0, 
        0.004), (275.79029, 0.01), (277.16924, 0.015), (282.68505, 0.02), (
        296.47456, 0.03), (310.26408, 0.04), (324.05359, 0.06), (344.73786, 0.08), 
        (355.76948, 0.09)))


    #2.2 Define section
    mdb.models['Model-0'].HomogeneousShellSection(name='Section-1', 
        preIntegrate=OFF, material='SI_mm113111_6061-T6(GB)', 
        thicknessType=UNIFORM, thickness=thickness, thicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=9)



    #2.3 Assign section
    p = mdb.models['Model-0'].parts['pipe']
    region = p.sets['pipe']
    p = mdb.models['Model-0'].parts['pipe']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

    #3 Assemble
    #3.1 Instance
    a = mdb.models['Model-0'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-0'].parts['bending-die']
    a.Instance(name='bending-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['clamp-die']
    a.Instance(name='clamp-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['pipe']
    a.Instance(name='pipe-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['pressure-die']
    a.Instance(name='pressure-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['wiper-die']
    a.Instance(name='wiper-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['insert-die']
    a.Instance(name='insert-die-1', part=p, dependent=ON)
    #3.2rotary
    a = mdb.models['Model-0'].rootAssembly
    a.rotate(instanceList=('bending-die-1', 'clamp-die-1','insert-die-1',), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, 1.0), angle=90.0)
    a.rotate(instanceList=('clamp-die-1','insert-die-1',), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 1.0, 0.0), angle=180.0)
    a.rotate(instanceList=('pipe-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
        0.0, 1.0, 0.0), angle=180.0)
    a.rotate(instanceList=('pressure-die-1', ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, -1.0), angle=90.0)
    a.rotate(instanceList=('wiper-die-1', ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, 1.0), angle=90.0)
    #3.3translate
    a = mdb.models['Model-0'].rootAssembly
    a.translate(instanceList=('pipe-1', ), vector=(0.0, radius, lengthofclamp+lengthofclamp))
    a.translate(instanceList=('clamp-die-1', ), vector=(0.0, 0.0, lengthofclamp))
    a.translate(instanceList=('wiper-die-1', ), vector=(0.0, radius, -lengthofwiper))
    a.translate(instanceList=('pressure-die-1', ), vector=(0.0, radius, -(lengthofpressure+initialpositionofpressure)))
    a.translate(instanceList=('insert-die-1', ), vector=(0.0, 0.0, lengthofclamp))
    #4Define step
    mdb.models['Model-0'].ExplicitDynamicsStep(name='Step-1', previous='Initial', 
    timePeriod=timeofstep1, massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 225.0, 
    0.0, None, 0, 0, 0.0, 0.0, 0, None), ))
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models['Model-0'].fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=36, timeMarks=ON)

    mdb.models['Model-0'].historyOutputRequests['H-Output-1'].setValues(
        variables=('ALLIE', 'ALLKE', 'ETOTAL'))


    #5Interaction
    #5.1 Define surface

    a = mdb.models['Model-0'].rootAssembly
    s1 = a.instances['pipe-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#3 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='pipe')


    s1 = a.instances['bending-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='bending')
    s1 = a.instances['clamp-die-1'].faces
    side2Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side2Faces=side2Faces1, name='clamp')#
    s1 = a.instances['pressure-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='pressure')#
    s1 = a.instances['wiper-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='wiper')#

    s1 = a.instances['insert-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='insert')#


    #5.2define contace property
    mdb.models['Model-0'].ContactProperty('bending')
    mdb.models['Model-0'].interactionProperties['bending'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofbending, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)#bending
    mdb.models['Model-0'].ContactProperty('pressure')
    mdb.models['Model-0'].interactionProperties['pressure'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofpressure, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)#pressure
    mdb.models['Model-0'].ContactProperty('wiper')
    mdb.models['Model-0'].interactionProperties['wiper'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofwiper, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)#wiper
    mdb.models['Model-0'].ContactProperty('clamp')
    mdb.models['Model-0'].interactionProperties['clamp'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofclamp, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)#clamp

    #5.3define contact
    a = mdb.models['Model-0'].rootAssembly
    region1=a.surfaces['bending']
    region2=a.surfaces['pipe']
    mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='bending', 
        createStepName='Step-1', master = region1, slave = region2, 
        mechanicalConstraint=PENALTY, sliding=FINITE, 
        interactionProperty='bending', initialClearance=OMIT, datumAxis=None, 
        clearanceRegion=None)#bending
    region1=a.surfaces['pressure']
    region2=a.surfaces['pipe']
    mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='pressure', 
        createStepName='Step-1', master = region1, slave = region2, 
        mechanicalConstraint=PENALTY, sliding=FINITE, 
        interactionProperty='pressure', initialClearance=OMIT, datumAxis=None, 
        clearanceRegion=None)#pressure
    region1=a.surfaces['wiper']
    region2=a.surfaces['pipe']
    mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='wiper', 
        createStepName='Step-1', master = region1, slave = region2, 
        mechanicalConstraint=PENALTY, sliding=FINITE, 
        interactionProperty='wiper', initialClearance=OMIT, datumAxis=None, 
        clearanceRegion=None)#wiper

    a = mdb.models['Model-0'].rootAssembly
    region1=a.surfaces['clamp']
    region2=a.surfaces['pipe']
    mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='clamp', 
        createStepName='Initial', master = region1, slave = region2, 
        mechanicalConstraint=PENALTY, sliding=FINITE, interactionProperty='clamp', 
        initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
    #: The interaction "clamp" has been created.

    a = mdb.models['Model-0'].rootAssembly
    region1=a.surfaces['insert']
    region2=a.surfaces['pipe']
    mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='insert', 
        createStepName='Initial', master = region1, slave = region2, 
        mechanicalConstraint=PENALTY, sliding=FINITE, interactionProperty='clamp', 
        initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
    #: The interaction "insert" has been created.


    #5.5define connection
    a = mdb.models['Model-0'].rootAssembly
    r1 = a.instances['bending-die-1'].referencePoints#
    r2 = a.instances['clamp-die-1'].referencePoints#
    a.WirePolyLine(points=((r1[2], r2[2]), ), mergeType=IMPRINT, meshable=OFF)
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(edges=edges1, name='Wire-1-Set-1')#
    a = mdb.models['Model-0'].rootAssembly
    r11 = a.instances['bending-die-1'].referencePoints
    r12 = a.instances['insert-die-1'].referencePoints
    a.WirePolyLine(points=((r11[2], r12[2]), ), mergeType=IMPRINT, meshable=OFF)
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(edges=edges1, name='Wire-2-Set-1')
    mdb.models['Model-0'].ConnectorSection(name='ConnSect-1', assembledType=BEAM)
    region=a.sets['Wire-1-Set-1']
    csa = a.SectionAssignment(sectionName='ConnSect-1', region=region)#
    mdb.models['Model-0'].ConnectorSection(name='ConnSect-2', assembledType=BEAM)
    region=a.sets['Wire-2-Set-1']
    csa = a.SectionAssignment(sectionName='ConnSect-2', region=region)

    #5.6inertia
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['clamp-die-1'].sets['clamp-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-1', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['insert-die-1'].sets['insert-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-2', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['bending-die-1'].sets['bending-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-3', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['pressure-die-1'].sets['pressure-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-4', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)

    #6boundry 
    #6.1wiper
    a = mdb.models['Model-0'].rootAssembly
    region = a.instances['wiper-die-1'].sets['wiper-die']
    mdb.models['Model-0'].EncastreBC(name='wiper', createStepName='Initial', 
        region=region, localCsys=None)
    #6.2pressure
    a = mdb.models['Model-0'].rootAssembly
    region = a.instances['pressure-die-1'].sets['pressure-die']
    mdb.models['Model-0'].VelocityBC(name='pressure', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=boostervelocityofpressure, vr1=0.0, vr2=0.0, 
        vr3=0.0, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, 
        fieldName='')

    #6.3bending
    a = mdb.models['Model-0'].rootAssembly
    region = a.instances['bending-die-1'].sets['bending-die']
    mdb.models['Model-0'].VelocityBC(name='bending', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=0.0, vr1=angularvelocity, vr2=0.0, vr3=0.0, 
        amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

    #7mesh
    #bending
    p = mdb.models['Model-0'].parts['bending-die']
    p.seedPart(size=(diameter*3.1415926)/42, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()#
    #clamp
    p = mdb.models['Model-0'].parts['clamp-die']
    p.seedPart(size=(diameter*3.1415926)/42, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #tube
    p = mdb.models['Model-0'].parts['pipe']
    p.seedPart(size=(diameter*3.1415926)/48, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #pressure
    p = mdb.models['Model-0'].parts['pressure-die']
    p.seedPart(size=(diameter*3.1415926)/42, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #wiper
    p = mdb.models['Model-0'].parts['wiper-die']
    p.seedPart(size=(diameter*3.1415926)/42, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #insert
    p = mdb.models['Model-0'].parts['insert-die']
    p.seedPart(size=(diameter*3.1415926)/42, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()

    mdb.models.changeKey(fromName='Model-0', toName='Model-'+paralist[i+2][0])#
    mdb.Model(name='Model-0', modelType=STANDARD_EXPLICIT)#
    mdb.Job(name='bending_process'+paralist[i+2][0], model='Model-'+paralist[i+2][0], description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, explicitPrecision=DOUBLE, 
    nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
    contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
    resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=1, 
    activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)#




    mdb.Model(name='Model-'+paralist[i+2][0]+'sp', objectToCopy=mdb.models['Model-'+paralist[i+2][0]])
        #: The model "Model-40sp" has been created.
    p = mdb.models['Model-'+paralist[i+2][0]+'sp'].parts['bending-die']
    a = mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly
    a.deleteFeatures(('bending-die-1', 'clamp-die-1', 'pressure-die-1', 
    'wiper-die-1', 'insert-die-1', 'Wire-2', 'Wire-1', 'Wire-1', 'Wire-2', ))
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly.sectionAssignments[1]
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly.sectionAssignments[0]
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly.engineeringFeatures.inertias['Inertia-1']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly.engineeringFeatures.inertias['Inertia-2']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly.engineeringFeatures.inertias['Inertia-3']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly.engineeringFeatures.inertias['Inertia-4']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].steps['Step-1']
    mdb.models['Model-'+paralist[i+2][0]+'sp'].interactions.delete(('clamp', 'insert', ))
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].interactionProperties['bending']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].interactionProperties['clamp']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].interactionProperties['pressure']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].interactionProperties['wiper']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].sections['ConnSect-1']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].sections['ConnSect-2']
    del mdb.models['Model-'+paralist[i+2][0]+'sp'].boundaryConditions['wiper']

    mdb.models['Model-'+paralist[i+2][0]+'sp'].StaticStep(name='Step-1', previous='Initial', 
        nlgeom=ON)
    instances=(mdb.models['Model-'+paralist[i+2][0]+'sp'].rootAssembly.instances['pipe-1'], )
    mdb.models['Model-'+paralist[i+2][0]+'sp'].InitialState(updateReferenceConfiguration=OFF, 
        fileName='bending_process'+paralist[i+2][0], endStep=LAST_STEP, endIncrement=STEP_END, 
        name='Predefined Field-1', createStepName='Initial', instances=instances)


    mdb.Job(name='springback_process'+paralist[i+2][0], model='Model-'+paralist[i+2][0]+'sp', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)



del mdb.models['Model-0']
mdb.saveAs(pathName='D:/Upload_GitHub/batch_model'+paralist[i+2][0])#Working directory for mdb.files saving
print 'End of programm'

