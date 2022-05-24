/*********************************************
 * OPL 20.1.0.0 Model
 * Author: Imanol
 * Creation Date: Apr 29, 2022 at 11:15:55 PM
 *********************************************/
main {
	// Creation of the model and importing data for the model
	var src = new IloOplModelSource("MainModel.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def,cplex);
	var data = new IloOplDataSource("n75_m500.dat");
	model.addDataSource(data);
	model.generate();
	
	

	
	var start = new Date();
	var start_time = start.getTime();
	
	cplex.epgap=0.01;
	
	//POSTPROCESSING AND SOLUTION
	if(cplex.solve()) {
		writeln("OBJECTIVE: " + cplex.getObjValue());
		writeln();
		write("PATH: 0 -> ")
		for (var i in model.nodes){
        	for (var j in model.nodes){
            	if (model.x[i][j] != 0) {
              		write(j, " -> ");
				}		
			}		
		}
	writeln("0");
	writeln();
	}	
	else{
		writeln("No solution found");	  
	}
	
	var end = new Date();
	var end_time = end.getTime();
	write("Time:", end_time - start_time);
	write
};