Species IS579 Fall 2023

# Invasive_Species_Propogation

Justin Tung: https://github.com/JayTongue

Matt Adam-Houser: https://github.com/mhouser42

--------------------------------------------------
 
## I.  Factual Background

The Spotted Lanternfly (SLF) (Lycorma delicatula) is an invasive species originating from China, Bangladesh, and Vietnam. It was accidentally introduced to North America in 2014, first detected in Pennsylvania before [eventually spreading to 14 other states](https://www.aphis.usda.gov/aphis/ourfocus/planthealth/plant-pest-and-disease-programs/pests-and-diseases/sa_insects/slf). The SLF is very problematic due to its consumption of plant life, both endemic and agricultural. Its droppings also encourage mold growth, further detrimentally impacting the host plant (University of Illinois Extension "Spotted Lanternfly Fact Sheet").

On September 16th of this year (2023), it has been spotted in Illinois for the first time (Illinois Department of Agriculture). The University of Illinois has warned that the SLF could potentially devastate grape and logging industries (University of Illinois Extension "Spotted Lanternfly Fact Sheet").
  
While the SLF has a relatively short range by flight, it often travels long distances when they or their eggs are carried by vehicles, shipping containers, or any other vector.
  
The SLF also has a unique interaction with an invasive tree, the Tree-of-Heaven (ToH) (Ailanthus altissima). This Tree comes from China and Taiwan and was introduced to the United States in the late 1700’s because of a rapid growth speed, toleration of poor air and soil, and ornamental qualities (Penn State Extension, "Tree of Heaven"). However, this tree soon fell out of favor because of its prolific root sprouting, foul odor, and weak wood (Penn State Extension "What Should You Do with Spotted Lanternfly Egg Masses"). The Tree-of-Heaven is the SLF’s preferred host.
  
The purpose of our Monte Carlo is to simulate the spread of the lanternfly and explore potential preventative measures.
  
--------------------------------------------------

## II. Available Data

Two primary datasets provided the data for this model The first is aggregate data from US locations compiled by Sebastiano De Bona et al. in their 2023 paper “lydemapr: an R package to track the spread of the invasive Spotted Lanternfly (Lycorma delicatula, White 1845) (Hemiptera, Fulgoridae) in the United States.” The data from this research paper is available [on GitHub](https://github.com/ieco-lab/lydemapr). The second is data compiled by Cornell University’s New York State Integrated Pest Management Program. Their map is frequently updated and freely available online.

For construction of the nodes, data was obtained via (Wikipedia)[https://en.wikipedia.org/wiki/List_of_municipalities_in_Illinois]. Additional information was collected on Tree of Heaven was collected from the website [EDDmaps](https://www.eddmaps.org/distribution/uscounty.cfm?sub=3003). This data is recorded sightings of the plant. Once sighted, experts will review the record and confirm if the sighting is authentic. Data from Illinois was separated out, and an aggregate of sightings from the last five years were added to our model. 

--------------------------------------------------

## III. Monte Carlo Simulations

### 1- Design

In researching mathematical models of ecological phenomena, we quickly encountered two primary challenges. Firstly, many of these models are much more mathematically complex than we could effectively do or learn to do in the assignment period. Secondly, many of these models evaluated a lot more information than we were specifically able to find about the SLF.

#### 1. Variables

Given this, we did our best to focus on a smaller selection of key variables. Instead of following an initial idea of modeling individual entities such as flies, wasps, trees, etc., we decided to relegate our abstractions to percents. For instance, a key variable, infestation rate, is indicated as a percentage, where 100% infestation means the maximum amount of SLF that the ecology can sustain. This allowed us to constrain our variables to appropriate ranges that could still meaningfully represent the concrete reality the variables are intended to capture. Other variables we consider this way are the ToH density of each county, which is similarly a percentage.

There are also several concrete variables we consider. For instance, the population density of each county, each county’s geometry, and each county’s centroid.

#### 2. Network Design

Another aspect of our test design was to represent counties as nodes in a network. After finding the counties adjacent to each county, we represented these borders as edges, since they would be natural corridors for the SLF to spread. We also represented spread via major roadways by incorporating additional edges along these roadways to represent a vehicle-based spread. While a more comprehensive project may consider more natural barriers, the length and speed limit of road edges rather than their mere existence, for the sake of simplicity, the only distinction we make between edges is if the counties are connected by an interstate. 

#### 3. Probabilities

The probabilities we used were tailored to each randomized variable. Each month, the intrinsic growth of a county’s infestation rate as well as the chance of infestation from each of the county’s neighbors is calculated to change the county’s new infestation rate. The chance of an infestation growing intrinsically is modeled by a normal distribution with a mean of 0.025 and a standard deviation of 0.01. The probability of neighboring influence from each county is modeled by a normal distribution with a mean of 0.5 and a standard deviation of 0.8.

The ToH is given a randomized chance to increase the infection rate due to its influence on SLF propagation. This probability is modeled with an exponential distribution with a scale of 0.02. Since the ToH is also a limited resource that SLF can deplete, and cannot host all SLF beyond a certain point, an exponential distribution seemed the most appropriate. The benefit to SLF would be great if they are in smaller number, but quickly diminishes as the ToH becomes saturated and depleted.
            
For population interventions, we modeled this effect with a normal with a mean of 0.3 and standard distribution of 0.1. The normal distribution here felt the most appropriate as a representation of human decision-making. This population will probably have some people who intervene a lot, and some people who intervene a little, and a median that is on neither extreme where most people sit.
            
For quarantine measures, we let the decision to quarantine be 50/50. Since this comes down largely to a matter of governance and public policy, any predictive or behaviorally normative model is likely going to be flawed. Rather than try to develop such a model by doing time-intensive historical research on quarantine-related countermeasures enacted by different jurisdictions that may be relevant to this study, this probability was left as a random Boolean.
            
The specifications for the numbers are largely the product of our best estimates. This is because of the difficulty in finding established statistical models for simulating the infestation of an invasive species that was appropriate in data requirements, mathematical complexity, and scope to what would be a successful project. These numbers were also adjusted as the model was developed and refined.

The majority of the numerical values used for this simulation were the result of best-effort estimations and deductions of variables. As mentioned before, established formulas for species propagation were beyond the appropriate scope in terms of complexity and data requirements for us to implement, if the data even exists at all. The existance and availablility of data was also strong contributing reason for the limitations on the design of the simulation. For instance, the Penn. Dept. of Agriculture states that "No efficacy data currently exists for any of the available systemic insecticides" in its discussion on trap trees (Penn. Dept of Ag., "Spotted Lanternfly Property Management").  

The numerical values used in our project can be therefore construed in two ways. The first is the result of a best-effort to repeat known results and conform to general realistic understandings of the situation the simulation models. The second is a simulation of a possible intervention. For example, there are a wide variety of ways that an ecologicla quarantine could be implemented by various state and local authorities. The quarantine simuation this model contains is one such possible quarantine model. 

### 2- Validation

A realistic projection of SLF infestation is very difficult to quantify, and available data and literature from reputable sources supports varying results. For instance, De Bona et al. show a map of the 8 years of spread since introduction to in 2014.

![alt text](https://github.com/mhouser42/Invasive_Species_Propogation/blob/main/references/Map_yearly.png)

(De Bona et al. 2023)

Howver, Jones et al, in developing a specially and temporally dynamic forecast for SLF infestation, show perhaps a quarter of the United States and being partially or completely innundated with SLF in just 7 years. 

![alt text](https://github.com/mhouser42/Invasive_Species_Propogation/blob/main/references/jones.png)

(Jones et al. 2022)

Our simulations, especially our baseline simulations, exhibited strong statistical convergence. Even without calculating a precise P-value, a clear trend line is still discernable. The resulting graph of our baseline simulation is very similar to a well-established species invasion model.
 
![alt text](https://github.com/mhouser42/Invasive_Species_Propogation/blob/main/references/standard_curve.jpg)
 
(This one is from Lovett et al., but many like it are available)

![alt text](https://github.com/mhouser42/Invasive_Species_Propogation/blob/main/references/our_curve.JPG)
 
More confidence was imparted in our simulation and methodology since our graph was reproducing a known statistical behavior. The outcome of the graph also makes intuitive sense. When an invasive species is relatively new to an area, their population is low and growth will be slow. As the population increases, so does the rate of infestation. However, an inflection point is reached, where the growth begins to slow due to depletion of natural resources such as food and habitat, and the growth increasingly slows as the ecology reaches full saturation.
 
 
            	Statistical convergence
            	Components and outcomes make sense
            	If possible, simulate a known statistical behavior
             
### 3- Hypotheses, experiments and predictions

Because of the nature of ecology, the cost associated with running different experiments is almost comprehensively prohibitive. Once a species has infested an area, their removal is nearly impossible. As such, areas facing infestation really only have one shot to try to get it right and achieve their desired outcomes.

In conducting our research, we came across several different countermeasures against SLF. We decided to include three experimental variables to manipulate and assess outcomes from.

#### 1. Targeting the Tree-of-Heaven.

Given the known connections between the ToH and the SLF, many efforts have targeted ToH populations in an area facing SLF infestation. These efforts largely take place in one of two ways. The first is to simply try to eliminate ToH. This is done as all tree removal is done, and is laborious, time and labor intensive, and can be impractical in many situations (Brandywine Conservancy). The second, called the “trap tree” approach, is to treat trees with a systemic insecticide. Doing so doesn’t kill the tree, but will make the tree poisonous to SLFs that will still preferentially seek it out (Penn State Extension "Controlling Tree of Heaven: Why It Matters").

Note that the ToH itself is invasive and ecologically harmful in many ways, so while insecticide may be a good way of counteracting SLF, counteracting the ToH itself may be a priority in many instances. However, this set of priorities is not incorporated into this simulation. Only the trap tree approach is evaluated here.

Implementation of the trap tree approach would effectively not just negate the benefit of the ToH to SLF, but actively harm it. Every SLF which would want to feed and lay eggs on it would instead find itself and its eggs poisoned. While this has the potential to substantially negatively impact the infestation rate, the way our simulation modeled this was to flip change the positive impact of the ToH to a negative one, but otherwise modeling the same probability.

We predicted that this experimental variable would have an effect in depressing the SLF, but a less substantial one. This is because ToH is not as well established in Illinois as it is in some other states where these measures have been taken, such as Pennsylvania.

#### 2. Population-based countermeasures

One common piece of advice given on sites discussing SLF is to report sightings, and moreover, to kill SLF if possible, and look for eggs and kill them, especially if they’re on something like car, which can help the SLF disperse (see e.g., Penn State Extension "What Should You Do with Spotted Lanternfly Egg Masses").

In order to model the efficacy of these population-based countermeasures, we factored in the population density of each county, and used a standard distribution to represent human decision-making. Since some individuals would kill very few SLF or eggs, and some would kill many, we assumed that most would be somewhere in the middle, probably on the lower side.

We predicted that this experimental variable would also help to prevent SLF, but a less substantial one. After all, while many counties have a high population density, many counties also have very low population densities. This means that if there are populations of the SLF in those counties where detection is very unlikely, then these can spread rampantly.

#### 3. Quarantine

Ecological quarantine is always a challenging to implement, given the how long boarders between counties can be. However, quarantines are still often implemented. One prominent model for this is Pennsylvania. Its department of agriculture instructs both residents to follow certain protocols, such as inspecting vehicles, boats, and natural materials such as logs which may get transferred from one area to another. Businesses are given further instructions and are required to have an SLF Permit or to hire companies that have a permit (Pennsylvania Department of Agriculture).

While no quarantine is 100% effective, our model simulates quarantine as if it were.  If an infestation rate is over 50% for a given county and a random choice generator picks True, then that county’s infection from neighboring counties is 0. That county’s quarantine then remains in place for the remainder of the simulation.

We predicted that this measure would be the most effective out of all three. First, it is non-discriminatory. Every county has the same chance to meet the required criteria for quarantine. Secondly, knocking a neighbor infection rate to 0 is a substantial mathematical impact on the growth of the infestation rate. These factors all combine to make this countermeasure a powerful one to consider.

--------------------------------------------------

## IV. Results

The results conformed to expectations in some ways and defied them in others. This is the resulting graph of the three countermeasures, compared to the baseline:

<result graph>
 
While all three countermeasures had an initial effect of slowing down the infestation of the SLF, the population-based countermeasures depressed the curve substantially more than other areas. This is probably because of the areas that had the most SLF introduced were also areas of major commerce and rigorous transportation, which also tend to be areas of higher population density. These measures were then followed by quarantine, then trap trees.

However, comparing the trend lines as well as extending the length of time simulated reveals two interesting things. The first is that at a certain point, the trap trees and population-based countermeasures lines both stop increasing. This simulation has been run out to 100 months and this is still true. Initially I assumed that this was due to some error in the mathematical model. But this may not be the case. The infestation percentage, in our model, is a representation of the maximum population of SLF a given area can sustain. Both trap trees and population-based countermeasures may have effectively changed, not just the rate of infestation, but the hospitability of the area to the SLF itself. Stated differently, these two countermeasures changed what 100% infestation means. They made the ecology fundamentally more hostile to the SLF.

The second surprise was that the same did not exist for the quarantine countermeasure. Although it initially depressed the infestation curve pretty well, the line continued to shoot up to where it was nearly identical to the baseline result after a while. But this also makes sense when considering that quarantine in this model only negates the infestation that comes to it from adjacent counties, not growth of the population it already has.

--------------------------------------------------
 
## V. Analysis and Discussions

The weakness of this simulation, as acknowledged several times, is the mathematical model. The expertise and resources it would take to model this more comprehensively were overwhelmingly prohibitory. However, despite this, several strong conclusions can still be supported by the outcome of the simulation.

Clearly, any countermeasures are better than an uninhibited spread. However, depending on the priorities of different locales, certain countermeasures may be preferable to others. For instance, the most overall depression in the model was with trap trees, but the highest initial depression was from population-based countermeasures. Quarantine may initially be more successful than trap trees but may be politically prohibitive. Trap trees requires expertise with identifying and treating trees, which may be too high an educational barrier to implement compared to population-based countermeasures, where residents may be taught to recognize the SLF from a few pictures.

An intuitive further step in this project would be to find more sources of reliable and data and change the model to suit it, given the aforementioned limitations on research and scope. A further expansion of this project could be to explore more variations within each countermeasure. For instance, the quarantine threshold would likely look different if a county was 75% or 25% likely to declare and enforce a quarantine, or if residents of a county were more enthusiastic about finding and killing SLF. Doing this may require a more comprehensive and complex simulation, but it may yield results that can show a more nuanced insight into each of these interventions.

--------------------------------------------------

## VI. Citations

1. APHIS. "Spotted Lanternfly." Animal and Plant Health Inspection Service, United States Department of Agriculture, n.d., https://www.aphis.usda.gov/aphis/resources/pests-diseases/hungry-pests/the-threat/spotted-lanternfly/spotted-lanternfly.
2. Brandywine Conservancy. "Invasive Species Spotlight: Tree of Heaven (Ailanthus altissima) and Spotted Lanternfly." Brandywine Conservancy, n.d., https://www.brandywine.org/conservancy/blog/invasive-species-spotlight-tree-heaven-ailanthus-altissima-and-spotted-lanternfly.
3. Cornell University, College of Agriculture and Life Sciences. "Spotted Lanternfly Reported Distribution Map." New York State Integrated Pest Management, n.d., https://cals.cornell.edu/new-york-state-integrated-pest-management/outreach-education/whats-bugging-you/spotted-lanternfly/spotted-lanternfly-reported-distribution-map.
4. De Bona, Sebastiano, et al. "LydeMaPR: An R Package to Track the Spread of the Invasive Spotted Lanternfly (Lycorma delicatula, White 1845) (Hemiptera, Fulgoridae) in the United States." bioRxiv, 2023.01.27.525992, doi: https://doi.org/10.1101/2023.01.27.525992.
5. Illinois Department of Agriculture. "Spotted Lanternfly." Illinois Department of Agriculture, n.d., https://agr.illinois.gov/insects/pests/spotted-lanternfly.html.
6. Jones, C., Skrip, M.M., Seliger, B.J., et al. "Spjsonotted Lanternfly Predicted to Establish in California by 2033 Without Preventative Management." Communications Biology, vol. 5, no. 1, 2022, p. 558. Nature Portfolio, doi: 10.1038/s42003-022-03447-0.
7. Lovett, Gary M., et al. "The Ecology of Fear: Optimal Foraging, Game Theory, and Trophic Interactions." Ecology, vol. 96, no. 10, 2015, pp. 2487-2497. https://esajournals.onlinelibrary.wiley.com/doi/full/10.1890/15-1176
8. Pennsylvania Department of Agriculture. Spotted Lanternfly Property Management." Pennsylvania Department of Agriculture, n.d., www.agriculture.pa.gov/Plants_Land_Water/PlantIndustry/Entomology/spotted_lanternfly/Documents/Spotted%20Lanternfly%20%20Property%20Management.pdf.
9. Pennsylvania Department of Agriculture. "Spotted Lanternfly Quarantine." Pennsylvania Department of Agriculture, n.d., https://www.agriculture.pa.gov/Plants_Land_Water/PlantIndustry/Entomology/spotted_lanternfly/quarantine/Pages/default.aspx.
10. Penn State Extension. "Controlling Tree of Heaven: Why It Matters." Penn State Extension, n.d., https://extension.psu.edu/controlling-tree-of-heaven-why-it-matters#:~:text=Tree%20of%20heaven%20is%20a,across%20most%20of%20southeastern%20PA.
11. Penn State Extension. "Tree of Heaven." Penn State Extension, n.d., https://extension.psu.edu/tree-of-heaven.
12. Penn State Extension. "What Should You Do with Spotted Lanternfly Egg Masses." Penn State Extension, n.d., https://extension.psu.edu/what-should-you-do-with-spotted-lanternfly-egg-masses.
13. University of Illinois Extension. "Spotted Lanternfly Fact Sheet." University of Illinois Extension, https://extension.illinois.edu/sites/default/files/spotted_lanternfly_fact_sheet_v8.pdf.
14. University of Illinois Extension. "Tree of Heaven." University of Illinois Extension, n.d., https://extension.illinois.edu/invasives/tree-heaven.

