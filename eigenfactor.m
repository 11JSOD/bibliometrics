% calculate the influence vector for a 
% citation network to determine eigenfactor scores

% ——————————————————————————————————
% STEP 1: Create an adjacency matrix
% —————————————————————————————————————

% upload adjacency matrix (this is the example from the pdf)
Z = [1,0,2,0,4,3;3,0,1,1,0,0;2,0,4,0,1,0;
    0,0,1,0,0,1;8,0,3,0,5,2;0,0,0,0,0,0];
n = length(Z);

% column labels indicate journals, row labels indicate references
% element i,j is the number of times journal j cites i (arrows j->i)

% ——————————————————————————————————
% STEP 2: Modify adjacency matrix
% ——————————————————————————————————

% make the diagonal a row of zeros
Z = Z - eye(n) .* Z;

% normalize columns, divide by sum
H = Z ./ sum(Z,1);
H(isnan(H)) = 0;

% find dangling nodes, create a vector d to record them

dangling_nodes = find(all(Z == 0));
d = zeros(1,n);
for i = 1:length(dangling_nodes)
    d(dangling_nodes(i)) = 1;
end

% ——————————————————————————————————
% STEP 3: Initialize important values
% ——————————————————————————————————

alpha = 0.85; % why 0.85? this seems arbitrary to me
epsilon = 0.00001;

% let A_tot be the total number of articles in all journals
% in this example, A_tot = 3 + 2 + 5 + 1 + 2 + 1
A_tot = 14;

% a is a normalized column vector with the number of articles/journal
a = [3;2;5;1;2;1];
a = a / A_tot;

% calculate transition matrix P
% TODO

% initialize start vector/dummy vector to pass first while loop

pi_k1 = 1/n * ones(n,1);
pi_k = pi_k1 + 10;

% these are backwards because they get flipped in the algorithm below

% ——————————————————————————————————
% STEP 4: Calculate influence vector pi_i
% ——————————————————————————————————

% this algorithm should converge to the leading eigenvector of P
% count iterations, out of curiosity
iterations = 0;
while all(pi_k1 - pi_k) > epsilon
    pi_k = pi_k1;
    pi_k1 = alpha*H*pi_k + (alpha*d*pi_k+(1-alpha))*a;
    iterations = iterations + 1;
end

% it works on the example!

pi = pi_k1;

% —————————————————————————————————————————————————————————


% We now have the stationary vector and can calculate a variety of scores

% ———

% Eigenfactor score

EF = 100 * H * pi / sum(H*pi);

% journal A score ~34, D is ~ 3.6, F is 0 (nobody cited F)

% ———

% Article Influence Score

AI = 0.01 * EF ./ a;

% this is interesting because E has higher influence than A but lower score











