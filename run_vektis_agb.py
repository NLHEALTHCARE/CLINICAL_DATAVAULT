import sys
sys.path.insert(0, '/home/costiaan/PYELT')
sys.path.insert(0, '/home/costiaan/CLINICAL_DATAVAULT')

from etl_mappings.vektis_agb.vektis_agb_proces import vektis_main()

if __name__ == '__main__':
    vektis_main()