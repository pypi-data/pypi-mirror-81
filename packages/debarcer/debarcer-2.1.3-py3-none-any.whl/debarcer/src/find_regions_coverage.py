# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:42:42 2019

@author: rjovelin
"""

import pysam
from src.utilities import get_consecutive_items
from src.utilities import GetContigs



def FindRegionsCoverage(bamfile, contig, min_cov, region_size, max_depth, ignore_orphans, stepper):
    '''
    (str, str, int, int, int, bool, str) -> list
    
    :param bamfile: Path to the bam file
    :param contig: Chromosome name, eg. chrN
    :param min_cov: Minimum read depth for all positions in genomic interval
    :param region_size: Minimum length of the genomic interval    
    :param max_depth: Maximum read depth
    :param ignore_orphans: Ignore orphan reads (paired reads not in proper pair) if True
    :param stepper: Controls how the iterator advances. Accepeted values:
                    'all': skip reads with following flags: BAM_FUNMAP, BAM_FSECONDARY, BAM_FQCFAIL, BAM_FDUP
                    'nofilter': uses every single read turning off any filtering    
    
    Find all genomic intervals on contig of minimum length region_size for which
    all positions have read depth equals to min_cov or greater
        
    Precondition: bamfile is coordinate-sorted and has 'SQ' fields    
    '''
    
    # open file for reading
    infile = pysam.AlignmentFile(bamfile, 'rb')
    # store read depth at positions {pos: read depth}
    D = {}
       
    for pileupcolumn in infile.pileup(contig, max_depth=max_depth, ignore_orphans=ignore_orphans, stepper=stepper):
        # compare number of reads at pileup position with minimum read depth required
        if pileupcolumn.nsegments >= min_cov:
            # get column position
            pos = int(pileupcolumn.reference_pos)
            D[pos] = pileupcolumn.nsegments
    infile.close()
    
    # make a list of genomic intervals for which all positions have min_cov 
    L = []
    for i in get_consecutive_items(list(D.keys())):
        # returns a generator with groups of consecutive positions
        # check size of genomic interval
        if i[-1] + 1 - i[0] >= region_size:
            L.append(i)
    return L


def WriteTargetsBed(bamfile, outputfile, min_cov, region_size, max_depth, ignore_orphans, stepper):
    '''
    (str, str, int, int, int, bool, str) -> None
    
    :param bamfile: Path to the bam file
    :param outputfile: Path to the output bed file
    :param contig: Chromosome name, eg. chrN
    :param min_cov: Minimum read depth for all positions in genomic interval
    :param region_size: Minimum length of the genomic interval    
    :param max_depth: Maximum read depth
    :param ignore_orphans: Ignore orphan reads (paired reads not in proper pair) if True
    :param stepper: Controls how the iterator advances. Accepeted values:
                    'all': skip reads with following flags: BAM_FUNMAP, BAM_FSECONDARY, BAM_FQCFAIL, BAM_FDUP
                    'nofilter': uses every single read turning off any filtering    
        
    Write a bed file (1-based coordinates) with all genomic intervals of minimum
    length region_size for which all positions have read depth equals to min_cov or greater
        
    Precondition: bamfile is coordinate-sorted and has 'SQ' fields    
    '''
    
    Regions = {}
    # make a list of chromosomes
    chromos = GetContigs(bamfile)
    # loop over chromosomes
    for contig in chromos:
        # find genomic intervals on given chromosome
        L = FindRegionsCoverage(bamfile, contig, min_cov, region_size, max_depth, ignore_orphans, stepper)
        # collect intervals for chromo
        if len(L) != 0:
            Regions[contig] = L
    
    newfile = open(outputfile, 'w')
    # loop over all chromosomes with recorded intervals
    for contig in Regions:
        for interval in sorted(Regions[contig]):
                # adjust interval positions to be 1-based
                start, end = interval[0] + 1, interval[1] + 1
                line = [contig, str(start), str(end)]
                newfile.write('\t'.join(line) + '\n')
    newfile.close()

