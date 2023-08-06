# pySEED
## A brief description of the SEED algorithm
pySEED is a Python implementation of the **Symmetric-Approximation Energy-Based Estimation of Distribution (SEED) algorithm: A Continuous Optimization Algorithm** [[1]](#1), which allows optimization in the continuous space for functions of independent variables. It is based on the Univariate Marginal Distribution scheme [[2]] of Estimation Distribution Algorithms (#2). Broadly speaking, SEED is an algorithm able to construct explicit probabilistic models that are iteratively refined to produce better and better solutions for a particular problem. To achieve this, SEED uses the Boltzmann Probability Distribution Function (PDF-B) defined in Eq. (1), since the PDF-B guarantees that the probability of finding new solutions (i.e. new individuals in evolutionary parlance) that performs worse than the previous solutions is almost zero.
<p align="center"><img src="img/eq1.svg" /><p>



Due to the difficulty in generating new solutions based on the PDF-B, an approximation to this distribution using Mu and Sigma parameters of the univariate normal distribution is estimated. To accomplish this, the Jeffrey's Divergence, which is a symmetric measure between two probability distributions, is minimized. This is given in Eq. (2):

<p align="center"><img src="img/2.svg" /><p>

where the normal distribution is given by Eq. (3)

<p align="center"><img src="img/eq3.svg" /><p>

Solving Eq. (2) for the mean, it is obtained Eq. (4):

<p align="center"><img src="img/eq4.svg" /><p>

Finally, from the minimization of Eq. (2) and solving for the variance, it is obtained Eq. (5):

<p align="center"><img src="img/eq5.svg" /><p>

With the results of Eqs. (4) and (5), new solutions are generated using the normal distribution. It is worth mentioning that SEED is an algorithm designed for the maximization case [[1]](#1).

## Requirements and installation
pySEED needs the requirements listed in the table below

| Requirement | Version |
| :---: | :---: |
| Python | >=3.5.2 |
| numpy | >=1.18.2 |


## Example
To exemplify the pySEED operation, we will use a classic function in optimization known as the Sphere function, it is defined in Eq. (6):

<p align="center"><img src="img/eq6.svg" /><p>


It is worth mentioning that SEED was designed to deal with maximization problems. For minimization problems, the functions must be transformed into a maximization case. To do this we simply apply the next operation: 1E8 - value_of_the_function, which has the optimum in 1E8.


In the pyseed/ package, we define the Benchmark_functions.py file, where different fitness functions are programmed. To import the Sphere funcion use the next code:

```
from Benchmark_functions import Sphere
```

Then the pySEED parameters must be set. The advantage of pySEED is that it does not require control parameters other than the number of elements in the population, which can be set to an empirically predefined value.


```
population_size = 300
dimensions = 200
lower_limit = -10
upper_limit = 5
fitness_function = Sphere()
stopping_criterion = 1E-6
iterations = 1000
```

With the parameters set, we can run the algorithm using the following code:

```
SEED = pySEED.SEED_EDA(population_size, dimensions, lower_limit, upper_limit, fitness_function, 1E8 - stopping_criterion, print_evolution=True)
Individuals = SEED.evolution(iterations)
```

For the minimization case, the stopping criterion must be transformed using the next operation: 1E8 - stopping_criterion.

In order to perform statistical analysis, the Optimize.evolution() method is able to return a list of the best-evolved individuals at each iteration. If you want to get the individual.chromosome and its corresponding fitness value, simply use the next code: 

```
for individual in Individuals:
    print("Chromosome:", individual.chromosome, "Fitness value:", 1E8 - individual.fitness_value)
```

Note that pySEED returns fitness values computed for the maximization case. So, in order to get the fitness values for a minimization case, those must be transformed using the next operation: 1E8 - individual.fitness_value


## Authors
### Valentin Calzada-Ledesma
### Juan de Anda-Suárez

## How to cite pySEED
```
@ARTICLE{8876622,
  author={J. {De Anda-Suárez} and J. M. {Carpio-Valadez} and H. J. {Puga-Soberanes} and V. {Calzada-Ledesma} and A. {Rojas-Domínguez} and S. {Jeyakumar} and A. {Espinal}},
  journal={IEEE Access},
  title={Symmetric-Approximation Energy-Based Estimation of Distribution (SEED): A Continuous Optimization Algorithm},
  year={2019},
  volume={7},
  number={},
  pages={154859-154871},}
```


## References
<a id="1">[1]</a>
J. De Anda-Suárez, J. M. Carpio-Valadez, H. J. Puga-Soberanes, V. Calzada-Ledesma, A. Rojas-Domínguez, S. Jeyakumar, A. Espinal. (2019). Symmetric-Approximation Energy-Based Estimation of Distribution (SEED): A Continuous Optimization Algorithm.
IEEE Access, 7, 154859-154871.

<a id="2">[2]</a>
Brownlee, J. (2011).
Clever Algorithms: Nature-inspired Programming Recipes.
Lulu.com, ISSN:9781446785065.
