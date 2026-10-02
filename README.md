Made my Asta Walor-Scott
Email: lwaorsc@msudenver.edu

It is hard coded to write to a file on my desktop. Please change the save_dir veritable.
Code has additional modifications to the values to add more info.

code is mostly copy and paste of each section. But it loops through each value set in a array. 
for equations 1-4 it also cycles through it. 
Due to the limitations of scipy.integrate as a value goes to infinity, it required to have safety "Blow up points" without these points it will act unstable and may require multiple generations in order to work.
equation 5 required two loops. One for generic plot, with additional information. The second is a moving bifurcation plot. Blue represents stable and red indicates as unstable. 
