Clazz.declarePackage ("J.export");
Clazz.load (["J.export.__CartesianExporter", "java.util.Hashtable", "JU.P3"], "J.export._VrmlExporter", ["java.lang.Boolean", "$.Float", "$.Short", "JU.A4", "$.AU", "$.Lst", "$.Measure", "$.PT", "$.Quat", "J.export.UseTable", "JU.Geodesic", "JV.Viewer"], function () {
c$ = Clazz.decorateAsClass (function () {
this.useTable = null;
this.htSpheresRendered = null;
this.plateVertices = null;
this.plateIndices = null;
this.plateColixes = null;
this.tempQ1 = null;
this.tempQ2 = null;
this.tempQ3 = null;
this.oneFace = null;
this.threeVertices = null;
this.fontSize = 0;
this.fontFace = null;
this.fontStyle = null;
this.fontChild = null;
Clazz.instantialize (this, arguments);
}, J["export"], "_VrmlExporter", J["export"].__CartesianExporter);
Clazz.prepareFields (c$, function () {
this.htSpheresRendered =  new java.util.Hashtable ();
this.tempQ1 =  new JU.P3 ();
this.tempQ2 =  new JU.P3 ();
this.tempQ3 =  new JU.P3 ();
});
Clazz.makeConstructor (c$, 
function () {
Clazz.superConstructor (this, J["export"]._VrmlExporter, []);
this.useTable =  new J["export"].UseTable ("USE ");
this.commentChar = "# ";
this.canCapCylinders = true;
this.solidOnly = true;
});
Clazz.defineMethod (c$, "output", 
function (pt) {
this.output (J["export"].___Exporter.round (pt));
}, "JU.T3");
Clazz.overrideMethod (c$, "outputHeader", 
function () {
this.output ("#VRML V2.0 utf8 Generated by Jmol " + JV.Viewer.getJmolVersion () + "\n");
this.output ("WorldInfo { \n");
this.output (" title " + JU.PT.esc (this.vwr.ms.modelSetName) + "\n");
this.output (" info [ \"Generated by Jmol " + JV.Viewer.getJmolVersion () + " \", \n");
this.output ("  \"http://www.jmol.org \", \n");
this.output ("  \"Creation date: " + this.getExportDate () + " \" ]\n");
this.output ("} \n");
this.output ("NavigationInfo { type \"EXAMINE\" } \n");
this.output ("Background { skyColor [" + this.rgbFractionalFromColix (this.backgroundColix) + "] } \n");
var angle = this.getViewpoint ();
this.output ("Viewpoint{fieldOfView " + angle);
this.output (" position ");
this.cameraPosition.scale (this.exportScale);
this.output (this.cameraPosition);
this.output (" orientation ");
this.output (this.tempP1);
this.output (" " + -this.viewpoint.angle);
this.output ("\n jump TRUE description \"v1\"\n}\n\n");
this.output (this.getJmolPerspective ());
this.outputInitialTransform ();
this.output ("\n");
});
Clazz.defineMethod (c$, "outputInitialTransform", 
function () {
this.pushMatrix ();
this.outputAttr ("scale", this.exportScale, this.exportScale, this.exportScale);
this.outputCloseTag ();
this.outputChildStart ();
this.pushMatrix ();
this.tempP1.setT (this.center);
this.tempP1.scale (-1);
this.outputAttrPt ("translation", this.tempP1);
this.outputCloseTag ();
this.outputChildStart ();
});
Clazz.defineMethod (c$, "getViewpoint", 
function () {
this.viewpoint.setM (this.vwr.tm.matrixRotate);
this.tempP1.set (this.viewpoint.x, this.viewpoint.y, (this.viewpoint.angle == 0 ? 1 : this.viewpoint.z));
return (this.apertureAngle * 3.141592653589793 / 180);
});
Clazz.overrideMethod (c$, "outputFooter", 
function () {
this.useTable = null;
this.output ("\n]}\n");
this.output ("]}");
});
Clazz.defineMethod (c$, "outputAppearance", 
function (colix, isText) {
var def = this.getDef ((isText ? "T" : "") + colix);
this.output ("appearance ");
if (def.charAt (0) == '_') {
var color = this.rgbFractionalFromColix (colix);
this.output (" DEF " + def + " Appearance{material Material{diffuseColor ");
if (isText) this.output (" 0 0 0 specularColor 0 0 0 ambientIntensity 0.0 shininess 0.0 emissiveColor " + color + " }}");
 else this.output (color + " transparency " + J["export"].___Exporter.translucencyFractionalFromColix (colix) + "}}");
return;
}this.output (def);
}, "~N,~B");
Clazz.defineMethod (c$, "pushMatrix", 
function () {
this.output ("Transform{");
});
Clazz.defineMethod (c$, "popMatrix", 
function () {
this.output ("}\n");
});
Clazz.defineMethod (c$, "outputAttrPt", 
function (attr, pt) {
this.output (" " + attr + " " + pt.x + " " + pt.y + " " + pt.z);
}, "~S,JU.T3");
Clazz.defineMethod (c$, "outputAttr", 
function (attr, x, y, z) {
this.output (" " + attr + " " + J["export"].___Exporter.round (x) + " " + J["export"].___Exporter.round (y) + " " + J["export"].___Exporter.round (z));
}, "~S,~N,~N,~N");
Clazz.defineMethod (c$, "outputRotation", 
function (a) {
this.output (" rotation " + a.x + " " + a.y + " " + a.z + " " + a.angle);
}, "JU.A4");
Clazz.defineMethod (c$, "outputTransRot", 
function (pt1, pt2, x, y, z) {
this.tempV1.ave (pt2, pt1);
this.outputAttrPt ("translation", this.tempV1);
this.tempV1.sub (pt1);
this.tempV1.normalize ();
this.tempV2.set (x, y, z);
this.tempV2.add (this.tempV1);
this.outputRotation (JU.A4.newVA (this.tempV2, 3.141592653589793));
}, "JU.P3,JU.P3,~N,~N,~N");
Clazz.defineMethod (c$, "outputQuaternionFrame", 
function (ptCenter, ptX, ptY, ptZ, xScale, yScale, zScale) {
this.tempQ1.setT (ptX);
this.tempQ2.setT (ptY);
var a = JU.Quat.getQuaternionFrame (ptCenter, this.tempQ1, this.tempQ2).toAxisAngle4f ();
if (!Float.isNaN (a.x)) {
this.tempQ1.set (a.x, a.y, a.z);
this.outputRotation (a);
}var sx = (ptX.distance (ptCenter) * xScale);
var sy = (ptY.distance (ptCenter) * yScale);
var sz = (ptZ.distance (ptCenter) * zScale);
this.outputAttr ("scale", sx, sy, sz);
}, "JU.P3,JU.P3,JU.P3,JU.P3,~N,~N,~N");
Clazz.defineMethod (c$, "outputChildShapeStart", 
function () {
this.outputChildStart ();
this.outputShapeStart ();
});
Clazz.defineMethod (c$, "outputChildStart", 
function () {
this.output (" children[");
});
Clazz.defineMethod (c$, "outputShapeStart", 
function () {
this.output (" Shape{geometry ");
});
Clazz.defineMethod (c$, "outputDefChildFaceSet", 
function (child) {
if (child != null) this.output ("DEF " + child + " ");
this.outputFaceSetStart ();
}, "~S");
Clazz.defineMethod (c$, "outputFaceSetStart", 
function () {
this.output ("IndexedFaceSet {");
});
Clazz.defineMethod (c$, "outputFaceSetClose", 
function () {
this.output ("}\n");
});
Clazz.defineMethod (c$, "outputUseChildClose", 
function (child) {
this.output (child);
}, "~S");
Clazz.defineMethod (c$, "outputChildShapeClose", 
function () {
this.outputShapeClose ();
this.outputChildClose ();
});
Clazz.defineMethod (c$, "outputChildClose", 
function () {
this.output ("]");
});
Clazz.defineMethod (c$, "outputShapeClose", 
function () {
this.output ("}");
});
Clazz.defineMethod (c$, "outputCloseTag", 
function () {
});
Clazz.overrideMethod (c$, "outputCircle", 
function (pt1, pt2, radius, colix, doFill) {
if (doFill) {
this.pushMatrix ();
this.tempV1.ave (pt1, pt2);
this.outputAttr ("translation", this.tempV1.x, this.tempV1.y, this.tempV1.z);
this.output (" children [ Billboard{axisOfRotation 0 0 0 children [ Transform{rotation 1 0 0 1.5708");
var height = (pt1.distance (pt2));
this.outputAttr ("scale", radius, height, radius);
this.outputCylinderChildScaled (colix, 2);
this.output ("}] }]\n");
this.popMatrix ();
return;
}var child = this.getDef ("C" + colix + "_" + radius);
this.pushMatrix ();
this.outputTransRot (pt1, pt2, 0, 0, 1);
this.outputAttr ("scale", radius, radius, radius);
this.output (" children [");
if (child.charAt (0) == '_') {
this.output ("DEF " + child);
this.output (" Billboard{axisOfRotation 0 0 0 children [ Transform{children[");
this.output (" Shape{");
this.output ("geometry Extrusion{beginCap FALSE convex FALSE endCap FALSE creaseAngle 1.57");
this.output (" crossSection [");
var rpd = 0.017453292;
var scale = 0.02 / radius;
for (var i = 0; i <= 360; i += 10) {
this.output (J["export"].___Exporter.round (Math.cos (i * rpd) * scale) + " ");
this.output (J["export"].___Exporter.round (Math.sin (i * rpd) * scale) + " ");
}
this.output ("] spine [");
for (var i = 0; i <= 360; i += 10) {
this.output (J["export"].___Exporter.round (Math.cos (i * rpd)) + " ");
this.output (J["export"].___Exporter.round (Math.sin (i * rpd)) + " 0 ");
}
this.output ("]");
this.output ("}");
this.outputAppearance (colix, false);
this.output ("}");
this.output ("]} ]}");
} else {
this.output (child);
}this.output ("]");
this.popMatrix ();
}, "JU.P3,JU.P3,~N,~N,~B");
Clazz.overrideMethod (c$, "outputCone", 
function (ptBase, ptTip, radius, colix) {
var height = (ptBase.distance (ptTip));
this.pushMatrix ();
this.outputTransRot (ptBase, ptTip, 0, 1, 0);
this.outputAttr ("scale", radius, height, radius);
this.outputCloseTag ();
this.outputChildShapeStart ();
var child = this.getDef ("c");
if (child.charAt (0) == '_') {
this.outputDefChildFaceSet (child);
this.outputConeGeometry (true);
this.outputFaceSetClose ();
} else {
this.outputUseChildClose (child);
}this.outputAppearance (colix, false);
this.outputChildShapeClose ();
this.popMatrix ();
}, "JU.P3,JU.P3,~N,~N");
Clazz.defineMethod (c$, "outputConeGeometry", 
 function (addBase) {
var ndeg = 10;
var n = Clazz.doubleToInt (360 / ndeg);
var vertexCount = n + (addBase ? 2 : 1);
var faces = JU.AU.newInt2 (n * (addBase ? 2 : 1));
for (var i = 0, fpt = 0; i < n; i++) {
faces[fpt++] =  Clazz.newIntArray (-1, [i, (i + n - 1) % n, n]);
if (addBase) faces[fpt++] =  Clazz.newIntArray (-1, [i, (i + 1) % n, n + 1]);
}
var vertexes =  new Array (vertexCount);
for (var i = 0; i < n; i++) {
var x = (Math.cos (i * ndeg / 180. * 3.141592653589793));
var y = (Math.sin (i * ndeg / 180. * 3.141592653589793));
vertexes[i] = JU.P3.new3 (x, -0.5, y);
}
vertexes[n++] = JU.P3.new3 (0, 0.5, 0);
if (addBase) vertexes[n++] = JU.P3.new3 (0, -0.5, 0);
this.outputGeometry (vertexes, null, null, faces, null, vertexCount, faces.length, null, 3, null, null, null);
}, "~B");
Clazz.overrideMethod (c$, "outputCylinder", 
function (ptCenter, pt1, pt2, colix, endcaps, radius, ptX, ptY, checkRadius) {
var height = (pt1.distance (pt2));
if (radius < 0.01 || height == 0) return false;
this.pushMatrix ();
if (ptX == null) {
this.outputTransRot (pt1, pt2, 0, 1, 0);
this.outputAttr ("scale", radius, height, radius);
} else {
this.outputAttrPt ("translation", ptCenter);
this.outputQuaternionFrame (ptCenter, ptY, pt1, ptX, 2, 2, 2);
pt1.set (0, 0, -0.5);
pt2.set (0, 0, 0.5);
}this.outputCloseTag ();
this.outputCylinderChildScaled (colix, endcaps);
this.popMatrix ();
if (radius > 0.1) switch (endcaps) {
case 3:
this.outputSphere (pt1, radius * 1.01, colix, checkRadius);
case 5:
case 4:
this.outputSphere (pt2, radius * 1.01, colix, checkRadius);
break;
case 2:
break;
}
return true;
}, "JU.P3,JU.P3,JU.P3,~N,~N,~N,JU.P3,JU.P3,~B");
Clazz.defineMethod (c$, "outputCylinderChildScaled", 
function (colix, endcaps) {
this.outputChildShapeStart ();
var child = this.getDef ("C" + "_" + endcaps);
if (child.charAt (0) == '_') {
this.outputDefChildFaceSet (child);
this.outputCylinderGeometry (endcaps);
this.outputFaceSetClose ();
} else {
this.outputUseChildClose (child);
}this.outputAppearance (colix, false);
this.outputChildShapeClose ();
}, "~N,~N");
Clazz.defineMethod (c$, "outputCylinderGeometry", 
 function (endcaps) {
var ndeg = 10;
var n = Clazz.doubleToInt (360 / ndeg);
var vertexCount = n * 2;
var addEndcaps = false;
switch (endcaps) {
case 3:
case 5:
case 4:
case 2:
vertexCount += 2;
addEndcaps = true;
break;
}
var faces = JU.AU.newInt2 (n * (addEndcaps ? 4 : 2));
for (var i = 0, fpt = 0; i < n; i++) {
faces[fpt++] =  Clazz.newIntArray (-1, [i, (i + 1) % n, i + n]);
faces[fpt++] =  Clazz.newIntArray (-1, [(i + 1) % n, (i + 1) % n + n, i + n]);
if (addEndcaps) {
faces[fpt++] =  Clazz.newIntArray (-1, [i, (i + n - 1) % n, vertexCount - 2]);
faces[fpt++] =  Clazz.newIntArray (-1, [i + n, (i + n + 1) % n + n, vertexCount - 1]);
}}
var vertexes =  new Array (vertexCount);
for (var i = 0; i < n; i++) {
var x = (Math.cos (i * ndeg / 180. * 3.141592653589793));
var y = (Math.sin (i * ndeg / 180. * 3.141592653589793));
vertexes[i] = JU.P3.new3 (x, 0.5, y);
}
for (var i = 0; i < n; i++) {
var x = (Math.cos ((i + 0.5) * ndeg / 180 * 3.141592653589793));
var y = (Math.sin ((i + 0.5) * ndeg / 180 * 3.141592653589793));
vertexes[i + n] = JU.P3.new3 (x, -0.5, y);
}
if (addEndcaps) {
vertexes[vertexCount - 2] = JU.P3.new3 (0, 0.5, 0);
vertexes[vertexCount - 1] = JU.P3.new3 (0, -0.5, 0);
}this.outputGeometry (vertexes, null, null, faces, null, vertexCount, faces.length, null, 3, null, null, null);
}, "~N");
Clazz.overrideMethod (c$, "outputSphere", 
function (ptCenter, radius, colix, checkRadius) {
var check = J["export"].___Exporter.round (ptCenter) + (checkRadius ? " " + Clazz.floatToInt (radius * 100) : "");
if (this.htSpheresRendered.get (check) != null) return;
this.htSpheresRendered.put (check, Boolean.TRUE);
this.outputSphereChildScaled (ptCenter, radius, null, colix);
}, "JU.P3,~N,~N,~B");
Clazz.overrideMethod (c$, "outputEllipsoid", 
function (ptCenter, points, colix) {
this.outputSphereChildScaled (ptCenter, 1.0, points, colix);
}, "JU.P3,~A,~N");
Clazz.defineMethod (c$, "outputSphereChildScaled", 
 function (ptCenter, radius, points, colix) {
this.pushMatrix ();
this.outputAttrPt ("translation", ptCenter);
if (points == null) this.outputAttr ("scale", radius, radius, radius);
 else this.outputQuaternionFrame (ptCenter, points[1], points[3], points[5], 1, 1, 1);
this.outputCloseTag ();
this.outputChildShapeStart ();
var child = this.getDef ("S");
if (child.charAt (0) == '_') {
this.outputDefChildFaceSet (child);
this.outputSphereGeometry ();
this.outputFaceSetClose ();
} else {
this.outputUseChildClose (child);
}this.outputAppearance (colix, false);
this.outputChildShapeClose ();
this.popMatrix ();
}, "JU.P3,~N,~A,~N");
Clazz.defineMethod (c$, "outputSphereGeometry", 
 function () {
var vertices = JU.Geodesic.getVertexVectors ();
var nVertices = 162;
var faceList = JU.Geodesic.getFaceVertexes (2);
var nFaces = Clazz.doubleToInt (faceList.length / 3);
var indices =  Clazz.newIntArray (nFaces, 3, 0);
for (var i = 0, p = 0; i < nFaces; i++) for (var j = 0; j < 3; j++) indices[i][j] = faceList[p++];


this.outputGeometry (vertices, null, null, indices, null, nVertices, nFaces, null, 3, null, null, null);
});
Clazz.overrideMethod (c$, "outputSolidPlate", 
function (tempP1, tempP2, tempP3, colix) {
if (this.plateVertices == null) {
this.plateVertices =  new Array (6);
for (var i = 0; i < 6; i++) this.plateVertices[i] =  new JU.P3 ();

this.plateIndices =  Clazz.newArray (-1, [ Clazz.newIntArray (-1, [0, 1, 2]),  Clazz.newIntArray (-1, [5, 4, 3]),  Clazz.newIntArray (-1, [0, 3, 1]),  Clazz.newIntArray (-1, [1, 3, 4]),  Clazz.newIntArray (-1, [1, 4, 2]),  Clazz.newIntArray (-1, [2, 4, 5]),  Clazz.newIntArray (-1, [2, 5, 0]),  Clazz.newIntArray (-1, [0, 5, 3])]);
}JU.Measure.calcNormalizedNormal (tempP1, tempP2, tempP3, this.tempV1, this.tempV2);
this.tempV1.scale (0.2);
this.plateVertices[0].setT (tempP1);
this.plateVertices[1].setT (tempP2);
this.plateVertices[2].setT (tempP3);
for (var i = 0; i < 3; i++) this.plateVertices[i].add (this.tempV1);

this.tempV1.scale (-2);
for (var i = 3; i < 6; i++) this.plateVertices[i].add2 (this.plateVertices[i - 3], this.tempV1);

this.outputSurface (this.plateVertices, null, null, this.plateIndices, this.plateColixes, 6, 8, 8, null, 3, colix, null, null, null);
}, "JU.P3,JU.P3,JU.P3,~N");
Clazz.overrideMethod (c$, "outputSurface", 
function (vertices, normals, colixes, indices, polygonColixes, nVertices, nPolygons, nTriangles, bsPolygons, faceVertexMax, colix, colorList, htColixes, offset) {
this.outputShapeStart ();
this.outputDefChildFaceSet (null);
this.outputGeometry (vertices, normals, colixes, indices, polygonColixes, nVertices, nPolygons, bsPolygons, faceVertexMax, colorList, htColixes, offset);
this.outputFaceSetClose ();
this.outputAppearance (colix, false);
this.outputShapeClose ();
}, "~A,~A,~A,~A,~A,~N,~N,~N,JU.BS,~N,~N,JU.Lst,java.util.Map,JU.P3");
Clazz.defineMethod (c$, "outputGeometry", 
function (vertices, normals, colixes, indices, polygonColixes, nVertices, nPolygons, bsPolygons, faceVertexMax, colorList, htColixes, offset) {
if (polygonColixes == null) this.output ("  creaseAngle 0.5  \n");
 else this.output (" colorPerVertex FALSE\n");
this.output ("coord Coordinate {\npoint [\n");
this.outputVertices (vertices, nVertices, offset);
this.output ("   ]\n");
this.output ("  }\n");
this.output ("  coordIndex [\n");
var map =  Clazz.newIntArray (nVertices, 0);
this.getCoordinateMap (vertices, map, null);
this.outputIndices (indices, map, nPolygons, bsPolygons, faceVertexMax);
this.output ("  ]\n");
if (normals != null) {
var vNormals =  new JU.Lst ();
map = this.getNormalMap (normals, nVertices, null, vNormals);
this.output ("  solid FALSE\n  normalPerVertex TRUE\n   normal Normal {\n  vector [\n");
this.outputNormals (vNormals);
this.output ("   ]\n");
this.output ("  }\n");
this.output ("  normalIndex [\n");
this.outputIndices (indices, map, nPolygons, bsPolygons, faceVertexMax);
this.output ("  ]\n");
}map = null;
if (colorList != null) {
this.output ("  color Color { color [\n");
this.outputColors (colorList);
this.output ("  ] } \n");
this.output ("  colorIndex [\n");
this.outputColorIndices (indices, nPolygons, bsPolygons, faceVertexMax, htColixes, colixes, polygonColixes);
this.output ("  ]\n");
}}, "~A,~A,~A,~A,~A,~N,~N,JU.BS,~N,JU.Lst,java.util.Map,JU.P3");
Clazz.overrideMethod (c$, "outputFace", 
function (face, map, faceVertexMax) {
this.output (map[face[0]] + " " + map[face[1]] + " " + map[face[2]] + " -1\n");
if (faceVertexMax == 4 && face.length == 4) this.output (map[face[0]] + " " + map[face[2]] + " " + map[face[3]] + " -1\n");
}, "~A,~A,~N");
Clazz.defineMethod (c$, "outputNormals", 
function (vNormals) {
var n = vNormals.size ();
for (var i = 0; i < n; i++) {
this.output (vNormals.get (i));
}
}, "JU.Lst");
Clazz.defineMethod (c$, "outputColors", 
function (colorList) {
var nColors = colorList.size ();
for (var i = 0; i < nColors; i++) {
var color = this.rgbFractionalFromColix (colorList.get (i).shortValue ());
this.output (" ");
this.output (color);
this.output ("\n");
}
}, "JU.Lst");
Clazz.defineMethod (c$, "outputColorIndices", 
function (indices, nPolygons, bsPolygons, faceVertexMax, htColixes, colixes, polygonColixes) {
var isAll = (bsPolygons == null);
var i0 = (isAll ? nPolygons - 1 : bsPolygons.nextSetBit (0));
for (var i = i0; i >= 0; i = (isAll ? i - 1 : bsPolygons.nextSetBit (i + 1))) {
if (polygonColixes == null) {
this.output (htColixes.get (Short.$valueOf (colixes[indices[i][0]])) + " " + htColixes.get (Short.$valueOf (colixes[indices[i][1]])) + " " + htColixes.get (Short.$valueOf (colixes[indices[i][2]])) + " -1\n");
if (faceVertexMax == 4 && indices[i].length == 4) this.output (htColixes.get (Short.$valueOf (colixes[indices[i][0]])) + " " + htColixes.get (Short.$valueOf (colixes[indices[i][2]])) + " " + htColixes.get (Short.$valueOf (colixes[indices[i][3]])) + " -1\n");
} else {
this.output (htColixes.get (Short.$valueOf (polygonColixes[i])) + "\n");
}}
}, "~A,~N,JU.BS,~N,java.util.Map,~A,~A");
Clazz.overrideMethod (c$, "outputTriangle", 
function (pt1, pt2, pt3, colix) {
this.output ("Shape{geometry IndexedFaceSet{ ");
this.outputTriangleGeometry (pt1, pt2, pt3, colix);
this.output ("}\n");
this.outputAppearance (colix, false);
this.output ("}\n");
}, "JU.T3,JU.T3,JU.T3,~N");
Clazz.defineMethod (c$, "outputTriangleGeometry", 
 function (pt1, pt2, pt3, colix) {
if (this.oneFace == null) {
this.oneFace =  Clazz.newArray (-1, [ Clazz.newIntArray (-1, [0, 1, 2])]);
this.threeVertices =  Clazz.newArray (-1, [this.tempP1, this.tempP2, this.tempP3]);
}this.threeVertices[0].setT (pt1);
this.threeVertices[1].setT (pt2);
this.threeVertices[2].setT (pt3);
this.outputGeometry (this.threeVertices, null, null, this.oneFace, null, 3, 1, null, 3, null, null, null);
}, "JU.T3,JU.T3,JU.T3,~N");
Clazz.overrideMethod (c$, "outputTextPixel", 
function (pt, argb) {
}, "JU.P3,~N");
Clazz.overrideMethod (c$, "plotText", 
function (x, y, z, colix, text, font3d) {
this.pushMatrix ();
this.tempP3.set (x, y, this.fixScreenZ (z));
this.tm.unTransformPoint (this.tempP3, this.tempP1);
this.outputAttrPt ("translation", this.tempP1);
this.setFont (colix, text, font3d);
this.outputChildStart ();
if (this.fontChild.charAt (0) == '_') {
this.output ("DEF " + this.fontChild + " Billboard{");
this.outputAttr ("axisOfRotation", 0, 0, 0);
this.outputChildStart ();
this.pushMatrix ();
this.outputChildShapeStart ();
this.output ("Text{fontStyle ");
var fontstyle = this.getDef ("F" + this.fontFace + this.fontStyle);
if (fontstyle.charAt (0) == '_') {
this.output ("DEF " + fontstyle + " FontStyle{size " + this.fontSize + " family \"" + this.fontFace + "\" style \"" + this.fontStyle + "\"}");
} else {
this.output (fontstyle);
}this.output (" string " + JU.PT.esc (text) + "}");
this.outputAppearance (colix, true);
this.outputChildShapeClose ();
this.popMatrix ();
this.outputChildClose ();
this.output ("}");
} else {
this.output (this.fontChild);
}this.outputChildClose ();
this.popMatrix ();
}, "~N,~N,~N,~N,~S,JU.Font");
Clazz.defineMethod (c$, "setFont", 
 function (colix, text, font3d) {
this.fontStyle = font3d.fontStyle.toUpperCase ();
this.fontFace = font3d.fontFace.toUpperCase ();
this.fontFace = (this.fontFace.equals ("MONOSPACED") ? "TYPEWRITER" : this.fontFace.equals ("SERIF") ? "SERIF" : "Arial");
this.fontSize = font3d.fontSize * 0.015;
this.fontChild = this.getDef ("T" + colix + this.fontFace + this.fontStyle + this.fontSize + "_" + text);
}, "~N,~S,JU.Font");
Clazz.defineMethod (c$, "getDef", 
function (key) {
return (this.useTable == null ? "_" : this.useTable.getDef (key));
}, "~S");
});
