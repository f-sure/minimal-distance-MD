from schrodinger.application.desmond.packages import topo                 #Needed for trajectory analysis
from schrodinger.application.desmond.packages import traj                 #Needed for trajectory analysis
from schrodinger.application.desmond.packages import traj_util            #Needed for trajectory analysis
from schrodinger.application.bioluminate.interaction_calculator import *  #Needed for interaction calculations
from schrodinger.structutils.measure import *                             #Needed for measurements and analysis 
from schrodinger.application.desmond.packages import analysis             #Needed for measurements and analysis 


#############
# SETTINGS  #
#############

#File of the *.cms file containing the MD trajectories
filepath = "placeholder - enter filepath here"

#File where the results shall be saved
resultspath = "placeholder - enter filepath here"

#Specification of chains and residues of both interaction partners 
chain_name_1 = "B"  #referes to beta ENaC in our MD simulations 
start_chain_1 = 77  #first resolved residue in beta ENaC
stop_chain_1 = 512  #last resolved residue in beta ENaC

chain_name_2 = "G"  #referes to gamma ENaC in our MD simulations 
start_chain_2 = 80  #first resolved residue in gamma ENaC
stop_chain_2 = 521  #last resolved residue in gamma ENaC 



#############
# ANALYSIS  #
#############

#Create empty Arrays to save all results 
all_results = []
hun_results = []

#Open Trajectory File!
msys_model, cms_model, tr = traj_util.read_cms_and_traj(filepath)

#Open File to save results 
with open((resultspath+".csv"), "w") as file:
    #Write column headers
	file.write("frame,residue,distance" + "\n")

#Iterate through all residues in betaENaC 
for betaRes in range(start_chain_1, stop_chain_1):

	#Define the first interaction partner (the current residue in beta ENaC) 
	com = analysis.Com(msys_model, cms_model, asl='(chain.name '+chain_name_1+') AND (res.num '+str(betaRes)+')')

	#Define the second interaction partner (the first residue in gamma ENaC)
	com2 = analysis.Com(msys_model, cms_model, asl='(chain.name '+chain_name_2+') AND (res.num '+str(start_chain_2)+')')
    
	#Initialize a Distance Analyzer object from Schrödinger Desmond with the current MD simulation and the two interaction partners just defined
	distanceAnalyzer = analysis.Distance(msys_model, cms_model, com, com2)
    
 	#Perform the analysis
	results = analysis.analyze(tr, distanceAnalyzer)
    
	#The results variable now contains the first analysis for the current residue in betaENaC 
	#It is a list with the distance from this residue to the first residue, each element in the list corresponds to the distance in the corresponding frame of the simulation

	#Now, we loop through every other residue from the second interaction partner (gamma ENaC)
	for gammaRes in range(start_chain_2 + 1, stop_chain_2):
		try:
            		#Similar process as above - definition of second interaction partner 
			com2 = analysis.Com(msys_model, cms_model, asl='(chain.name '+chain_name_2+') AND (res.num '+str(gammaRes)+')')
            
            		#Initialization of Distance Analyzer Object
			distanceAnalyzer = analysis.Distance(msys_model, cms_model, com, com2)
            
            		#Perform the Analysis - save results in temp_results
			temp_results = analysis.analyze(tr, distanceAnalyzer)
            
			#The temp_results variable now contains the distance of the current residue in gammaENaC in each frame 
			
			#We iterate through our results 
			for i, res in enumerate(results):
            
                		#Now we compare if the distance of the current evaluation is lower than all previously identified comparisons 
				if(res > temp_results[i]):
                    
                    			#If this is the case, the lower distance is saved as the new "lowest distance" in the results array 
					results[i] = temp_results[i]
        
 		except: 
			#This exception is reached when a residue to be analysed is not present in the structure - this is logged in the console
			print("- EXCEPTION: "+str(gammaRes))
            
	#After the iteration through all residues in gamma, the results variable contains the lowest distance for the current residue from interaction partner 1 (betaENaC) to all residues in interaction partner 2 (gammaENaC). 
    
     	#These results are appended to the results file 
	with open((resultspath+".csv"), "a") as file:
		for i, res in enumerate(results):
			file.write(str(i) + "," + str(betaRes) + "," + str(round(res, 2)) + "\n")
