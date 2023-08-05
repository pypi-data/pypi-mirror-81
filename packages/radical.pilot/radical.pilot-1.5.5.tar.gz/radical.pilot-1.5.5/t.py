#!/usr/bin/env python

import os

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()

    try:
        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource'      : 'local.localhost',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'cores'         : 32,
                   'prepare_env'   : {'env_1' : {'type'   : 'virtualenv', 
                                                 'version': 'python3.8',
                                                 'setup'  : ['numpy']}}
                  }
        pdesc  = rp.ComputePilotDescription(pd_init)
        pilots = pmgr.submit_pilots([pdesc] * 1)
        umgr   = rp.UnitManager(session=session)
        umgr.add_pilots(pilots)

        for pilot in pilots:
            pilot.prepare_env({'env_2' : {'type'   : 'virtualenv', 
                                          'version': 'python3.8',
                                          'setup'  : ['numpy']}})
        n    = 10
        cuds = list()
        for i in range(0, n):

            cud = rp.ComputeUnitDescription()
            cud.executable       = '%s/examples/hello_rp.sh' % os.getcwd()
            cud.arguments        = ['1']
            cud.cpu_processes    = 1
            cud.named_env        = 'env_1'
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()

    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

