#!/bin/bash

exp_dir="/home/tangxilin/xxx/data1/xtra"
L3_cache_size=20185088

# read arguments
helpFunction()
{
   echo ""
   echo "Usage: $0 -d exp_dir -c L3_cache_size"
   echo -e "\t-d the experiment results directory"
   echo -e "\t-c the L3 cache size of the current CPU"
   exit 1 # Exit script after printing help
}

while getopts "d:c:" opt
do
   case "$opt" in
      d ) exp_dir="$OPTARG" ;;
      c ) L3_cache_size="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$exp_dir" ] || [ -z "$L3_cache_size" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

# Begin script in case all parameters are correct
echo "$exp_dir"
echo "$L3_cache_size"

<<COMMENT

# update in case some package can be missing.
sudo apt update

## install all packages needed
sudo apt install -y cmake
sudo apt install -y texlive-fonts-recommended texlive-fonts-extra
sudo apt install -y dvipng
sudo apt install -y font-manager
sudo apt install -y cm-super
sudo apt install -y python3
sudo apt install -y python3-pip
pip3 install numpy
pip3 install matplotlib
sudo apt install -y libnuma-dev
sudo apt install -y zlib1g-dev
sudo apt install -y python-tk
sudo apt install -y linux-tools-common
sudo apt install -y linux-tools-$(uname -r) # XXX is the kernel version of your linux, use uname -r to check it. e.g. 4.15.0-91-generic
git clone https://github.com/lyrahgames/pxart.git
mkdir pxart-cmake-build
cd pxart-cmake-build
cmake ../pxart
sudo cmake --build . --target install
sudo echo -1 > /proc/sys/kernel/perf_event_paranoid # if permission denied, try to run this at root user.
sudo modprobe msr



## Create directories on your machine.
mkdir -p $exp_dir/results/breakdown/partition_buildsort_probemerge_join
mkdir -p $exp_dir/results/breakdown/partition_only
mkdir -p $exp_dir/results/breakdown/partition_buildsort_only
mkdir -p $exp_dir/results/breakdown/partition_buildsort_probemerge_only
mkdir -p $exp_dir/results/breakdown/allIncludes

mkdir -p $exp_dir/results/figure
mkdir -p $exp_dir/results/gaps
mkdir -p $exp_dir/results/latency
mkdir -p $exp_dir/results/records
mkdir -p $exp_dir/results/timestamps
COMMENT
# copy custom pmu events to experiment dir.
cp pcm* $exp_dir
# copy cpu mappings to exp_dir
cp cpu-mapping.txt $exp_dir

exp_secction="APP_BENCH,MICRO_BENCH,SCALE_STUDY,PROFILE_MICRO,PROFILE,PROFILE_MEMORY_CONSUMPTION,PROFILE_PMU_COUNTERS"

sudo sysctl kernel.perf_event_paranoid=-1
sudo modprobe msr

# execute experiment
cd ./hashing/scripts || exit
bash benchmark.sh -e $exp_secction -d $exp_dir -c $L3_cache_size

# cd ./sorting/scripts || exit
# bash benchmark.sh -e $exp_secction -d $exp_dir -c $L3_cache_size
