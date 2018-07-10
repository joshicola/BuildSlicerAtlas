def putIt(acr):
  if not '[' in acr: #if there is an acronymn that starts with '[', we don't use it.
  	#construct the model name.
    ind=ind2acr.index(acr)
    fullname=ind2full[ind]
    modelName='Model_'+str(ind)+'__'+fullname.replace('\\/','_').replace(' ','_').replace(',','_')+'_'
    node=nodes[acr]
    #if it exists, load it.
    (exists, mNode)=slicer.util.loadModel(RootDir+modelName+'.obj',returnNode=True)
    print(modelName,exists)
    if exists:
      if isParent[acr]: #if the acronymn is a parent AND has a model associated, we need to place the model node as a part of a leaf node in the hierarchy
        cnode=slicer.vtkMRMLModelHierarchyNode()
        cnode.SetParentNodeID(node.GetID())
        scene.AddNode(cnode)
        dnode=slicer.vtkMRMLModelDisplayNode()
        scene.AddNode(dnode)
        node.SetAndObserveDisplayNodeID(dnode.GetID())        
        node=cnode
      mNode.SetName(ind2full[ind2acr.index(acr)])
      mNode.SetScene(slicer.mrmlScene)
      #Get the color in the material file (mtl) and set it to the display node of the model
      f=open(RootDir+modelName+'.mtl','r')
      lines=f.readlines()
      rgb=map(float,lines[4].split()[1:])      
      mNode.GetDisplayNode().SetColor(rgb[0],rgb[1],rgb[2])
      mNode.GetDisplayNode().SetSliceIntersectionVisibility(True)
      #Add model node to a "Leaf" in the hierarchy.  Cannot be a parent of any other hierarchy node.
      node.SetModelNodeID(mNode.GetID())
      node.HideFromEditorsOn()#These two lines hide the "leaf" node from the editor and update... I don't know why...
      node.ExpandedOff()
    else:
      dnode=slicer.vtkMRMLModelDisplayNode()
      scene.AddNode(dnode)
      node.SetAndObserveDisplayNodeID(dnode.GetID())
      
