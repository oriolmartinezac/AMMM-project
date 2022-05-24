// Length of codes.
int m = ...;

// Number of codes.
int n = ...;

int S[1..n][1..m] = ...;

// Indexes for the stops
range nodes = 1 .. n;

// Cost Matrix cij
int F[nodes][nodes];

// Decision variables xij
dvar boolean x[nodes][nodes];

// Rank variable ui
dvar float+ u[nodes];

//PREPROCESSING of the F matrix (distances matrix)
execute{
  	for (var i=1; i<n+1;i++){
  	  for (var j=i+1; j<n+1;j++){
  	  	for(var k=1; k<m+1; k++){
  			if(S[i][k] != S[j][k]){
  			  F[i][j] += 1;
  			  F[j][i] += 1;
  			  }	  	  
  	  	  }
  	  }
  }
}

// Objective function
minimize sum (i, j in nodes) x[i][j] * F[i][j];

// Constraints
subject to {

    forall (i in nodes) x[i][i] == 0; // A code cannot be followed by itself.

    rule_one_out:
    forall (i in nodes) sum (j in nodes) x[i][j] == 1; // Avoid code repetition

    rule_one_in:
    forall (j in nodes) sum (i in nodes) x[i][j] == 1; // Avoid code repetition

    rule_no_subtour:
    forall (i, j in nodes : j != 1) u[i] + x[i][j] <= u[j] + (n - 1) * (1 - x[i][j]); // Avoid subtouring

    u[1] == 0; // Fixes the rank of the first node
}