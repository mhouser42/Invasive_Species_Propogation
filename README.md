# Invasive_Species_Propogation
A Monte Carlo simulating the hypothetical spread of the Spotted Lanternfly in Illinois.


Tentative README.md

INVASIVE SPECIES PROPAGATION MONTE CARLO

https://github.com/mhouser42/Invasive_Species_Propogation

Team members: 

Justin Tung: https://github.com/JayTongue
Matt Adam-Houser: https://github.com/mhouser42
 

The spotted lanternfly (SLF) is an invasive species originating in China. It was accidentally introduced to North America in 2014, first detected in Pennsylvania before eventually spreading to 14 other states. Just this past September, it has been spotted in Illinois for the first time. The purpose of our Monte Carlo is to simulate the spread of the lanternfly and explore potential preventative measures.

 

Aggregate data from US locations compiled by a previous study will be used to inform our design: https://github.com/ieco-lab/lydemapr, and NetworkX to create graph structures.

 

There will effectively be two levels of the simulation. A high level graph with geographical nodes representing locations in Illinois and the trade routes (edges) between them, and a “zoomed in” level for each node which we will create a matrix  that classes representing the lanternflies, people, and trees can populate and move around in.

 

Deterministic Variables:

High level

Geospatial nodes - Nodes representing different areas of illinois. These nodes will have a number of deterministic properties, including:

Longitude and Latitude - used as a method of establishing distance between nodes.
Population - Higher population areas will have a better chance of detecting and destroying SLF
Lanternfly density: initial lanternfly levels for an area. Most of these will be zero at the beginning.
Tree density: SLFs primary host tree is another invasive species from East Asia known as the “tree of heaven”, but is known to use more than 170 different plants as potential hosts, a number of which, like walnut and maple trees, are common in Illinois (our state tree the white oak is fortunately spared). Higher tree density will result in faster lanternfly spread.

This will mean we have effectively two densities, one for trees of heaven, and another for native trees. High tree of heaven density will increase reproduction rate.

Certain nodes will be “checkpoints” along routes between larger population centers and forests. These will have zero population.

Routes and Vehicles - SLFs are what is known as a “hitchhiker” pest. While they have wings, they only fly short distances, and mostly remain in a localized area. They primarily spread by laying eggs on shipping containers and trade goods.

There are a number of train and truck routes throughout illinois. These will be weighted edges between the geospatial nodes. We will use OSMnx for this part.

Trucks and Trains (inherited from a generic Vehicle class) will “travel” along edges. These classes will have an “infested rate” and “detection rate”. Infested rate is the likelihood a vehicle will have an egg nest, which will increase if the geonode it is leaving has higher lanternfly density. “Detection rate” will be used to simulate the length of vehicles, with higher levels for trains and lower levels for trucks (but will increase for number of cars a truck has) 

Seasons - SLF have a life cycle of one generation per year. While the adults and nymphs die off during the winter, their egg masses are resistant to the cold and can survive. This is an opportune time to find egg nests and destroy them. Seasons will be used to simulate the slow down in colder months, as well as be triggers for SLF to transition to the next phase of their life cycle.

Local level

While we are considering that this may be too granular an approach, and that implementing the grid may be too complicated, some ideas for potential Classes to populate it are:


Insect - The Insect class will be a generic class that will be inherited by the LanternFly class and the Wasp class. It will have attributes like movement, gestation, and age. 

LanternFly

Will have a life cycle based on age, corresponding to seasons. Will only be able to reproduce while adults.
Considering having “hunger” levels, which will make SLF prioritize navigating to trees, otherwise adults will try to mate then lay eggs.

Wasp:  SLF have a natural predator in the form of a parasitoid wasp.
Wasps will hunt SLFs, killing adults and destroying nests.

For any any SLF killed by a wasp, another wasp will be created.

Tree - The Tree Class will represent two types of Trees, Regular Trees and Tree of Heaven. 

Tree of Heaven will be targeted by lanternflies at higher rates and will increase their reproduction rate
As Tree of Heaven density reaches certain thresholds, it will decrease regular tree density, imitating its invasive nature. Conversely, as tree of heaven density declines, regular tree density will increase. These effects will be slow, taking many seasons.

Person

This will be dependent on the population of the GeoNode. People will randomly move around. If they come in contact with a SLF they will kill it. 

They can also remove Trees of Heaven
 

Randomized Variables:

The randomized variables will fall into two separate categories, ones that simulate the spread of the pest, and another for mitigation efforts.


Propagation

Transport infestation - For each trade route, there will be some number of trucks traversing them. Each truck has a random chance of being infested which increases with lanternfly density.

Spread rate - This will be the rate that lanternflies reproduce once they have established themselves in an area. 
Mitigation efforts

Truck inspections - At each checkpoint node, there is the possibility of egg nest detection.
This may be set at a global uniform level, or may vary from checkpoint to checkpoint.

Bug smashing and egg destruction - Areas will have different levels of “awareness” of the SLF problem, and will represent more active measures being taken to deal with them. The effectiveness of bug smashing will be (population × awareness)
The Chinese Needle Snake approach: In addition to regular culling efforts, certain areas will have the parasitoid wasp introduced into the population. 

Deforestation - The degree/rate that trees of heaven are removed from areas.

Additionally, trees of heaven could be converted to “trap trees” treated with insecticide, killing lanternflies which feed on it.

Quarantine - Considering that the impact of SLF isn't dire enough to merit large scale changes in the transportation of goods, this next approach is somewhat unrealistic. With that in mind, if an area reaches a certain SLF population density, a quarantine will be enacted. Manual removal efforts will increase, traffic of outgoing trucks decrease, and detection rates at checkpoints along routes will increase. 

 

Hypotheses:

While we will probably formalize hypotheses later, some tentative ideas are:   

Urban areas (high population, low tree density) will experience faster growth due to increased trade traffic. 

Removal of a large percentage of the tree of heaven will significantly reduce the lanternfly population.

Parasitoid wasps will be more effective than simple tree of heaven removal or human interventions, except for when a quarantine goes into effect. 

