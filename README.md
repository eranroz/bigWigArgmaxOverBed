# Usage
bigWigArgmaxOverBed - Compute the argmax position of bigWig over each bed.

```
bigWigArgmaxOverBed.py in.bigwig in.bedfile
```

Optional parameters:
```
    -h, --height: include the max height in additional column
    -z, --zero: treat non covered as zero (otherwise nan)
    --bedOut: output as bed file
    --valley: Find argmin instead of argmax

```    


The output columns are:
```
   name - For bed with name field (otherwise skipped)
   argmax - position of argmax within each bed
```
