#Yes, this is sloppy and needs to be cleaned up.  However, a lot of work went into getting this going so far!

#import various lists extracted from the website
execfile('/home/josher/Projects_Phat/BrainDataSets/Mouse_Atlases/ABA_v3/ind.py')
#set obj root directory
RootDir='/home/josher/Projects_Phat/BrainDataSets/Mouse_Atlases/ABA_v3/obj/small/'

#compile a dictionary indicating whether a node is a parent or not
isParent={}
for acr in ind2acr:
  isParent[acr]=(acr in ACR_TO_PARENT.values())

scene=slicer.mrmlScene

#mNodes=slicer.util.getNodes(pattern='Model_*__*')
#for k in mNodes.keys():
#  scene.RemoveNode(mNodes[k])

#Create a Node Dictionary pointing to every node in the acronymn (acr) list
nodes={}	
for acr in ind2acr:
  node=slicer.vtkMRMLModelHierarchyNode()
  node.SetName(ind2full[ind2acr.index(acr)]+' .')
  nodes[acr]=node

#Create a hierarchy by assigning parents to nodes
for acr in ind2acr: 
  if not '[' in acr:
    node=nodes[acr]
    scene.AddNode(node)
    if acr in ACR_TO_PARENT.keys():
      pNode=nodes[ACR_TO_PARENT[acr]]
      node.SetParentNodeID(pNode.GetID())
      
#File used to define hierarchy insertion function
execfile('/home/josher/Projects_Phat/BrainDataSets/Mouse_Atlases/Code/putIt.py')

#use the following to actually insert
for acr in ind2acr:
  putIt(acr)
