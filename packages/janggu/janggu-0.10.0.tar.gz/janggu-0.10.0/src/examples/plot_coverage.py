from pkg_resources import resource_filename

from janggu.data import Cover
from janggu.data import HeatTrack
from janggu.data import LineTrack
from janggu.data import plotGenomeTrack

roi = resource_filename('janggu',
                        'resources/sample.bed')

bw_file = resource_filename('janggu',
                            'resources/sample.bw')

cover = Cover.create_from_bigwig('coverage1',
                                 bigwigfiles=[bw_file] * 2,
                                 conditions=['rep1', 'rep2'],
                                 roi=roi,
                                 binsize=200,
                                 stepsize=200,
                                 resolution=50)

cover2 = Cover.create_from_bigwig('coverage2',
                                  bigwigfiles=bw_file,
                                  roi=roi,
                                  binsize=200,
                                  stepsize=200,
                                  resolution=50)

plotGenomeTrack([cover, cover2],
                'chr1', 16000, 18000).savefig('coverage.png')

plotGenomeTrack([HeatTrack(cover), LineTrack(cover2)],
                'chr1', 16000, 18000).savefig('coverage2.png')
