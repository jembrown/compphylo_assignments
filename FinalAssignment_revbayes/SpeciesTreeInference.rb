################################################################################
#
# RevBayes Example: Species tree inference using the multispecies coalescent.
#
# 
# This file: specifies the multispecies coalescent, with different effective population sizes for each branch of the species tree, and with a calibration on the root node.
# 			 We assume the species tree is drawn from a constant birth-death process.
#			 Along the branches of the species tree, a multispecies coalescent process generates gene trees.
#			 Along each gene tree, gene sequences are evolved according to an HKY model with a strict clock. 
#            Here, we run an MCMC on this model, using data from 10 genes in 23 mammalian species.
#
# authors: Bastien Boussau and Sebastian Hoehna
#
################################################################################

#######################
# Reading in the Data #
#######################

###### This just defines a single model for all sites #######
# read in each data matrix together which will create a vector of objects
data = readDiscreteCharacterData("data/Cercospora_cat.nex")

# Now we get some useful variables from the data. We need these later on.
d1 <- data[1]
num_loci = data.size()
# get the number of species
n_species <- data.ntaxa()
# get the taxon information (e.g. the taxon names)
taxa <- data.taxa()
n_branches <- 2 * n_species - 1 # number of branches in a rooted tree

# We set our move index
mi = 0



######################
# Species-Tree model #
######################

# Specify a prior on the diversification and turnover rate
speciation ~ dnGamma(2,2)
relativeExtinction ~ dnBeta(1,1)

# now transform the diversification and turnover rates into speciation and extinction rates
extinction := speciation * relativeExtinction

# specify a prior on the root age (our informed guess is about 75-80 mya)
root ~ dnNormal(mean=80,sd=2.5,min=0.0, max=Inf)

sampling_fraction <- 56 / 659 # 56 out of the ~ 659 recognized Cercospora species

# create some moves that change the stochastic variables
# all moves are sliding and scaling proposals
moves[++mi] = mvSlide(speciation,delta=1,tune=true,weight=2)
moves[++mi] = mvSlide(relativeExtinction,delta=1,tune=true,weight=2)
moves[++mi] = mvScale(speciation,lambda=1,tune=true,weight=2)
moves[++mi] = mvScale(relativeExtinction,lambda=1,tune=true,weight=2)
moves[++mi] = mvSlide(root,delta=1,tune=true,weight=0.2)


# construct a variable for the tree drawn from a birth death process
psi ~ dnBDP(lambda=speciation, mu=extinction, rootAge=root, rho=sampling_fraction, taxa=taxa )

moves[++mi] = mvNarrow(psi, weight=5.0)
moves[++mi] = mvNNI(psi, weight=1.0)
moves[++mi] = mvFNPR(psi, weight=3.0)
moves[++mi] = mvGPR(psi, weight=3.0)
moves[++mi] = mvSubtreeScale(psi, weight=3.0)
moves[++mi] = mvNodeTimeSlideUniform(psi, weight=15.0)




###############
# Clock Model #
###############

for ( i in 1:num_loci ) { 
   log_clock_rate[i] ~ dnUniform(-8,4)
   clock_rate[i] := 10^log_clock_rate[i]
   
   moves[++mi] = mvSlide(log_clock_rate[i], weight=1.0)
}


######################
# Substitution Model #
######################


for ( i in 1:num_loci ) {

    #### specify the HKY substitution model applied uniformly to all sites ###
    kappa[i] ~ dnLognormal(0,1)
    moves[++mi] = mvScale(kappa[i],weight=1)


    pi_prior[i] <- v(1,1,1,1) 
    pi[i] ~ dnDirichlet(pi_prior[i])
    moves[++mi] = mvSimplexElementScale(pi[i],weight=2)


    #### create a deterministic variable for the rate matrix ####
    Q[i] := fnHKY(kappa[i],pi[i]) 

}




#############################
# Among Site Rate Variation #
#############################


for ( i in 1:num_loci ) {

    alpha_prior[i] <- 0.05
    alpha[i] ~ dnExponential( alpha_prior[i] )
    gamma_rates[i] := fnDiscretizeGamma( alpha[i], alpha[i], 4, false )

    # add moves for the stationary frequencies, exchangeability rates and the shape parameter
    moves[++mi] = mvScale(alpha[i],weight=2)

}

###################
# PhyloCTMC Model #
###################



for ( i in 1:num_loci ) { 
    # the sequence evolution model
    seq[i] ~ dnPhyloCTMC(tree=psi, Q=Q[i], branchRates=clock_rate[i], siteRates=gamma_rates[i], type="DNA")

    # attach the data
    D <- data[i]
    seq[i].clamp(data)
}




#############
# THE Model #
#############

# We get a handle on our model.
# We can use any node of our model as a handle, here we choose to use the topology.
mymodel = model(psi)

# Monitors to check the progression of the program
monitors[1] = mnScreen(printgen=100, root)
monitors[2] = mnModel(filename="output/cercospora_concatenation_root_calibration.log",printgen=10, separator = TAB)
monitors[3] = mnFile(filename="output/cercospora_concatenation_root_calibration.trees",printgen=10, separator = TAB, psi)

# Here we use a plain MCMC. You could also set nruns=2 for a replicated analysis
# or use mcmcmc with heated chains.
mymcmc = mcmc(mymodel, monitors, moves)

# This should be sufficient to obtain enough MCMC samples
mymcmc.burnin(generations=1500,tuningInterval=50)
mymcmc.run(generations=7000)


# Now, we will analyze the tree output.
# Let us start by reading in the tree trace
treetrace = readTreeTrace("output/cercospora_concatenation_root_calibration.trees", treetype="clock")
# and get the summary of the tree trace
#treetrace.summarize()

mapTree(treetrace,"output/cercospora_concatenation_root_calibration.tree")

# you may want to quit RevBayes now
q()

