#This is a handy Slicer3D Script to save all vtk models as obj files

nodes=slicer.util.getNodesByClass('vtkMRMLModelNode')

for node in nodes:
	name=node.GetName()
	stNode=node.GetStorageNode()
	if stNode != None:
		fileName=stNode.GetFileName()[:-3]+'obj'
		slicer.util.saveNode(node,fileName)
	


#The above with a root node followed by parsing through the model hiearchy to create a reflective directory structure
import os
def saveChildrenNodes(Node,Dir):
	NumChild=Node.GetNumberOfChildrenNodes()
	if NumChild>0:
		for i in range(NumChild):
			chNode=Node.GetNthChildNode(i)
			print(i,NumChild,chNode.GetName())
			mNode=chNode.GetModelNode()
			print(type(mNode),chNode.GetName())
			if mNode!=None:
				print('****',mNode.GetName())
				sNode=mNode.GetStorageNode()
				if sNode!=None:
				  sName=sNode.GetFileName()
				  sName=sName[sName.rfind('/'):-3]+'obj'
				else:
				  sName=mNode.GetName()+'.obj'
				fileName=Dir+'/'+sName
				slicer.util.saveNode(mNode,fileName)
			elif type(chNode)==type(slicer.vtkMRMLModelHierarchyNode()):
				DirName=Dir+'/'+chNode.GetName().replace(' .','')
				if not os.path.exists(DirName):
					os.makedirs(DirName)
				saveChildrenNodes(chNode,DirName)


Root=slicer.util.getNode('Allen Mouse Atlas ABA v3')
Root_Dir='/home/josher/TST/'
if not os.path.exists(Root_Dir):
	os.makedirs(Root_Dir)

saveChildrenNodes(Root,Root_Dir)

nodes=slicer.util.getNodesByClass('vtkMRMLVolumeNode')
nodes+=slicer.util.getNodesByClass('vtkMRMLSceneViewNode')
for node in nodes:
	slicer.mrmlScene.RemoveNode(node)

slicer.util.saveScene(Root_Dir+'Scene.mrml')


#Unfinished DSURQE parsing of types of structures.
import csv

path='/media/josher/Phatastic/Projects/BrainDataSets/Mouse_Atlases/DSURQE_40micron/DSURQE_40micron_R_mapping.csv'
f=open(path,'r')
reader=csv.reader(f,delimiter=',')
rows=[]
for row in reader:
    rows.append(row)
D={}
for row in rows:
    if not row[3] in D.keys():
        D[row[3]]=[]
    D[row[3]].append(row[0])
    
D={}
for row in rows:
	D[row[1]]=row[0]+': right'
	D[row[2]]=row[0]+': left'
    
for k in D.keys():
	node=slicer.util.getNode('Model_'+str(k)+'_'+str(k))
	if node!=None:
		node.SetName(D[k])

