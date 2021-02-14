import Rhino
import rhinoscriptsyntax as rs
import scriptcontext

def MarkSelfIntersectingMeshFaces():
    
    print("Mark Selfintersections Starts !")
    
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt("Select mesh to mark selfintersections")
    go.GeometryFilter = Rhino.DocObjects.ObjectType.Mesh
    go.SubObjectSelect = False
    go.GroupSelect = False
    go.Get()
    if go.CommandResult()!=Rhino.Commands.Result.Success:
        return Rhino.Commands.Result.Cancel    
    
    mesh = go.Object(0).Mesh()
    rs.UnselectAllObjects()
    
    topEdges = mesh.TopologyEdges
    topVertices = mesh.TopologyVertices
    
    intersectingEdges = []
    
    for ei in xrange(0, topEdges.Count):
        ij = topEdges.GetTopologyVertices(ei)
        faceIndexSet = set(topVertices.ConnectedFaces(ij.I))
        faceIndexSet.update(topVertices.ConnectedFaces(ij.J))
        
        edgeLine = topEdges.EdgeLine(ei)
        rc, faces = Rhino.Geometry.Intersect.Intersection.MeshLine(mesh, edgeLine)
        if faces is not None:
            faceSet = set(faces)
            faceSet = faceSet - faceIndexSet
            if len(faceSet) > 0:
                intersectingEdges.append(edgeLine)
    for i in xrange(0, len(intersectingEdges)):
        edge = intersectingEdges[i]
        rs.AddLine(edge.From, edge.To)
    
    print("Mark Selfintersections Finished !")

if (__name__=="__main__"):
    MarkSelfIntersectingMeshFaces()

