from schrodinger.application.desmond.packages import topo
from schrodinger.application.desmond.packages import traj
from schrodinger.application.desmond.packages import traj_util
from schrodinger.application.bioluminate.interaction_calculator import *
from schrodinger.structutils.measure import *
from schrodinger.application.desmond.packages import analysis

filepath = "placeholder - enter filepath here"
resultspath = "placeholder - enter filepath here"

chain_name_1 = "B" 
start_chain_1 = 77 
stop_chain_1 = 512 

chain_name_2 = "G" 
start_chain_2 = 80 
stop_chain_2 = 521 

all_results = []
hun_results = []

msys_model, cms_model, tr = traj_util.read_cms_and_traj(filepath)


with open((resultspath+".csv"), "w") as file:
	file.write("frame,residue,distance" + "\n")


for betaRes in range(start_chain_1, stop_chain_1):
	com = analysis.Com(msys_model, cms_model, asl='(chain.name '+chain_name_1+') AND (res.num '+str(betaRes)+')')
	com2 = analysis.Com(msys_model, cms_model, asl='(chain.name '+chain_name_2+') AND (res.num '+str(start_chain_2)+')')
	distanceAnalyzer = analysis.Distance(msys_model, cms_model, com, com2)
	results = analysis.analyze(tr, distanceAnalyzer)
    
	for gammaRes in range(start_chain_2 + 1, stop_chain_2):
		try:
			com2 = analysis.Com(msys_model, cms_model, asl='(chain.name '+chain_name_2+') AND (res.num '+str(gammaRes)+')')
			distanceAnalyzer = analysis.Distance(msys_model, cms_model, com, com2)
			temp_results = analysis.analyze(tr, distanceAnalyzer)
			
			for i, res in enumerate(results):
				if(res > temp_results[i]):
					results[i] = temp_results[i]
        
		except: 
			print("- EXCEPTION: "+str(gammaRes))


	with open((resultspath+".csv"), "a") as file:
		for i, res in enumerate(results):
			file.write(str(i) + "," + str(betaRes) + "," + str(round(res, 2)) + "\n")
