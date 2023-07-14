# Bi-Probe

We implement Bi-Probe and other approaches for comparison here.
The experimental environment is shown in the table below.

|Component | Description |
|-|-|
|Processor | Intel® Core™ i9-10900X, 2(socket)\*10\*3.70GHz |
|L3 cache | 19.25M |
|Instruction set extension | SSE4.1, SSE4.2, AVX2, AVX-512 |
|Memory | 4\*32G DDR4, 2400 MHz |
|OS | Linux 5.11.0 |
|Compiler | g++ -O3 |

For the datasets, you can fetch them at [https://anonymous.4open.science/r/BiProbeRealWorldData-CA52](https://anonymous.4open.science/r/BiProbeRealWorldData-CA52).

To run the code, please first determine the experiment directory (denoted by `exp_dir`) and L3 cache size in `./run_all.sh` as well as the mapping of your intel cpu in `./cpu-mapping.txt`. Note that the directory of the datasets should match the experiment directory you set.

With the code and datasets, you can reproduce all the experiment results in our article.
The intermediate results are in `${exp_dir}/results/breakdown`. Most files' names obey the form of `${phase}_${workload}_${algorithm}_profile_${group}_${id}.txt`, and you can check their human-readable contents. Due to heavily repeated experiments for high-quality measurement and intensive compiling, it may take weeks to produce all the results, and you can manually shrink the test group size for a quicker check.
