# Skript finding the minimal distance between two sets of proteins

This script analyses Molecular Dynamics simulations performed with Schrödinger Desmond using the Schrödinger Python API 2023-1. Between two sets of protein residues - it calculates for each frame of the simulation, for each residue of the first set, the minimal distance to any residue in the second set. The results are then saved into a .csv-File as follows:

    frame,residue,distance  <- Headline
    0,77,7.68               <- In Frame 0, the minimal distance of residue 77 from interaction partner 1 to any residue in interaction partner 2 was 7.68 Angstroms
    1,77,7.61               <- In Frame 1, the minimal distance of residue 77 from interaction partner 1 to any residue in interaction partner 2 was 7.61 Angstroms
    2,77,8.57               <- And so on for every frame in the simulation for this residue
    3,77,8.78
    [...]
    2999,77,6.39
    3000,77,5.53            <- Last Frame of the simulation
    0,78,6.7                <- New Residue (residue #78)
    1,78,6.45
    2,78,6.53
    [...]

This script needs to be started via the `$SCHRODINGER/run` command.

The repository contains a version with detailed comments on how the skript works and an additional uncommented version. 

This code was used to generate distance data in the following publication:
Sure F, Einsiedel J, Gmeiner P, Duchstein P, Zahn D, Korbmacher C, Ilyaskin AV. The small molecule activator S3969 stimulates the epithelial sodium channel (ENaC) by interacting with a specific binding pocket in the channel's beta-subunit. under review. 

For questions, contact florian.sure@fau.de
